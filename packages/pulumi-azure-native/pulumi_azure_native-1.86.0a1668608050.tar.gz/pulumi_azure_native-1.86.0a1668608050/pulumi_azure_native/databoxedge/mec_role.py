# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['MECRoleArgs', 'MECRole']

@pulumi.input_type
class MECRoleArgs:
    def __init__(__self__, *,
                 device_name: pulumi.Input[str],
                 kind: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 role_status: pulumi.Input[Union[str, 'RoleStatus']],
                 connection_string: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MECRole resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] kind: Role type.
               Expected value is 'MEC'.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'RoleStatus']] role_status: Role status.
        :param pulumi.Input['AsymmetricEncryptedSecretArgs'] connection_string: Activation key of the MEC.
        :param pulumi.Input[str] name: The role name.
        """
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "kind", 'MEC')
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "role_status", role_status)
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)
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
        Expected value is 'MEC'.
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
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]:
        """
        Activation key of the MEC.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]):
        pulumi.set(self, "connection_string", value)

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


class MECRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_string: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_status: Optional[pulumi.Input[Union[str, 'RoleStatus']]] = None,
                 __props__=None):
        """
        MEC role.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']] connection_string: Activation key of the MEC.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] kind: Role type.
               Expected value is 'MEC'.
        :param pulumi.Input[str] name: The role name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'RoleStatus']] role_status: Role status.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MECRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        MEC role.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param MECRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MECRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_string: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
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
            __props__ = MECRoleArgs.__new__(MECRoleArgs)

            __props__.__dict__["connection_string"] = connection_string
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'MEC'
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if role_status is None and not opts.urn:
                raise TypeError("Missing required property 'role_status'")
            __props__.__dict__["role_status"] = role_status
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databoxedge/v20190301:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190701:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190801:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200501preview:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200901preview:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210201:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210201preview:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210601:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210601preview:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20220301:MECRole"), pulumi.Alias(type_="azure-native:databoxedge/v20220401preview:MECRole")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MECRole, __self__).__init__(
            'azure-native:databoxedge:MECRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MECRole':
        """
        Get an existing MECRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MECRoleArgs.__new__(MECRoleArgs)

        __props__.__dict__["connection_string"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["role_status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return MECRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Output[Optional['outputs.AsymmetricEncryptedSecretResponse']]:
        """
        Activation key of the MEC.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Role type.
        Expected value is 'MEC'.
        """
        return pulumi.get(self, "kind")

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

