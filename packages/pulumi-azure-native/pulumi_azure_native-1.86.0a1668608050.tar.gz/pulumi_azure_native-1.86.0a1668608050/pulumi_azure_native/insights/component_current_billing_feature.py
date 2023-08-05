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
from ._inputs import *

__all__ = ['ComponentCurrentBillingFeatureArgs', 'ComponentCurrentBillingFeature']

@pulumi.input_type
class ComponentCurrentBillingFeatureArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 current_billing_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_volume_cap: Optional[pulumi.Input['ApplicationInsightsComponentDataVolumeCapArgs']] = None):
        """
        The set of arguments for constructing a ComponentCurrentBillingFeature resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name: The name of the Application Insights component resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] current_billing_features: Current enabled pricing plan. When the component is in the Enterprise plan, this will list both 'Basic' and 'Application Insights Enterprise'.
        :param pulumi.Input['ApplicationInsightsComponentDataVolumeCapArgs'] data_volume_cap: An Application Insights component daily data volume cap
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if current_billing_features is not None:
            pulumi.set(__self__, "current_billing_features", current_billing_features)
        if data_volume_cap is not None:
            pulumi.set(__self__, "data_volume_cap", data_volume_cap)

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
        The name of the Application Insights component resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="currentBillingFeatures")
    def current_billing_features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Current enabled pricing plan. When the component is in the Enterprise plan, this will list both 'Basic' and 'Application Insights Enterprise'.
        """
        return pulumi.get(self, "current_billing_features")

    @current_billing_features.setter
    def current_billing_features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "current_billing_features", value)

    @property
    @pulumi.getter(name="dataVolumeCap")
    def data_volume_cap(self) -> Optional[pulumi.Input['ApplicationInsightsComponentDataVolumeCapArgs']]:
        """
        An Application Insights component daily data volume cap
        """
        return pulumi.get(self, "data_volume_cap")

    @data_volume_cap.setter
    def data_volume_cap(self, value: Optional[pulumi.Input['ApplicationInsightsComponentDataVolumeCapArgs']]):
        pulumi.set(self, "data_volume_cap", value)


class ComponentCurrentBillingFeature(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 current_billing_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_volume_cap: Optional[pulumi.Input[pulumi.InputType['ApplicationInsightsComponentDataVolumeCapArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An Application Insights component billing features
        API Version: 2015-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] current_billing_features: Current enabled pricing plan. When the component is in the Enterprise plan, this will list both 'Basic' and 'Application Insights Enterprise'.
        :param pulumi.Input[pulumi.InputType['ApplicationInsightsComponentDataVolumeCapArgs']] data_volume_cap: An Application Insights component daily data volume cap
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the Application Insights component resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ComponentCurrentBillingFeatureArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Application Insights component billing features
        API Version: 2015-05-01.

        :param str resource_name: The name of the resource.
        :param ComponentCurrentBillingFeatureArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ComponentCurrentBillingFeatureArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 current_billing_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 data_volume_cap: Optional[pulumi.Input[pulumi.InputType['ApplicationInsightsComponentDataVolumeCapArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ComponentCurrentBillingFeatureArgs.__new__(ComponentCurrentBillingFeatureArgs)

            __props__.__dict__["current_billing_features"] = current_billing_features
            __props__.__dict__["data_volume_cap"] = data_volume_cap
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:insights/v20150501:ComponentCurrentBillingFeature")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ComponentCurrentBillingFeature, __self__).__init__(
            'azure-native:insights:ComponentCurrentBillingFeature',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ComponentCurrentBillingFeature':
        """
        Get an existing ComponentCurrentBillingFeature resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ComponentCurrentBillingFeatureArgs.__new__(ComponentCurrentBillingFeatureArgs)

        __props__.__dict__["current_billing_features"] = None
        __props__.__dict__["data_volume_cap"] = None
        return ComponentCurrentBillingFeature(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="currentBillingFeatures")
    def current_billing_features(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Current enabled pricing plan. When the component is in the Enterprise plan, this will list both 'Basic' and 'Application Insights Enterprise'.
        """
        return pulumi.get(self, "current_billing_features")

    @property
    @pulumi.getter(name="dataVolumeCap")
    def data_volume_cap(self) -> pulumi.Output[Optional['outputs.ApplicationInsightsComponentDataVolumeCapResponse']]:
        """
        An Application Insights component daily data volume cap
        """
        return pulumi.get(self, "data_volume_cap")

