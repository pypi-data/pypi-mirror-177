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

__all__ = ['ProximityPlacementGroupArgs', 'ProximityPlacementGroup']

@pulumi.input_type
class ProximityPlacementGroupArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 proximity_placement_group_name: Optional[pulumi.Input[str]] = None,
                 proximity_placement_group_type: Optional[pulumi.Input[Union[str, 'ProximityPlacementGroupType']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ProximityPlacementGroup resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] proximity_placement_group_name: The name of the proximity placement group.
        :param pulumi.Input[Union[str, 'ProximityPlacementGroupType']] proximity_placement_group_type: Specifies the type of the proximity placement group. <br><br> Possible values are: <br><br> **Standard** : Co-locate resources within an Azure region or Availability Zone. <br><br> **Ultra** : For future use.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if proximity_placement_group_name is not None:
            pulumi.set(__self__, "proximity_placement_group_name", proximity_placement_group_name)
        if proximity_placement_group_type is not None:
            pulumi.set(__self__, "proximity_placement_group_type", proximity_placement_group_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="proximityPlacementGroupName")
    def proximity_placement_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the proximity placement group.
        """
        return pulumi.get(self, "proximity_placement_group_name")

    @proximity_placement_group_name.setter
    def proximity_placement_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proximity_placement_group_name", value)

    @property
    @pulumi.getter(name="proximityPlacementGroupType")
    def proximity_placement_group_type(self) -> Optional[pulumi.Input[Union[str, 'ProximityPlacementGroupType']]]:
        """
        Specifies the type of the proximity placement group. <br><br> Possible values are: <br><br> **Standard** : Co-locate resources within an Azure region or Availability Zone. <br><br> **Ultra** : For future use.
        """
        return pulumi.get(self, "proximity_placement_group_type")

    @proximity_placement_group_type.setter
    def proximity_placement_group_type(self, value: Optional[pulumi.Input[Union[str, 'ProximityPlacementGroupType']]]):
        pulumi.set(self, "proximity_placement_group_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Version 2018-10-01 will be removed in v2 of the provider.""", DeprecationWarning)


class ProximityPlacementGroup(pulumi.CustomResource):
    warnings.warn("""Version 2018-10-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 proximity_placement_group_name: Optional[pulumi.Input[str]] = None,
                 proximity_placement_group_type: Optional[pulumi.Input[Union[str, 'ProximityPlacementGroupType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Specifies information about the proximity placement group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] proximity_placement_group_name: The name of the proximity placement group.
        :param pulumi.Input[Union[str, 'ProximityPlacementGroupType']] proximity_placement_group_type: Specifies the type of the proximity placement group. <br><br> Possible values are: <br><br> **Standard** : Co-locate resources within an Azure region or Availability Zone. <br><br> **Ultra** : For future use.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProximityPlacementGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Specifies information about the proximity placement group.

        :param str resource_name: The name of the resource.
        :param ProximityPlacementGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProximityPlacementGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 proximity_placement_group_name: Optional[pulumi.Input[str]] = None,
                 proximity_placement_group_type: Optional[pulumi.Input[Union[str, 'ProximityPlacementGroupType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""ProximityPlacementGroup is deprecated: Version 2018-10-01 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProximityPlacementGroupArgs.__new__(ProximityPlacementGroupArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["proximity_placement_group_name"] = proximity_placement_group_name
            __props__.__dict__["proximity_placement_group_type"] = proximity_placement_group_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["availability_sets"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["virtual_machine_scale_sets"] = None
            __props__.__dict__["virtual_machines"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:compute:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20180401:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20180601:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20190301:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20190701:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20191201:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20200601:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20201201:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20210301:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20210401:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20210701:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20211101:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20220301:ProximityPlacementGroup"), pulumi.Alias(type_="azure-native:compute/v20220801:ProximityPlacementGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ProximityPlacementGroup, __self__).__init__(
            'azure-native:compute/v20181001:ProximityPlacementGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ProximityPlacementGroup':
        """
        Get an existing ProximityPlacementGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ProximityPlacementGroupArgs.__new__(ProximityPlacementGroupArgs)

        __props__.__dict__["availability_sets"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["proximity_placement_group_type"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_machine_scale_sets"] = None
        __props__.__dict__["virtual_machines"] = None
        return ProximityPlacementGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilitySets")
    def availability_sets(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        A list of references to all availability sets in the proximity placement group.
        """
        return pulumi.get(self, "availability_sets")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="proximityPlacementGroupType")
    def proximity_placement_group_type(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the type of the proximity placement group. <br><br> Possible values are: <br><br> **Standard** : Co-locate resources within an Azure region or Availability Zone. <br><br> **Ultra** : For future use.
        """
        return pulumi.get(self, "proximity_placement_group_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualMachineScaleSets")
    def virtual_machine_scale_sets(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        A list of references to all virtual machine scale sets in the proximity placement group.
        """
        return pulumi.get(self, "virtual_machine_scale_sets")

    @property
    @pulumi.getter(name="virtualMachines")
    def virtual_machines(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        A list of references to all virtual machines in the proximity placement group.
        """
        return pulumi.get(self, "virtual_machines")

