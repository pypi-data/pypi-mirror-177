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

__all__ = [
    'AuthorizationInfoResponse',
    'AzureDevOpsConnectorPropertiesResponse',
    'AzureDevOpsOrgMetadataResponse',
    'AzureDevOpsProjectMetadataResponse',
    'GitHubConnectorPropertiesResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class AuthorizationInfoResponse(dict):
    def __init__(__self__, *,
                 code: Optional[str] = None):
        """
        :param str code: Gets or sets one-time OAuth code to exchange for refresh and access tokens.
        """
        if code is not None:
            pulumi.set(__self__, "code", code)

    @property
    @pulumi.getter
    def code(self) -> Optional[str]:
        """
        Gets or sets one-time OAuth code to exchange for refresh and access tokens.
        """
        return pulumi.get(self, "code")


@pulumi.output_type
class AzureDevOpsConnectorPropertiesResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AzureDevOpsConnectorPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AzureDevOpsConnectorPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AzureDevOpsConnectorPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 authorization: Optional['outputs.AuthorizationInfoResponse'] = None,
                 orgs: Optional[Sequence['outputs.AzureDevOpsOrgMetadataResponse']] = None,
                 provisioning_state: Optional[str] = None):
        """
        :param Sequence['AzureDevOpsOrgMetadataResponse'] orgs: Gets or sets org onboarding information.
        """
        if authorization is not None:
            pulumi.set(__self__, "authorization", authorization)
        if orgs is not None:
            pulumi.set(__self__, "orgs", orgs)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter
    def authorization(self) -> Optional['outputs.AuthorizationInfoResponse']:
        return pulumi.get(self, "authorization")

    @property
    @pulumi.getter
    def orgs(self) -> Optional[Sequence['outputs.AzureDevOpsOrgMetadataResponse']]:
        """
        Gets or sets org onboarding information.
        """
        return pulumi.get(self, "orgs")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        return pulumi.get(self, "provisioning_state")


@pulumi.output_type
class AzureDevOpsOrgMetadataResponse(dict):
    """
    Org onboarding info.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoDiscovery":
            suggest = "auto_discovery"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AzureDevOpsOrgMetadataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AzureDevOpsOrgMetadataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AzureDevOpsOrgMetadataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_discovery: Optional[str] = None,
                 name: Optional[str] = None,
                 projects: Optional[Sequence['outputs.AzureDevOpsProjectMetadataResponse']] = None):
        """
        Org onboarding info.
        :param str name: Gets or sets name of the AzureDevOps Org.
        """
        if auto_discovery is not None:
            pulumi.set(__self__, "auto_discovery", auto_discovery)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if projects is not None:
            pulumi.set(__self__, "projects", projects)

    @property
    @pulumi.getter(name="autoDiscovery")
    def auto_discovery(self) -> Optional[str]:
        return pulumi.get(self, "auto_discovery")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets name of the AzureDevOps Org.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def projects(self) -> Optional[Sequence['outputs.AzureDevOpsProjectMetadataResponse']]:
        return pulumi.get(self, "projects")


@pulumi.output_type
class AzureDevOpsProjectMetadataResponse(dict):
    """
    Project onboarding info.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "autoDiscovery":
            suggest = "auto_discovery"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AzureDevOpsProjectMetadataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AzureDevOpsProjectMetadataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AzureDevOpsProjectMetadataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 auto_discovery: Optional[str] = None,
                 name: Optional[str] = None,
                 repos: Optional[Sequence[str]] = None):
        """
        Project onboarding info.
        :param str name: Gets or sets name of the AzureDevOps Project.
        :param Sequence[str] repos: Gets or sets repositories.
        """
        if auto_discovery is not None:
            pulumi.set(__self__, "auto_discovery", auto_discovery)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if repos is not None:
            pulumi.set(__self__, "repos", repos)

    @property
    @pulumi.getter(name="autoDiscovery")
    def auto_discovery(self) -> Optional[str]:
        return pulumi.get(self, "auto_discovery")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets name of the AzureDevOps Project.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def repos(self) -> Optional[Sequence[str]]:
        """
        Gets or sets repositories.
        """
        return pulumi.get(self, "repos")


@pulumi.output_type
class GitHubConnectorPropertiesResponse(dict):
    """
    Properties of the ARM resource for /subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.SecurityDevOps/gitHubConnectors.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GitHubConnectorPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GitHubConnectorPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GitHubConnectorPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 code: Optional[str] = None,
                 provisioning_state: Optional[str] = None):
        """
        Properties of the ARM resource for /subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.SecurityDevOps/gitHubConnectors.
        :param str code: Gets or sets one-time OAuth code to exchange for refresh and access tokens.
        """
        if code is not None:
            pulumi.set(__self__, "code", code)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter
    def code(self) -> Optional[str]:
        """
        Gets or sets one-time OAuth code to exchange for refresh and access tokens.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        return pulumi.get(self, "provisioning_state")


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


