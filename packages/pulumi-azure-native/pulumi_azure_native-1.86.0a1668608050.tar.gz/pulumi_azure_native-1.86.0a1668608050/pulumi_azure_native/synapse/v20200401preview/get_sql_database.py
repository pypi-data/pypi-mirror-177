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
    'GetSqlDatabaseResult',
    'AwaitableGetSqlDatabaseResult',
    'get_sql_database',
    'get_sql_database_output',
]

warnings.warn("""Version 2020-04-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetSqlDatabaseResult:
    """
    A sql database resource.
    """
    def __init__(__self__, collation=None, data_retention=None, database_guid=None, id=None, location=None, name=None, status=None, storage_redundancy=None, system_data=None, tags=None, type=None):
        if collation and not isinstance(collation, str):
            raise TypeError("Expected argument 'collation' to be a str")
        pulumi.set(__self__, "collation", collation)
        if data_retention and not isinstance(data_retention, dict):
            raise TypeError("Expected argument 'data_retention' to be a dict")
        pulumi.set(__self__, "data_retention", data_retention)
        if database_guid and not isinstance(database_guid, str):
            raise TypeError("Expected argument 'database_guid' to be a str")
        pulumi.set(__self__, "database_guid", database_guid)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if storage_redundancy and not isinstance(storage_redundancy, str):
            raise TypeError("Expected argument 'storage_redundancy' to be a str")
        pulumi.set(__self__, "storage_redundancy", storage_redundancy)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def collation(self) -> Optional[str]:
        """
        The collation of the database.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="dataRetention")
    def data_retention(self) -> Optional['outputs.SqlDatabaseDataRetentionResponse']:
        """
        Sql database data retention.
        """
        return pulumi.get(self, "data_retention")

    @property
    @pulumi.getter(name="databaseGuid")
    def database_guid(self) -> str:
        """
        The Guid of the database.
        """
        return pulumi.get(self, "database_guid")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the database.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageRedundancy")
    def storage_redundancy(self) -> Optional[str]:
        """
        The storage redundancy of the database.
        """
        return pulumi.get(self, "storage_redundancy")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        SystemData of SqlDatabase.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSqlDatabaseResult(GetSqlDatabaseResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlDatabaseResult(
            collation=self.collation,
            data_retention=self.data_retention,
            database_guid=self.database_guid,
            id=self.id,
            location=self.location,
            name=self.name,
            status=self.status,
            storage_redundancy=self.storage_redundancy,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_sql_database(resource_group_name: Optional[str] = None,
                     sql_database_name: Optional[str] = None,
                     workspace_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlDatabaseResult:
    """
    A sql database resource.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sql_database_name: The name of the sql database.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn("""get_sql_database is deprecated: Version 2020-04-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlDatabaseName'] = sql_database_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:synapse/v20200401preview:getSqlDatabase', __args__, opts=opts, typ=GetSqlDatabaseResult).value

    return AwaitableGetSqlDatabaseResult(
        collation=__ret__.collation,
        data_retention=__ret__.data_retention,
        database_guid=__ret__.database_guid,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        status=__ret__.status,
        storage_redundancy=__ret__.storage_redundancy,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_sql_database)
def get_sql_database_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                            sql_database_name: Optional[pulumi.Input[str]] = None,
                            workspace_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSqlDatabaseResult]:
    """
    A sql database resource.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sql_database_name: The name of the sql database.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn("""get_sql_database is deprecated: Version 2020-04-01-preview will be removed in v2 of the provider.""")
    ...
