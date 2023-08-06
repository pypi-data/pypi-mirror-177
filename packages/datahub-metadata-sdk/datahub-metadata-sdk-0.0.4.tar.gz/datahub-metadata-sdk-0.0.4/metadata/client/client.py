# -*- encoding: utf-8 -*-

import copy
import json
import logging
import pathlib
import os.path
from string import Template
from time import sleep
from datetime import datetime
from typing import List, Tuple

from datahub.metadata.schema_classes import (
    ChangeTypeClass,
    GlobalTagsClass, TagAssociationClass,
    OwnershipClass, OwnerClass, OwnershipTypeClass,
    BrowsePathsClass
)
from datahub.emitter.mce_builder import make_tag_urn, make_user_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper

from metadata.utils.lang import clean_nones
from metadata.exception import MetadataException
from metadata.context import MetadataContext
from metadata.entity.entity import BaseEntity, Entity

from .mixins.dataset import DatasetMixin
from .mixins.dataset_group import DatasetGroupMixin
from .mixins.model import ModelMixin
from .mixins.model_group import ModelGroupMixin

logger = logging.getLogger(__name__)
__all__ = ['Client']


class Client(DatasetMixin, DatasetGroupMixin, ModelMixin, ModelGroupMixin):

    def __init__(self, context: MetadataContext):
        self.context = context 

    def _delete_entity(self, urn: str, soft=False):
        self.context.request('DELETE', '/openapi/entities/v1/', params={'urns': urn, 'soft': 'true' if soft else 'false'})

    def _get_ownership_aspect(self, owners: List[str]):
        aspect = OwnershipClass(
            [OwnerClass(make_user_urn(owner), OwnershipTypeClass.TECHNICAL_OWNER) for owner in owners]
        )
        return aspect

    def _get_tags_aspect(self, tags: list[str]):
        aspect = GlobalTagsClass(
            [TagAssociationClass(make_tag_urn(tag)) for tag in (tags or [])]
        )
        return aspect

    def _get_graphql_template(self, category, template):
        import metadata
        template_file_path = os.path.join(metadata.__path__[0], 'client', 'resources', category, f'{template}.graphql')
        with open(template_file_path) as f:
            return '\n'.join(filter(lambda x: not x.startswith('#'), map(lambda x: x.strip(), f.readlines())))

    def _query_graphql(self, template, **kwargs):
        teg = Template(self._get_graphql_template('queries', template))
        query = teg.substitute(kwargs)
        return clean_nones(self.context.request('POST', '/api/graphql', data=json.dumps({'query': query})).json())
    
    def check_entity_exists(self, urn: str):
        return self._query_graphql('entityExists', urn=urn)['data']['entityExists']

    def _sync_check(self, task, check, *args, **kwargs):
        logger.debug(f'start sync check task : {task}')
        if self.context.options['defaults.metadata.client.sync_wait']:
            sync_wait_timeout = int(self.context.options['defaults.metadata.client.sync_wait_timeout'])
            sync_wait_interval = int(self.context.options['defaults.metadata.client.sync_wait_interval'])

            start = current = datetime.now()
            while (current - start).total_seconds() < sync_wait_timeout:
                sleep(sync_wait_interval)
                logger.debug(f'check task : {task}')
                if check(*args, **kwargs):
                    logger.debug(f'success sync check task : {task}')
                    return
                current = datetime.now()
            raise MetadataException(f'{task} process exceed max allowd sync time {sync_wait_timeout}')
        logger.debug(f'end sync check task : {task}')
    
    def _emit_aspects(self, entity_type, urn, aspects, change_type=ChangeTypeClass.UPSERT):
        for aspect in aspects:
            metadata_event = MetadataChangeProposalWrapper(                                                                                                                                                                                        
                entityType=entity_type,                                                                                                                                                                                                              
                changeType=change_type,                                                                                                                                                                                                 
                entityUrn=urn,                                                                                                                                                                                                                      
                aspectName=aspect.ASPECT_NAME,                                                                                                                                                                                                    
                aspect=aspect,                                                                                                                                                                                                         
            )      
            self.context.emitter.emit(metadata_event)
    
    def _get_entities_by_facts(self, entity_type: str, facts: List[Tuple[str, str, bool, str]], *, search: str=''):
        conditions = ""
        for field, values, negated, condition in facts:
            values = "[%s]" % (", ".join([json.dumps(str(value)) for value in values]))
            negated = 'true' if negated else 'false'
            conditions += f"""\n{{\n field: "{field}"\n values: {values}\n negated: {negated}\n condition: {condition}\n}}\n"""
        rs = self._query_graphql('searchAcrossEntities',
            conditions=conditions,
            types=entity_type.upper(), start=0, count=1000, search=search)['data']['searchAcrossEntities']

        return [r['entity']['urn'] for r in rs['searchResults']]

    def _get_current_user(self):
        return self._query_graphql('me')['data']['me']['corpUser']