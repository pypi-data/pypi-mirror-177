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
    'GetMetadataResult',
    'AwaitableGetMetadataResult',
    'get_metadata',
    'get_metadata_output',
]

@pulumi.output_type
class GetMetadataResult:
    """
    Metadata resource definition.
    """
    def __init__(__self__, author=None, categories=None, content_id=None, content_schema_version=None, custom_version=None, dependencies=None, etag=None, first_publish_date=None, icon=None, id=None, kind=None, last_publish_date=None, name=None, parent_id=None, preview_images=None, preview_images_dark=None, providers=None, source=None, support=None, system_data=None, threat_analysis_tactics=None, threat_analysis_techniques=None, type=None, version=None):
        if author and not isinstance(author, dict):
            raise TypeError("Expected argument 'author' to be a dict")
        pulumi.set(__self__, "author", author)
        if categories and not isinstance(categories, dict):
            raise TypeError("Expected argument 'categories' to be a dict")
        pulumi.set(__self__, "categories", categories)
        if content_id and not isinstance(content_id, str):
            raise TypeError("Expected argument 'content_id' to be a str")
        pulumi.set(__self__, "content_id", content_id)
        if content_schema_version and not isinstance(content_schema_version, str):
            raise TypeError("Expected argument 'content_schema_version' to be a str")
        pulumi.set(__self__, "content_schema_version", content_schema_version)
        if custom_version and not isinstance(custom_version, str):
            raise TypeError("Expected argument 'custom_version' to be a str")
        pulumi.set(__self__, "custom_version", custom_version)
        if dependencies and not isinstance(dependencies, dict):
            raise TypeError("Expected argument 'dependencies' to be a dict")
        pulumi.set(__self__, "dependencies", dependencies)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if first_publish_date and not isinstance(first_publish_date, str):
            raise TypeError("Expected argument 'first_publish_date' to be a str")
        pulumi.set(__self__, "first_publish_date", first_publish_date)
        if icon and not isinstance(icon, str):
            raise TypeError("Expected argument 'icon' to be a str")
        pulumi.set(__self__, "icon", icon)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_publish_date and not isinstance(last_publish_date, str):
            raise TypeError("Expected argument 'last_publish_date' to be a str")
        pulumi.set(__self__, "last_publish_date", last_publish_date)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parent_id and not isinstance(parent_id, str):
            raise TypeError("Expected argument 'parent_id' to be a str")
        pulumi.set(__self__, "parent_id", parent_id)
        if preview_images and not isinstance(preview_images, list):
            raise TypeError("Expected argument 'preview_images' to be a list")
        pulumi.set(__self__, "preview_images", preview_images)
        if preview_images_dark and not isinstance(preview_images_dark, list):
            raise TypeError("Expected argument 'preview_images_dark' to be a list")
        pulumi.set(__self__, "preview_images_dark", preview_images_dark)
        if providers and not isinstance(providers, list):
            raise TypeError("Expected argument 'providers' to be a list")
        pulumi.set(__self__, "providers", providers)
        if source and not isinstance(source, dict):
            raise TypeError("Expected argument 'source' to be a dict")
        pulumi.set(__self__, "source", source)
        if support and not isinstance(support, dict):
            raise TypeError("Expected argument 'support' to be a dict")
        pulumi.set(__self__, "support", support)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if threat_analysis_tactics and not isinstance(threat_analysis_tactics, list):
            raise TypeError("Expected argument 'threat_analysis_tactics' to be a list")
        pulumi.set(__self__, "threat_analysis_tactics", threat_analysis_tactics)
        if threat_analysis_techniques and not isinstance(threat_analysis_techniques, list):
            raise TypeError("Expected argument 'threat_analysis_techniques' to be a list")
        pulumi.set(__self__, "threat_analysis_techniques", threat_analysis_techniques)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def author(self) -> Optional['outputs.MetadataAuthorResponse']:
        """
        The creator of the content item.
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter
    def categories(self) -> Optional['outputs.MetadataCategoriesResponse']:
        """
        Categories for the solution content item
        """
        return pulumi.get(self, "categories")

    @property
    @pulumi.getter(name="contentId")
    def content_id(self) -> Optional[str]:
        """
        Static ID for the content.  Used to identify dependencies and content from solutions or community.  Hard-coded/static for out of the box content and solutions. Dynamic for user-created.  This is the resource name
        """
        return pulumi.get(self, "content_id")

    @property
    @pulumi.getter(name="contentSchemaVersion")
    def content_schema_version(self) -> Optional[str]:
        """
        Schema version of the content. Can be used to distinguish between different flow based on the schema version
        """
        return pulumi.get(self, "content_schema_version")

    @property
    @pulumi.getter(name="customVersion")
    def custom_version(self) -> Optional[str]:
        """
        The custom version of the content. A optional free text
        """
        return pulumi.get(self, "custom_version")

    @property
    @pulumi.getter
    def dependencies(self) -> Optional['outputs.MetadataDependenciesResponse']:
        """
        Dependencies for the content item, what other content items it requires to work.  Can describe more complex dependencies using a recursive/nested structure. For a single dependency an id/kind/version can be supplied or operator/criteria for complex formats.
        """
        return pulumi.get(self, "dependencies")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="firstPublishDate")
    def first_publish_date(self) -> Optional[str]:
        """
        first publish date solution content item
        """
        return pulumi.get(self, "first_publish_date")

    @property
    @pulumi.getter
    def icon(self) -> Optional[str]:
        """
        the icon identifier. this id can later be fetched from the solution template
        """
        return pulumi.get(self, "icon")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of content the metadata is for.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastPublishDate")
    def last_publish_date(self) -> Optional[str]:
        """
        last publish date for the solution content item
        """
        return pulumi.get(self, "last_publish_date")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> str:
        """
        Full parent resource ID of the content item the metadata is for.  This is the full resource ID including the scope (subscription and resource group)
        """
        return pulumi.get(self, "parent_id")

    @property
    @pulumi.getter(name="previewImages")
    def preview_images(self) -> Optional[Sequence[str]]:
        """
        preview image file names. These will be taken from the solution artifacts
        """
        return pulumi.get(self, "preview_images")

    @property
    @pulumi.getter(name="previewImagesDark")
    def preview_images_dark(self) -> Optional[Sequence[str]]:
        """
        preview image file names. These will be taken from the solution artifacts. used for dark theme support
        """
        return pulumi.get(self, "preview_images_dark")

    @property
    @pulumi.getter
    def providers(self) -> Optional[Sequence[str]]:
        """
        Providers for the solution content item
        """
        return pulumi.get(self, "providers")

    @property
    @pulumi.getter
    def source(self) -> Optional['outputs.MetadataSourceResponse']:
        """
        Source of the content.  This is where/how it was created.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def support(self) -> Optional['outputs.MetadataSupportResponse']:
        """
        Support information for the metadata - type, name, contact information
        """
        return pulumi.get(self, "support")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="threatAnalysisTactics")
    def threat_analysis_tactics(self) -> Optional[Sequence[str]]:
        """
        the tactics the resource covers
        """
        return pulumi.get(self, "threat_analysis_tactics")

    @property
    @pulumi.getter(name="threatAnalysisTechniques")
    def threat_analysis_techniques(self) -> Optional[Sequence[str]]:
        """
        the techniques the resource covers, these have to be aligned with the tactics being used
        """
        return pulumi.get(self, "threat_analysis_techniques")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the content.  Default and recommended format is numeric (e.g. 1, 1.0, 1.0.0, 1.0.0.0), following ARM template best practices.  Can also be any string, but then we cannot guarantee any version checks
        """
        return pulumi.get(self, "version")


class AwaitableGetMetadataResult(GetMetadataResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMetadataResult(
            author=self.author,
            categories=self.categories,
            content_id=self.content_id,
            content_schema_version=self.content_schema_version,
            custom_version=self.custom_version,
            dependencies=self.dependencies,
            etag=self.etag,
            first_publish_date=self.first_publish_date,
            icon=self.icon,
            id=self.id,
            kind=self.kind,
            last_publish_date=self.last_publish_date,
            name=self.name,
            parent_id=self.parent_id,
            preview_images=self.preview_images,
            preview_images_dark=self.preview_images_dark,
            providers=self.providers,
            source=self.source,
            support=self.support,
            system_data=self.system_data,
            threat_analysis_tactics=self.threat_analysis_tactics,
            threat_analysis_techniques=self.threat_analysis_techniques,
            type=self.type,
            version=self.version)


def get_metadata(metadata_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 workspace_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMetadataResult:
    """
    Metadata resource definition.


    :param str metadata_name: The Metadata name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['metadataName'] = metadata_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20221001preview:getMetadata', __args__, opts=opts, typ=GetMetadataResult).value

    return AwaitableGetMetadataResult(
        author=__ret__.author,
        categories=__ret__.categories,
        content_id=__ret__.content_id,
        content_schema_version=__ret__.content_schema_version,
        custom_version=__ret__.custom_version,
        dependencies=__ret__.dependencies,
        etag=__ret__.etag,
        first_publish_date=__ret__.first_publish_date,
        icon=__ret__.icon,
        id=__ret__.id,
        kind=__ret__.kind,
        last_publish_date=__ret__.last_publish_date,
        name=__ret__.name,
        parent_id=__ret__.parent_id,
        preview_images=__ret__.preview_images,
        preview_images_dark=__ret__.preview_images_dark,
        providers=__ret__.providers,
        source=__ret__.source,
        support=__ret__.support,
        system_data=__ret__.system_data,
        threat_analysis_tactics=__ret__.threat_analysis_tactics,
        threat_analysis_techniques=__ret__.threat_analysis_techniques,
        type=__ret__.type,
        version=__ret__.version)


@_utilities.lift_output_func(get_metadata)
def get_metadata_output(metadata_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        workspace_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMetadataResult]:
    """
    Metadata resource definition.


    :param str metadata_name: The Metadata name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
