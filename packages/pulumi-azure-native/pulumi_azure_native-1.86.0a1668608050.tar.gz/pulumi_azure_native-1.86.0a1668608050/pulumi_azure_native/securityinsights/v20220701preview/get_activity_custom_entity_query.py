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
    'GetActivityCustomEntityQueryResult',
    'AwaitableGetActivityCustomEntityQueryResult',
    'get_activity_custom_entity_query',
    'get_activity_custom_entity_query_output',
]

@pulumi.output_type
class GetActivityCustomEntityQueryResult:
    """
    Represents Activity entity query.
    """
    def __init__(__self__, content=None, created_time_utc=None, description=None, enabled=None, entities_filter=None, etag=None, id=None, input_entity_type=None, kind=None, last_modified_time_utc=None, name=None, query_definitions=None, required_input_fields_sets=None, system_data=None, template_name=None, title=None, type=None):
        if content and not isinstance(content, str):
            raise TypeError("Expected argument 'content' to be a str")
        pulumi.set(__self__, "content", content)
        if created_time_utc and not isinstance(created_time_utc, str):
            raise TypeError("Expected argument 'created_time_utc' to be a str")
        pulumi.set(__self__, "created_time_utc", created_time_utc)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if entities_filter and not isinstance(entities_filter, dict):
            raise TypeError("Expected argument 'entities_filter' to be a dict")
        pulumi.set(__self__, "entities_filter", entities_filter)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if input_entity_type and not isinstance(input_entity_type, str):
            raise TypeError("Expected argument 'input_entity_type' to be a str")
        pulumi.set(__self__, "input_entity_type", input_entity_type)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_modified_time_utc and not isinstance(last_modified_time_utc, str):
            raise TypeError("Expected argument 'last_modified_time_utc' to be a str")
        pulumi.set(__self__, "last_modified_time_utc", last_modified_time_utc)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if query_definitions and not isinstance(query_definitions, dict):
            raise TypeError("Expected argument 'query_definitions' to be a dict")
        pulumi.set(__self__, "query_definitions", query_definitions)
        if required_input_fields_sets and not isinstance(required_input_fields_sets, list):
            raise TypeError("Expected argument 'required_input_fields_sets' to be a list")
        pulumi.set(__self__, "required_input_fields_sets", required_input_fields_sets)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if template_name and not isinstance(template_name, str):
            raise TypeError("Expected argument 'template_name' to be a str")
        pulumi.set(__self__, "template_name", template_name)
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, "title", title)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def content(self) -> Optional[str]:
        """
        The entity query content to display in timeline
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="createdTimeUtc")
    def created_time_utc(self) -> str:
        """
        The time the activity was created
        """
        return pulumi.get(self, "created_time_utc")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The entity query description
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Determines whether this activity is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="entitiesFilter")
    def entities_filter(self) -> Optional[Mapping[str, Sequence[str]]]:
        """
        The query applied only to entities matching to all filters
        """
        return pulumi.get(self, "entities_filter")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inputEntityType")
    def input_entity_type(self) -> Optional[str]:
        """
        The type of the query's source entity
        """
        return pulumi.get(self, "input_entity_type")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the entity query
        Expected value is 'Activity'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedTimeUtc")
    def last_modified_time_utc(self) -> str:
        """
        The last time the activity was updated
        """
        return pulumi.get(self, "last_modified_time_utc")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="queryDefinitions")
    def query_definitions(self) -> Optional['outputs.ActivityEntityQueriesPropertiesResponseQueryDefinitions']:
        """
        The Activity query definitions
        """
        return pulumi.get(self, "query_definitions")

    @property
    @pulumi.getter(name="requiredInputFieldsSets")
    def required_input_fields_sets(self) -> Optional[Sequence[Sequence[str]]]:
        """
        List of the fields of the source entity that are required to run the query
        """
        return pulumi.get(self, "required_input_fields_sets")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="templateName")
    def template_name(self) -> Optional[str]:
        """
        The template id this activity was created from
        """
        return pulumi.get(self, "template_name")

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        The entity query title
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetActivityCustomEntityQueryResult(GetActivityCustomEntityQueryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActivityCustomEntityQueryResult(
            content=self.content,
            created_time_utc=self.created_time_utc,
            description=self.description,
            enabled=self.enabled,
            entities_filter=self.entities_filter,
            etag=self.etag,
            id=self.id,
            input_entity_type=self.input_entity_type,
            kind=self.kind,
            last_modified_time_utc=self.last_modified_time_utc,
            name=self.name,
            query_definitions=self.query_definitions,
            required_input_fields_sets=self.required_input_fields_sets,
            system_data=self.system_data,
            template_name=self.template_name,
            title=self.title,
            type=self.type)


def get_activity_custom_entity_query(entity_query_id: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     workspace_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActivityCustomEntityQueryResult:
    """
    Represents Activity entity query.


    :param str entity_query_id: entity query ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['entityQueryId'] = entity_query_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20220701preview:getActivityCustomEntityQuery', __args__, opts=opts, typ=GetActivityCustomEntityQueryResult).value

    return AwaitableGetActivityCustomEntityQueryResult(
        content=__ret__.content,
        created_time_utc=__ret__.created_time_utc,
        description=__ret__.description,
        enabled=__ret__.enabled,
        entities_filter=__ret__.entities_filter,
        etag=__ret__.etag,
        id=__ret__.id,
        input_entity_type=__ret__.input_entity_type,
        kind=__ret__.kind,
        last_modified_time_utc=__ret__.last_modified_time_utc,
        name=__ret__.name,
        query_definitions=__ret__.query_definitions,
        required_input_fields_sets=__ret__.required_input_fields_sets,
        system_data=__ret__.system_data,
        template_name=__ret__.template_name,
        title=__ret__.title,
        type=__ret__.type)


@_utilities.lift_output_func(get_activity_custom_entity_query)
def get_activity_custom_entity_query_output(entity_query_id: Optional[pulumi.Input[str]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            workspace_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetActivityCustomEntityQueryResult]:
    """
    Represents Activity entity query.


    :param str entity_query_id: entity query ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
