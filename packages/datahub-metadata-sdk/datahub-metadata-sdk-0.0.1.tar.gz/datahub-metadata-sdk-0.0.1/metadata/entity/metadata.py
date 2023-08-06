import json
import os
import uuid
from urllib.error import HTTPError

import datahub.emitter.mce_builder as builder
import requests
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DataHubRestEmitter
from datahub.metadata.schema_classes import (ChangeTypeClass, ContainerClass,
                                             ContainerPropertiesClass,
                                             DatasetPropertiesClass)

from .utils.query import ENV, PLATFORM, dataset_urn_query, get_auto_name, container_urn_query


class Dataset():

    def __init__(self,
                 uri: str,
                 name: str,
                 namespace: str = None,
                 auto_fix: bool = True):
        self.uri = uri
        if auto_fix:
            self.name = name + "-" + get_auto_name()
        else:
            self.name = name
        self.namespace = namespace
        self.auto_fix = auto_fix

    def properties(self, key: str, value: str):
        if hasattr(self, "_properties"):
            self._properties[key] = value
        else:
            self._properties = {key: value}
        return self

    def tags(self, tag: str):
        if hasattr(self, "_tags"):
            self._tags.append(tag)
        else:
            self._tags = [tag]
        return self

    # todo 这个函数存在应该也是提供一个pre_browsepath
    def pre_browsepath(self, path: str):
        self._pre_browsepath = path
        return self

    def get_urn(self):
        if hasattr(self, "urn"):
            return self.urn
        name = self.name
        if self.namespace is not None:
            name = self.namespace + "." + name
        if hasattr(self, "_pre_browsepath"):
            name = self._pre_browsepath + "." + name
        self.urn = builder.make_dataset_urn(PLATFORM, name, ENV)
        return self.urn


class DatasetGroup():

    def __init__(self,
                 name: str,
                 namespace: str = None,
                 auto_fix: bool = True):
        if auto_fix:
            self.name = name + "-" + get_auto_name()
        else:
            self.name = name
        if namespace is not None:
            self.name = namespace + "." + self.name

    def properties(self, key: str, value: str):
        if hasattr(self, "_properties"):
            self._properties[key] = value
        else:
            self._properties = {key: value}
        return self

    def get_urn(self):
        if hasattr(self, "urn"):
            return self.urn
        self.urn = builder.make_container_urn(guid=uuid.uuid1())
        return self.urn


class MetadataClient():

    def __init__(self, gms_server: str, graphql_server: str, token=None):
        self.graphql_server = graphql_server
        if token is None:
            token = os.getenv("datahub_token")
        self.token = token
        self.emiter = DataHubRestEmitter(gms_server=gms_server, token=token)
        self.emiter.test_connection()

    def create_dataset(self, d: Dataset):
        dataset_urn = d.get_urn()
        d.properties("uri", d.uri)
        # todo set tag是有问题的 
        # ./metadata-ingestion/examples/library/dataset_add_tag.py:39:
        data_properties = DatasetPropertiesClass(
            tags=d._tags, customProperties=d._properties)
        event = MetadataChangeProposalWrapper(
            entityType="dataset",
            changeType=ChangeTypeClass.UPSERT,
            entityUrn=dataset_urn,
            aspectName="datasetProperties",
            aspect=data_properties)
        self.emiter.emit(event)

    def create_datasetgroup(self, g: DatasetGroup):
        container_urn = g.get_urn()
        if not hasattr(g, "_properties"):
            properties = {}
        else:
            properties = g._properties
        container_properties = ContainerPropertiesClass(
            customProperties=properties, name=g.name)
        event = MetadataChangeProposalWrapper(entityType="container",
                                              entityUrn=container_urn,
                                              aspect=container_properties)
        self.emiter.emit(event)

    def set_dataset_to_datasetgroup(self, d: Dataset, g: DatasetGroup):
        dataset_urn = d.urn
        container_urn = g.get_urn()
        container = ContainerClass(container_urn)
        event = MetadataChangeProposalWrapper(
            entityType="dataset",
            changeType=ChangeTypeClass.UPSERT,
            entityUrn=dataset_urn,
            aspectName=container.ASPECT_NAME,
            aspect=container,
        )
        self.emiter.emit(event)

    def get_dataset_by_urn(self, urn: str):
        query = dataset_urn_query(urn)
        res = requests.post(url=self.graphql_server,
                            headers=self.get_headers(),
                            data=json.dumps(query))
        if res.status_code < 200 or res.status_code > 299:
            raise HTTPError("got unexcepted status %d" % res.status_code)
        d = json.loads(res.text).get("data", {}).get("dataset", {}).get(
            "properties", {}).get("customProperties", {})
        if d is {}:
            raise ValueError("no dataset found with urn:%s" % urn)
        kwargs = {}
        for _dict in d:
            kwargs[_dict["key"]] = _dict["value"]
        return Dataset(**kwargs)

    def get_urn_from_group(self, urn: str):
        query = container_urn_query(urn)
        res = requests.post(url=self.graphql_server,
                            headers=self.get_headers(),
                            data=json.dumps(query))
        if res.status_code < 200 or res.status_code > 299:
            raise HTTPError("got unexceptet status %d" % res.status_code)
        urn_dict_list = json.loads(res.text).get("data", {}).get(
            "container", {}).get("entities", {}).get("searchResults", [])
        urn_list = []
        for urn_dict in urn_dict_list:
            urn_list.append(urn_dict["entity"]["urn"])
        return urn_list

    def get_headers(self):
        if self.token is not None:
            return {"Authorization": "Bearer " + self.token}
        return {}
