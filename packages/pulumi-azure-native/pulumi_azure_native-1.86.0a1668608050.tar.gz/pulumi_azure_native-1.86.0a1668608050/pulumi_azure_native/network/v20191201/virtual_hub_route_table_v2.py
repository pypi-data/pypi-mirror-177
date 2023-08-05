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
from ._inputs import *

__all__ = ['VirtualHubRouteTableV2InitArgs', 'VirtualHubRouteTableV2']

@pulumi.input_type
class VirtualHubRouteTableV2InitArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 virtual_hub_name: pulumi.Input[str],
                 attached_connections: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 route_table_name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualHubRouteV2Args']]]] = None):
        """
        The set of arguments for constructing a VirtualHubRouteTableV2 resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualHub.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attached_connections: List of all connections attached to this route table v2.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] route_table_name: The name of the VirtualHubRouteTableV2.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualHubRouteV2Args']]] routes: List of all routes.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_hub_name", virtual_hub_name)
        if attached_connections is not None:
            pulumi.set(__self__, "attached_connections", attached_connections)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if route_table_name is not None:
            pulumi.set(__self__, "route_table_name", route_table_name)
        if routes is not None:
            pulumi.set(__self__, "routes", routes)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name of the VirtualHub.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="virtualHubName")
    def virtual_hub_name(self) -> pulumi.Input[str]:
        """
        The name of the VirtualHub.
        """
        return pulumi.get(self, "virtual_hub_name")

    @virtual_hub_name.setter
    def virtual_hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_name", value)

    @property
    @pulumi.getter(name="attachedConnections")
    def attached_connections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of all connections attached to this route table v2.
        """
        return pulumi.get(self, "attached_connections")

    @attached_connections.setter
    def attached_connections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "attached_connections", value)

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
    @pulumi.getter(name="routeTableName")
    def route_table_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the VirtualHubRouteTableV2.
        """
        return pulumi.get(self, "route_table_name")

    @route_table_name.setter
    def route_table_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "route_table_name", value)

    @property
    @pulumi.getter
    def routes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualHubRouteV2Args']]]]:
        """
        List of all routes.
        """
        return pulumi.get(self, "routes")

    @routes.setter
    def routes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualHubRouteV2Args']]]]):
        pulumi.set(self, "routes", value)


class VirtualHubRouteTableV2(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attached_connections: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 route_table_name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualHubRouteV2Args']]]]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        VirtualHubRouteTableV2 Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attached_connections: List of all connections attached to this route table v2.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualHub.
        :param pulumi.Input[str] route_table_name: The name of the VirtualHubRouteTableV2.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualHubRouteV2Args']]]] routes: List of all routes.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualHubRouteTableV2InitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        VirtualHubRouteTableV2 Resource.

        :param str resource_name: The name of the resource.
        :param VirtualHubRouteTableV2InitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualHubRouteTableV2InitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attached_connections: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 route_table_name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualHubRouteV2Args']]]]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VirtualHubRouteTableV2InitArgs.__new__(VirtualHubRouteTableV2InitArgs)

            __props__.__dict__["attached_connections"] = attached_connections
            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["route_table_name"] = route_table_name
            __props__.__dict__["routes"] = routes
            if virtual_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_name'")
            __props__.__dict__["virtual_hub_name"] = virtual_hub_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20190901:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20191101:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20200301:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20200401:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20200501:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20200601:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20200701:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20200801:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20201101:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20210201:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20210301:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20210501:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20210801:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20220101:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20220501:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-native:network/v20220701:VirtualHubRouteTableV2")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualHubRouteTableV2, __self__).__init__(
            'azure-native:network/v20191201:VirtualHubRouteTableV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualHubRouteTableV2':
        """
        Get an existing VirtualHubRouteTableV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualHubRouteTableV2InitArgs.__new__(VirtualHubRouteTableV2InitArgs)

        __props__.__dict__["attached_connections"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["routes"] = None
        return VirtualHubRouteTableV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachedConnections")
    def attached_connections(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of all connections attached to this route table v2.
        """
        return pulumi.get(self, "attached_connections")

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
        The provisioning state of the virtual hub route table v2 resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def routes(self) -> pulumi.Output[Optional[Sequence['outputs.VirtualHubRouteV2Response']]]:
        """
        List of all routes.
        """
        return pulumi.get(self, "routes")

