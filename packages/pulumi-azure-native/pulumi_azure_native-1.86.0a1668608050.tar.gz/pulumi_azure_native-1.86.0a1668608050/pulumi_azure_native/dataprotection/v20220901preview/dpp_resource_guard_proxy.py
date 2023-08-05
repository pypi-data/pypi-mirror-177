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

__all__ = ['DppResourceGuardProxyArgs', 'DppResourceGuardProxy']

@pulumi.input_type
class DppResourceGuardProxyArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 vault_name: pulumi.Input[str],
                 properties: Optional[pulumi.Input['ResourceGuardProxyBaseArgs']] = None,
                 resource_guard_proxy_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DppResourceGuardProxy resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the backup vault is present.
        :param pulumi.Input[str] vault_name: The name of the backup vault.
        :param pulumi.Input['ResourceGuardProxyBaseArgs'] properties: ResourceGuardProxyBaseResource properties
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "vault_name", vault_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_guard_proxy_name is not None:
            pulumi.set(__self__, "resource_guard_proxy_name", resource_guard_proxy_name)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the backup vault is present.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="vaultName")
    def vault_name(self) -> pulumi.Input[str]:
        """
        The name of the backup vault.
        """
        return pulumi.get(self, "vault_name")

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['ResourceGuardProxyBaseArgs']]:
        """
        ResourceGuardProxyBaseResource properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['ResourceGuardProxyBaseArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceGuardProxyName")
    def resource_guard_proxy_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_guard_proxy_name")

    @resource_guard_proxy_name.setter
    def resource_guard_proxy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_guard_proxy_name", value)


class DppResourceGuardProxy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ResourceGuardProxyBaseArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guard_proxy_name: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a DppResourceGuardProxy resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ResourceGuardProxyBaseArgs']] properties: ResourceGuardProxyBaseResource properties
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the backup vault is present.
        :param pulumi.Input[str] vault_name: The name of the backup vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DppResourceGuardProxyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a DppResourceGuardProxy resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param DppResourceGuardProxyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DppResourceGuardProxyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ResourceGuardProxyBaseArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guard_proxy_name: Optional[pulumi.Input[str]] = None,
                 vault_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DppResourceGuardProxyArgs.__new__(DppResourceGuardProxyArgs)

            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_guard_proxy_name"] = resource_guard_proxy_name
            if vault_name is None and not opts.urn:
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__["vault_name"] = vault_name
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:dataprotection/v20221001preview:DppResourceGuardProxy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DppResourceGuardProxy, __self__).__init__(
            'azure-native:dataprotection/v20220901preview:DppResourceGuardProxy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DppResourceGuardProxy':
        """
        Get an existing DppResourceGuardProxy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DppResourceGuardProxyArgs.__new__(DppResourceGuardProxyArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return DppResourceGuardProxy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name associated with the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ResourceGuardProxyBaseResponse']:
        """
        ResourceGuardProxyBaseResource properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        return pulumi.get(self, "type")

