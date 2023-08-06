"""data.pu
"""
# Python imports
from uuid import uuid4
import logging as _logging
from datetime import datetime

# Third-pary imports
from pydantic import BaseModel, Field, types

# Local imports
from .base import ERPItem


class InventoryAccount(ERPItem):
    sku: str = Field(alias=':sku')
    lifecycle_state: str = Field(alias=':lifecycle_state')
    consignor: str = Field(alias=':consignor')
    location: str = Field(alias=':location')


class SKU(ERPItem):
    rdfs_label: str = Field(alias='rdfs:label')
    asset: str = Field(alias=':asset')
    formfactor: str = Field(alias=':formfactor')


class LifeCycleState(ERPItem):
    index: int = Field(alias=':index')
    rdfs_label: str = Field(alias='rdfs:label')
    verb: str = Field(alias=':verb')


class Consignor(ERPItem):
    rdfs_label: str = Field(alias='rdfs:label')


class Location(ERPItem):
    rdfs_label: str = Field(alias='rdfs:label')


class Asset(ERPItem):
    rdfs_label: str = Field(alias='rdfs:label')
    asset_type: str = Field(alias=':asset_type')


class FormFactor(ERPItem):
    rdfs_label: str = Field(alias='rdfs:label')


class AssetType(ERPItem):
    rdfs_label: str = Field(alias='rdfs:label')
    parent_type: str = Field(alias=':parent_type')
