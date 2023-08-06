# -*- encoding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class DatasetGroupMixin:
    
    def create_dataset_group(self, dataset_group, upsert=True):
        pass

    def get_dataset_group(self, group_urn):
        pass

    def delete_dataset_group(self, group_urn):
        pass

    def add_dataset_into_group(self, group_urn, urn):
        pass 

    def remove_dataset_from_group(self, group_urn, urn):
        pass 

    def get_datasets_by_group(self, group_urn):
        pass 
