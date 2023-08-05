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

__all__ = ['LinkedServiceArgs', 'LinkedService']

@pulumi.input_type
class LinkedServiceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 identity: Optional[pulumi.Input['IdentityArgs']] = None,
                 link_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['LinkedServicePropsArgs']] = None):
        """
        The set of arguments for constructing a LinkedService resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group in which workspace is located.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        :param pulumi.Input['IdentityArgs'] identity: Identity for the resource.
        :param pulumi.Input[str] link_name: Friendly name of the linked workspace
        :param pulumi.Input[str] location: location of the linked service.
        :param pulumi.Input[str] name: Friendly name of the linked service
        :param pulumi.Input['LinkedServicePropsArgs'] properties: LinkedService specific properties.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if link_name is not None:
            pulumi.set(__self__, "link_name", link_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group in which workspace is located.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        Name of Azure Machine Learning workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityArgs']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="linkName")
    def link_name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly name of the linked workspace
        """
        return pulumi.get(self, "link_name")

    @link_name.setter
    def link_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "link_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        location of the linked service.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly name of the linked service
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['LinkedServicePropsArgs']]:
        """
        LinkedService specific properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['LinkedServicePropsArgs']]):
        pulumi.set(self, "properties", value)


class LinkedService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 link_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['LinkedServicePropsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Linked service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: Identity for the resource.
        :param pulumi.Input[str] link_name: Friendly name of the linked workspace
        :param pulumi.Input[str] location: location of the linked service.
        :param pulumi.Input[str] name: Friendly name of the linked service
        :param pulumi.Input[pulumi.InputType['LinkedServicePropsArgs']] properties: LinkedService specific properties.
        :param pulumi.Input[str] resource_group_name: Name of the resource group in which workspace is located.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LinkedServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Linked service.

        :param str resource_name: The name of the resource.
        :param LinkedServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LinkedServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 link_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['LinkedServicePropsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LinkedServiceArgs.__new__(LinkedServiceArgs)

            __props__.__dict__["identity"] = identity
            __props__.__dict__["link_name"] = link_name
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:machinelearningservices:LinkedService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LinkedService, __self__).__init__(
            'azure-native:machinelearningservices/v20200901preview:LinkedService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LinkedService':
        """
        Get an existing LinkedService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = LinkedServiceArgs.__new__(LinkedServiceArgs)

        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return LinkedService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        location of the linked service.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Friendly name of the linked service.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.LinkedServicePropsResponse']:
        """
        LinkedService specific properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type of linked service.
        """
        return pulumi.get(self, "type")

