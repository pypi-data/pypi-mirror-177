# -*- encoding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class ModelMixin:

    def create_model(self,  model, upsert=True):
        pass

    def update_model(self, urn, model):
        pass

    def get_model(self, urn):
        pass 
    
    def delete_model(self, urn):
        pass 