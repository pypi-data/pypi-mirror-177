# -*- encoding: utf-8 -*-

import logging
import json

from metadata.entity.dataset import Dataset

logger = logging.getLogger(__name__)


class DatasetMixin:

    def create_dataset(self,  dataset: Dataset, upsert=True):
        aspect_metas = [
            {
                'entityType': 'dataset',
                'entityUrn': dataset.urn,
                'aspect': {
                    "__type": "DatasetProperties",
                    "customProperties": dataset.properties,
                    "uri": dataset.uri,
                    "name": dataset.display_name,
                    "description": dataset.description,
                },
                'aspectName': 'datasetProperties',
            },
            #self._get_ownership_aspect(dataset.urn, self.context.user_email)
        ]
        
        if dataset.tags:
            aspect_metas.append(self._get_tags_aspect(dataset.urn, dataset.tags))
        
        self.context.request('POST', '/openapi/entities/v1/', data=json.dumps(aspect_metas))

        aspect_metas = [self._get_ownership_aspect(dataset.urn, self.context.user_email)]
        self.context.request('POST', '/openapi/entities/v1/', data=json.dumps(aspect_metas))

        return dataset.urn

    def get_dataset(self, urn: str):
        res = self.context.request('GET', '/openapi/entities/v1/latest', params={'urns': urn})
        data = res.json()
        aspects = data['responses'][urn]['aspects']
        if 'datasetProperties' not in aspects:
            return
        dataset_properties = aspects['datasetProperties']['value']
        display_name = dataset_properties.get('name')
        uri = dataset_properties.get('uri')
        description = dataset_properties.get('description')
        properties = dataset_properties.get('customProperties')
        global_tags = aspects.get('globalTags', {}).get('value', {}).get('tags', [])
        tags = [t['tag'].split(':', maxsplit=3)[3] for t in global_tags]
        return Dataset(urn, display_name, uri, description, tags=tags, properties=properties)
    
    def delete_dataset(self, urn):
        self.context.request('DELETE', '/openapi/entities/v1/', params={'urns': urn})