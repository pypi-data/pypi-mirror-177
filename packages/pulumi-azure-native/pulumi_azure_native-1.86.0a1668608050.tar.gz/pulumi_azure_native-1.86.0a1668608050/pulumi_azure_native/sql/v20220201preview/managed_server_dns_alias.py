# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ManagedServerDnsAliasArgs', 'ManagedServerDnsAlias']

@pulumi.input_type
class ManagedServerDnsAliasArgs:
    def __init__(__self__, *,
                 managed_instance_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 create_dns_record: Optional[pulumi.Input[bool]] = None,
                 dns_alias_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ManagedServerDnsAlias resource.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[bool] create_dns_record: Whether or not DNS record should be created for this alias.
        """
        pulumi.set(__self__, "managed_instance_name", managed_instance_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if create_dns_record is None:
            create_dns_record = True
        if create_dns_record is not None:
            pulumi.set(__self__, "create_dns_record", create_dns_record)
        if dns_alias_name is not None:
            pulumi.set(__self__, "dns_alias_name", dns_alias_name)

    @property
    @pulumi.getter(name="managedInstanceName")
    def managed_instance_name(self) -> pulumi.Input[str]:
        """
        The name of the managed instance.
        """
        return pulumi.get(self, "managed_instance_name")

    @managed_instance_name.setter
    def managed_instance_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "managed_instance_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="createDnsRecord")
    def create_dns_record(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not DNS record should be created for this alias.
        """
        return pulumi.get(self, "create_dns_record")

    @create_dns_record.setter
    def create_dns_record(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "create_dns_record", value)

    @property
    @pulumi.getter(name="dnsAliasName")
    def dns_alias_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "dns_alias_name")

    @dns_alias_name.setter
    def dns_alias_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_alias_name", value)


class ManagedServerDnsAlias(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 create_dns_record: Optional[pulumi.Input[bool]] = None,
                 dns_alias_name: Optional[pulumi.Input[str]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A managed server DNS alias.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] create_dns_record: Whether or not DNS record should be created for this alias.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedServerDnsAliasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A managed server DNS alias.

        :param str resource_name: The name of the resource.
        :param ManagedServerDnsAliasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedServerDnsAliasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 create_dns_record: Optional[pulumi.Input[bool]] = None,
                 dns_alias_name: Optional[pulumi.Input[str]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedServerDnsAliasArgs.__new__(ManagedServerDnsAliasArgs)

            if create_dns_record is None:
                create_dns_record = True
            __props__.__dict__["create_dns_record"] = create_dns_record
            __props__.__dict__["dns_alias_name"] = dns_alias_name
            if managed_instance_name is None and not opts.urn:
                raise TypeError("Missing required property 'managed_instance_name'")
            __props__.__dict__["managed_instance_name"] = managed_instance_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["azure_dns_record"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["public_azure_dns_record"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:ManagedServerDnsAlias"), pulumi.Alias(type_="azure-native:sql/v20211101:ManagedServerDnsAlias"), pulumi.Alias(type_="azure-native:sql/v20211101preview:ManagedServerDnsAlias"), pulumi.Alias(type_="azure-native:sql/v20220501preview:ManagedServerDnsAlias")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedServerDnsAlias, __self__).__init__(
            'azure-native:sql/v20220201preview:ManagedServerDnsAlias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedServerDnsAlias':
        """
        Get an existing ManagedServerDnsAlias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagedServerDnsAliasArgs.__new__(ManagedServerDnsAliasArgs)

        __props__.__dict__["azure_dns_record"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["public_azure_dns_record"] = None
        __props__.__dict__["type"] = None
        return ManagedServerDnsAlias(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="azureDnsRecord")
    def azure_dns_record(self) -> pulumi.Output[str]:
        """
        The fully qualified DNS record for managed server alias
        """
        return pulumi.get(self, "azure_dns_record")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicAzureDnsRecord")
    def public_azure_dns_record(self) -> pulumi.Output[str]:
        """
        The fully qualified public DNS record for managed server alias
        """
        return pulumi.get(self, "public_azure_dns_record")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

