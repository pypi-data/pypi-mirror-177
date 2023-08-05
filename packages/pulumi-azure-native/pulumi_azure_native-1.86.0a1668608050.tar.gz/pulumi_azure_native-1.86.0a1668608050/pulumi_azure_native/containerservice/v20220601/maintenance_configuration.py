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

__all__ = ['MaintenanceConfigurationArgs', 'MaintenanceConfiguration']

@pulumi.input_type
class MaintenanceConfigurationArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 config_name: Optional[pulumi.Input[str]] = None,
                 not_allowed_time: Optional[pulumi.Input[Sequence[pulumi.Input['TimeSpanArgs']]]] = None,
                 time_in_week: Optional[pulumi.Input[Sequence[pulumi.Input['TimeInWeekArgs']]]] = None):
        """
        The set of arguments for constructing a MaintenanceConfiguration resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name: The name of the managed cluster resource.
        :param pulumi.Input[str] config_name: The name of the maintenance configuration.
        :param pulumi.Input[Sequence[pulumi.Input['TimeSpanArgs']]] not_allowed_time: Time slots on which upgrade is not allowed.
        :param pulumi.Input[Sequence[pulumi.Input['TimeInWeekArgs']]] time_in_week: If two array entries specify the same day of the week, the applied configuration is the union of times in both entries.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if config_name is not None:
            pulumi.set(__self__, "config_name", config_name)
        if not_allowed_time is not None:
            pulumi.set(__self__, "not_allowed_time", not_allowed_time)
        if time_in_week is not None:
            pulumi.set(__self__, "time_in_week", time_in_week)

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
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the managed cluster resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="configName")
    def config_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the maintenance configuration.
        """
        return pulumi.get(self, "config_name")

    @config_name.setter
    def config_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "config_name", value)

    @property
    @pulumi.getter(name="notAllowedTime")
    def not_allowed_time(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TimeSpanArgs']]]]:
        """
        Time slots on which upgrade is not allowed.
        """
        return pulumi.get(self, "not_allowed_time")

    @not_allowed_time.setter
    def not_allowed_time(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TimeSpanArgs']]]]):
        pulumi.set(self, "not_allowed_time", value)

    @property
    @pulumi.getter(name="timeInWeek")
    def time_in_week(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TimeInWeekArgs']]]]:
        """
        If two array entries specify the same day of the week, the applied configuration is the union of times in both entries.
        """
        return pulumi.get(self, "time_in_week")

    @time_in_week.setter
    def time_in_week(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TimeInWeekArgs']]]]):
        pulumi.set(self, "time_in_week", value)


class MaintenanceConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config_name: Optional[pulumi.Input[str]] = None,
                 not_allowed_time: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeSpanArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 time_in_week: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeInWeekArgs']]]]] = None,
                 __props__=None):
        """
        See [planned maintenance](https://docs.microsoft.com/azure/aks/planned-maintenance) for more information about planned maintenance.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] config_name: The name of the maintenance configuration.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeSpanArgs']]]] not_allowed_time: Time slots on which upgrade is not allowed.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the managed cluster resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeInWeekArgs']]]] time_in_week: If two array entries specify the same day of the week, the applied configuration is the union of times in both entries.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MaintenanceConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        See [planned maintenance](https://docs.microsoft.com/azure/aks/planned-maintenance) for more information about planned maintenance.

        :param str resource_name: The name of the resource.
        :param MaintenanceConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MaintenanceConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config_name: Optional[pulumi.Input[str]] = None,
                 not_allowed_time: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeSpanArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 time_in_week: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeInWeekArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MaintenanceConfigurationArgs.__new__(MaintenanceConfigurationArgs)

            __props__.__dict__["config_name"] = config_name
            __props__.__dict__["not_allowed_time"] = not_allowed_time
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["time_in_week"] = time_in_week
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerservice:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20201201:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20210201:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20210301:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20210501:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20210701:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20210801:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20210901:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20211001:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20211101preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220101:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220102preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220201:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220202preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220301:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220302preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220401:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220402preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220502preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220602preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220701:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220702preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220802preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220803preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220901:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:containerservice/v20220902preview:MaintenanceConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MaintenanceConfiguration, __self__).__init__(
            'azure-native:containerservice/v20220601:MaintenanceConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MaintenanceConfiguration':
        """
        Get an existing MaintenanceConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MaintenanceConfigurationArgs.__new__(MaintenanceConfigurationArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["not_allowed_time"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["time_in_week"] = None
        __props__.__dict__["type"] = None
        return MaintenanceConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notAllowedTime")
    def not_allowed_time(self) -> pulumi.Output[Optional[Sequence['outputs.TimeSpanResponse']]]:
        """
        Time slots on which upgrade is not allowed.
        """
        return pulumi.get(self, "not_allowed_time")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="timeInWeek")
    def time_in_week(self) -> pulumi.Output[Optional[Sequence['outputs.TimeInWeekResponse']]]:
        """
        If two array entries specify the same day of the week, the applied configuration is the union of times in both entries.
        """
        return pulumi.get(self, "time_in_week")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

