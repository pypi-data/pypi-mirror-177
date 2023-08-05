# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AssessmentDayOfWeek',
    'AutoBackupDaysOfWeek',
    'BackupScheduleType',
    'ClusterSubnetType',
    'Commit',
    'ConnectivityType',
    'DayOfWeek',
    'DiskConfigurationType',
    'Failover',
    'FullBackupFrequencyType',
    'IdentityType',
    'LeastPrivilegeMode',
    'ReadableSecondary',
    'Role',
    'SqlImageSku',
    'SqlManagementMode',
    'SqlServerLicenseType',
    'SqlVmGroupImageSku',
    'SqlWorkloadType',
    'StorageWorkloadType',
]


class AssessmentDayOfWeek(str, Enum):
    """
    Day of the week to run assessment.
    """
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class AutoBackupDaysOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class BackupScheduleType(str, Enum):
    """
    Backup schedule type.
    """
    MANUAL = "Manual"
    AUTOMATED = "Automated"


class ClusterSubnetType(str, Enum):
    """
    Cluster subnet type.
    """
    SINGLE_SUBNET = "SingleSubnet"
    MULTI_SUBNET = "MultiSubnet"


class Commit(str, Enum):
    """
    Replica commit mode in availability group.
    """
    SYNCHRONOU_S_COMMIT = "SYNCHRONOUS_COMMIT"
    ASYNCHRONOU_S_COMMIT = "ASYNCHRONOUS_COMMIT"


class ConnectivityType(str, Enum):
    """
    SQL Server connectivity option.
    """
    LOCAL = "LOCAL"
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"


class DayOfWeek(str, Enum):
    """
    Day of week to apply the patch on.
    """
    EVERYDAY = "Everyday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class DiskConfigurationType(str, Enum):
    """
    Disk configuration to apply to SQL Server.
    """
    NEW = "NEW"
    EXTEND = "EXTEND"
    ADD = "ADD"


class Failover(str, Enum):
    """
    Replica failover mode in availability group.
    """
    AUTOMATIC = "AUTOMATIC"
    MANUAL = "MANUAL"


class FullBackupFrequencyType(str, Enum):
    """
    Frequency of full backups. In both cases, full backups begin during the next scheduled time window.
    """
    DAILY = "Daily"
    WEEKLY = "Weekly"


class IdentityType(str, Enum):
    """
    The identity type. Set this to 'SystemAssigned' in order to automatically create and assign an Azure Active Directory principal for the resource.
    """
    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"


class LeastPrivilegeMode(str, Enum):
    """
    SQL IaaS Agent least privilege mode.
    """
    ENABLED = "Enabled"


class ReadableSecondary(str, Enum):
    """
    Replica readable secondary mode in availability group.
    """
    NO = "NO"
    ALL = "ALL"
    REA_D_ONLY = "READ_ONLY"


class Role(str, Enum):
    """
    Replica Role in availability group.
    """
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"


class SqlImageSku(str, Enum):
    """
    SQL Server edition type.
    """
    DEVELOPER = "Developer"
    EXPRESS = "Express"
    STANDARD = "Standard"
    ENTERPRISE = "Enterprise"
    WEB = "Web"


class SqlManagementMode(str, Enum):
    """
    SQL Server Management type.
    """
    FULL = "Full"
    LIGHT_WEIGHT = "LightWeight"
    NO_AGENT = "NoAgent"


class SqlServerLicenseType(str, Enum):
    """
    SQL Server license type.
    """
    PAYG = "PAYG"
    AHUB = "AHUB"
    DR = "DR"


class SqlVmGroupImageSku(str, Enum):
    """
    SQL image sku.
    """
    DEVELOPER = "Developer"
    ENTERPRISE = "Enterprise"


class SqlWorkloadType(str, Enum):
    """
    SQL Server workload type.
    """
    GENERAL = "GENERAL"
    OLTP = "OLTP"
    DW = "DW"


class StorageWorkloadType(str, Enum):
    """
    Storage workload type.
    """
    GENERAL = "GENERAL"
    OLTP = "OLTP"
    DW = "DW"
