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

__all__ = [
    'GetSyncGroupResult',
    'AwaitableGetSyncGroupResult',
    'get_sync_group',
    'get_sync_group_output',
]

@pulumi.output_type
class GetSyncGroupResult:
    """
    An Azure SQL Database sync group.
    """
    def __init__(__self__, conflict_logging_retention_in_days=None, conflict_resolution_policy=None, enable_conflict_logging=None, hub_database_user_name=None, id=None, interval=None, last_sync_time=None, name=None, private_endpoint_name=None, schema=None, sku=None, sync_database_id=None, sync_state=None, type=None, use_private_link_connection=None):
        if conflict_logging_retention_in_days and not isinstance(conflict_logging_retention_in_days, int):
            raise TypeError("Expected argument 'conflict_logging_retention_in_days' to be a int")
        pulumi.set(__self__, "conflict_logging_retention_in_days", conflict_logging_retention_in_days)
        if conflict_resolution_policy and not isinstance(conflict_resolution_policy, str):
            raise TypeError("Expected argument 'conflict_resolution_policy' to be a str")
        pulumi.set(__self__, "conflict_resolution_policy", conflict_resolution_policy)
        if enable_conflict_logging and not isinstance(enable_conflict_logging, bool):
            raise TypeError("Expected argument 'enable_conflict_logging' to be a bool")
        pulumi.set(__self__, "enable_conflict_logging", enable_conflict_logging)
        if hub_database_user_name and not isinstance(hub_database_user_name, str):
            raise TypeError("Expected argument 'hub_database_user_name' to be a str")
        pulumi.set(__self__, "hub_database_user_name", hub_database_user_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if interval and not isinstance(interval, int):
            raise TypeError("Expected argument 'interval' to be a int")
        pulumi.set(__self__, "interval", interval)
        if last_sync_time and not isinstance(last_sync_time, str):
            raise TypeError("Expected argument 'last_sync_time' to be a str")
        pulumi.set(__self__, "last_sync_time", last_sync_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_endpoint_name and not isinstance(private_endpoint_name, str):
            raise TypeError("Expected argument 'private_endpoint_name' to be a str")
        pulumi.set(__self__, "private_endpoint_name", private_endpoint_name)
        if schema and not isinstance(schema, dict):
            raise TypeError("Expected argument 'schema' to be a dict")
        pulumi.set(__self__, "schema", schema)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if sync_database_id and not isinstance(sync_database_id, str):
            raise TypeError("Expected argument 'sync_database_id' to be a str")
        pulumi.set(__self__, "sync_database_id", sync_database_id)
        if sync_state and not isinstance(sync_state, str):
            raise TypeError("Expected argument 'sync_state' to be a str")
        pulumi.set(__self__, "sync_state", sync_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if use_private_link_connection and not isinstance(use_private_link_connection, bool):
            raise TypeError("Expected argument 'use_private_link_connection' to be a bool")
        pulumi.set(__self__, "use_private_link_connection", use_private_link_connection)

    @property
    @pulumi.getter(name="conflictLoggingRetentionInDays")
    def conflict_logging_retention_in_days(self) -> Optional[int]:
        """
        Conflict logging retention period.
        """
        return pulumi.get(self, "conflict_logging_retention_in_days")

    @property
    @pulumi.getter(name="conflictResolutionPolicy")
    def conflict_resolution_policy(self) -> Optional[str]:
        """
        Conflict resolution policy of the sync group.
        """
        return pulumi.get(self, "conflict_resolution_policy")

    @property
    @pulumi.getter(name="enableConflictLogging")
    def enable_conflict_logging(self) -> Optional[bool]:
        """
        If conflict logging is enabled.
        """
        return pulumi.get(self, "enable_conflict_logging")

    @property
    @pulumi.getter(name="hubDatabaseUserName")
    def hub_database_user_name(self) -> Optional[str]:
        """
        User name for the sync group hub database credential.
        """
        return pulumi.get(self, "hub_database_user_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def interval(self) -> Optional[int]:
        """
        Sync interval of the sync group.
        """
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter(name="lastSyncTime")
    def last_sync_time(self) -> str:
        """
        Last sync time of the sync group.
        """
        return pulumi.get(self, "last_sync_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointName")
    def private_endpoint_name(self) -> str:
        """
        Private endpoint name of the sync group if use private link connection is enabled.
        """
        return pulumi.get(self, "private_endpoint_name")

    @property
    @pulumi.getter
    def schema(self) -> Optional['outputs.SyncGroupSchemaResponse']:
        """
        Sync schema of the sync group.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The name and capacity of the SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="syncDatabaseId")
    def sync_database_id(self) -> Optional[str]:
        """
        ARM resource id of the sync database in the sync group.
        """
        return pulumi.get(self, "sync_database_id")

    @property
    @pulumi.getter(name="syncState")
    def sync_state(self) -> str:
        """
        Sync state of the sync group.
        """
        return pulumi.get(self, "sync_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usePrivateLinkConnection")
    def use_private_link_connection(self) -> Optional[bool]:
        """
        If use private link connection is enabled.
        """
        return pulumi.get(self, "use_private_link_connection")


class AwaitableGetSyncGroupResult(GetSyncGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSyncGroupResult(
            conflict_logging_retention_in_days=self.conflict_logging_retention_in_days,
            conflict_resolution_policy=self.conflict_resolution_policy,
            enable_conflict_logging=self.enable_conflict_logging,
            hub_database_user_name=self.hub_database_user_name,
            id=self.id,
            interval=self.interval,
            last_sync_time=self.last_sync_time,
            name=self.name,
            private_endpoint_name=self.private_endpoint_name,
            schema=self.schema,
            sku=self.sku,
            sync_database_id=self.sync_database_id,
            sync_state=self.sync_state,
            type=self.type,
            use_private_link_connection=self.use_private_link_connection)


def get_sync_group(database_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   server_name: Optional[str] = None,
                   sync_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSyncGroupResult:
    """
    An Azure SQL Database sync group.


    :param str database_name: The name of the database on which the sync group is hosted.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str sync_group_name: The name of the sync group.
    """
    __args__ = dict()
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    __args__['syncGroupName'] = sync_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql/v20200801preview:getSyncGroup', __args__, opts=opts, typ=GetSyncGroupResult).value

    return AwaitableGetSyncGroupResult(
        conflict_logging_retention_in_days=__ret__.conflict_logging_retention_in_days,
        conflict_resolution_policy=__ret__.conflict_resolution_policy,
        enable_conflict_logging=__ret__.enable_conflict_logging,
        hub_database_user_name=__ret__.hub_database_user_name,
        id=__ret__.id,
        interval=__ret__.interval,
        last_sync_time=__ret__.last_sync_time,
        name=__ret__.name,
        private_endpoint_name=__ret__.private_endpoint_name,
        schema=__ret__.schema,
        sku=__ret__.sku,
        sync_database_id=__ret__.sync_database_id,
        sync_state=__ret__.sync_state,
        type=__ret__.type,
        use_private_link_connection=__ret__.use_private_link_connection)


@_utilities.lift_output_func(get_sync_group)
def get_sync_group_output(database_name: Optional[pulumi.Input[str]] = None,
                          resource_group_name: Optional[pulumi.Input[str]] = None,
                          server_name: Optional[pulumi.Input[str]] = None,
                          sync_group_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSyncGroupResult]:
    """
    An Azure SQL Database sync group.


    :param str database_name: The name of the database on which the sync group is hosted.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str sync_group_name: The name of the sync group.
    """
    ...
