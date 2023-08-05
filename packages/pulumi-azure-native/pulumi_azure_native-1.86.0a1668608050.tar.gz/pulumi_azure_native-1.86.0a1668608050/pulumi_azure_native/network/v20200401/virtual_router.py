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

__all__ = ['VirtualRouterArgs', 'VirtualRouter']

@pulumi.input_type
class VirtualRouterArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 hosted_gateway: Optional[pulumi.Input['SubResourceArgs']] = None,
                 hosted_subnet: Optional[pulumi.Input['SubResourceArgs']] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_router_asn: Optional[pulumi.Input[float]] = None,
                 virtual_router_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 virtual_router_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a VirtualRouter resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['SubResourceArgs'] hosted_gateway: The Gateway on which VirtualRouter is hosted.
        :param pulumi.Input['SubResourceArgs'] hosted_subnet: The Subnet on which VirtualRouter is hosted.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[float] virtual_router_asn: VirtualRouter ASN.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] virtual_router_ips: VirtualRouter IPs.
        :param pulumi.Input[str] virtual_router_name: The name of the Virtual Router.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if hosted_gateway is not None:
            pulumi.set(__self__, "hosted_gateway", hosted_gateway)
        if hosted_subnet is not None:
            pulumi.set(__self__, "hosted_subnet", hosted_subnet)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if virtual_router_asn is not None:
            pulumi.set(__self__, "virtual_router_asn", virtual_router_asn)
        if virtual_router_ips is not None:
            pulumi.set(__self__, "virtual_router_ips", virtual_router_ips)
        if virtual_router_name is not None:
            pulumi.set(__self__, "virtual_router_name", virtual_router_name)

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
    @pulumi.getter(name="hostedGateway")
    def hosted_gateway(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The Gateway on which VirtualRouter is hosted.
        """
        return pulumi.get(self, "hosted_gateway")

    @hosted_gateway.setter
    def hosted_gateway(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "hosted_gateway", value)

    @property
    @pulumi.getter(name="hostedSubnet")
    def hosted_subnet(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The Subnet on which VirtualRouter is hosted.
        """
        return pulumi.get(self, "hosted_subnet")

    @hosted_subnet.setter
    def hosted_subnet(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "hosted_subnet", value)

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
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="virtualRouterAsn")
    def virtual_router_asn(self) -> Optional[pulumi.Input[float]]:
        """
        VirtualRouter ASN.
        """
        return pulumi.get(self, "virtual_router_asn")

    @virtual_router_asn.setter
    def virtual_router_asn(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "virtual_router_asn", value)

    @property
    @pulumi.getter(name="virtualRouterIps")
    def virtual_router_ips(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        VirtualRouter IPs.
        """
        return pulumi.get(self, "virtual_router_ips")

    @virtual_router_ips.setter
    def virtual_router_ips(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "virtual_router_ips", value)

    @property
    @pulumi.getter(name="virtualRouterName")
    def virtual_router_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Virtual Router.
        """
        return pulumi.get(self, "virtual_router_name")

    @virtual_router_name.setter
    def virtual_router_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_router_name", value)


class VirtualRouter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosted_gateway: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 hosted_subnet: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_router_asn: Optional[pulumi.Input[float]] = None,
                 virtual_router_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 virtual_router_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        VirtualRouter Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] hosted_gateway: The Gateway on which VirtualRouter is hosted.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] hosted_subnet: The Subnet on which VirtualRouter is hosted.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[float] virtual_router_asn: VirtualRouter ASN.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] virtual_router_ips: VirtualRouter IPs.
        :param pulumi.Input[str] virtual_router_name: The name of the Virtual Router.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualRouterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        VirtualRouter Resource.

        :param str resource_name: The name of the resource.
        :param VirtualRouterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualRouterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosted_gateway: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 hosted_subnet: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_router_asn: Optional[pulumi.Input[float]] = None,
                 virtual_router_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 virtual_router_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VirtualRouterArgs.__new__(VirtualRouterArgs)

            __props__.__dict__["hosted_gateway"] = hosted_gateway
            __props__.__dict__["hosted_subnet"] = hosted_subnet
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["virtual_router_asn"] = virtual_router_asn
            __props__.__dict__["virtual_router_ips"] = virtual_router_ips
            __props__.__dict__["virtual_router_name"] = virtual_router_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["peerings"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20190701:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20190801:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20190901:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20191101:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20191201:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20200301:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20200501:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20200601:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20200701:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20200801:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20201101:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20210201:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20210301:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20210501:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20210801:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20220101:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20220501:VirtualRouter"), pulumi.Alias(type_="azure-native:network/v20220701:VirtualRouter")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualRouter, __self__).__init__(
            'azure-native:network/v20200401:VirtualRouter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualRouter':
        """
        Get an existing VirtualRouter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualRouterArgs.__new__(VirtualRouterArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["hosted_gateway"] = None
        __props__.__dict__["hosted_subnet"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["peerings"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_router_asn"] = None
        __props__.__dict__["virtual_router_ips"] = None
        return VirtualRouter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hostedGateway")
    def hosted_gateway(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The Gateway on which VirtualRouter is hosted.
        """
        return pulumi.get(self, "hosted_gateway")

    @property
    @pulumi.getter(name="hostedSubnet")
    def hosted_subnet(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The Subnet on which VirtualRouter is hosted.
        """
        return pulumi.get(self, "hosted_subnet")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def peerings(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to VirtualRouterPeerings.
        """
        return pulumi.get(self, "peerings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualRouterAsn")
    def virtual_router_asn(self) -> pulumi.Output[Optional[float]]:
        """
        VirtualRouter ASN.
        """
        return pulumi.get(self, "virtual_router_asn")

    @property
    @pulumi.getter(name="virtualRouterIps")
    def virtual_router_ips(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        VirtualRouter IPs.
        """
        return pulumi.get(self, "virtual_router_ips")

