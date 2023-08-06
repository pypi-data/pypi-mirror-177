"""base.py
"""
# Python imports
from uuid import uuid4
from datetime import datetime
import logging as _logging

# Third-pary imports
from pydantic import BaseModel, Field, types, PrivateAttr

# Local imports


class ERPItem(BaseModel):
    # Mandatory fields for all ERP items
    id: types.UUID4
    rdf_type: str = Field(alias='rdf:type')
    last_update: datetime = Field(alias=':last_update', default=None)

    # Private field
    _uri_fqdn: str = PrivateAttr(default=None)

    # Computed property
    @property
    def uri(self):
        return F"{self._uri_fqdn}/{self.id}"

    # Constructor
    def __init__(self, uri_fqdn: str, **data):
        super().__init__(**data)
        _logging.debug(F"ERPItem()-uri_fqdn: {uri_fqdn}")
        self._uri_fqdn = uri_fqdn
