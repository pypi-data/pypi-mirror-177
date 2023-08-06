# -*- encoding: utf-8 -*-

import copy
import os.path
import logging
from typing import List

from datahub.emitter.mce_builder import make_tag_urn, make_user_urn
from datahub.metadata.schema_classes import DatasetPropertiesClass, ContainerClass, ChangeTypeClass

from metadata.entity.dataset import Dataset


logger = logging.getLogger(__name__)


class DatasetMixin:

    def create_dataset(self,  dataset: Dataset, upsert=True):
        properties = copy.deepcopy(dataset.properties)
        properties['uri'] = dataset.uri
        dataset_properties = DatasetPropertiesClass(
            name=dataset.display_name,
            customProperties=properties,
            description=dataset.description,
        )
        global_tags = self._get_tags_aspect(dataset.tags)
        owner_aspect = self._get_ownership_aspect(dataset.owners or [self.context.user_email])
        container_aspect = ContainerClass(
            dataset.group
        ) if dataset.group else None
        self._emit_aspects(Dataset.entity_type, dataset.urn, filter(None, [dataset_properties, global_tags, owner_aspect, container_aspect]))
        return dataset.urn

    def update_dataset(self, dataset: Dataset):
        return self.create_dataset(dataset, upsert=True)

    def get_dataset(self, urn: str):
        if not self.check_entity_exists(urn):
            return
        r = self._query_graphql(Dataset.entity_type, urn=urn)['data']['dataset']
        properties = r['properties']
        custom_properties = {e['key']: e['value'] for e in properties.get('customProperties', {})}
        display_name = properties.get('name', r.get('name'))
        uri = custom_properties.pop('uri', None)
        tags = [t['tag']['urn'].split(':', maxsplit=3)[-1] for t in r.get('tags', {}).get('tags', [])]
        dataset = Dataset(
            urn=urn,
            display_name=display_name,
            uri=uri,
            tags=tags,
            description=properties.get('description', r.get('description', '')),
            properties=custom_properties,
            owners=[o['owner']['urn'].split(':', maxsplit=3)[-1] for o in r.get('ownership', {}).get('owners')],
            group=r.get('container', {}).get('urn'),
        )
        return dataset

    def delete_dataset(self, urn: str, soft=True):
        return self._delete_entity(urn, soft=soft)
    
    def get_datasets_by_facts(self, *, owner: str=None, group: str=None, tags: List[str]=None, search: str=''):
        facts = []
        if group:
            facts.append(('container', [group], False, 'EQUAL'))
        if tags:
            facts.append(('tags', [make_tag_urn(tag) for tag in tags], False, 'CONTAIN'))
        if owner:
            facts.append(('owners', [make_user_urn(self.context.user_email if owner == 'me' else owner), False, 'CONTAIN']))
        return self._get_entities_by_facts(Dataset.entity_type, facts, search=search)