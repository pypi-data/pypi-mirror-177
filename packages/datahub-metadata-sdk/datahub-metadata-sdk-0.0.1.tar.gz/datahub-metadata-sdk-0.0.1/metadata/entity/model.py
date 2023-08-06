import json
from typing import Dict, List, Union

import datahub.emitter.mce_builder as builder
import requests
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DataHubRestEmitter
from datahub.metadata.schema_classes import (ChangeTypeClass,
                                             DatasetPropertiesClass)
from dflow import S3Artifact, upload_artifact

from .artifacts import Artifact, GitArtifact, HTTPArtifact, LocalPath
from .utils.query import (DATASET_PREFIX, MODEL_PREFIX, OP_PREDIX, PLATFORM,
                    WORKFLOW_PREFIX, info2urn_query, dataset_urn_query)

test_gms_domain = "https://datahub-gms.dp.tech"
test_domain = "https://datahub.dp.tech"

def obj_to_dict(obj):
    if isinstance(obj, Artifact):
        return obj.to_dict()
    elif isinstance(obj, S3Artifact):
        return {"s3": obj.to_dict()}
    elif isinstance(obj, Model):
        return {"model": {"id": obj.id}}
    elif isinstance(obj, Dataset):
        return {"dataset": {"id": obj.id}}


def obj_from_dict(d):
    if "model" in d:
        return Model.query(id=d["model"]["id"])
    if "dataset" in d:
        return Dataset.query(id=d["dataset"]["id"])
    else:
        return Artifact.from_dict(d)


class Model:

    def __init__(self,
                 namespace: str,
                 name: str,
                 version: str,
                 description: str = None,
                 readme: str = None,
                 author: str = None,
                 labels: Dict[str, str] = None,
                 status: str = None,
                 size: int = None,
                 id: str = None,
                 location: Union[HTTPArtifact, LocalPath, S3Artifact,
                                 Dict[str, Union[LocalPath,
                                                 S3Artifact, HTTPArtifact]],
                                 List[Union[LocalPath, S3Artifact,
                                            HTTPArtifact]]] = None,
                 code: GitArtifact = None,
                 source: Union[HTTPArtifact, LocalPath, S3Artifact, "Dataset",
                               Dict[str, Union[HTTPArtifact, LocalPath,
                                               S3Artifact, "Dataset"]],
                               List[Union[HTTPArtifact, LocalPath,
                                          S3Artifact, "Dataset"]]] = None,
                 parameters: Union[dict, LocalPath] = None,
                 spec: Union[dict, LocalPath] = None,
                 resources: Union[HTTPArtifact, LocalPath, S3Artifact,
                                  "Dataset",
                                  Dict[str, Union[HTTPArtifact, LocalPath,
                                                  S3Artifact, "Dataset"]],
                                  List[Union[HTTPArtifact, LocalPath,
                                             S3Artifact, "Dataset"]]] = None,
                 **kwargs,
                 ) -> None:
        """
        Model

        Args:
            namespace: namespace
            name: name
            version: version
            description: short description
            readme: long description
            author: author
            labels: labels
            status: status
            size: artifact size
            location: storage location, either locally or remotely
            code: source code used for generating the model
            source: artifacts used for generating the model
            parameters: parameters used for generating the model
            spec: specification of the model
            resources: related artifacts of the model
        """
        self.namespace = namespace
        self.name = name
        self.description = description
        self.readme = readme
        self.author = author
        self.version = version
        self.labels = labels
        self.status = status
        self.size = size
        self.location = location
        self.code = code
        self.source = source
        self.parameters = parameters
        self.spec = spec
        self.resources = resources
        self.id = id

    def __repr__(self):
        return "<Model %s/%s:%s>" % (self.namespace, self.name, self.version)

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if value is None:
                continue
            if key in ["location", "code", "source", "resources"]:
                if value is None:
                    d[key] = None
                elif isinstance(value, (Artifact, S3Artifact, Model, Dataset)):
                    d[key] = json.dumps(obj_to_dict(value))
                elif isinstance(value, dict):
                    d[key] = json.dumps({"dict": {k: obj_to_dict(v) for k, v in value.items()}})
                elif isinstance(value, list):
                    d[key] = json.dumps({"list": [obj_to_dict(i) for i in value]})
                else:
                    raise TypeError("%s is not supported artifact"
                                    % type(value))
            else:
                d[key] = value
        return d

    @classmethod
    def from_dict(cls, d):
        kwargs = {}
        for key, value in d.items():
            if key in ["location", "code", "source", "resources"]:
                if not value:
                    kwargs[key] = None
                elif "dict" in value:
                    kwargs[key] = {k: obj_from_dict(v) for k, v in
                                   value["dict"].items()}
                elif "list" in value:
                    kwargs[key] = [obj_from_dict(i) for i in value["list"]]
                else:
                    kwargs[key] = obj_from_dict(value)
            else:
                kwargs[key] = value
        return cls(**kwargs)

    def handle_local_artifacts(self):
        for key in ["location", "code", "source", "resources"]:
            value = getattr(self, key)
            if isinstance(value, LocalPath):
                setattr(self, key, upload_artifact(value.path))
            elif isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, LocalPath):
                        value[k] = upload_artifact(v.path)
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    if isinstance(v, LocalPath):
                        value[i] = upload_artifact(v.path)

    def insert(self,
               domain: str = test_gms_domain,
               token: str = None):
        emiter = DataHubRestEmitter(gms_server=domain, token=token)
        emiter.test_connection()
        self.handle_local_artifacts()
        urn = builder.make_dataset_urn(PLATFORM, "%s.%s.%s:%s" % (MODEL_PREFIX, self.namespace, self.name, self.version))
        dataset_properties = DatasetPropertiesClass(
            description=self.description,
            customProperties=self.to_dict(),
        )
        metadata_event = MetadataChangeProposalWrapper(
            entityType="dataset",
            entityUrn=urn,
            aspect=dataset_properties,
            aspectName="datasetProperties"
        )
        emiter.emit(metadata_event)

    @classmethod
    def query(cls,
              namespace: str = None,
              name: str = None,
              version: str = None,
              domain: str = test_domain,
              id: str = None,
              token: str = None,
              count: int = 10,
              force: bool = False) -> list:
        # todo
        # add force
        # 因为query包含模糊搜索的原因现在的接口对于数据的过滤能力并不好
        urn_query = info2urn_query(namespace=namespace,
                                   name=name,
                                   version=version,
                                   count=count)
        domain = domain + "/api/graphql"
        headers = {}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        res = requests.post(url=domain, headers=headers, data=json.dumps(urn_query))
        if res.status_code < 200 or res.status_code > 299:
            print("got unexpected code %d" % res.status_code)
            return
        d = json.loads(res.text).get("data", {}).get("searchAcrossEntities", {}).get("searchResults", [])
        if d is []:
            return []
        urn_list = []
        for entity in d:
            urn = entity.get("entity", {}).get("urn", None)
            if urn is not None:
                urn_list.append(urn)
        dataset_list = []
        for urn in urn_list:
            query = dataset_urn_query(urn)
            res = requests.post(url=domain, headers=headers, data=json.dumps(query))
            d = json.loads(res.text).get("data", {}).get("dataset", {}).get("properties", {}).get("customProperties", {})
            if d is {}:
                continue
            self_dict = {}
            for _dict in d:
                self_dict[_dict["key"]] = _dict["value"]
            dataset_list.append(Model.from_dict(self_dict))
        return dataset_list


class Dataset:

    def __init__(self,
                 namespace: str,
                 name: str,
                 version: str,
                 description: str = None,
                 readme: str = None,
                 author: str = None,
                 labels: Dict[str, str] = None,
                 status: str = None,
                 size: int = None,
                 id: str = None,
                 location: Union[HTTPArtifact, LocalPath, S3Artifact,
                                 Dict[str, Union[LocalPath,
                                                 S3Artifact, HTTPArtifact]],
                                 List[Union[LocalPath, S3Artifact,
                                            HTTPArtifact]]] = None,
                 code: GitArtifact = None,
                 source: Union[HTTPArtifact, LocalPath, S3Artifact, "Dataset",
                               Dict[str, Union[HTTPArtifact, LocalPath,
                                               S3Artifact, "Dataset"]],
                               List[Union[HTTPArtifact, LocalPath,
                                          S3Artifact, "Dataset"]]] = None,
                 parameters: Union[dict, LocalPath] = None,
                 spec: Union[dict, LocalPath] = None,
                 resources: Union[HTTPArtifact, LocalPath, S3Artifact,
                                  "Dataset",
                                  Dict[str, Union[HTTPArtifact, LocalPath,
                                                  S3Artifact, "Dataset"]],
                                  List[Union[HTTPArtifact, LocalPath,
                                             S3Artifact, "Dataset"]]] = None,
                 **kwargs,
                 ) -> None:
        self.namespace = namespace
        self.name = name
        self.description = description
        self.readme = readme
        self.author = author
        self.version = version
        self.labels = labels
        self.status = status
        self.size = size
        self.location = location
        self.code = code
        self.source = source
        self.parameters = parameters
        self.spec = spec
        self.resources = resources
        self.id = id

    def __repr__(self):
        return "<Dataset %s/%s:%s>" % (self.namespace, self.name, self.version)

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if value is None:
                continue
            if key in ["location", "code", "source", "resources"]:
                if value is None:
                    d[key] = None
                elif isinstance(value, (Artifact, S3Artifact, Model, Dataset)):
                    d[key] = json.dumps(obj_to_dict(value))
                elif isinstance(value, dict):
                    d[key] = json.dumps({"dict": {k: obj_to_dict(v) for k, v in value.items()}})
                elif isinstance(value, list):
                    d[key] = json.dumps({"list": [obj_to_dict(i) for i in value]})
                else:
                    raise TypeError("%s is not supported artifact"
                                    % type(value))
            else:
                d[key] = value
        return d

    @classmethod
    def from_dict(cls, d):
        kwargs = {}
        for key, value in d.items():
            if key in ["location", "code", "source", "resources"]:
                if not value:
                    kwargs[key] = None
                elif "dict" in value:
                    value = json.loads(value)
                    kwargs[key] = {k: obj_from_dict(v) for k, v in
                                   value["dict"].items()}
                elif "list" in value:
                    value = json.loads(value)
                    kwargs[key] = [obj_from_dict(i) for i in value["list"]]
                else:
                    value = json.loads(value)
                    kwargs[key] = obj_from_dict(value)
            else:
                kwargs[key] = value
        return cls(**kwargs)

    def handle_local_artifacts(self):
        for key in ["location", "code", "source", "resources"]:
            value = getattr(self, key)
            if isinstance(value, LocalPath):
                setattr(self, key, upload_artifact(value.path))
            elif isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, LocalPath):
                        value[k] = upload_artifact(v.path)
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    if isinstance(v, LocalPath):
                        value[i] = upload_artifact(v.path)

    def insert(self,
               domain: str = test_gms_domain,
               token: str = None):
        emiter = DataHubRestEmitter(gms_server=domain, token=token)
        emiter.test_connection()
        self.handle_local_artifacts()
        urn = builder.make_dataset_urn(PLATFORM, "%s.%s.%s.%s" % (DATASET_PREFIX, self.namespace, self.name, self.version))
        d = self.to_dict()
        dataset_properties = DatasetPropertiesClass(
            description=self.description,
            customProperties=d,
        )
        metadata_event = MetadataChangeProposalWrapper(
            entityType="dataset",
            entityUrn=urn,
            aspect=dataset_properties,
            aspectName="datasetProperties"
        )
        emiter.emit(metadata_event)

    @classmethod
    def query(cls,
              namespace: str = None,
              name: str = None,
              version: str = None,
              domain: str = test_domain,
              id: int = None,
              token: str = None,
              count: int = 10,
              force: bool = False) -> list:
        urn_query = info2urn_query(namespace=namespace,
                                   name=name,
                                   version=version,
                                   count=count)
        domain = domain + "/api/graphql"
        headers = {}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        res = requests.post(url=domain, headers=headers, data=json.dumps(urn_query))
        if res.status_code < 200 or res.status_code > 299:
            print("got unexpected code %d" % res.status_code)
            return
        d = json.loads(res.text).get("data", {}).get("searchAcrossEntities", {}).get("searchResults", [])
        if d is []:
            return []
        urn_list = []
        for entity in d:
            urn = entity.get("entity", {}).get("urn", None)
            if urn is not None:
                urn_list.append(urn)
        dataset_list = []
        for urn in urn_list:
            query = marsharl_urn2query(urn)
            res = requests.post(url=domain, headers=headers, data=json.dumps(query))
            d = json.loads(res.text).get("data", {}).get("dataset", {}).get("properties", {}).get("customProperties", {})
            if d is {}:
                continue
            self_dict = {}
            for _dict in d:
                self_dict[_dict["key"]] = _dict["value"]
            dataset_list.append(Dataset.from_dict(self_dict))
        return dataset_list


class Workflow:

    def __init__(self,
                 namespace: str,
                 name: str,
                 version: str,
                 description: str = None,
                 readme: str = None,
                 author: str = None,
                 labels: dict = None,
                 status: str = None,
                 code: dict = None,
                 python_package: str = None,
                 docker_image: str = None,
                 id: str = None) -> None:
        self.namespace = namespace
        self.name = name
        self.description = description
        self.readme = readme
        self.author = author
        self.version = version
        self.labels = labels
        self.status = status
        self.code = code
        self.python_package = python_package
        self.docker_image = docker_image
        self.id = id

    def insert(self,
               domain: str = test_domain,
               token: str = None):
        emiter = DataHubRestEmitter(gms_server=domain, token=token)
        emiter.test_connection()
        urn = builder.make_dataset_urn(PLATFORM, "%s.%s.%s:%s" % (WORKFLOW_PREFIX, self.namespace, self.name, self.version))
        dataset_properties = DatasetPropertiesClass(
            description=self.description,
            customProperties=self.__dict__,
        )
        metadata_event = MetadataChangeProposalWrapper(
            entityType="dataset",
            changeType=ChangeTypeClass.UPSERT,
            entityUrn=urn,
            aspect=dataset_properties,
            aspectName="datasetProperties"
        )
        emiter.emit(metadata_event)

    @classmethod
    def query(cls,
              namespace: str = None,
              name: str = None,
              version: str = None,
              domain: str = test_gms_domain,
              id: str = None,
              count: int = 10,
              force: bool = False,
              token: str = None) -> list:
        urn_query = info2urn_query(namespace=namespace,
                                   name=name,
                                   version=version,
                                   count=count)
        domain = domain + "/api/graphql"
        headers = {}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        res = requests.post(url=domain, headers=headers, data=json.dumps(urn_query))
        if res.status_code < 200 or res.status_code > 299:
            print("got unexpected code %d" % res.status_code)
            return
        d = json.loads(res.text).get("data", {}).get("searchAcrossEntities", {}).get("searchResults", [])
        if d is []:
            return []
        urn_list = []
        for entity in d:
            urn = entity.get("entity", {}).get("urn", None)
            if urn is not None:
                urn_list.append(urn)
        dataset_list = []
        for urn in urn_list:
            query = marsharl_urn2query(urn)
            res = requests.post(url=domain, headers=headers, data=json.dumps(query))
            d = json.loads(res.text).get("data", {}).get("dataset", {}).get("properties", {}).get("customProperties", {})
            if d is {}:
                continue
            self_dict = {}
            for _dict in d:
                self_dict[_dict["key"]] = _dict["value"]
            workflow = cls(namespace, name, version)
            for k, v in self_dict:
                workflow.__setattr__(k, v)
        return dataset_list


class OP:

    def __init__(self,
                 namespace: str,
                 name: str,
                 version: str,
                 description: str = None,
                 readme: str = None,
                 author: str = None,
                 labels: dict = None,
                 status: str = None,
                 code: dict = None,
                 python_package: str = None,
                 docker_image: str = None,
                 inputs: dict = None,
                 outputs: dict = None,
                 execute: dict = None,
                 id: str = None) -> None:
        self.namespace = namespace
        self.name = name
        self.description = description
        self.readme = readme
        self.author = author
        self.version = version
        self.labels = labels
        self.status = status
        self.code = code
        self.python_package = python_package
        self.docker_image = docker_image
        self.inputs = inputs
        self.outputs = outputs
        self.execute = execute
        self.id = id

    def insert(self,
               domain: str = test_gms_domain,
               token: str = None):
        emiter = DataHubRestEmitter(gms_server=domain, token=token)
        emiter.test_connection()
        urn = builder.make_dataset_urn(PLATFORM, "%s.%s.%s:%s" % (OP_PREDIX, self.namespace, self.name, self.version))
        dataset_properties = DatasetPropertiesClass(
            description=self.description,
            customProperties=self.__dict__,
        )
        metadata_event = MetadataChangeProposalWrapper(
            entityType="dataset",
            entityUrn=urn,
            aspect=dataset_properties,
            aspectName="datasetProperties"
        )
        emiter.emit(metadata_event)

    @classmethod
    def query(cls,
              namespace: str = None,
              name: str = None,
              version: str = None,
              domain: str = test_domain,
              id: str = None,
              count: int = 10,
              force: bool = False,
              token: str = None) -> list:
        urn_query = info2urn_query(namespace=namespace,
                                   name=name,
                                   version=version,
                                   count=count)
        domain = domain + "/api/graphql"
        headers = {}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        res = requests.post(url=domain, headers=headers, data=json.dumps(urn_query))
        if res.status_code < 200 or res.status_code > 299:
            print("got unexpected code %d" % res.status_code)
            return
        d = json.loads(res.text).get("data", {}).get("searchAcrossEntities", {}).get("searchResults", [])
        if d is []:
            return []
        urn_list = []
        for entity in d:
            urn = entity.get("entity", {}).get("urn", None)
            if urn is not None:
                urn_list.append(urn)
        dataset_list = []
        for urn in urn_list:
            query = marsharl_urn2query(urn)
            res = requests.post(url=domain, headers=headers, data=json.dumps(query))
            d = json.loads(res.text).get("data", {}).get("dataset", {}).get("properties", {}).get("customProperties", {})
            if d is {}:
                continue
            self_dict = {}
            for _dict in d:
                self_dict[_dict["key"]] = _dict["value"]
            workflow = cls(namespace, name, version)
            for k, v in self_dict:
                workflow.__setattr__(k, v)
        return dataset_list
