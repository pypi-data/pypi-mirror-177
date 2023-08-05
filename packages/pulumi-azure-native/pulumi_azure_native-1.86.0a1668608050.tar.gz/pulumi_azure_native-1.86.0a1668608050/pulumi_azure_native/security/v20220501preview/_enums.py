# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'CloudName',
    'EnvironmentType',
    'OfferingType',
    'OrganizationMembershipType',
    'ScanningMode',
    'SubPlan',
    'Type',
]


class CloudName(str, Enum):
    """
    The multi cloud resource's cloud name.
    """
    AZURE = "Azure"
    AWS = "AWS"
    GCP = "GCP"
    GITHUB = "Github"
    AZURE_DEV_OPS = "AzureDevOps"


class EnvironmentType(str, Enum):
    """
    The type of the environment data.
    """
    AWS_ACCOUNT = "AwsAccount"
    GCP_PROJECT = "GcpProject"
    GITHUB_SCOPE = "GithubScope"
    AZURE_DEV_OPS_SCOPE = "AzureDevOpsScope"


class OfferingType(str, Enum):
    """
    The type of the security offering.
    """
    CSPM_MONITOR_AWS = "CspmMonitorAws"
    DEFENDER_FOR_CONTAINERS_AWS = "DefenderForContainersAws"
    DEFENDER_FOR_SERVERS_AWS = "DefenderForServersAws"
    DEFENDER_FOR_DATABASES_AWS = "DefenderForDatabasesAws"
    INFORMATION_PROTECTION_AWS = "InformationProtectionAws"
    CSPM_MONITOR_GCP = "CspmMonitorGcp"
    CSPM_MONITOR_GITHUB = "CspmMonitorGithub"
    CSPM_MONITOR_AZURE_DEV_OPS = "CspmMonitorAzureDevOps"
    DEFENDER_FOR_SERVERS_GCP = "DefenderForServersGcp"
    DEFENDER_FOR_CONTAINERS_GCP = "DefenderForContainersGcp"
    DEFENDER_FOR_DATABASES_GCP = "DefenderForDatabasesGcp"


class OrganizationMembershipType(str, Enum):
    """
    The multi cloud account's membership type in the organization
    """
    MEMBER = "Member"
    ORGANIZATION = "Organization"


class ScanningMode(str, Enum):
    """
    The scanning mode for the vm scan.
    """
    DEFAULT = "Default"


class SubPlan(str, Enum):
    """
    The available sub plans
    """
    P1 = "P1"
    P2 = "P2"


class Type(str, Enum):
    """
    The Vulnerability Assessment solution to be provisioned. Can be either 'TVM' or 'Qualys'
    """
    QUALYS = "Qualys"
    TVM = "TVM"
