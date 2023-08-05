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

__all__ = ['RoleManagementPolicyAssignmentArgs', 'RoleManagementPolicyAssignment']

@pulumi.input_type
class RoleManagementPolicyAssignmentArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 policy_id: Optional[pulumi.Input[str]] = None,
                 role_definition_id: Optional[pulumi.Input[str]] = None,
                 role_management_policy_assignment_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RoleManagementPolicyAssignment resource.
        :param pulumi.Input[str] scope: The role management policy scope.
        :param pulumi.Input[str] policy_id: The policy id role management policy assignment.
        :param pulumi.Input[str] role_definition_id: The role definition of management policy assignment.
        :param pulumi.Input[str] role_management_policy_assignment_name: The name of format {guid_guid} the role management policy assignment to upsert.
        """
        pulumi.set(__self__, "scope", scope)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if role_definition_id is not None:
            pulumi.set(__self__, "role_definition_id", role_definition_id)
        if role_management_policy_assignment_name is not None:
            pulumi.set(__self__, "role_management_policy_assignment_name", role_management_policy_assignment_name)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The role management policy scope.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The policy id role management policy assignment.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> Optional[pulumi.Input[str]]:
        """
        The role definition of management policy assignment.
        """
        return pulumi.get(self, "role_definition_id")

    @role_definition_id.setter
    def role_definition_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_definition_id", value)

    @property
    @pulumi.getter(name="roleManagementPolicyAssignmentName")
    def role_management_policy_assignment_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of format {guid_guid} the role management policy assignment to upsert.
        """
        return pulumi.get(self, "role_management_policy_assignment_name")

    @role_management_policy_assignment_name.setter
    def role_management_policy_assignment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_management_policy_assignment_name", value)


class RoleManagementPolicyAssignment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 role_definition_id: Optional[pulumi.Input[str]] = None,
                 role_management_policy_assignment_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Role management policy

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy_id: The policy id role management policy assignment.
        :param pulumi.Input[str] role_definition_id: The role definition of management policy assignment.
        :param pulumi.Input[str] role_management_policy_assignment_name: The name of format {guid_guid} the role management policy assignment to upsert.
        :param pulumi.Input[str] scope: The role management policy scope.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RoleManagementPolicyAssignmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Role management policy

        :param str resource_name: The name of the resource.
        :param RoleManagementPolicyAssignmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleManagementPolicyAssignmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy_id: Optional[pulumi.Input[str]] = None,
                 role_definition_id: Optional[pulumi.Input[str]] = None,
                 role_management_policy_assignment_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RoleManagementPolicyAssignmentArgs.__new__(RoleManagementPolicyAssignmentArgs)

            __props__.__dict__["policy_id"] = policy_id
            __props__.__dict__["role_definition_id"] = role_definition_id
            __props__.__dict__["role_management_policy_assignment_name"] = role_management_policy_assignment_name
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["effective_rules"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["policy_assignment_properties"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:authorization:RoleManagementPolicyAssignment"), pulumi.Alias(type_="azure-native:authorization/v20201001preview:RoleManagementPolicyAssignment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RoleManagementPolicyAssignment, __self__).__init__(
            'azure-native:authorization/v20201001:RoleManagementPolicyAssignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RoleManagementPolicyAssignment':
        """
        Get an existing RoleManagementPolicyAssignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RoleManagementPolicyAssignmentArgs.__new__(RoleManagementPolicyAssignmentArgs)

        __props__.__dict__["effective_rules"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policy_assignment_properties"] = None
        __props__.__dict__["policy_id"] = None
        __props__.__dict__["role_definition_id"] = None
        __props__.__dict__["scope"] = None
        __props__.__dict__["type"] = None
        return RoleManagementPolicyAssignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="effectiveRules")
    def effective_rules(self) -> pulumi.Output[Sequence[Any]]:
        """
        The readonly computed rule applied to the policy.
        """
        return pulumi.get(self, "effective_rules")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The role management policy name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyAssignmentProperties")
    def policy_assignment_properties(self) -> pulumi.Output['outputs.PolicyAssignmentPropertiesResponse']:
        """
        Additional properties of scope, role definition and policy
        """
        return pulumi.get(self, "policy_assignment_properties")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Output[Optional[str]]:
        """
        The policy id role management policy assignment.
        """
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> pulumi.Output[Optional[str]]:
        """
        The role definition of management policy assignment.
        """
        return pulumi.get(self, "role_definition_id")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Optional[str]]:
        """
        The role management policy scope.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The role management policy type.
        """
        return pulumi.get(self, "type")

