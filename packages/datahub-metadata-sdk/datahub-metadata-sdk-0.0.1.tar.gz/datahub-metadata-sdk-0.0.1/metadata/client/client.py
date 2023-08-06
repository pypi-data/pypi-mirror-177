# -*- encoding: utf-8 -*-

import json
import logging

logger = logging.getLogger(__name__)

__all__ = ['Client']

from .mixins.dataset import DatasetMixin


class Client(DatasetMixin):

    def __init__(self, context):
        self.context = context 

    def _get_ownership_aspect(self, urn, user_email):
        entity_type = urn.split(':')[2]
        aspect_meta = {
            'entityType': entity_type,
            'entityUrn': urn,
            'aspect': {
                "__type": "Ownership",
                "owners": [
                    {
                        "owner": f"urn:li:corpuser:{user_email}",
                        "type": "TECHNICAL_OWNER",
                    }
                ]
            },
            'aspectName': 'owership',
        }
        return aspect_meta

    def _get_tags_aspect(self, urn, tags):
        entity_type = urn.split(':')[2]
        aspect_meta = {
            'entityType': entity_type,
            'entityUrn': urn,
            'aspect': {
                "__type":"GlobalTags",
                "tags":[
                    {
                        "tag": f"urn:li:tag:{tag}"
                    } for tag in tags
                ]
            },
            'aspectName': 'globalTags',
        }
        return aspect_meta



 
