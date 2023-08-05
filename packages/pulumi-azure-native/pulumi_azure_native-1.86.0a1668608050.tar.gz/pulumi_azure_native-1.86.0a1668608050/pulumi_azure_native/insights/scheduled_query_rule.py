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

__all__ = ['ScheduledQueryRuleArgs', 'ScheduledQueryRule']

@pulumi.input_type
class ScheduledQueryRuleArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[Union['AlertingActionArgs', 'LogToMetricActionArgs']],
                 resource_group_name: pulumi.Input[str],
                 source: pulumi.Input['SourceArgs'],
                 auto_mitigate: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[Union[str, 'Enabled']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input['ScheduleArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ScheduledQueryRule resource.
        :param pulumi.Input[Union['AlertingActionArgs', 'LogToMetricActionArgs']] action: Action needs to be taken on rule execution.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input['SourceArgs'] source: Data Source against which rule will Query Data
        :param pulumi.Input[bool] auto_mitigate: The flag that indicates whether the alert should be automatically resolved or not. The default is false.
        :param pulumi.Input[str] description: The description of the Log Search rule.
        :param pulumi.Input[str] display_name: The display name of the alert rule
        :param pulumi.Input[Union[str, 'Enabled']] enabled: The flag which indicates whether the Log Search rule is enabled. Value should be true or false
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] rule_name: The name of the rule.
        :param pulumi.Input['ScheduleArgs'] schedule: Schedule (Frequency, Time Window) for rule. Required for action type - AlertingAction
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "source", source)
        if auto_mitigate is None:
            auto_mitigate = False
        if auto_mitigate is not None:
            pulumi.set(__self__, "auto_mitigate", auto_mitigate)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if rule_name is not None:
            pulumi.set(__self__, "rule_name", rule_name)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[Union['AlertingActionArgs', 'LogToMetricActionArgs']]:
        """
        Action needs to be taken on rule execution.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[Union['AlertingActionArgs', 'LogToMetricActionArgs']]):
        pulumi.set(self, "action", value)

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
    @pulumi.getter
    def source(self) -> pulumi.Input['SourceArgs']:
        """
        Data Source against which rule will Query Data
        """
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: pulumi.Input['SourceArgs']):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter(name="autoMitigate")
    def auto_mitigate(self) -> Optional[pulumi.Input[bool]]:
        """
        The flag that indicates whether the alert should be automatically resolved or not. The default is false.
        """
        return pulumi.get(self, "auto_mitigate")

    @auto_mitigate.setter
    def auto_mitigate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_mitigate", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Log Search rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of the alert rule
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[Union[str, 'Enabled']]]:
        """
        The flag which indicates whether the Log Search rule is enabled. Value should be true or false
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[Union[str, 'Enabled']]]):
        pulumi.set(self, "enabled", value)

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
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rule.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['ScheduleArgs']]:
        """
        Schedule (Frequency, Time Window) for rule. Required for action type - AlertingAction
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['ScheduleArgs']]):
        pulumi.set(self, "schedule", value)

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


class ScheduledQueryRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[Union[pulumi.InputType['AlertingActionArgs'], pulumi.InputType['LogToMetricActionArgs']]]] = None,
                 auto_mitigate: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[Union[str, 'Enabled']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['ScheduleArgs']]] = None,
                 source: Optional[pulumi.Input[pulumi.InputType['SourceArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The Log Search Rule resource.
        API Version: 2018-04-16.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[pulumi.InputType['AlertingActionArgs'], pulumi.InputType['LogToMetricActionArgs']]] action: Action needs to be taken on rule execution.
        :param pulumi.Input[bool] auto_mitigate: The flag that indicates whether the alert should be automatically resolved or not. The default is false.
        :param pulumi.Input[str] description: The description of the Log Search rule.
        :param pulumi.Input[str] display_name: The display name of the alert rule
        :param pulumi.Input[Union[str, 'Enabled']] enabled: The flag which indicates whether the Log Search rule is enabled. Value should be true or false
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] rule_name: The name of the rule.
        :param pulumi.Input[pulumi.InputType['ScheduleArgs']] schedule: Schedule (Frequency, Time Window) for rule. Required for action type - AlertingAction
        :param pulumi.Input[pulumi.InputType['SourceArgs']] source: Data Source against which rule will Query Data
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScheduledQueryRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Log Search Rule resource.
        API Version: 2018-04-16.

        :param str resource_name: The name of the resource.
        :param ScheduledQueryRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScheduledQueryRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[Union[pulumi.InputType['AlertingActionArgs'], pulumi.InputType['LogToMetricActionArgs']]]] = None,
                 auto_mitigate: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[Union[str, 'Enabled']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['ScheduleArgs']]] = None,
                 source: Optional[pulumi.Input[pulumi.InputType['SourceArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ScheduledQueryRuleArgs.__new__(ScheduledQueryRuleArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            if auto_mitigate is None:
                auto_mitigate = False
            __props__.__dict__["auto_mitigate"] = auto_mitigate
            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["rule_name"] = rule_name
            __props__.__dict__["schedule"] = schedule
            if source is None and not opts.urn:
                raise TypeError("Missing required property 'source'")
            __props__.__dict__["source"] = source
            __props__.__dict__["tags"] = tags
            __props__.__dict__["created_with_api_version"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["is_legacy_log_analytics_rule"] = None
            __props__.__dict__["kind"] = None
            __props__.__dict__["last_updated_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:insights/v20180416:ScheduledQueryRule"), pulumi.Alias(type_="azure-native:insights/v20200501preview:ScheduledQueryRule"), pulumi.Alias(type_="azure-native:insights/v20210201preview:ScheduledQueryRule"), pulumi.Alias(type_="azure-native:insights/v20210801:ScheduledQueryRule"), pulumi.Alias(type_="azure-native:insights/v20220615:ScheduledQueryRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ScheduledQueryRule, __self__).__init__(
            'azure-native:insights:ScheduledQueryRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ScheduledQueryRule':
        """
        Get an existing ScheduledQueryRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ScheduledQueryRuleArgs.__new__(ScheduledQueryRuleArgs)

        __props__.__dict__["action"] = None
        __props__.__dict__["auto_mitigate"] = None
        __props__.__dict__["created_with_api_version"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["is_legacy_log_analytics_rule"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["last_updated_time"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["schedule"] = None
        __props__.__dict__["source"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ScheduledQueryRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[Any]:
        """
        Action needs to be taken on rule execution.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="autoMitigate")
    def auto_mitigate(self) -> pulumi.Output[Optional[bool]]:
        """
        The flag that indicates whether the alert should be automatically resolved or not. The default is false.
        """
        return pulumi.get(self, "auto_mitigate")

    @property
    @pulumi.getter(name="createdWithApiVersion")
    def created_with_api_version(self) -> pulumi.Output[str]:
        """
        The api-version used when creating this alert rule
        """
        return pulumi.get(self, "created_with_api_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the Log Search rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The display name of the alert rule
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[str]]:
        """
        The flag which indicates whether the Log Search rule is enabled. Value should be true or false
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal etag convention.  Entity tags are used for comparing two or more entities from the same requested resource. HTTP/1.1 uses entity tags in the etag (section 14.19), If-Match (section 14.24), If-None-Match (section 14.26), and If-Range (section 14.27) header fields. 
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="isLegacyLogAnalyticsRule")
    def is_legacy_log_analytics_rule(self) -> pulumi.Output[bool]:
        """
        True if alert rule is legacy Log Analytic rule
        """
        return pulumi.get(self, "is_legacy_log_analytics_rule")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> pulumi.Output[str]:
        """
        Last time the rule was updated in IS08601 format.
        """
        return pulumi.get(self, "last_updated_time")

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
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the scheduled query rule
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional['outputs.ScheduleResponse']]:
        """
        Schedule (Frequency, Time Window) for rule. Required for action type - AlertingAction
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def source(self) -> pulumi.Output['outputs.SourceResponse']:
        """
        Data Source against which rule will Query Data
        """
        return pulumi.get(self, "source")

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
        Azure resource type
        """
        return pulumi.get(self, "type")

