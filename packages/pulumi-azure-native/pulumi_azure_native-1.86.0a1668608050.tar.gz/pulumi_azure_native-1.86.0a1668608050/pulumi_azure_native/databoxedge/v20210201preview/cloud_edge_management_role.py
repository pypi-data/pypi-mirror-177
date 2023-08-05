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

__all__ = ['CloudEdgeManagementRoleArgs', 'CloudEdgeManagementRole']

@pulumi.input_type
class CloudEdgeManagementRoleArgs:
    def __init__(__self__, *,
                 device_name: pulumi.Input[str],
                 kind: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 role_status: pulumi.Input[Union[str, 'RoleStatus']],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CloudEdgeManagementRole resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] kind: Role type.
               Expected value is 'CloudEdgeManagement'.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'RoleStatus']] role_status: Role status.
        :param pulumi.Input[str] name: The role name.
        """
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "kind", 'CloudEdgeManagement')
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "role_status", role_status)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="deviceName")
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, "device_name")

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_name", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        Role type.
        Expected value is 'CloudEdgeManagement'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="roleStatus")
    def role_status(self) -> pulumi.Input[Union[str, 'RoleStatus']]:
        """
        Role status.
        """
        return pulumi.get(self, "role_status")

    @role_status.setter
    def role_status(self, value: pulumi.Input[Union[str, 'RoleStatus']]):
        pulumi.set(self, "role_status", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The role name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class CloudEdgeManagementRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_status: Optional[pulumi.Input[Union[str, 'RoleStatus']]] = None,
                 __props__=None):
        """
        CloudEdgeManagementRole role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] kind: Role type.
               Expected value is 'CloudEdgeManagement'.
        :param pulumi.Input[str] name: The role name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'RoleStatus']] role_status: Role status.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CloudEdgeManagementRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        CloudEdgeManagementRole role.

        :param str resource_name: The name of the resource.
        :param CloudEdgeManagementRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CloudEdgeManagementRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_status: Optional[pulumi.Input[Union[str, 'RoleStatus']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CloudEdgeManagementRoleArgs.__new__(CloudEdgeManagementRoleArgs)

            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'CloudEdgeManagement'
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if role_status is None and not opts.urn:
                raise TypeError("Missing required property 'role_status'")
            __props__.__dict__["role_status"] = role_status
            __props__.__dict__["edge_profile"] = None
            __props__.__dict__["local_management_status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databoxedge:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190301:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190701:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190801:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200501preview:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200901preview:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210201:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210601:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210601preview:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20220301:CloudEdgeManagementRole"), pulumi.Alias(type_="azure-native:databoxedge/v20220401preview:CloudEdgeManagementRole")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(CloudEdgeManagementRole, __self__).__init__(
            'azure-native:databoxedge/v20210201preview:CloudEdgeManagementRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CloudEdgeManagementRole':
        """
        Get an existing CloudEdgeManagementRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CloudEdgeManagementRoleArgs.__new__(CloudEdgeManagementRoleArgs)

        __props__.__dict__["edge_profile"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["local_management_status"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["role_status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return CloudEdgeManagementRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="edgeProfile")
    def edge_profile(self) -> pulumi.Output['outputs.EdgeProfileResponse']:
        """
        Edge Profile of the resource
        """
        return pulumi.get(self, "edge_profile")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Role type.
        Expected value is 'CloudEdgeManagement'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="localManagementStatus")
    def local_management_status(self) -> pulumi.Output[str]:
        """
        Local Edge Management Status
        """
        return pulumi.get(self, "local_management_status")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleStatus")
    def role_status(self) -> pulumi.Output[str]:
        """
        Role status.
        """
        return pulumi.get(self, "role_status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Role configured on ASE resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

