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

__all__ = ['NrtAlertRuleArgs', 'NrtAlertRule']

@pulumi.input_type
class NrtAlertRuleArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 enabled: pulumi.Input[bool],
                 kind: pulumi.Input[str],
                 query: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 severity: pulumi.Input[Union[str, 'AlertSeverity']],
                 suppression_duration: pulumi.Input[str],
                 suppression_enabled: pulumi.Input[bool],
                 workspace_name: pulumi.Input[str],
                 alert_details_override: Optional[pulumi.Input['AlertDetailsOverrideArgs']] = None,
                 alert_rule_template_name: Optional[pulumi.Input[str]] = None,
                 custom_details: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 entity_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['EntityMappingArgs']]]] = None,
                 incident_configuration: Optional[pulumi.Input['IncidentConfigurationArgs']] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 tactics: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]]] = None,
                 techniques: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NrtAlertRule resource.
        :param pulumi.Input[str] display_name: The display name for alerts created by this alert rule.
        :param pulumi.Input[bool] enabled: Determines whether this alert rule is enabled or disabled.
        :param pulumi.Input[str] kind: The kind of the alert rule
               Expected value is 'NRT'.
        :param pulumi.Input[str] query: The query that creates alerts for this rule.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Union[str, 'AlertSeverity']] severity: The severity for alerts created by this alert rule.
        :param pulumi.Input[str] suppression_duration: The suppression (in ISO 8601 duration format) to wait since last time this alert rule been triggered.
        :param pulumi.Input[bool] suppression_enabled: Determines whether the suppression for this alert rule is enabled or disabled.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input['AlertDetailsOverrideArgs'] alert_details_override: The alert details override settings
        :param pulumi.Input[str] alert_rule_template_name: The Name of the alert rule template used to create this rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_details: Dictionary of string key-value pairs of columns to be attached to the alert
        :param pulumi.Input[str] description: The description of the alert rule.
        :param pulumi.Input[Sequence[pulumi.Input['EntityMappingArgs']]] entity_mappings: Array of the entity mappings of the alert rule
        :param pulumi.Input['IncidentConfigurationArgs'] incident_configuration: The settings of the incidents that created from alerts triggered by this analytics rule
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]] tactics: The tactics of the alert rule
        :param pulumi.Input[Sequence[pulumi.Input[str]]] techniques: The techniques of the alert rule
        :param pulumi.Input[str] template_version: The version of the alert rule template used to create this rule - in format <a.b.c>, where all are numbers, for example 0 <1.0.2>
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "kind", 'NRT')
        pulumi.set(__self__, "query", query)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "severity", severity)
        pulumi.set(__self__, "suppression_duration", suppression_duration)
        pulumi.set(__self__, "suppression_enabled", suppression_enabled)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if alert_details_override is not None:
            pulumi.set(__self__, "alert_details_override", alert_details_override)
        if alert_rule_template_name is not None:
            pulumi.set(__self__, "alert_rule_template_name", alert_rule_template_name)
        if custom_details is not None:
            pulumi.set(__self__, "custom_details", custom_details)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if entity_mappings is not None:
            pulumi.set(__self__, "entity_mappings", entity_mappings)
        if incident_configuration is not None:
            pulumi.set(__self__, "incident_configuration", incident_configuration)
        if rule_id is not None:
            pulumi.set(__self__, "rule_id", rule_id)
        if tactics is not None:
            pulumi.set(__self__, "tactics", tactics)
        if techniques is not None:
            pulumi.set(__self__, "techniques", techniques)
        if template_version is not None:
            pulumi.set(__self__, "template_version", template_version)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the alert rule
        Expected value is 'NRT'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def query(self) -> pulumi.Input[str]:
        """
        The query that creates alerts for this rule.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: pulumi.Input[str]):
        pulumi.set(self, "query", value)

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
    def severity(self) -> pulumi.Input[Union[str, 'AlertSeverity']]:
        """
        The severity for alerts created by this alert rule.
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: pulumi.Input[Union[str, 'AlertSeverity']]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter(name="suppressionDuration")
    def suppression_duration(self) -> pulumi.Input[str]:
        """
        The suppression (in ISO 8601 duration format) to wait since last time this alert rule been triggered.
        """
        return pulumi.get(self, "suppression_duration")

    @suppression_duration.setter
    def suppression_duration(self, value: pulumi.Input[str]):
        pulumi.set(self, "suppression_duration", value)

    @property
    @pulumi.getter(name="suppressionEnabled")
    def suppression_enabled(self) -> pulumi.Input[bool]:
        """
        Determines whether the suppression for this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "suppression_enabled")

    @suppression_enabled.setter
    def suppression_enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "suppression_enabled", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="alertDetailsOverride")
    def alert_details_override(self) -> Optional[pulumi.Input['AlertDetailsOverrideArgs']]:
        """
        The alert details override settings
        """
        return pulumi.get(self, "alert_details_override")

    @alert_details_override.setter
    def alert_details_override(self, value: Optional[pulumi.Input['AlertDetailsOverrideArgs']]):
        pulumi.set(self, "alert_details_override", value)

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @alert_rule_template_name.setter
    def alert_rule_template_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "alert_rule_template_name", value)

    @property
    @pulumi.getter(name="customDetails")
    def custom_details(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Dictionary of string key-value pairs of columns to be attached to the alert
        """
        return pulumi.get(self, "custom_details")

    @custom_details.setter
    def custom_details(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "custom_details", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="entityMappings")
    def entity_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EntityMappingArgs']]]]:
        """
        Array of the entity mappings of the alert rule
        """
        return pulumi.get(self, "entity_mappings")

    @entity_mappings.setter
    def entity_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EntityMappingArgs']]]]):
        pulumi.set(self, "entity_mappings", value)

    @property
    @pulumi.getter(name="incidentConfiguration")
    def incident_configuration(self) -> Optional[pulumi.Input['IncidentConfigurationArgs']]:
        """
        The settings of the incidents that created from alerts triggered by this analytics rule
        """
        return pulumi.get(self, "incident_configuration")

    @incident_configuration.setter
    def incident_configuration(self, value: Optional[pulumi.Input['IncidentConfigurationArgs']]):
        pulumi.set(self, "incident_configuration", value)

    @property
    @pulumi.getter(name="ruleId")
    def rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        Alert rule ID
        """
        return pulumi.get(self, "rule_id")

    @rule_id.setter
    def rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_id", value)

    @property
    @pulumi.getter
    def tactics(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]]]:
        """
        The tactics of the alert rule
        """
        return pulumi.get(self, "tactics")

    @tactics.setter
    def tactics(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]]]):
        pulumi.set(self, "tactics", value)

    @property
    @pulumi.getter
    def techniques(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The techniques of the alert rule
        """
        return pulumi.get(self, "techniques")

    @techniques.setter
    def techniques(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "techniques", value)

    @property
    @pulumi.getter(name="templateVersion")
    def template_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the alert rule template used to create this rule - in format <a.b.c>, where all are numbers, for example 0 <1.0.2>
        """
        return pulumi.get(self, "template_version")

    @template_version.setter
    def template_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template_version", value)


class NrtAlertRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_details_override: Optional[pulumi.Input[pulumi.InputType['AlertDetailsOverrideArgs']]] = None,
                 alert_rule_template_name: Optional[pulumi.Input[str]] = None,
                 custom_details: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 entity_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EntityMappingArgs']]]]] = None,
                 incident_configuration: Optional[pulumi.Input[pulumi.InputType['IncidentConfigurationArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[Union[str, 'AlertSeverity']]] = None,
                 suppression_duration: Optional[pulumi.Input[str]] = None,
                 suppression_enabled: Optional[pulumi.Input[bool]] = None,
                 tactics: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]]] = None,
                 techniques: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_version: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents NRT alert rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AlertDetailsOverrideArgs']] alert_details_override: The alert details override settings
        :param pulumi.Input[str] alert_rule_template_name: The Name of the alert rule template used to create this rule.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_details: Dictionary of string key-value pairs of columns to be attached to the alert
        :param pulumi.Input[str] description: The description of the alert rule.
        :param pulumi.Input[str] display_name: The display name for alerts created by this alert rule.
        :param pulumi.Input[bool] enabled: Determines whether this alert rule is enabled or disabled.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EntityMappingArgs']]]] entity_mappings: Array of the entity mappings of the alert rule
        :param pulumi.Input[pulumi.InputType['IncidentConfigurationArgs']] incident_configuration: The settings of the incidents that created from alerts triggered by this analytics rule
        :param pulumi.Input[str] kind: The kind of the alert rule
               Expected value is 'NRT'.
        :param pulumi.Input[str] query: The query that creates alerts for this rule.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[Union[str, 'AlertSeverity']] severity: The severity for alerts created by this alert rule.
        :param pulumi.Input[str] suppression_duration: The suppression (in ISO 8601 duration format) to wait since last time this alert rule been triggered.
        :param pulumi.Input[bool] suppression_enabled: Determines whether the suppression for this alert rule is enabled or disabled.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]] tactics: The tactics of the alert rule
        :param pulumi.Input[Sequence[pulumi.Input[str]]] techniques: The techniques of the alert rule
        :param pulumi.Input[str] template_version: The version of the alert rule template used to create this rule - in format <a.b.c>, where all are numbers, for example 0 <1.0.2>
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NrtAlertRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents NRT alert rule.

        :param str resource_name: The name of the resource.
        :param NrtAlertRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NrtAlertRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_details_override: Optional[pulumi.Input[pulumi.InputType['AlertDetailsOverrideArgs']]] = None,
                 alert_rule_template_name: Optional[pulumi.Input[str]] = None,
                 custom_details: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 entity_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EntityMappingArgs']]]]] = None,
                 incident_configuration: Optional[pulumi.Input[pulumi.InputType['IncidentConfigurationArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 severity: Optional[pulumi.Input[Union[str, 'AlertSeverity']]] = None,
                 suppression_duration: Optional[pulumi.Input[str]] = None,
                 suppression_enabled: Optional[pulumi.Input[bool]] = None,
                 tactics: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AttackTactic']]]]] = None,
                 techniques: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_version: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NrtAlertRuleArgs.__new__(NrtAlertRuleArgs)

            __props__.__dict__["alert_details_override"] = alert_details_override
            __props__.__dict__["alert_rule_template_name"] = alert_rule_template_name
            __props__.__dict__["custom_details"] = custom_details
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if enabled is None and not opts.urn:
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["entity_mappings"] = entity_mappings
            __props__.__dict__["incident_configuration"] = incident_configuration
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'NRT'
            if query is None and not opts.urn:
                raise TypeError("Missing required property 'query'")
            __props__.__dict__["query"] = query
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["rule_id"] = rule_id
            if severity is None and not opts.urn:
                raise TypeError("Missing required property 'severity'")
            __props__.__dict__["severity"] = severity
            if suppression_duration is None and not opts.urn:
                raise TypeError("Missing required property 'suppression_duration'")
            __props__.__dict__["suppression_duration"] = suppression_duration
            if suppression_enabled is None and not opts.urn:
                raise TypeError("Missing required property 'suppression_enabled'")
            __props__.__dict__["suppression_enabled"] = suppression_enabled
            __props__.__dict__["tactics"] = tactics
            __props__.__dict__["techniques"] = techniques
            __props__.__dict__["template_version"] = template_version
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["last_modified_utc"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:securityinsights:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20190101preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20200101:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20210301preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20210901preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20211001:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20211001preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220101preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220401preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220501preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220601preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220801:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220801preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20220901preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20221001preview:NrtAlertRule"), pulumi.Alias(type_="azure-native:securityinsights/v20221101preview:NrtAlertRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NrtAlertRule, __self__).__init__(
            'azure-native:securityinsights/v20220701preview:NrtAlertRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NrtAlertRule':
        """
        Get an existing NrtAlertRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NrtAlertRuleArgs.__new__(NrtAlertRuleArgs)

        __props__.__dict__["alert_details_override"] = None
        __props__.__dict__["alert_rule_template_name"] = None
        __props__.__dict__["custom_details"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["entity_mappings"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["incident_configuration"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["last_modified_utc"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["query"] = None
        __props__.__dict__["severity"] = None
        __props__.__dict__["suppression_duration"] = None
        __props__.__dict__["suppression_enabled"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tactics"] = None
        __props__.__dict__["techniques"] = None
        __props__.__dict__["template_version"] = None
        __props__.__dict__["type"] = None
        return NrtAlertRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="alertDetailsOverride")
    def alert_details_override(self) -> pulumi.Output[Optional['outputs.AlertDetailsOverrideResponse']]:
        """
        The alert details override settings
        """
        return pulumi.get(self, "alert_details_override")

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> pulumi.Output[Optional[str]]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @property
    @pulumi.getter(name="customDetails")
    def custom_details(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Dictionary of string key-value pairs of columns to be attached to the alert
        """
        return pulumi.get(self, "custom_details")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="entityMappings")
    def entity_mappings(self) -> pulumi.Output[Optional[Sequence['outputs.EntityMappingResponse']]]:
        """
        Array of the entity mappings of the alert rule
        """
        return pulumi.get(self, "entity_mappings")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="incidentConfiguration")
    def incident_configuration(self) -> pulumi.Output[Optional['outputs.IncidentConfigurationResponse']]:
        """
        The settings of the incidents that created from alerts triggered by this analytics rule
        """
        return pulumi.get(self, "incident_configuration")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of the alert rule
        Expected value is 'NRT'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedUtc")
    def last_modified_utc(self) -> pulumi.Output[str]:
        """
        The last time that this alert rule has been modified.
        """
        return pulumi.get(self, "last_modified_utc")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        The query that creates alerts for this rule.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[str]:
        """
        The severity for alerts created by this alert rule.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="suppressionDuration")
    def suppression_duration(self) -> pulumi.Output[str]:
        """
        The suppression (in ISO 8601 duration format) to wait since last time this alert rule been triggered.
        """
        return pulumi.get(self, "suppression_duration")

    @property
    @pulumi.getter(name="suppressionEnabled")
    def suppression_enabled(self) -> pulumi.Output[bool]:
        """
        Determines whether the suppression for this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "suppression_enabled")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tactics(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The tactics of the alert rule
        """
        return pulumi.get(self, "tactics")

    @property
    @pulumi.getter
    def techniques(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The techniques of the alert rule
        """
        return pulumi.get(self, "techniques")

    @property
    @pulumi.getter(name="templateVersion")
    def template_version(self) -> pulumi.Output[Optional[str]]:
        """
        The version of the alert rule template used to create this rule - in format <a.b.c>, where all are numbers, for example 0 <1.0.2>
        """
        return pulumi.get(self, "template_version")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

