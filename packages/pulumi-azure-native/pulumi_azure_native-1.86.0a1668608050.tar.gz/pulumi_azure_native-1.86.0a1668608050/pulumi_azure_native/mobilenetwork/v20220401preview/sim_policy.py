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

__all__ = ['SimPolicyArgs', 'SimPolicy']

@pulumi.input_type
class SimPolicyArgs:
    def __init__(__self__, *,
                 default_slice: pulumi.Input['SliceResourceIdArgs'],
                 mobile_network_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 slice_configurations: pulumi.Input[Sequence[pulumi.Input['SliceConfigurationArgs']]],
                 ue_ambr: pulumi.Input['AmbrArgs'],
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 created_by_type: Optional[pulumi.Input[Union[str, 'CreatedByType']]] = None,
                 last_modified_at: Optional[pulumi.Input[str]] = None,
                 last_modified_by: Optional[pulumi.Input[str]] = None,
                 last_modified_by_type: Optional[pulumi.Input[Union[str, 'CreatedByType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 registration_timer: Optional[pulumi.Input[int]] = None,
                 rfsp_index: Optional[pulumi.Input[int]] = None,
                 sim_policy_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SimPolicy resource.
        :param pulumi.Input['SliceResourceIdArgs'] default_slice: The default slice to use if the UE does not explicitly specify it. This slice must exist in the `sliceConfigurations` map.
        :param pulumi.Input[str] mobile_network_name: The name of the mobile network.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Sequence[pulumi.Input['SliceConfigurationArgs']]] slice_configurations: The allowed slices and the settings to use for them. The list must not contain duplicate items and must contain at least one item.
        :param pulumi.Input['AmbrArgs'] ue_ambr: Aggregate maximum bit rate across all non-GBR QoS flows of all PDU sessions of a given UE. See 3GPP TS23.501 section 5.7.2.6 for a full description of the UE-AMBR.
        :param pulumi.Input[str] created_at: The timestamp of resource creation (UTC).
        :param pulumi.Input[str] created_by: The identity that created the resource.
        :param pulumi.Input[Union[str, 'CreatedByType']] created_by_type: The type of identity that created the resource.
        :param pulumi.Input[str] last_modified_at: The timestamp of resource last modification (UTC)
        :param pulumi.Input[str] last_modified_by: The identity that last modified the resource.
        :param pulumi.Input[Union[str, 'CreatedByType']] last_modified_by_type: The type of identity that last modified the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[int] registration_timer: Interval for the UE periodic registration update procedure, in seconds.
        :param pulumi.Input[int] rfsp_index: RAT/Frequency Selection Priority Index, defined in 3GPP TS 36.413. This is an optional setting and by default is unspecified.
        :param pulumi.Input[str] sim_policy_name: The name of the SIM policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "default_slice", default_slice)
        pulumi.set(__self__, "mobile_network_name", mobile_network_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "slice_configurations", slice_configurations)
        pulumi.set(__self__, "ue_ambr", ue_ambr)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if registration_timer is None:
            registration_timer = 3240
        if registration_timer is not None:
            pulumi.set(__self__, "registration_timer", registration_timer)
        if rfsp_index is not None:
            pulumi.set(__self__, "rfsp_index", rfsp_index)
        if sim_policy_name is not None:
            pulumi.set(__self__, "sim_policy_name", sim_policy_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="defaultSlice")
    def default_slice(self) -> pulumi.Input['SliceResourceIdArgs']:
        """
        The default slice to use if the UE does not explicitly specify it. This slice must exist in the `sliceConfigurations` map.
        """
        return pulumi.get(self, "default_slice")

    @default_slice.setter
    def default_slice(self, value: pulumi.Input['SliceResourceIdArgs']):
        pulumi.set(self, "default_slice", value)

    @property
    @pulumi.getter(name="mobileNetworkName")
    def mobile_network_name(self) -> pulumi.Input[str]:
        """
        The name of the mobile network.
        """
        return pulumi.get(self, "mobile_network_name")

    @mobile_network_name.setter
    def mobile_network_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "mobile_network_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="sliceConfigurations")
    def slice_configurations(self) -> pulumi.Input[Sequence[pulumi.Input['SliceConfigurationArgs']]]:
        """
        The allowed slices and the settings to use for them. The list must not contain duplicate items and must contain at least one item.
        """
        return pulumi.get(self, "slice_configurations")

    @slice_configurations.setter
    def slice_configurations(self, value: pulumi.Input[Sequence[pulumi.Input['SliceConfigurationArgs']]]):
        pulumi.set(self, "slice_configurations", value)

    @property
    @pulumi.getter(name="ueAmbr")
    def ue_ambr(self) -> pulumi.Input['AmbrArgs']:
        """
        Aggregate maximum bit rate across all non-GBR QoS flows of all PDU sessions of a given UE. See 3GPP TS23.501 section 5.7.2.6 for a full description of the UE-AMBR.
        """
        return pulumi.get(self, "ue_ambr")

    @ue_ambr.setter
    def ue_ambr(self, value: pulumi.Input['AmbrArgs']):
        pulumi.set(self, "ue_ambr", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[pulumi.Input[str]]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @created_by.setter
    def created_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by", value)

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[pulumi.Input[Union[str, 'CreatedByType']]]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @created_by_type.setter
    def created_by_type(self, value: Optional[pulumi.Input[Union[str, 'CreatedByType']]]):
        pulumi.set(self, "created_by_type", value)

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @last_modified_at.setter
    def last_modified_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_modified_at", value)

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[pulumi.Input[str]]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @last_modified_by.setter
    def last_modified_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_modified_by", value)

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[pulumi.Input[Union[str, 'CreatedByType']]]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

    @last_modified_by_type.setter
    def last_modified_by_type(self, value: Optional[pulumi.Input[Union[str, 'CreatedByType']]]):
        pulumi.set(self, "last_modified_by_type", value)

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
    @pulumi.getter(name="registrationTimer")
    def registration_timer(self) -> Optional[pulumi.Input[int]]:
        """
        Interval for the UE periodic registration update procedure, in seconds.
        """
        return pulumi.get(self, "registration_timer")

    @registration_timer.setter
    def registration_timer(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "registration_timer", value)

    @property
    @pulumi.getter(name="rfspIndex")
    def rfsp_index(self) -> Optional[pulumi.Input[int]]:
        """
        RAT/Frequency Selection Priority Index, defined in 3GPP TS 36.413. This is an optional setting and by default is unspecified.
        """
        return pulumi.get(self, "rfsp_index")

    @rfsp_index.setter
    def rfsp_index(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "rfsp_index", value)

    @property
    @pulumi.getter(name="simPolicyName")
    def sim_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the SIM policy.
        """
        return pulumi.get(self, "sim_policy_name")

    @sim_policy_name.setter
    def sim_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sim_policy_name", value)

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


class SimPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 created_by_type: Optional[pulumi.Input[Union[str, 'CreatedByType']]] = None,
                 default_slice: Optional[pulumi.Input[pulumi.InputType['SliceResourceIdArgs']]] = None,
                 last_modified_at: Optional[pulumi.Input[str]] = None,
                 last_modified_by: Optional[pulumi.Input[str]] = None,
                 last_modified_by_type: Optional[pulumi.Input[Union[str, 'CreatedByType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_name: Optional[pulumi.Input[str]] = None,
                 registration_timer: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rfsp_index: Optional[pulumi.Input[int]] = None,
                 sim_policy_name: Optional[pulumi.Input[str]] = None,
                 slice_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SliceConfigurationArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ue_ambr: Optional[pulumi.Input[pulumi.InputType['AmbrArgs']]] = None,
                 __props__=None):
        """
        SIM policy resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: The timestamp of resource creation (UTC).
        :param pulumi.Input[str] created_by: The identity that created the resource.
        :param pulumi.Input[Union[str, 'CreatedByType']] created_by_type: The type of identity that created the resource.
        :param pulumi.Input[pulumi.InputType['SliceResourceIdArgs']] default_slice: The default slice to use if the UE does not explicitly specify it. This slice must exist in the `sliceConfigurations` map.
        :param pulumi.Input[str] last_modified_at: The timestamp of resource last modification (UTC)
        :param pulumi.Input[str] last_modified_by: The identity that last modified the resource.
        :param pulumi.Input[Union[str, 'CreatedByType']] last_modified_by_type: The type of identity that last modified the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] mobile_network_name: The name of the mobile network.
        :param pulumi.Input[int] registration_timer: Interval for the UE periodic registration update procedure, in seconds.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[int] rfsp_index: RAT/Frequency Selection Priority Index, defined in 3GPP TS 36.413. This is an optional setting and by default is unspecified.
        :param pulumi.Input[str] sim_policy_name: The name of the SIM policy.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SliceConfigurationArgs']]]] slice_configurations: The allowed slices and the settings to use for them. The list must not contain duplicate items and must contain at least one item.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['AmbrArgs']] ue_ambr: Aggregate maximum bit rate across all non-GBR QoS flows of all PDU sessions of a given UE. See 3GPP TS23.501 section 5.7.2.6 for a full description of the UE-AMBR.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SimPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        SIM policy resource.

        :param str resource_name: The name of the resource.
        :param SimPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SimPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 created_by_type: Optional[pulumi.Input[Union[str, 'CreatedByType']]] = None,
                 default_slice: Optional[pulumi.Input[pulumi.InputType['SliceResourceIdArgs']]] = None,
                 last_modified_at: Optional[pulumi.Input[str]] = None,
                 last_modified_by: Optional[pulumi.Input[str]] = None,
                 last_modified_by_type: Optional[pulumi.Input[Union[str, 'CreatedByType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mobile_network_name: Optional[pulumi.Input[str]] = None,
                 registration_timer: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rfsp_index: Optional[pulumi.Input[int]] = None,
                 sim_policy_name: Optional[pulumi.Input[str]] = None,
                 slice_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SliceConfigurationArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ue_ambr: Optional[pulumi.Input[pulumi.InputType['AmbrArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SimPolicyArgs.__new__(SimPolicyArgs)

            __props__.__dict__["created_at"] = created_at
            __props__.__dict__["created_by"] = created_by
            __props__.__dict__["created_by_type"] = created_by_type
            if default_slice is None and not opts.urn:
                raise TypeError("Missing required property 'default_slice'")
            __props__.__dict__["default_slice"] = default_slice
            __props__.__dict__["last_modified_at"] = last_modified_at
            __props__.__dict__["last_modified_by"] = last_modified_by
            __props__.__dict__["last_modified_by_type"] = last_modified_by_type
            __props__.__dict__["location"] = location
            if mobile_network_name is None and not opts.urn:
                raise TypeError("Missing required property 'mobile_network_name'")
            __props__.__dict__["mobile_network_name"] = mobile_network_name
            if registration_timer is None:
                registration_timer = 3240
            __props__.__dict__["registration_timer"] = registration_timer
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["rfsp_index"] = rfsp_index
            __props__.__dict__["sim_policy_name"] = sim_policy_name
            if slice_configurations is None and not opts.urn:
                raise TypeError("Missing required property 'slice_configurations'")
            __props__.__dict__["slice_configurations"] = slice_configurations
            __props__.__dict__["tags"] = tags
            if ue_ambr is None and not opts.urn:
                raise TypeError("Missing required property 'ue_ambr'")
            __props__.__dict__["ue_ambr"] = ue_ambr
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:mobilenetwork:SimPolicy"), pulumi.Alias(type_="azure-native:mobilenetwork/v20220301preview:SimPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SimPolicy, __self__).__init__(
            'azure-native:mobilenetwork/v20220401preview:SimPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SimPolicy':
        """
        Get an existing SimPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SimPolicyArgs.__new__(SimPolicyArgs)

        __props__.__dict__["created_at"] = None
        __props__.__dict__["created_by"] = None
        __props__.__dict__["created_by_type"] = None
        __props__.__dict__["default_slice"] = None
        __props__.__dict__["last_modified_at"] = None
        __props__.__dict__["last_modified_by"] = None
        __props__.__dict__["last_modified_by_type"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["registration_timer"] = None
        __props__.__dict__["rfsp_index"] = None
        __props__.__dict__["slice_configurations"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["ue_ambr"] = None
        return SimPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[Optional[str]]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> pulumi.Output[Optional[str]]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="defaultSlice")
    def default_slice(self) -> pulumi.Output['outputs.SliceResourceIdResponse']:
        """
        The default slice to use if the UE does not explicitly specify it. This slice must exist in the `sliceConfigurations` map.
        """
        return pulumi.get(self, "default_slice")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> pulumi.Output[Optional[str]]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> pulumi.Output[Optional[str]]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the SIM policy resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="registrationTimer")
    def registration_timer(self) -> pulumi.Output[Optional[int]]:
        """
        Interval for the UE periodic registration update procedure, in seconds.
        """
        return pulumi.get(self, "registration_timer")

    @property
    @pulumi.getter(name="rfspIndex")
    def rfsp_index(self) -> pulumi.Output[Optional[int]]:
        """
        RAT/Frequency Selection Priority Index, defined in 3GPP TS 36.413. This is an optional setting and by default is unspecified.
        """
        return pulumi.get(self, "rfsp_index")

    @property
    @pulumi.getter(name="sliceConfigurations")
    def slice_configurations(self) -> pulumi.Output[Sequence['outputs.SliceConfigurationResponse']]:
        """
        The allowed slices and the settings to use for them. The list must not contain duplicate items and must contain at least one item.
        """
        return pulumi.get(self, "slice_configurations")

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

    @property
    @pulumi.getter(name="ueAmbr")
    def ue_ambr(self) -> pulumi.Output['outputs.AmbrResponse']:
        """
        Aggregate maximum bit rate across all non-GBR QoS flows of all PDU sessions of a given UE. See 3GPP TS23.501 section 5.7.2.6 for a full description of the UE-AMBR.
        """
        return pulumi.get(self, "ue_ambr")

