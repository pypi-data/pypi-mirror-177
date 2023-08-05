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
from ._enums import *
from ._inputs import *

__all__ = ['NetworkInterfaceTapConfigurationArgs', 'NetworkInterfaceTapConfiguration']

@pulumi.input_type
class NetworkInterfaceTapConfigurationArgs:
    def __init__(__self__, *,
                 network_interface_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tap_configuration_name: Optional[pulumi.Input[str]] = None,
                 virtual_network_tap: Optional[pulumi.Input['VirtualNetworkTapArgs']] = None):
        """
        The set of arguments for constructing a NetworkInterfaceTapConfiguration resource.
        :param pulumi.Input[str] network_interface_name: The name of the network interface.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] tap_configuration_name: The name of the tap configuration.
        :param pulumi.Input['VirtualNetworkTapArgs'] virtual_network_tap: The reference of the Virtual Network Tap resource.
        """
        pulumi.set(__self__, "network_interface_name", network_interface_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tap_configuration_name is not None:
            pulumi.set(__self__, "tap_configuration_name", tap_configuration_name)
        if virtual_network_tap is not None:
            pulumi.set(__self__, "virtual_network_tap", virtual_network_tap)

    @property
    @pulumi.getter(name="networkInterfaceName")
    def network_interface_name(self) -> pulumi.Input[str]:
        """
        The name of the network interface.
        """
        return pulumi.get(self, "network_interface_name")

    @network_interface_name.setter
    def network_interface_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_interface_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="tapConfigurationName")
    def tap_configuration_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the tap configuration.
        """
        return pulumi.get(self, "tap_configuration_name")

    @tap_configuration_name.setter
    def tap_configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tap_configuration_name", value)

    @property
    @pulumi.getter(name="virtualNetworkTap")
    def virtual_network_tap(self) -> Optional[pulumi.Input['VirtualNetworkTapArgs']]:
        """
        The reference of the Virtual Network Tap resource.
        """
        return pulumi.get(self, "virtual_network_tap")

    @virtual_network_tap.setter
    def virtual_network_tap(self, value: Optional[pulumi.Input['VirtualNetworkTapArgs']]):
        pulumi.set(self, "virtual_network_tap", value)


class NetworkInterfaceTapConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_interface_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tap_configuration_name: Optional[pulumi.Input[str]] = None,
                 virtual_network_tap: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkTapArgs']]] = None,
                 __props__=None):
        """
        Tap configuration in a Network Interface.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] network_interface_name: The name of the network interface.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] tap_configuration_name: The name of the tap configuration.
        :param pulumi.Input[pulumi.InputType['VirtualNetworkTapArgs']] virtual_network_tap: The reference of the Virtual Network Tap resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkInterfaceTapConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Tap configuration in a Network Interface.

        :param str resource_name: The name of the resource.
        :param NetworkInterfaceTapConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkInterfaceTapConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_interface_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tap_configuration_name: Optional[pulumi.Input[str]] = None,
                 virtual_network_tap: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkTapArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkInterfaceTapConfigurationArgs.__new__(NetworkInterfaceTapConfigurationArgs)

            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            if network_interface_name is None and not opts.urn:
                raise TypeError("Missing required property 'network_interface_name'")
            __props__.__dict__["network_interface_name"] = network_interface_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tap_configuration_name"] = tap_configuration_name
            __props__.__dict__["virtual_network_tap"] = virtual_network_tap
            __props__.__dict__["etag"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20180801:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20181001:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20181101:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20181201:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20190201:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20190401:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20190601:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20190701:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20190801:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20191101:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20191201:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20200301:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20200401:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20200501:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20200601:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20200701:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20200801:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20201101:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20210201:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20210301:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20210501:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20210801:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20220101:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20220501:NetworkInterfaceTapConfiguration"), pulumi.Alias(type_="azure-native:network/v20220701:NetworkInterfaceTapConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NetworkInterfaceTapConfiguration, __self__).__init__(
            'azure-native:network/v20190901:NetworkInterfaceTapConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkInterfaceTapConfiguration':
        """
        Get an existing NetworkInterfaceTapConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkInterfaceTapConfigurationArgs.__new__(NetworkInterfaceTapConfigurationArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_network_tap"] = None
        return NetworkInterfaceTapConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the network interface tap configuration resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Sub Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualNetworkTap")
    def virtual_network_tap(self) -> pulumi.Output[Optional['outputs.VirtualNetworkTapResponse']]:
        """
        The reference of the Virtual Network Tap resource.
        """
        return pulumi.get(self, "virtual_network_tap")

