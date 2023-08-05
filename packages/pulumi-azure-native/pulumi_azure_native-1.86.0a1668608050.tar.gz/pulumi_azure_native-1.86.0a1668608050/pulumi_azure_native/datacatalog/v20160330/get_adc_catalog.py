# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetADCCatalogResult',
    'AwaitableGetADCCatalogResult',
    'get_adc_catalog',
    'get_adc_catalog_output',
]

@pulumi.output_type
class GetADCCatalogResult:
    """
    Azure Data Catalog.
    """
    def __init__(__self__, admins=None, enable_automatic_unit_adjustment=None, etag=None, id=None, location=None, name=None, sku=None, successfully_provisioned=None, tags=None, type=None, units=None, users=None):
        if admins and not isinstance(admins, list):
            raise TypeError("Expected argument 'admins' to be a list")
        pulumi.set(__self__, "admins", admins)
        if enable_automatic_unit_adjustment and not isinstance(enable_automatic_unit_adjustment, bool):
            raise TypeError("Expected argument 'enable_automatic_unit_adjustment' to be a bool")
        pulumi.set(__self__, "enable_automatic_unit_adjustment", enable_automatic_unit_adjustment)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if successfully_provisioned and not isinstance(successfully_provisioned, bool):
            raise TypeError("Expected argument 'successfully_provisioned' to be a bool")
        pulumi.set(__self__, "successfully_provisioned", successfully_provisioned)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if units and not isinstance(units, int):
            raise TypeError("Expected argument 'units' to be a int")
        pulumi.set(__self__, "units", units)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def admins(self) -> Optional[Sequence['outputs.PrincipalsResponse']]:
        """
        Azure data catalog admin list.
        """
        return pulumi.get(self, "admins")

    @property
    @pulumi.getter(name="enableAutomaticUnitAdjustment")
    def enable_automatic_unit_adjustment(self) -> Optional[bool]:
        """
        Automatic unit adjustment enabled or not.
        """
        return pulumi.get(self, "enable_automatic_unit_adjustment")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Resource etag
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sku(self) -> Optional[str]:
        """
        Azure data catalog SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="successfullyProvisioned")
    def successfully_provisioned(self) -> Optional[bool]:
        """
        Azure data catalog provision status.
        """
        return pulumi.get(self, "successfully_provisioned")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def units(self) -> Optional[int]:
        """
        Azure data catalog units.
        """
        return pulumi.get(self, "units")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence['outputs.PrincipalsResponse']]:
        """
        Azure data catalog user list.
        """
        return pulumi.get(self, "users")


class AwaitableGetADCCatalogResult(GetADCCatalogResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetADCCatalogResult(
            admins=self.admins,
            enable_automatic_unit_adjustment=self.enable_automatic_unit_adjustment,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            sku=self.sku,
            successfully_provisioned=self.successfully_provisioned,
            tags=self.tags,
            type=self.type,
            units=self.units,
            users=self.users)


def get_adc_catalog(catalog_name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetADCCatalogResult:
    """
    Azure Data Catalog.


    :param str catalog_name: The name of the data catalog in the specified subscription and resource group.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['catalogName'] = catalog_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:datacatalog/v20160330:getADCCatalog', __args__, opts=opts, typ=GetADCCatalogResult).value

    return AwaitableGetADCCatalogResult(
        admins=__ret__.admins,
        enable_automatic_unit_adjustment=__ret__.enable_automatic_unit_adjustment,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        sku=__ret__.sku,
        successfully_provisioned=__ret__.successfully_provisioned,
        tags=__ret__.tags,
        type=__ret__.type,
        units=__ret__.units,
        users=__ret__.users)


@_utilities.lift_output_func(get_adc_catalog)
def get_adc_catalog_output(catalog_name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetADCCatalogResult]:
    """
    Azure Data Catalog.


    :param str catalog_name: The name of the data catalog in the specified subscription and resource group.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    ...
