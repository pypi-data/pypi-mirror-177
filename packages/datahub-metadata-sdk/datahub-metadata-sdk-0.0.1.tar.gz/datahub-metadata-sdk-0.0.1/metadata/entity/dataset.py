# -*- coding: utf-8 -*-

from collections.abc import Mapping
from dataclasses import dataclass, field

from metadata.ensure import ensure_entity_name_format, ensure_uri_format, ensure_platform_format
from metadata.entity.entity import Entity

@dataclass
class Dataset(Entity):

    display_name: str
    uri: str
    description: str = field(repr=False, default='')
    tags: list[str] = field(repr=False, default_factory=list)
    properties: Mapping[str, str] = field(repr=False, default_factory=dict)

    def __post_init__(self):
        ensure_uri_format(self.uri)

    @classmethod
    def gen_urn(cls, context, platform, name, auto_suffix=True):
        ensure_entity_name_format(name)
        env = context.env
        ensure_platform_format(platform)
        qualified_name = cls._gen_qual_name(context, name, auto_suffix=auto_suffix)
        return f'urn:li:dataset:(urn:li:dataPlatform:{platform},{qualified_name},{env})'