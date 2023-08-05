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

__all__ = ['NetworkConnectionArgs', 'NetworkConnection']

@pulumi.input_type
class NetworkConnectionArgs:
    def __init__(__self__, *,
                 domain_join_type: pulumi.Input[Union[str, 'DomainJoinType']],
                 resource_group_name: pulumi.Input[str],
                 subnet_id: pulumi.Input[str],
                 domain_name: Optional[pulumi.Input[str]] = None,
                 domain_password: Optional[pulumi.Input[str]] = None,
                 domain_username: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_connection_name: Optional[pulumi.Input[str]] = None,
                 networking_resource_group_name: Optional[pulumi.Input[str]] = None,
                 organization_unit: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkConnection resource.
        :param pulumi.Input[Union[str, 'DomainJoinType']] domain_join_type: AAD Join type.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the Azure subscription.
        :param pulumi.Input[str] subnet_id: The subnet to attach Virtual Machines to
        :param pulumi.Input[str] domain_name: Active Directory domain name
        :param pulumi.Input[str] domain_password: The password for the account used to join domain
        :param pulumi.Input[str] domain_username: The username of an Active Directory account (user or service account) that has permissions to create computer objects in Active Directory. Required format: admin@contoso.com.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] network_connection_name: Name of the Network Connection that can be applied to a Pool.
        :param pulumi.Input[str] networking_resource_group_name: The name for resource group where NICs will be placed.
        :param pulumi.Input[str] organization_unit: Active Directory domain Organization Unit (OU)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "domain_join_type", domain_join_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "subnet_id", subnet_id)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if domain_password is not None:
            pulumi.set(__self__, "domain_password", domain_password)
        if domain_username is not None:
            pulumi.set(__self__, "domain_username", domain_username)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_connection_name is not None:
            pulumi.set(__self__, "network_connection_name", network_connection_name)
        if networking_resource_group_name is not None:
            pulumi.set(__self__, "networking_resource_group_name", networking_resource_group_name)
        if organization_unit is not None:
            pulumi.set(__self__, "organization_unit", organization_unit)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="domainJoinType")
    def domain_join_type(self) -> pulumi.Input[Union[str, 'DomainJoinType']]:
        """
        AAD Join type.
        """
        return pulumi.get(self, "domain_join_type")

    @domain_join_type.setter
    def domain_join_type(self, value: pulumi.Input[Union[str, 'DomainJoinType']]):
        pulumi.set(self, "domain_join_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The subnet to attach Virtual Machines to
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Active Directory domain name
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="domainPassword")
    def domain_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password for the account used to join domain
        """
        return pulumi.get(self, "domain_password")

    @domain_password.setter
    def domain_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_password", value)

    @property
    @pulumi.getter(name="domainUsername")
    def domain_username(self) -> Optional[pulumi.Input[str]]:
        """
        The username of an Active Directory account (user or service account) that has permissions to create computer objects in Active Directory. Required format: admin@contoso.com.
        """
        return pulumi.get(self, "domain_username")

    @domain_username.setter
    def domain_username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_username", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkConnectionName")
    def network_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Network Connection that can be applied to a Pool.
        """
        return pulumi.get(self, "network_connection_name")

    @network_connection_name.setter
    def network_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_connection_name", value)

    @property
    @pulumi.getter(name="networkingResourceGroupName")
    def networking_resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for resource group where NICs will be placed.
        """
        return pulumi.get(self, "networking_resource_group_name")

    @networking_resource_group_name.setter
    def networking_resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "networking_resource_group_name", value)

    @property
    @pulumi.getter(name="organizationUnit")
    def organization_unit(self) -> Optional[pulumi.Input[str]]:
        """
        Active Directory domain Organization Unit (OU)
        """
        return pulumi.get(self, "organization_unit")

    @organization_unit.setter
    def organization_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "organization_unit", value)

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


class NetworkConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_join_type: Optional[pulumi.Input[Union[str, 'DomainJoinType']]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 domain_password: Optional[pulumi.Input[str]] = None,
                 domain_username: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_connection_name: Optional[pulumi.Input[str]] = None,
                 networking_resource_group_name: Optional[pulumi.Input[str]] = None,
                 organization_unit: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Network related settings
        API Version: 2022-09-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'DomainJoinType']] domain_join_type: AAD Join type.
        :param pulumi.Input[str] domain_name: Active Directory domain name
        :param pulumi.Input[str] domain_password: The password for the account used to join domain
        :param pulumi.Input[str] domain_username: The username of an Active Directory account (user or service account) that has permissions to create computer objects in Active Directory. Required format: admin@contoso.com.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] network_connection_name: Name of the Network Connection that can be applied to a Pool.
        :param pulumi.Input[str] networking_resource_group_name: The name for resource group where NICs will be placed.
        :param pulumi.Input[str] organization_unit: Active Directory domain Organization Unit (OU)
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the Azure subscription.
        :param pulumi.Input[str] subnet_id: The subnet to attach Virtual Machines to
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Network related settings
        API Version: 2022-09-01-preview.

        :param str resource_name: The name of the resource.
        :param NetworkConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_join_type: Optional[pulumi.Input[Union[str, 'DomainJoinType']]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 domain_password: Optional[pulumi.Input[str]] = None,
                 domain_username: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_connection_name: Optional[pulumi.Input[str]] = None,
                 networking_resource_group_name: Optional[pulumi.Input[str]] = None,
                 organization_unit: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkConnectionArgs.__new__(NetworkConnectionArgs)

            if domain_join_type is None and not opts.urn:
                raise TypeError("Missing required property 'domain_join_type'")
            __props__.__dict__["domain_join_type"] = domain_join_type
            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["domain_password"] = domain_password
            __props__.__dict__["domain_username"] = domain_username
            __props__.__dict__["location"] = location
            __props__.__dict__["network_connection_name"] = network_connection_name
            __props__.__dict__["networking_resource_group_name"] = networking_resource_group_name
            __props__.__dict__["organization_unit"] = organization_unit
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if subnet_id is None and not opts.urn:
                raise TypeError("Missing required property 'subnet_id'")
            __props__.__dict__["subnet_id"] = subnet_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["health_check_status"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:devcenter/v20220801preview:NetworkConnection"), pulumi.Alias(type_="azure-native:devcenter/v20220901preview:NetworkConnection"), pulumi.Alias(type_="azure-native:devcenter/v20221012preview:NetworkConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NetworkConnection, __self__).__init__(
            'azure-native:devcenter:NetworkConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkConnection':
        """
        Get an existing NetworkConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkConnectionArgs.__new__(NetworkConnectionArgs)

        __props__.__dict__["domain_join_type"] = None
        __props__.__dict__["domain_name"] = None
        __props__.__dict__["domain_password"] = None
        __props__.__dict__["domain_username"] = None
        __props__.__dict__["health_check_status"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["networking_resource_group_name"] = None
        __props__.__dict__["organization_unit"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["subnet_id"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return NetworkConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="domainJoinType")
    def domain_join_type(self) -> pulumi.Output[str]:
        """
        AAD Join type.
        """
        return pulumi.get(self, "domain_join_type")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[Optional[str]]:
        """
        Active Directory domain name
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="domainPassword")
    def domain_password(self) -> pulumi.Output[Optional[str]]:
        """
        The password for the account used to join domain
        """
        return pulumi.get(self, "domain_password")

    @property
    @pulumi.getter(name="domainUsername")
    def domain_username(self) -> pulumi.Output[Optional[str]]:
        """
        The username of an Active Directory account (user or service account) that has permissions to create computer objects in Active Directory. Required format: admin@contoso.com.
        """
        return pulumi.get(self, "domain_username")

    @property
    @pulumi.getter(name="healthCheckStatus")
    def health_check_status(self) -> pulumi.Output[str]:
        """
        Overall health status of the network connection. Health checks are run on creation, update, and periodically to validate the network connection.
        """
        return pulumi.get(self, "health_check_status")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkingResourceGroupName")
    def networking_resource_group_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name for resource group where NICs will be placed.
        """
        return pulumi.get(self, "networking_resource_group_name")

    @property
    @pulumi.getter(name="organizationUnit")
    def organization_unit(self) -> pulumi.Output[Optional[str]]:
        """
        Active Directory domain Organization Unit (OU)
        """
        return pulumi.get(self, "organization_unit")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[str]:
        """
        The subnet to attach Virtual Machines to
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

