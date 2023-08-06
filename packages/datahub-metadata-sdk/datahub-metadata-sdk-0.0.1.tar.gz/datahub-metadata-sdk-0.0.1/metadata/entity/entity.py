# -*- encoding: utf-8 -*-

import uuid
from dataclasses import dataclass

from metadata.ensure import ensure_entity_urn_format

@dataclass
class Entity:

    urn: str

    def __post_init__(self):
        ensure_entity_urn_format(self.urn)

    @classmethod
    def _gen_qual_name(cls, context, name, auto_suffix):
        project = context.project
        suffix = ('-' + uuid.uuid4().hex[:6]) if auto_suffix else ''
        qualified_name = f'{project}.{name}{suffix}'
        return qualified_name