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

__all__ = ['ReplicationPolicyArgs', 'ReplicationPolicy']

@pulumi.input_type
class ReplicationPolicyArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['CreatePolicyInputPropertiesArgs']] = None):
        """
        The set of arguments for constructing a ReplicationPolicy resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name: The name of the recovery services vault.
        :param pulumi.Input[str] policy_name: Replication policy name.
        :param pulumi.Input['CreatePolicyInputPropertiesArgs'] properties: Policy creation properties.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if policy_name is not None:
            pulumi.set(__self__, "policy_name", policy_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the recovery services vault is present.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the recovery services vault.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Replication policy name.
        """
        return pulumi.get(self, "policy_name")

    @policy_name.setter
    def policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['CreatePolicyInputPropertiesArgs']]:
        """
        Policy creation properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['CreatePolicyInputPropertiesArgs']]):
        pulumi.set(self, "properties", value)


class ReplicationPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CreatePolicyInputPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Protection profile details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_name: Replication policy name.
        :param pulumi.Input[pulumi.InputType['CreatePolicyInputPropertiesArgs']] properties: Policy creation properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name_: The name of the recovery services vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Protection profile details.

        :param str resource_name: The name of the resource.
        :param ReplicationPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CreatePolicyInputPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationPolicyArgs.__new__(ReplicationPolicyArgs)

            __props__.__dict__["policy_name"] = policy_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20160810:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20180110:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20180710:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210210:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210601:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210701:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20211101:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220101:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220201:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220301:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220401:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220501:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220801:ReplicationPolicy"), pulumi.Alias(type_="azure-native:recoveryservices/v20220910:ReplicationPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ReplicationPolicy, __self__).__init__(
            'azure-native:recoveryservices/v20211001:ReplicationPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ReplicationPolicy':
        """
        Get an existing ReplicationPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ReplicationPolicyArgs.__new__(ReplicationPolicyArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return ReplicationPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.PolicyPropertiesResponse']:
        """
        The custom data.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource Type
        """
        return pulumi.get(self, "type")

