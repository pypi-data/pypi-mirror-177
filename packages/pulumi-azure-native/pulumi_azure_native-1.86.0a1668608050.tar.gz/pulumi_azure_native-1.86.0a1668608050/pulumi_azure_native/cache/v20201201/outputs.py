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
    'PrivateEndpointConnectionResponse',
    'PrivateEndpointResponse',
    'PrivateLinkServiceConnectionStateResponse',
    'RedisAccessKeysResponse',
    'RedisCommonPropertiesResponseRedisConfiguration',
    'RedisInstanceDetailsResponse',
    'RedisLinkedServerResponse',
    'ScheduleEntryResponse',
    'SkuResponse',
]

@pulumi.output_type
class PrivateEndpointConnectionResponse(dict):
    """
    The Private Endpoint Connection resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "privateLinkServiceConnectionState":
            suggest = "private_link_service_connection_state"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "privateEndpoint":
            suggest = "private_endpoint"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateEndpointConnectionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateEndpointConnectionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateEndpointConnectionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 name: str,
                 private_link_service_connection_state: 'outputs.PrivateLinkServiceConnectionStateResponse',
                 provisioning_state: str,
                 type: str,
                 private_endpoint: Optional['outputs.PrivateEndpointResponse'] = None):
        """
        The Private Endpoint Connection resource.
        :param str id: Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        :param str name: The name of the resource
        :param 'PrivateLinkServiceConnectionStateResponse' private_link_service_connection_state: A collection of information about the state of the connection between service consumer and provider.
        :param str provisioning_state: The provisioning state of the private endpoint connection resource.
        :param str type: The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        :param 'PrivateEndpointResponse' private_endpoint: The resource of private end point.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "type", type)
        if private_endpoint is not None:
            pulumi.set(__self__, "private_endpoint", private_endpoint)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> 'outputs.PrivateLinkServiceConnectionStateResponse':
        """
        A collection of information about the state of the connection between service consumer and provider.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the private endpoint connection resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        The resource of private end point.
        """
        return pulumi.get(self, "private_endpoint")


@pulumi.output_type
class PrivateEndpointResponse(dict):
    """
    The Private Endpoint resource.
    """
    def __init__(__self__, *,
                 id: str):
        """
        The Private Endpoint resource.
        :param str id: The ARM identifier for Private Endpoint
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ARM identifier for Private Endpoint
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class PrivateLinkServiceConnectionStateResponse(dict):
    """
    A collection of information about the state of the connection between service consumer and provider.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "actionsRequired":
            suggest = "actions_required"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkServiceConnectionStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkServiceConnectionStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkServiceConnectionStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 actions_required: Optional[str] = None,
                 description: Optional[str] = None,
                 status: Optional[str] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param str actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param str description: The reason for approval/rejection of the connection.
        :param str status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[str]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class RedisAccessKeysResponse(dict):
    """
    Redis cache access keys.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "primaryKey":
            suggest = "primary_key"
        elif key == "secondaryKey":
            suggest = "secondary_key"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RedisAccessKeysResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RedisAccessKeysResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RedisAccessKeysResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 primary_key: str,
                 secondary_key: str):
        """
        Redis cache access keys.
        :param str primary_key: The current primary key that clients can use to authenticate with Redis cache.
        :param str secondary_key: The current secondary key that clients can use to authenticate with Redis cache.
        """
        pulumi.set(__self__, "primary_key", primary_key)
        pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> str:
        """
        The current primary key that clients can use to authenticate with Redis cache.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> str:
        """
        The current secondary key that clients can use to authenticate with Redis cache.
        """
        return pulumi.get(self, "secondary_key")


@pulumi.output_type
class RedisCommonPropertiesResponseRedisConfiguration(dict):
    """
    All Redis Settings. Few possible keys: rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-samples,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set-max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "zonalConfiguration":
            suggest = "zonal_configuration"
        elif key == "aofBackupEnabled":
            suggest = "aof_backup_enabled"
        elif key == "aofStorageConnectionString0":
            suggest = "aof_storage_connection_string0"
        elif key == "aofStorageConnectionString1":
            suggest = "aof_storage_connection_string1"
        elif key == "maxfragmentationmemoryReserved":
            suggest = "maxfragmentationmemory_reserved"
        elif key == "maxmemoryDelta":
            suggest = "maxmemory_delta"
        elif key == "maxmemoryPolicy":
            suggest = "maxmemory_policy"
        elif key == "maxmemoryReserved":
            suggest = "maxmemory_reserved"
        elif key == "rdbBackupEnabled":
            suggest = "rdb_backup_enabled"
        elif key == "rdbBackupFrequency":
            suggest = "rdb_backup_frequency"
        elif key == "rdbBackupMaxSnapshotCount":
            suggest = "rdb_backup_max_snapshot_count"
        elif key == "rdbStorageConnectionString":
            suggest = "rdb_storage_connection_string"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RedisCommonPropertiesResponseRedisConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RedisCommonPropertiesResponseRedisConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RedisCommonPropertiesResponseRedisConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 maxclients: str,
                 zonal_configuration: str,
                 aof_backup_enabled: Optional[str] = None,
                 aof_storage_connection_string0: Optional[str] = None,
                 aof_storage_connection_string1: Optional[str] = None,
                 authnotrequired: Optional[str] = None,
                 maxfragmentationmemory_reserved: Optional[str] = None,
                 maxmemory_delta: Optional[str] = None,
                 maxmemory_policy: Optional[str] = None,
                 maxmemory_reserved: Optional[str] = None,
                 rdb_backup_enabled: Optional[str] = None,
                 rdb_backup_frequency: Optional[str] = None,
                 rdb_backup_max_snapshot_count: Optional[str] = None,
                 rdb_storage_connection_string: Optional[str] = None):
        """
        All Redis Settings. Few possible keys: rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-samples,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set-max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc.
        :param str maxclients: The max clients config
        :param str zonal_configuration: Zonal Configuration
        :param str aof_backup_enabled: Specifies whether the aof backup is enabled
        :param str aof_storage_connection_string0: First storage account connection string
        :param str aof_storage_connection_string1: Second storage account connection string
        :param str authnotrequired: Specifies whether the authentication is disabled. Setting this property is highly discouraged from security point of view.
        :param str maxfragmentationmemory_reserved: Value in megabytes reserved for fragmentation per shard
        :param str maxmemory_delta: Value in megabytes reserved for non-cache usage per shard e.g. failover.
        :param str maxmemory_policy: The eviction strategy used when your data won't fit within its memory limit.
        :param str maxmemory_reserved: Value in megabytes reserved for non-cache usage per shard e.g. failover.
        :param str rdb_backup_enabled: Specifies whether the rdb backup is enabled
        :param str rdb_backup_frequency: Specifies the frequency for creating rdb backup
        :param str rdb_backup_max_snapshot_count: Specifies the maximum number of snapshots for rdb backup
        :param str rdb_storage_connection_string: The storage account connection string for storing rdb file
        """
        pulumi.set(__self__, "maxclients", maxclients)
        pulumi.set(__self__, "zonal_configuration", zonal_configuration)
        if aof_backup_enabled is not None:
            pulumi.set(__self__, "aof_backup_enabled", aof_backup_enabled)
        if aof_storage_connection_string0 is not None:
            pulumi.set(__self__, "aof_storage_connection_string0", aof_storage_connection_string0)
        if aof_storage_connection_string1 is not None:
            pulumi.set(__self__, "aof_storage_connection_string1", aof_storage_connection_string1)
        if authnotrequired is not None:
            pulumi.set(__self__, "authnotrequired", authnotrequired)
        if maxfragmentationmemory_reserved is not None:
            pulumi.set(__self__, "maxfragmentationmemory_reserved", maxfragmentationmemory_reserved)
        if maxmemory_delta is not None:
            pulumi.set(__self__, "maxmemory_delta", maxmemory_delta)
        if maxmemory_policy is not None:
            pulumi.set(__self__, "maxmemory_policy", maxmemory_policy)
        if maxmemory_reserved is not None:
            pulumi.set(__self__, "maxmemory_reserved", maxmemory_reserved)
        if rdb_backup_enabled is not None:
            pulumi.set(__self__, "rdb_backup_enabled", rdb_backup_enabled)
        if rdb_backup_frequency is not None:
            pulumi.set(__self__, "rdb_backup_frequency", rdb_backup_frequency)
        if rdb_backup_max_snapshot_count is not None:
            pulumi.set(__self__, "rdb_backup_max_snapshot_count", rdb_backup_max_snapshot_count)
        if rdb_storage_connection_string is not None:
            pulumi.set(__self__, "rdb_storage_connection_string", rdb_storage_connection_string)

    @property
    @pulumi.getter
    def maxclients(self) -> str:
        """
        The max clients config
        """
        return pulumi.get(self, "maxclients")

    @property
    @pulumi.getter(name="zonalConfiguration")
    def zonal_configuration(self) -> str:
        """
        Zonal Configuration
        """
        return pulumi.get(self, "zonal_configuration")

    @property
    @pulumi.getter(name="aofBackupEnabled")
    def aof_backup_enabled(self) -> Optional[str]:
        """
        Specifies whether the aof backup is enabled
        """
        return pulumi.get(self, "aof_backup_enabled")

    @property
    @pulumi.getter(name="aofStorageConnectionString0")
    def aof_storage_connection_string0(self) -> Optional[str]:
        """
        First storage account connection string
        """
        return pulumi.get(self, "aof_storage_connection_string0")

    @property
    @pulumi.getter(name="aofStorageConnectionString1")
    def aof_storage_connection_string1(self) -> Optional[str]:
        """
        Second storage account connection string
        """
        return pulumi.get(self, "aof_storage_connection_string1")

    @property
    @pulumi.getter
    def authnotrequired(self) -> Optional[str]:
        """
        Specifies whether the authentication is disabled. Setting this property is highly discouraged from security point of view.
        """
        return pulumi.get(self, "authnotrequired")

    @property
    @pulumi.getter(name="maxfragmentationmemoryReserved")
    def maxfragmentationmemory_reserved(self) -> Optional[str]:
        """
        Value in megabytes reserved for fragmentation per shard
        """
        return pulumi.get(self, "maxfragmentationmemory_reserved")

    @property
    @pulumi.getter(name="maxmemoryDelta")
    def maxmemory_delta(self) -> Optional[str]:
        """
        Value in megabytes reserved for non-cache usage per shard e.g. failover.
        """
        return pulumi.get(self, "maxmemory_delta")

    @property
    @pulumi.getter(name="maxmemoryPolicy")
    def maxmemory_policy(self) -> Optional[str]:
        """
        The eviction strategy used when your data won't fit within its memory limit.
        """
        return pulumi.get(self, "maxmemory_policy")

    @property
    @pulumi.getter(name="maxmemoryReserved")
    def maxmemory_reserved(self) -> Optional[str]:
        """
        Value in megabytes reserved for non-cache usage per shard e.g. failover.
        """
        return pulumi.get(self, "maxmemory_reserved")

    @property
    @pulumi.getter(name="rdbBackupEnabled")
    def rdb_backup_enabled(self) -> Optional[str]:
        """
        Specifies whether the rdb backup is enabled
        """
        return pulumi.get(self, "rdb_backup_enabled")

    @property
    @pulumi.getter(name="rdbBackupFrequency")
    def rdb_backup_frequency(self) -> Optional[str]:
        """
        Specifies the frequency for creating rdb backup
        """
        return pulumi.get(self, "rdb_backup_frequency")

    @property
    @pulumi.getter(name="rdbBackupMaxSnapshotCount")
    def rdb_backup_max_snapshot_count(self) -> Optional[str]:
        """
        Specifies the maximum number of snapshots for rdb backup
        """
        return pulumi.get(self, "rdb_backup_max_snapshot_count")

    @property
    @pulumi.getter(name="rdbStorageConnectionString")
    def rdb_storage_connection_string(self) -> Optional[str]:
        """
        The storage account connection string for storing rdb file
        """
        return pulumi.get(self, "rdb_storage_connection_string")


@pulumi.output_type
class RedisInstanceDetailsResponse(dict):
    """
    Details of single instance of redis.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "isMaster":
            suggest = "is_master"
        elif key == "isPrimary":
            suggest = "is_primary"
        elif key == "nonSslPort":
            suggest = "non_ssl_port"
        elif key == "shardId":
            suggest = "shard_id"
        elif key == "sslPort":
            suggest = "ssl_port"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RedisInstanceDetailsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RedisInstanceDetailsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RedisInstanceDetailsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 is_master: bool,
                 is_primary: bool,
                 non_ssl_port: int,
                 shard_id: int,
                 ssl_port: int,
                 zone: str):
        """
        Details of single instance of redis.
        :param bool is_master: Specifies whether the instance is a primary node.
        :param bool is_primary: Specifies whether the instance is a primary node.
        :param int non_ssl_port: If enableNonSslPort is true, provides Redis instance Non-SSL port.
        :param int shard_id: If clustering is enabled, the Shard ID of Redis Instance
        :param int ssl_port: Redis instance SSL port.
        :param str zone: If the Cache uses availability zones, specifies availability zone where this instance is located.
        """
        pulumi.set(__self__, "is_master", is_master)
        pulumi.set(__self__, "is_primary", is_primary)
        pulumi.set(__self__, "non_ssl_port", non_ssl_port)
        pulumi.set(__self__, "shard_id", shard_id)
        pulumi.set(__self__, "ssl_port", ssl_port)
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="isMaster")
    def is_master(self) -> bool:
        """
        Specifies whether the instance is a primary node.
        """
        return pulumi.get(self, "is_master")

    @property
    @pulumi.getter(name="isPrimary")
    def is_primary(self) -> bool:
        """
        Specifies whether the instance is a primary node.
        """
        return pulumi.get(self, "is_primary")

    @property
    @pulumi.getter(name="nonSslPort")
    def non_ssl_port(self) -> int:
        """
        If enableNonSslPort is true, provides Redis instance Non-SSL port.
        """
        return pulumi.get(self, "non_ssl_port")

    @property
    @pulumi.getter(name="shardId")
    def shard_id(self) -> int:
        """
        If clustering is enabled, the Shard ID of Redis Instance
        """
        return pulumi.get(self, "shard_id")

    @property
    @pulumi.getter(name="sslPort")
    def ssl_port(self) -> int:
        """
        Redis instance SSL port.
        """
        return pulumi.get(self, "ssl_port")

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        If the Cache uses availability zones, specifies availability zone where this instance is located.
        """
        return pulumi.get(self, "zone")


@pulumi.output_type
class RedisLinkedServerResponse(dict):
    """
    Linked server Id
    """
    def __init__(__self__, *,
                 id: str):
        """
        Linked server Id
        :param str id: Linked server Id.
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Linked server Id.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class ScheduleEntryResponse(dict):
    """
    Patch schedule entry for a Premium Redis Cache.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dayOfWeek":
            suggest = "day_of_week"
        elif key == "startHourUtc":
            suggest = "start_hour_utc"
        elif key == "maintenanceWindow":
            suggest = "maintenance_window"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ScheduleEntryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ScheduleEntryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ScheduleEntryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 day_of_week: str,
                 start_hour_utc: int,
                 maintenance_window: Optional[str] = None):
        """
        Patch schedule entry for a Premium Redis Cache.
        :param str day_of_week: Day of the week when a cache can be patched.
        :param int start_hour_utc: Start hour after which cache patching can start.
        :param str maintenance_window: ISO8601 timespan specifying how much time cache patching can take.
        """
        pulumi.set(__self__, "day_of_week", day_of_week)
        pulumi.set(__self__, "start_hour_utc", start_hour_utc)
        if maintenance_window is None:
            maintenance_window = 'PT5H'
        if maintenance_window is not None:
            pulumi.set(__self__, "maintenance_window", maintenance_window)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> str:
        """
        Day of the week when a cache can be patched.
        """
        return pulumi.get(self, "day_of_week")

    @property
    @pulumi.getter(name="startHourUtc")
    def start_hour_utc(self) -> int:
        """
        Start hour after which cache patching can start.
        """
        return pulumi.get(self, "start_hour_utc")

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> Optional[str]:
        """
        ISO8601 timespan specifying how much time cache patching can take.
        """
        return pulumi.get(self, "maintenance_window")


@pulumi.output_type
class SkuResponse(dict):
    """
    SKU parameters supplied to the create Redis operation.
    """
    def __init__(__self__, *,
                 capacity: int,
                 family: str,
                 name: str):
        """
        SKU parameters supplied to the create Redis operation.
        :param int capacity: The size of the Redis cache to deploy. Valid values: for C (Basic/Standard) family (0, 1, 2, 3, 4, 5, 6), for P (Premium) family (1, 2, 3, 4).
        :param str family: The SKU family to use. Valid values: (C, P). (C = Basic/Standard, P = Premium).
        :param str name: The type of Redis cache to deploy. Valid values: (Basic, Standard, Premium)
        """
        pulumi.set(__self__, "capacity", capacity)
        pulumi.set(__self__, "family", family)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> int:
        """
        The size of the Redis cache to deploy. Valid values: for C (Basic/Standard) family (0, 1, 2, 3, 4, 5, 6), for P (Premium) family (1, 2, 3, 4).
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def family(self) -> str:
        """
        The SKU family to use. Valid values: (C, P). (C = Basic/Standard, P = Premium).
        """
        return pulumi.get(self, "family")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The type of Redis cache to deploy. Valid values: (Basic, Standard, Premium)
        """
        return pulumi.get(self, "name")


