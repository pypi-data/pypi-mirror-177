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

__all__ = [
    'AuthorizationResponse',
    'EligibleApproverResponse',
    'EligibleAuthorizationResponse',
    'JustInTimeAccessPolicyResponse',
    'PlanResponse',
    'RegistrationAssignmentPropertiesResponse',
    'RegistrationAssignmentPropertiesResponseProperties',
    'RegistrationAssignmentPropertiesResponseRegistrationDefinition',
    'RegistrationDefinitionPropertiesResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class AuthorizationResponse(dict):
    """
    The Azure Active Directory principal identifier and Azure built-in role that describes the access the principal will receive on the delegated resource in the managed tenant.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "roleDefinitionId":
            suggest = "role_definition_id"
        elif key == "delegatedRoleDefinitionIds":
            suggest = "delegated_role_definition_ids"
        elif key == "principalIdDisplayName":
            suggest = "principal_id_display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AuthorizationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuthorizationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AuthorizationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 role_definition_id: str,
                 delegated_role_definition_ids: Optional[Sequence[str]] = None,
                 principal_id_display_name: Optional[str] = None):
        """
        The Azure Active Directory principal identifier and Azure built-in role that describes the access the principal will receive on the delegated resource in the managed tenant.
        :param str principal_id: The identifier of the Azure Active Directory principal.
        :param str role_definition_id: The identifier of the Azure built-in role that defines the permissions that the Azure Active Directory principal will have on the projected scope.
        :param Sequence[str] delegated_role_definition_ids: The delegatedRoleDefinitionIds field is required when the roleDefinitionId refers to the User Access Administrator Role. It is the list of role definition ids which define all the permissions that the user in the authorization can assign to other principals.
        :param str principal_id_display_name: The display name of the Azure Active Directory principal.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)
        if delegated_role_definition_ids is not None:
            pulumi.set(__self__, "delegated_role_definition_ids", delegated_role_definition_ids)
        if principal_id_display_name is not None:
            pulumi.set(__self__, "principal_id_display_name", principal_id_display_name)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The identifier of the Azure Active Directory principal.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> str:
        """
        The identifier of the Azure built-in role that defines the permissions that the Azure Active Directory principal will have on the projected scope.
        """
        return pulumi.get(self, "role_definition_id")

    @property
    @pulumi.getter(name="delegatedRoleDefinitionIds")
    def delegated_role_definition_ids(self) -> Optional[Sequence[str]]:
        """
        The delegatedRoleDefinitionIds field is required when the roleDefinitionId refers to the User Access Administrator Role. It is the list of role definition ids which define all the permissions that the user in the authorization can assign to other principals.
        """
        return pulumi.get(self, "delegated_role_definition_ids")

    @property
    @pulumi.getter(name="principalIdDisplayName")
    def principal_id_display_name(self) -> Optional[str]:
        """
        The display name of the Azure Active Directory principal.
        """
        return pulumi.get(self, "principal_id_display_name")


@pulumi.output_type
class EligibleApproverResponse(dict):
    """
    Defines the Azure Active Directory principal that can approve any just-in-time access requests by the principal defined in the EligibleAuthorization.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "principalIdDisplayName":
            suggest = "principal_id_display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EligibleApproverResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EligibleApproverResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EligibleApproverResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 principal_id_display_name: Optional[str] = None):
        """
        Defines the Azure Active Directory principal that can approve any just-in-time access requests by the principal defined in the EligibleAuthorization.
        :param str principal_id: The identifier of the Azure Active Directory principal.
        :param str principal_id_display_name: The display name of the Azure Active Directory principal.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        if principal_id_display_name is not None:
            pulumi.set(__self__, "principal_id_display_name", principal_id_display_name)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The identifier of the Azure Active Directory principal.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="principalIdDisplayName")
    def principal_id_display_name(self) -> Optional[str]:
        """
        The display name of the Azure Active Directory principal.
        """
        return pulumi.get(self, "principal_id_display_name")


@pulumi.output_type
class EligibleAuthorizationResponse(dict):
    """
    The Azure Active Directory principal identifier, Azure built-in role, and just-in-time access policy that describes the just-in-time access the principal will receive on the delegated resource in the managed tenant.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "roleDefinitionId":
            suggest = "role_definition_id"
        elif key == "justInTimeAccessPolicy":
            suggest = "just_in_time_access_policy"
        elif key == "principalIdDisplayName":
            suggest = "principal_id_display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EligibleAuthorizationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EligibleAuthorizationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EligibleAuthorizationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 role_definition_id: str,
                 just_in_time_access_policy: Optional['outputs.JustInTimeAccessPolicyResponse'] = None,
                 principal_id_display_name: Optional[str] = None):
        """
        The Azure Active Directory principal identifier, Azure built-in role, and just-in-time access policy that describes the just-in-time access the principal will receive on the delegated resource in the managed tenant.
        :param str principal_id: The identifier of the Azure Active Directory principal.
        :param str role_definition_id: The identifier of the Azure built-in role that defines the permissions that the Azure Active Directory principal will have on the projected scope.
        :param 'JustInTimeAccessPolicyResponse' just_in_time_access_policy: The just-in-time access policy setting.
        :param str principal_id_display_name: The display name of the Azure Active Directory principal.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)
        if just_in_time_access_policy is not None:
            pulumi.set(__self__, "just_in_time_access_policy", just_in_time_access_policy)
        if principal_id_display_name is not None:
            pulumi.set(__self__, "principal_id_display_name", principal_id_display_name)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The identifier of the Azure Active Directory principal.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> str:
        """
        The identifier of the Azure built-in role that defines the permissions that the Azure Active Directory principal will have on the projected scope.
        """
        return pulumi.get(self, "role_definition_id")

    @property
    @pulumi.getter(name="justInTimeAccessPolicy")
    def just_in_time_access_policy(self) -> Optional['outputs.JustInTimeAccessPolicyResponse']:
        """
        The just-in-time access policy setting.
        """
        return pulumi.get(self, "just_in_time_access_policy")

    @property
    @pulumi.getter(name="principalIdDisplayName")
    def principal_id_display_name(self) -> Optional[str]:
        """
        The display name of the Azure Active Directory principal.
        """
        return pulumi.get(self, "principal_id_display_name")


@pulumi.output_type
class JustInTimeAccessPolicyResponse(dict):
    """
    Just-in-time access policy setting.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "multiFactorAuthProvider":
            suggest = "multi_factor_auth_provider"
        elif key == "managedByTenantApprovers":
            suggest = "managed_by_tenant_approvers"
        elif key == "maximumActivationDuration":
            suggest = "maximum_activation_duration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in JustInTimeAccessPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        JustInTimeAccessPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        JustInTimeAccessPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 multi_factor_auth_provider: str,
                 managed_by_tenant_approvers: Optional[Sequence['outputs.EligibleApproverResponse']] = None,
                 maximum_activation_duration: Optional[str] = None):
        """
        Just-in-time access policy setting.
        :param str multi_factor_auth_provider: The multi-factor authorization provider to be used for just-in-time access requests.
        :param Sequence['EligibleApproverResponse'] managed_by_tenant_approvers: The list of managedByTenant approvers for the eligible authorization.
        :param str maximum_activation_duration: The maximum access duration in ISO 8601 format for just-in-time access requests.
        """
        if multi_factor_auth_provider is None:
            multi_factor_auth_provider = 'None'
        pulumi.set(__self__, "multi_factor_auth_provider", multi_factor_auth_provider)
        if managed_by_tenant_approvers is not None:
            pulumi.set(__self__, "managed_by_tenant_approvers", managed_by_tenant_approvers)
        if maximum_activation_duration is None:
            maximum_activation_duration = 'PT8H'
        if maximum_activation_duration is not None:
            pulumi.set(__self__, "maximum_activation_duration", maximum_activation_duration)

    @property
    @pulumi.getter(name="multiFactorAuthProvider")
    def multi_factor_auth_provider(self) -> str:
        """
        The multi-factor authorization provider to be used for just-in-time access requests.
        """
        return pulumi.get(self, "multi_factor_auth_provider")

    @property
    @pulumi.getter(name="managedByTenantApprovers")
    def managed_by_tenant_approvers(self) -> Optional[Sequence['outputs.EligibleApproverResponse']]:
        """
        The list of managedByTenant approvers for the eligible authorization.
        """
        return pulumi.get(self, "managed_by_tenant_approvers")

    @property
    @pulumi.getter(name="maximumActivationDuration")
    def maximum_activation_duration(self) -> Optional[str]:
        """
        The maximum access duration in ISO 8601 format for just-in-time access requests.
        """
        return pulumi.get(self, "maximum_activation_duration")


@pulumi.output_type
class PlanResponse(dict):
    """
    The details for the Managed Services offer’s plan in Azure Marketplace.
    """
    def __init__(__self__, *,
                 name: str,
                 product: str,
                 publisher: str,
                 version: str):
        """
        The details for the Managed Services offer’s plan in Azure Marketplace.
        :param str name: Azure Marketplace plan name.
        :param str product: Azure Marketplace product code.
        :param str publisher: Azure Marketplace publisher ID.
        :param str version: Azure Marketplace plan's version.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "product", product)
        pulumi.set(__self__, "publisher", publisher)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure Marketplace plan name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def product(self) -> str:
        """
        Azure Marketplace product code.
        """
        return pulumi.get(self, "product")

    @property
    @pulumi.getter
    def publisher(self) -> str:
        """
        Azure Marketplace publisher ID.
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Azure Marketplace plan's version.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class RegistrationAssignmentPropertiesResponse(dict):
    """
    The properties of the registration assignment.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "registrationDefinition":
            suggest = "registration_definition"
        elif key == "registrationDefinitionId":
            suggest = "registration_definition_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistrationAssignmentPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistrationAssignmentPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistrationAssignmentPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 provisioning_state: str,
                 registration_definition: 'outputs.RegistrationAssignmentPropertiesResponseRegistrationDefinition',
                 registration_definition_id: str):
        """
        The properties of the registration assignment.
        :param str provisioning_state: The current provisioning state of the registration assignment.
        :param 'RegistrationAssignmentPropertiesResponseRegistrationDefinition' registration_definition: The registration definition associated with the registration assignment.
        :param str registration_definition_id: The fully qualified path of the registration definition.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "registration_definition", registration_definition)
        pulumi.set(__self__, "registration_definition_id", registration_definition_id)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The current provisioning state of the registration assignment.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="registrationDefinition")
    def registration_definition(self) -> 'outputs.RegistrationAssignmentPropertiesResponseRegistrationDefinition':
        """
        The registration definition associated with the registration assignment.
        """
        return pulumi.get(self, "registration_definition")

    @property
    @pulumi.getter(name="registrationDefinitionId")
    def registration_definition_id(self) -> str:
        """
        The fully qualified path of the registration definition.
        """
        return pulumi.get(self, "registration_definition_id")


@pulumi.output_type
class RegistrationAssignmentPropertiesResponseProperties(dict):
    """
    The properties of the registration definition associated with the registration assignment.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "eligibleAuthorizations":
            suggest = "eligible_authorizations"
        elif key == "managedByTenantId":
            suggest = "managed_by_tenant_id"
        elif key == "managedByTenantName":
            suggest = "managed_by_tenant_name"
        elif key == "manageeTenantId":
            suggest = "managee_tenant_id"
        elif key == "manageeTenantName":
            suggest = "managee_tenant_name"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "registrationDefinitionName":
            suggest = "registration_definition_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistrationAssignmentPropertiesResponseProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistrationAssignmentPropertiesResponseProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistrationAssignmentPropertiesResponseProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authorizations: Optional[Sequence['outputs.AuthorizationResponse']] = None,
                 description: Optional[str] = None,
                 eligible_authorizations: Optional[Sequence['outputs.EligibleAuthorizationResponse']] = None,
                 managed_by_tenant_id: Optional[str] = None,
                 managed_by_tenant_name: Optional[str] = None,
                 managee_tenant_id: Optional[str] = None,
                 managee_tenant_name: Optional[str] = None,
                 provisioning_state: Optional[str] = None,
                 registration_definition_name: Optional[str] = None):
        """
        The properties of the registration definition associated with the registration assignment.
        :param Sequence['AuthorizationResponse'] authorizations: The collection of authorization objects describing the access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        :param str description: The description of the registration definition.
        :param Sequence['EligibleAuthorizationResponse'] eligible_authorizations: The collection of eligible authorization objects describing the just-in-time access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        :param str managed_by_tenant_id: The identifier of the managedBy tenant.
        :param str managed_by_tenant_name: The name of the managedBy tenant.
        :param str managee_tenant_id: The identifier of the managed tenant.
        :param str managee_tenant_name: The name of the managed tenant.
        :param str provisioning_state: The current provisioning state of the registration definition.
        :param str registration_definition_name: The name of the registration definition.
        """
        if authorizations is not None:
            pulumi.set(__self__, "authorizations", authorizations)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if eligible_authorizations is not None:
            pulumi.set(__self__, "eligible_authorizations", eligible_authorizations)
        if managed_by_tenant_id is not None:
            pulumi.set(__self__, "managed_by_tenant_id", managed_by_tenant_id)
        if managed_by_tenant_name is not None:
            pulumi.set(__self__, "managed_by_tenant_name", managed_by_tenant_name)
        if managee_tenant_id is not None:
            pulumi.set(__self__, "managee_tenant_id", managee_tenant_id)
        if managee_tenant_name is not None:
            pulumi.set(__self__, "managee_tenant_name", managee_tenant_name)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if registration_definition_name is not None:
            pulumi.set(__self__, "registration_definition_name", registration_definition_name)

    @property
    @pulumi.getter
    def authorizations(self) -> Optional[Sequence['outputs.AuthorizationResponse']]:
        """
        The collection of authorization objects describing the access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        """
        return pulumi.get(self, "authorizations")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the registration definition.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eligibleAuthorizations")
    def eligible_authorizations(self) -> Optional[Sequence['outputs.EligibleAuthorizationResponse']]:
        """
        The collection of eligible authorization objects describing the just-in-time access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        """
        return pulumi.get(self, "eligible_authorizations")

    @property
    @pulumi.getter(name="managedByTenantId")
    def managed_by_tenant_id(self) -> Optional[str]:
        """
        The identifier of the managedBy tenant.
        """
        return pulumi.get(self, "managed_by_tenant_id")

    @property
    @pulumi.getter(name="managedByTenantName")
    def managed_by_tenant_name(self) -> Optional[str]:
        """
        The name of the managedBy tenant.
        """
        return pulumi.get(self, "managed_by_tenant_name")

    @property
    @pulumi.getter(name="manageeTenantId")
    def managee_tenant_id(self) -> Optional[str]:
        """
        The identifier of the managed tenant.
        """
        return pulumi.get(self, "managee_tenant_id")

    @property
    @pulumi.getter(name="manageeTenantName")
    def managee_tenant_name(self) -> Optional[str]:
        """
        The name of the managed tenant.
        """
        return pulumi.get(self, "managee_tenant_name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The current provisioning state of the registration definition.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="registrationDefinitionName")
    def registration_definition_name(self) -> Optional[str]:
        """
        The name of the registration definition.
        """
        return pulumi.get(self, "registration_definition_name")


@pulumi.output_type
class RegistrationAssignmentPropertiesResponseRegistrationDefinition(dict):
    """
    The registration definition associated with the registration assignment.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "systemData":
            suggest = "system_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistrationAssignmentPropertiesResponseRegistrationDefinition. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistrationAssignmentPropertiesResponseRegistrationDefinition.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistrationAssignmentPropertiesResponseRegistrationDefinition.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 name: str,
                 system_data: 'outputs.SystemDataResponse',
                 type: str,
                 plan: Optional['outputs.PlanResponse'] = None,
                 properties: Optional['outputs.RegistrationAssignmentPropertiesResponseProperties'] = None):
        """
        The registration definition associated with the registration assignment.
        :param str id: The fully qualified path of the registration definition.
        :param str name: The name of the registration definition.
        :param 'SystemDataResponse' system_data: The metadata for the registration definition resource.
        :param str type: The type of the Azure resource (Microsoft.ManagedServices/registrationDefinitions).
        :param 'PlanResponse' plan: The details for the Managed Services offer’s plan in Azure Marketplace.
        :param 'RegistrationAssignmentPropertiesResponseProperties' properties: The properties of the registration definition associated with the registration assignment.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "system_data", system_data)
        pulumi.set(__self__, "type", type)
        if plan is not None:
            pulumi.set(__self__, "plan", plan)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The fully qualified path of the registration definition.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the registration definition.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The metadata for the registration definition resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the Azure resource (Microsoft.ManagedServices/registrationDefinitions).
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def plan(self) -> Optional['outputs.PlanResponse']:
        """
        The details for the Managed Services offer’s plan in Azure Marketplace.
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter
    def properties(self) -> Optional['outputs.RegistrationAssignmentPropertiesResponseProperties']:
        """
        The properties of the registration definition associated with the registration assignment.
        """
        return pulumi.get(self, "properties")


@pulumi.output_type
class RegistrationDefinitionPropertiesResponse(dict):
    """
    The properties of a registration definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "managedByTenantId":
            suggest = "managed_by_tenant_id"
        elif key == "managedByTenantName":
            suggest = "managed_by_tenant_name"
        elif key == "manageeTenantId":
            suggest = "managee_tenant_id"
        elif key == "manageeTenantName":
            suggest = "managee_tenant_name"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "eligibleAuthorizations":
            suggest = "eligible_authorizations"
        elif key == "registrationDefinitionName":
            suggest = "registration_definition_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RegistrationDefinitionPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RegistrationDefinitionPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RegistrationDefinitionPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authorizations: Sequence['outputs.AuthorizationResponse'],
                 managed_by_tenant_id: str,
                 managed_by_tenant_name: str,
                 managee_tenant_id: str,
                 managee_tenant_name: str,
                 provisioning_state: str,
                 description: Optional[str] = None,
                 eligible_authorizations: Optional[Sequence['outputs.EligibleAuthorizationResponse']] = None,
                 registration_definition_name: Optional[str] = None):
        """
        The properties of a registration definition.
        :param Sequence['AuthorizationResponse'] authorizations: The collection of authorization objects describing the access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        :param str managed_by_tenant_id: The identifier of the managedBy tenant.
        :param str managed_by_tenant_name: The name of the managedBy tenant.
        :param str managee_tenant_id: The identifier of the managed tenant.
        :param str managee_tenant_name: The name of the managed tenant.
        :param str provisioning_state: The current provisioning state of the registration definition.
        :param str description: The description of the registration definition.
        :param Sequence['EligibleAuthorizationResponse'] eligible_authorizations: The collection of eligible authorization objects describing the just-in-time access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        :param str registration_definition_name: The name of the registration definition.
        """
        pulumi.set(__self__, "authorizations", authorizations)
        pulumi.set(__self__, "managed_by_tenant_id", managed_by_tenant_id)
        pulumi.set(__self__, "managed_by_tenant_name", managed_by_tenant_name)
        pulumi.set(__self__, "managee_tenant_id", managee_tenant_id)
        pulumi.set(__self__, "managee_tenant_name", managee_tenant_name)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if eligible_authorizations is not None:
            pulumi.set(__self__, "eligible_authorizations", eligible_authorizations)
        if registration_definition_name is not None:
            pulumi.set(__self__, "registration_definition_name", registration_definition_name)

    @property
    @pulumi.getter
    def authorizations(self) -> Sequence['outputs.AuthorizationResponse']:
        """
        The collection of authorization objects describing the access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        """
        return pulumi.get(self, "authorizations")

    @property
    @pulumi.getter(name="managedByTenantId")
    def managed_by_tenant_id(self) -> str:
        """
        The identifier of the managedBy tenant.
        """
        return pulumi.get(self, "managed_by_tenant_id")

    @property
    @pulumi.getter(name="managedByTenantName")
    def managed_by_tenant_name(self) -> str:
        """
        The name of the managedBy tenant.
        """
        return pulumi.get(self, "managed_by_tenant_name")

    @property
    @pulumi.getter(name="manageeTenantId")
    def managee_tenant_id(self) -> str:
        """
        The identifier of the managed tenant.
        """
        return pulumi.get(self, "managee_tenant_id")

    @property
    @pulumi.getter(name="manageeTenantName")
    def managee_tenant_name(self) -> str:
        """
        The name of the managed tenant.
        """
        return pulumi.get(self, "managee_tenant_name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The current provisioning state of the registration definition.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the registration definition.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="eligibleAuthorizations")
    def eligible_authorizations(self) -> Optional[Sequence['outputs.EligibleAuthorizationResponse']]:
        """
        The collection of eligible authorization objects describing the just-in-time access Azure Active Directory principals in the managedBy tenant will receive on the delegated resource in the managed tenant.
        """
        return pulumi.get(self, "eligible_authorizations")

    @property
    @pulumi.getter(name="registrationDefinitionName")
    def registration_definition_name(self) -> Optional[str]:
        """
        The name of the registration definition.
        """
        return pulumi.get(self, "registration_definition_name")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
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

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


