# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AdministratorType',
    'CreateMode',
    'GeoRedundantBackup',
    'MinimalTlsVersionEnum',
    'ServerVersion',
    'SkuTier',
    'SslEnforcementEnum',
    'StorageAutogrow',
]


class AdministratorType(str, Enum):
    """
    The type of administrator.
    """
    ACTIVE_DIRECTORY = "ActiveDirectory"


class CreateMode(str, Enum):
    """
    The mode to create a new server.
    """
    DEFAULT = "Default"
    POINT_IN_TIME_RESTORE = "PointInTimeRestore"
    GEO_RESTORE = "GeoRestore"
    REPLICA = "Replica"


class GeoRedundantBackup(str, Enum):
    """
    Enable Geo-redundant or not for server backup.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class MinimalTlsVersionEnum(str, Enum):
    """
    Enforce a minimal Tls version for the server.
    """
    TLS1_0 = "TLS1_0"
    TLS1_1 = "TLS1_1"
    TLS1_2 = "TLS1_2"
    TLS_ENFORCEMENT_DISABLED = "TLSEnforcementDisabled"


class ServerVersion(str, Enum):
    """
    Server version.
    """
    SERVER_VERSION_5_6 = "5.6"
    SERVER_VERSION_5_7 = "5.7"
    SERVER_VERSION_8_0 = "8.0"


class SkuTier(str, Enum):
    """
    The tier of the particular SKU, e.g. Basic.
    """
    BASIC = "Basic"
    GENERAL_PURPOSE = "GeneralPurpose"
    MEMORY_OPTIMIZED = "MemoryOptimized"


class SslEnforcementEnum(str, Enum):
    """
    Enable ssl enforcement or not when connect to server.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class StorageAutogrow(str, Enum):
    """
    Enable Storage Auto Grow.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"
