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
    'ColumnResponse',
    'IdentityResponse',
    'PrivateLinkScopedResourceResponse',
    'RestoredLogsResponse',
    'ResultStatisticsResponse',
    'SchemaResponse',
    'SearchResultsResponse',
    'SystemDataResponse',
    'UserIdentityPropertiesResponse',
    'WorkspaceCappingResponse',
    'WorkspaceFeaturesResponse',
    'WorkspaceSkuResponse',
]

@pulumi.output_type
class ColumnResponse(dict):
    """
    Table column.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "isDefaultDisplay":
            suggest = "is_default_display"
        elif key == "isHidden":
            suggest = "is_hidden"
        elif key == "dataTypeHint":
            suggest = "data_type_hint"
        elif key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ColumnResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ColumnResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ColumnResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 is_default_display: bool,
                 is_hidden: bool,
                 data_type_hint: Optional[str] = None,
                 description: Optional[str] = None,
                 display_name: Optional[str] = None,
                 name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        Table column.
        :param bool is_default_display: Is displayed by default.
        :param bool is_hidden: Is column hidden.
        :param str data_type_hint: Column data type logical hint.
        :param str description: Column description.
        :param str display_name: Column display name.
        :param str name: Column name.
        :param str type: Column data type.
        """
        pulumi.set(__self__, "is_default_display", is_default_display)
        pulumi.set(__self__, "is_hidden", is_hidden)
        if data_type_hint is not None:
            pulumi.set(__self__, "data_type_hint", data_type_hint)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="isDefaultDisplay")
    def is_default_display(self) -> bool:
        """
        Is displayed by default.
        """
        return pulumi.get(self, "is_default_display")

    @property
    @pulumi.getter(name="isHidden")
    def is_hidden(self) -> bool:
        """
        Is column hidden.
        """
        return pulumi.get(self, "is_hidden")

    @property
    @pulumi.getter(name="dataTypeHint")
    def data_type_hint(self) -> Optional[str]:
        """
        Column data type logical hint.
        """
        return pulumi.get(self, "data_type_hint")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Column description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Column display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Column name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Column data type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class IdentityResponse(dict):
    """
    Identity for the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.UserIdentityPropertiesResponse']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: Type of managed service identity.
        :param Mapping[str, 'UserIdentityPropertiesResponse'] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of managed service identity.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserIdentityPropertiesResponse']]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class PrivateLinkScopedResourceResponse(dict):
    """
    The private link scope resource reference.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceId":
            suggest = "resource_id"
        elif key == "scopeId":
            suggest = "scope_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkScopedResourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkScopedResourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PrivateLinkScopedResourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 resource_id: Optional[str] = None,
                 scope_id: Optional[str] = None):
        """
        The private link scope resource reference.
        :param str resource_id: The full resource Id of the private link scope resource.
        :param str scope_id: The private link scope unique Identifier.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if scope_id is not None:
            pulumi.set(__self__, "scope_id", scope_id)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The full resource Id of the private link scope resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="scopeId")
    def scope_id(self) -> Optional[str]:
        """
        The private link scope unique Identifier.
        """
        return pulumi.get(self, "scope_id")


@pulumi.output_type
class RestoredLogsResponse(dict):
    """
    Restore parameters.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "azureAsyncOperationId":
            suggest = "azure_async_operation_id"
        elif key == "endRestoreTime":
            suggest = "end_restore_time"
        elif key == "sourceTable":
            suggest = "source_table"
        elif key == "startRestoreTime":
            suggest = "start_restore_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RestoredLogsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RestoredLogsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RestoredLogsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 azure_async_operation_id: str,
                 end_restore_time: Optional[str] = None,
                 source_table: Optional[str] = None,
                 start_restore_time: Optional[str] = None):
        """
        Restore parameters.
        :param str azure_async_operation_id: Search results table async operation id.
        :param str end_restore_time: The timestamp to end the restore by (UTC).
        :param str source_table: The table to restore data from.
        :param str start_restore_time: The timestamp to start the restore from (UTC).
        """
        pulumi.set(__self__, "azure_async_operation_id", azure_async_operation_id)
        if end_restore_time is not None:
            pulumi.set(__self__, "end_restore_time", end_restore_time)
        if source_table is not None:
            pulumi.set(__self__, "source_table", source_table)
        if start_restore_time is not None:
            pulumi.set(__self__, "start_restore_time", start_restore_time)

    @property
    @pulumi.getter(name="azureAsyncOperationId")
    def azure_async_operation_id(self) -> str:
        """
        Search results table async operation id.
        """
        return pulumi.get(self, "azure_async_operation_id")

    @property
    @pulumi.getter(name="endRestoreTime")
    def end_restore_time(self) -> Optional[str]:
        """
        The timestamp to end the restore by (UTC).
        """
        return pulumi.get(self, "end_restore_time")

    @property
    @pulumi.getter(name="sourceTable")
    def source_table(self) -> Optional[str]:
        """
        The table to restore data from.
        """
        return pulumi.get(self, "source_table")

    @property
    @pulumi.getter(name="startRestoreTime")
    def start_restore_time(self) -> Optional[str]:
        """
        The timestamp to start the restore from (UTC).
        """
        return pulumi.get(self, "start_restore_time")


@pulumi.output_type
class ResultStatisticsResponse(dict):
    """
    Search job execution statistics.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "ingestedRecords":
            suggest = "ingested_records"
        elif key == "scannedGb":
            suggest = "scanned_gb"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResultStatisticsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResultStatisticsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResultStatisticsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 ingested_records: int,
                 progress: float,
                 scanned_gb: float):
        """
        Search job execution statistics.
        :param int ingested_records: The number of rows that were returned by the search job.
        :param float progress: Search job completion percentage.
        :param float scanned_gb: Search job: Amount of scanned data.
        """
        pulumi.set(__self__, "ingested_records", ingested_records)
        pulumi.set(__self__, "progress", progress)
        pulumi.set(__self__, "scanned_gb", scanned_gb)

    @property
    @pulumi.getter(name="ingestedRecords")
    def ingested_records(self) -> int:
        """
        The number of rows that were returned by the search job.
        """
        return pulumi.get(self, "ingested_records")

    @property
    @pulumi.getter
    def progress(self) -> float:
        """
        Search job completion percentage.
        """
        return pulumi.get(self, "progress")

    @property
    @pulumi.getter(name="scannedGb")
    def scanned_gb(self) -> float:
        """
        Search job: Amount of scanned data.
        """
        return pulumi.get(self, "scanned_gb")


@pulumi.output_type
class SchemaResponse(dict):
    """
    Table's schema.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "standardColumns":
            suggest = "standard_columns"
        elif key == "tableSubType":
            suggest = "table_sub_type"
        elif key == "tableType":
            suggest = "table_type"
        elif key == "displayName":
            suggest = "display_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SchemaResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SchemaResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SchemaResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 categories: Sequence[str],
                 labels: Sequence[str],
                 solutions: Sequence[str],
                 source: str,
                 standard_columns: Sequence['outputs.ColumnResponse'],
                 table_sub_type: str,
                 table_type: str,
                 columns: Optional[Sequence['outputs.ColumnResponse']] = None,
                 description: Optional[str] = None,
                 display_name: Optional[str] = None,
                 name: Optional[str] = None):
        """
        Table's schema.
        :param Sequence[str] categories: Table category.
        :param Sequence[str] labels: Table labels.
        :param Sequence[str] solutions: List of solutions the table is affiliated with
        :param str source: Table's creator.
        :param Sequence['ColumnResponse'] standard_columns: A list of table standard columns.
        :param str table_sub_type: The subtype describes what APIs can be used to interact with the table, and what features are available against it.
        :param str table_type: Table's creator.
        :param Sequence['ColumnResponse'] columns: A list of table custom columns.
        :param str description: Table description.
        :param str display_name: Table display name.
        :param str name: Table name.
        """
        pulumi.set(__self__, "categories", categories)
        pulumi.set(__self__, "labels", labels)
        pulumi.set(__self__, "solutions", solutions)
        pulumi.set(__self__, "source", source)
        pulumi.set(__self__, "standard_columns", standard_columns)
        pulumi.set(__self__, "table_sub_type", table_sub_type)
        pulumi.set(__self__, "table_type", table_type)
        if columns is not None:
            pulumi.set(__self__, "columns", columns)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def categories(self) -> Sequence[str]:
        """
        Table category.
        """
        return pulumi.get(self, "categories")

    @property
    @pulumi.getter
    def labels(self) -> Sequence[str]:
        """
        Table labels.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def solutions(self) -> Sequence[str]:
        """
        List of solutions the table is affiliated with
        """
        return pulumi.get(self, "solutions")

    @property
    @pulumi.getter
    def source(self) -> str:
        """
        Table's creator.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter(name="standardColumns")
    def standard_columns(self) -> Sequence['outputs.ColumnResponse']:
        """
        A list of table standard columns.
        """
        return pulumi.get(self, "standard_columns")

    @property
    @pulumi.getter(name="tableSubType")
    def table_sub_type(self) -> str:
        """
        The subtype describes what APIs can be used to interact with the table, and what features are available against it.
        """
        return pulumi.get(self, "table_sub_type")

    @property
    @pulumi.getter(name="tableType")
    def table_type(self) -> str:
        """
        Table's creator.
        """
        return pulumi.get(self, "table_type")

    @property
    @pulumi.getter
    def columns(self) -> Optional[Sequence['outputs.ColumnResponse']]:
        """
        A list of table custom columns.
        """
        return pulumi.get(self, "columns")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Table description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Table display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Table name.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class SearchResultsResponse(dict):
    """
    Parameters of the search job that initiated this table.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "azureAsyncOperationId":
            suggest = "azure_async_operation_id"
        elif key == "sourceTable":
            suggest = "source_table"
        elif key == "endSearchTime":
            suggest = "end_search_time"
        elif key == "startSearchTime":
            suggest = "start_search_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SearchResultsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SearchResultsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SearchResultsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 azure_async_operation_id: str,
                 source_table: str,
                 description: Optional[str] = None,
                 end_search_time: Optional[str] = None,
                 limit: Optional[int] = None,
                 query: Optional[str] = None,
                 start_search_time: Optional[str] = None):
        """
        Parameters of the search job that initiated this table.
        :param str azure_async_operation_id: Search results table async operation id.
        :param str source_table: The table used in the search job.
        :param str description: Search job Description.
        :param str end_search_time: The timestamp to end the search by (UTC)
        :param int limit: Limit the search job to return up to specified number of rows.
        :param str query: Search job query.
        :param str start_search_time: The timestamp to start the search from (UTC)
        """
        pulumi.set(__self__, "azure_async_operation_id", azure_async_operation_id)
        pulumi.set(__self__, "source_table", source_table)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if end_search_time is not None:
            pulumi.set(__self__, "end_search_time", end_search_time)
        if limit is not None:
            pulumi.set(__self__, "limit", limit)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if start_search_time is not None:
            pulumi.set(__self__, "start_search_time", start_search_time)

    @property
    @pulumi.getter(name="azureAsyncOperationId")
    def azure_async_operation_id(self) -> str:
        """
        Search results table async operation id.
        """
        return pulumi.get(self, "azure_async_operation_id")

    @property
    @pulumi.getter(name="sourceTable")
    def source_table(self) -> str:
        """
        The table used in the search job.
        """
        return pulumi.get(self, "source_table")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Search job Description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endSearchTime")
    def end_search_time(self) -> Optional[str]:
        """
        The timestamp to end the search by (UTC)
        """
        return pulumi.get(self, "end_search_time")

    @property
    @pulumi.getter
    def limit(self) -> Optional[int]:
        """
        Limit the search job to return up to specified number of rows.
        """
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def query(self) -> Optional[str]:
        """
        Search job query.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter(name="startSearchTime")
    def start_search_time(self) -> Optional[str]:
        """
        The timestamp to start the search from (UTC)
        """
        return pulumi.get(self, "start_search_time")


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


@pulumi.output_type
class UserIdentityPropertiesResponse(dict):
    """
    User assigned identity properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserIdentityPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserIdentityPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserIdentityPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        User assigned identity properties.
        :param str client_id: The client id of user assigned identity.
        :param str principal_id: The principal id of user assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")


@pulumi.output_type
class WorkspaceCappingResponse(dict):
    """
    The daily volume cap for ingestion.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataIngestionStatus":
            suggest = "data_ingestion_status"
        elif key == "quotaNextResetTime":
            suggest = "quota_next_reset_time"
        elif key == "dailyQuotaGb":
            suggest = "daily_quota_gb"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceCappingResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceCappingResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceCappingResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_ingestion_status: str,
                 quota_next_reset_time: str,
                 daily_quota_gb: Optional[float] = None):
        """
        The daily volume cap for ingestion.
        :param str data_ingestion_status: The status of data ingestion for this workspace.
        :param str quota_next_reset_time: The time when the quota will be rest.
        :param float daily_quota_gb: The workspace daily quota for ingestion.
        """
        pulumi.set(__self__, "data_ingestion_status", data_ingestion_status)
        pulumi.set(__self__, "quota_next_reset_time", quota_next_reset_time)
        if daily_quota_gb is not None:
            pulumi.set(__self__, "daily_quota_gb", daily_quota_gb)

    @property
    @pulumi.getter(name="dataIngestionStatus")
    def data_ingestion_status(self) -> str:
        """
        The status of data ingestion for this workspace.
        """
        return pulumi.get(self, "data_ingestion_status")

    @property
    @pulumi.getter(name="quotaNextResetTime")
    def quota_next_reset_time(self) -> str:
        """
        The time when the quota will be rest.
        """
        return pulumi.get(self, "quota_next_reset_time")

    @property
    @pulumi.getter(name="dailyQuotaGb")
    def daily_quota_gb(self) -> Optional[float]:
        """
        The workspace daily quota for ingestion.
        """
        return pulumi.get(self, "daily_quota_gb")


@pulumi.output_type
class WorkspaceFeaturesResponse(dict):
    """
    Workspace features.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clusterResourceId":
            suggest = "cluster_resource_id"
        elif key == "disableLocalAuth":
            suggest = "disable_local_auth"
        elif key == "enableDataExport":
            suggest = "enable_data_export"
        elif key == "enableLogAccessUsingOnlyResourcePermissions":
            suggest = "enable_log_access_using_only_resource_permissions"
        elif key == "immediatePurgeDataOn30Days":
            suggest = "immediate_purge_data_on30_days"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceFeaturesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceFeaturesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceFeaturesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cluster_resource_id: Optional[str] = None,
                 disable_local_auth: Optional[bool] = None,
                 enable_data_export: Optional[bool] = None,
                 enable_log_access_using_only_resource_permissions: Optional[bool] = None,
                 immediate_purge_data_on30_days: Optional[bool] = None):
        """
        Workspace features.
        :param str cluster_resource_id: Dedicated LA cluster resourceId that is linked to the workspaces.
        :param bool disable_local_auth: Disable Non-AAD based Auth.
        :param bool enable_data_export: Flag that indicate if data should be exported.
        :param bool enable_log_access_using_only_resource_permissions: Flag that indicate which permission to use - resource or workspace or both.
        :param bool immediate_purge_data_on30_days: Flag that describes if we want to remove the data after 30 days.
        """
        if cluster_resource_id is not None:
            pulumi.set(__self__, "cluster_resource_id", cluster_resource_id)
        if disable_local_auth is not None:
            pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if enable_data_export is not None:
            pulumi.set(__self__, "enable_data_export", enable_data_export)
        if enable_log_access_using_only_resource_permissions is not None:
            pulumi.set(__self__, "enable_log_access_using_only_resource_permissions", enable_log_access_using_only_resource_permissions)
        if immediate_purge_data_on30_days is not None:
            pulumi.set(__self__, "immediate_purge_data_on30_days", immediate_purge_data_on30_days)

    @property
    @pulumi.getter(name="clusterResourceId")
    def cluster_resource_id(self) -> Optional[str]:
        """
        Dedicated LA cluster resourceId that is linked to the workspaces.
        """
        return pulumi.get(self, "cluster_resource_id")

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[bool]:
        """
        Disable Non-AAD based Auth.
        """
        return pulumi.get(self, "disable_local_auth")

    @property
    @pulumi.getter(name="enableDataExport")
    def enable_data_export(self) -> Optional[bool]:
        """
        Flag that indicate if data should be exported.
        """
        return pulumi.get(self, "enable_data_export")

    @property
    @pulumi.getter(name="enableLogAccessUsingOnlyResourcePermissions")
    def enable_log_access_using_only_resource_permissions(self) -> Optional[bool]:
        """
        Flag that indicate which permission to use - resource or workspace or both.
        """
        return pulumi.get(self, "enable_log_access_using_only_resource_permissions")

    @property
    @pulumi.getter(name="immediatePurgeDataOn30Days")
    def immediate_purge_data_on30_days(self) -> Optional[bool]:
        """
        Flag that describes if we want to remove the data after 30 days.
        """
        return pulumi.get(self, "immediate_purge_data_on30_days")


@pulumi.output_type
class WorkspaceSkuResponse(dict):
    """
    The SKU (tier) of a workspace.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastSkuUpdate":
            suggest = "last_sku_update"
        elif key == "capacityReservationLevel":
            suggest = "capacity_reservation_level"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceSkuResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceSkuResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceSkuResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 last_sku_update: str,
                 name: str,
                 capacity_reservation_level: Optional[int] = None):
        """
        The SKU (tier) of a workspace.
        :param str last_sku_update: The last time when the sku was updated.
        :param str name: The name of the SKU.
        :param int capacity_reservation_level: The capacity reservation level in GB for this workspace, when CapacityReservation sku is selected.
        """
        pulumi.set(__self__, "last_sku_update", last_sku_update)
        pulumi.set(__self__, "name", name)
        if capacity_reservation_level is not None:
            pulumi.set(__self__, "capacity_reservation_level", capacity_reservation_level)

    @property
    @pulumi.getter(name="lastSkuUpdate")
    def last_sku_update(self) -> str:
        """
        The last time when the sku was updated.
        """
        return pulumi.get(self, "last_sku_update")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="capacityReservationLevel")
    def capacity_reservation_level(self) -> Optional[int]:
        """
        The capacity reservation level in GB for this workspace, when CapacityReservation sku is selected.
        """
        return pulumi.get(self, "capacity_reservation_level")


