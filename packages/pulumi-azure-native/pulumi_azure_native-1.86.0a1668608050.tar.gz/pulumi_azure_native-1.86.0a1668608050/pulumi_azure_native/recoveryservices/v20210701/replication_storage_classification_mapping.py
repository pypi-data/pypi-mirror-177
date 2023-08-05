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

__all__ = ['ReplicationStorageClassificationMappingArgs', 'ReplicationStorageClassificationMapping']

@pulumi.input_type
class ReplicationStorageClassificationMappingArgs:
    def __init__(__self__, *,
                 fabric_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 storage_classification_name: pulumi.Input[str],
                 properties: Optional[pulumi.Input['StorageMappingInputPropertiesArgs']] = None,
                 storage_classification_mapping_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ReplicationStorageClassificationMapping resource.
        :param pulumi.Input[str] fabric_name: Fabric name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name: The name of the recovery services vault.
        :param pulumi.Input[str] storage_classification_name: Storage classification name.
        :param pulumi.Input['StorageMappingInputPropertiesArgs'] properties: Storage mapping input properties.
        :param pulumi.Input[str] storage_classification_mapping_name: Storage classification mapping name.
        """
        pulumi.set(__self__, "fabric_name", fabric_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        pulumi.set(__self__, "storage_classification_name", storage_classification_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if storage_classification_mapping_name is not None:
            pulumi.set(__self__, "storage_classification_mapping_name", storage_classification_mapping_name)

    @property
    @pulumi.getter(name="fabricName")
    def fabric_name(self) -> pulumi.Input[str]:
        """
        Fabric name.
        """
        return pulumi.get(self, "fabric_name")

    @fabric_name.setter
    def fabric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "fabric_name", value)

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
    @pulumi.getter(name="storageClassificationName")
    def storage_classification_name(self) -> pulumi.Input[str]:
        """
        Storage classification name.
        """
        return pulumi.get(self, "storage_classification_name")

    @storage_classification_name.setter
    def storage_classification_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_classification_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['StorageMappingInputPropertiesArgs']]:
        """
        Storage mapping input properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['StorageMappingInputPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="storageClassificationMappingName")
    def storage_classification_mapping_name(self) -> Optional[pulumi.Input[str]]:
        """
        Storage classification mapping name.
        """
        return pulumi.get(self, "storage_classification_mapping_name")

    @storage_classification_mapping_name.setter
    def storage_classification_mapping_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_classification_mapping_name", value)


class ReplicationStorageClassificationMapping(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['StorageMappingInputPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 storage_classification_mapping_name: Optional[pulumi.Input[str]] = None,
                 storage_classification_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Storage mapping object.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] fabric_name: Fabric name.
        :param pulumi.Input[pulumi.InputType['StorageMappingInputPropertiesArgs']] properties: Storage mapping input properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name_: The name of the recovery services vault.
        :param pulumi.Input[str] storage_classification_mapping_name: Storage classification mapping name.
        :param pulumi.Input[str] storage_classification_name: Storage classification name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationStorageClassificationMappingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Storage mapping object.

        :param str resource_name: The name of the resource.
        :param ReplicationStorageClassificationMappingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationStorageClassificationMappingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['StorageMappingInputPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 storage_classification_mapping_name: Optional[pulumi.Input[str]] = None,
                 storage_classification_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationStorageClassificationMappingArgs.__new__(ReplicationStorageClassificationMappingArgs)

            if fabric_name is None and not opts.urn:
                raise TypeError("Missing required property 'fabric_name'")
            __props__.__dict__["fabric_name"] = fabric_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["storage_classification_mapping_name"] = storage_classification_mapping_name
            if storage_classification_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_classification_name'")
            __props__.__dict__["storage_classification_name"] = storage_classification_name
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20160810:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20180110:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20180710:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210210:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210601:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20211001:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20211101:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220101:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220201:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220301:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220401:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220501:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220801:ReplicationStorageClassificationMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20220910:ReplicationStorageClassificationMapping")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ReplicationStorageClassificationMapping, __self__).__init__(
            'azure-native:recoveryservices/v20210701:ReplicationStorageClassificationMapping',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ReplicationStorageClassificationMapping':
        """
        Get an existing ReplicationStorageClassificationMapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ReplicationStorageClassificationMappingArgs.__new__(ReplicationStorageClassificationMappingArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return ReplicationStorageClassificationMapping(resource_name, opts=opts, __props__=__props__)

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
    def properties(self) -> pulumi.Output['outputs.StorageClassificationMappingPropertiesResponse']:
        """
        Properties of the storage mapping object.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource Type
        """
        return pulumi.get(self, "type")

