# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetWebAppSwiftVirtualNetworkConnectionSlotResult',
    'AwaitableGetWebAppSwiftVirtualNetworkConnectionSlotResult',
    'get_web_app_swift_virtual_network_connection_slot',
    'get_web_app_swift_virtual_network_connection_slot_output',
]

@pulumi.output_type
class GetWebAppSwiftVirtualNetworkConnectionSlotResult:
    """
    Swift Virtual Network Contract. This is used to enable the new Swift way of doing virtual network integration.
    """
    def __init__(__self__, id=None, kind=None, name=None, subnet_resource_id=None, swift_supported=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if subnet_resource_id and not isinstance(subnet_resource_id, str):
            raise TypeError("Expected argument 'subnet_resource_id' to be a str")
        pulumi.set(__self__, "subnet_resource_id", subnet_resource_id)
        if swift_supported and not isinstance(swift_supported, bool):
            raise TypeError("Expected argument 'swift_supported' to be a bool")
        pulumi.set(__self__, "swift_supported", swift_supported)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subnetResourceId")
    def subnet_resource_id(self) -> Optional[str]:
        """
        The Virtual Network subnet's resource ID. This is the subnet that this Web App will join. This subnet must have a delegation to Microsoft.Web/serverFarms defined first.
        """
        return pulumi.get(self, "subnet_resource_id")

    @property
    @pulumi.getter(name="swiftSupported")
    def swift_supported(self) -> Optional[bool]:
        """
        A flag that specifies if the scale unit this Web App is on supports Swift integration.
        """
        return pulumi.get(self, "swift_supported")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWebAppSwiftVirtualNetworkConnectionSlotResult(GetWebAppSwiftVirtualNetworkConnectionSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppSwiftVirtualNetworkConnectionSlotResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            subnet_resource_id=self.subnet_resource_id,
            swift_supported=self.swift_supported,
            type=self.type)


def get_web_app_swift_virtual_network_connection_slot(name: Optional[str] = None,
                                                      resource_group_name: Optional[str] = None,
                                                      slot: Optional[str] = None,
                                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppSwiftVirtualNetworkConnectionSlotResult:
    """
    Swift Virtual Network Contract. This is used to enable the new Swift way of doing virtual network integration.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get a gateway for the production slot's Virtual Network.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20210201:getWebAppSwiftVirtualNetworkConnectionSlot', __args__, opts=opts, typ=GetWebAppSwiftVirtualNetworkConnectionSlotResult).value

    return AwaitableGetWebAppSwiftVirtualNetworkConnectionSlotResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        subnet_resource_id=__ret__.subnet_resource_id,
        swift_supported=__ret__.swift_supported,
        type=__ret__.type)


@_utilities.lift_output_func(get_web_app_swift_virtual_network_connection_slot)
def get_web_app_swift_virtual_network_connection_slot_output(name: Optional[pulumi.Input[str]] = None,
                                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                                             slot: Optional[pulumi.Input[str]] = None,
                                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebAppSwiftVirtualNetworkConnectionSlotResult]:
    """
    Swift Virtual Network Contract. This is used to enable the new Swift way of doing virtual network integration.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get a gateway for the production slot's Virtual Network.
    """
    ...
