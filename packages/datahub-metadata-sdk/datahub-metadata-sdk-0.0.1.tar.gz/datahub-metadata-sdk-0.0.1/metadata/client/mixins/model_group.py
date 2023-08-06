# -*- encoding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class ModelGroupMixin:
    
    def create_model_group(self, model_group, upsert=True):
        pass

    def get_model_group(self, group_urn):
        pass

    def delete_model_group(self, group_urn):
        pass

    def get_models_by_group(self, group_urn):
        pass 

    def add_model_into_group(self, group_urn, urn):
        pass 

    def remove_model_from_group(self, group_urn, urn):
        pass 