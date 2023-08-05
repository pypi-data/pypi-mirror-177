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
from ._inputs import *

__all__ = ['OperationalizationClusterArgs', 'OperationalizationCluster']

@pulumi.input_type
class OperationalizationClusterArgs:
    def __init__(__self__, *,
                 cluster_type: pulumi.Input[Union[str, 'ClusterType']],
                 resource_group_name: pulumi.Input[str],
                 app_insights: Optional[pulumi.Input['AppInsightsPropertiesArgs']] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 container_registry: Optional[pulumi.Input['ContainerRegistryPropertiesArgs']] = None,
                 container_service: Optional[pulumi.Input['AcsClusterPropertiesArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 global_service_configuration: Optional[pulumi.Input['GlobalServiceConfigurationArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 storage_account: Optional[pulumi.Input['StorageAccountPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a OperationalizationCluster resource.
        :param pulumi.Input[Union[str, 'ClusterType']] cluster_type: The cluster type.
        :param pulumi.Input[str] resource_group_name: Name of the resource group in which the cluster is located.
        :param pulumi.Input['AppInsightsPropertiesArgs'] app_insights: AppInsights configuration.
        :param pulumi.Input[str] cluster_name: The name of the cluster.
        :param pulumi.Input['ContainerRegistryPropertiesArgs'] container_registry: Container Registry properties.
        :param pulumi.Input['AcsClusterPropertiesArgs'] container_service: Parameters for the Azure Container Service cluster.
        :param pulumi.Input[str] description: The description of the cluster.
        :param pulumi.Input['GlobalServiceConfigurationArgs'] global_service_configuration: Contains global configuration for the web services in the cluster.
        :param pulumi.Input[str] location: Specifies the location of the resource.
        :param pulumi.Input['StorageAccountPropertiesArgs'] storage_account: Storage Account properties.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Contains resource tags defined as key/value pairs.
        """
        pulumi.set(__self__, "cluster_type", cluster_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if app_insights is not None:
            pulumi.set(__self__, "app_insights", app_insights)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if container_registry is not None:
            pulumi.set(__self__, "container_registry", container_registry)
        if container_service is not None:
            pulumi.set(__self__, "container_service", container_service)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if global_service_configuration is not None:
            pulumi.set(__self__, "global_service_configuration", global_service_configuration)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if storage_account is not None:
            pulumi.set(__self__, "storage_account", storage_account)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> pulumi.Input[Union[str, 'ClusterType']]:
        """
        The cluster type.
        """
        return pulumi.get(self, "cluster_type")

    @cluster_type.setter
    def cluster_type(self, value: pulumi.Input[Union[str, 'ClusterType']]):
        pulumi.set(self, "cluster_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group in which the cluster is located.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="appInsights")
    def app_insights(self) -> Optional[pulumi.Input['AppInsightsPropertiesArgs']]:
        """
        AppInsights configuration.
        """
        return pulumi.get(self, "app_insights")

    @app_insights.setter
    def app_insights(self, value: Optional[pulumi.Input['AppInsightsPropertiesArgs']]):
        pulumi.set(self, "app_insights", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the cluster.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="containerRegistry")
    def container_registry(self) -> Optional[pulumi.Input['ContainerRegistryPropertiesArgs']]:
        """
        Container Registry properties.
        """
        return pulumi.get(self, "container_registry")

    @container_registry.setter
    def container_registry(self, value: Optional[pulumi.Input['ContainerRegistryPropertiesArgs']]):
        pulumi.set(self, "container_registry", value)

    @property
    @pulumi.getter(name="containerService")
    def container_service(self) -> Optional[pulumi.Input['AcsClusterPropertiesArgs']]:
        """
        Parameters for the Azure Container Service cluster.
        """
        return pulumi.get(self, "container_service")

    @container_service.setter
    def container_service(self, value: Optional[pulumi.Input['AcsClusterPropertiesArgs']]):
        pulumi.set(self, "container_service", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the cluster.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="globalServiceConfiguration")
    def global_service_configuration(self) -> Optional[pulumi.Input['GlobalServiceConfigurationArgs']]:
        """
        Contains global configuration for the web services in the cluster.
        """
        return pulumi.get(self, "global_service_configuration")

    @global_service_configuration.setter
    def global_service_configuration(self, value: Optional[pulumi.Input['GlobalServiceConfigurationArgs']]):
        pulumi.set(self, "global_service_configuration", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="storageAccount")
    def storage_account(self) -> Optional[pulumi.Input['StorageAccountPropertiesArgs']]:
        """
        Storage Account properties.
        """
        return pulumi.get(self, "storage_account")

    @storage_account.setter
    def storage_account(self, value: Optional[pulumi.Input['StorageAccountPropertiesArgs']]):
        pulumi.set(self, "storage_account", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class OperationalizationCluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_insights: Optional[pulumi.Input[pulumi.InputType['AppInsightsPropertiesArgs']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 cluster_type: Optional[pulumi.Input[Union[str, 'ClusterType']]] = None,
                 container_registry: Optional[pulumi.Input[pulumi.InputType['ContainerRegistryPropertiesArgs']]] = None,
                 container_service: Optional[pulumi.Input[pulumi.InputType['AcsClusterPropertiesArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 global_service_configuration: Optional[pulumi.Input[pulumi.InputType['GlobalServiceConfigurationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_account: Optional[pulumi.Input[pulumi.InputType['StorageAccountPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Instance of an Azure ML Operationalization Cluster resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AppInsightsPropertiesArgs']] app_insights: AppInsights configuration.
        :param pulumi.Input[str] cluster_name: The name of the cluster.
        :param pulumi.Input[Union[str, 'ClusterType']] cluster_type: The cluster type.
        :param pulumi.Input[pulumi.InputType['ContainerRegistryPropertiesArgs']] container_registry: Container Registry properties.
        :param pulumi.Input[pulumi.InputType['AcsClusterPropertiesArgs']] container_service: Parameters for the Azure Container Service cluster.
        :param pulumi.Input[str] description: The description of the cluster.
        :param pulumi.Input[pulumi.InputType['GlobalServiceConfigurationArgs']] global_service_configuration: Contains global configuration for the web services in the cluster.
        :param pulumi.Input[str] location: Specifies the location of the resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group in which the cluster is located.
        :param pulumi.Input[pulumi.InputType['StorageAccountPropertiesArgs']] storage_account: Storage Account properties.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Contains resource tags defined as key/value pairs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OperationalizationClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Instance of an Azure ML Operationalization Cluster resource.

        :param str resource_name: The name of the resource.
        :param OperationalizationClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OperationalizationClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_insights: Optional[pulumi.Input[pulumi.InputType['AppInsightsPropertiesArgs']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 cluster_type: Optional[pulumi.Input[Union[str, 'ClusterType']]] = None,
                 container_registry: Optional[pulumi.Input[pulumi.InputType['ContainerRegistryPropertiesArgs']]] = None,
                 container_service: Optional[pulumi.Input[pulumi.InputType['AcsClusterPropertiesArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 global_service_configuration: Optional[pulumi.Input[pulumi.InputType['GlobalServiceConfigurationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_account: Optional[pulumi.Input[pulumi.InputType['StorageAccountPropertiesArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OperationalizationClusterArgs.__new__(OperationalizationClusterArgs)

            __props__.__dict__["app_insights"] = app_insights
            __props__.__dict__["cluster_name"] = cluster_name
            if cluster_type is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_type'")
            __props__.__dict__["cluster_type"] = cluster_type
            __props__.__dict__["container_registry"] = container_registry
            __props__.__dict__["container_service"] = container_service
            __props__.__dict__["description"] = description
            __props__.__dict__["global_service_configuration"] = global_service_configuration
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["storage_account"] = storage_account
            __props__.__dict__["tags"] = tags
            __props__.__dict__["created_on"] = None
            __props__.__dict__["modified_on"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_errors"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:machinelearningcompute:OperationalizationCluster"), pulumi.Alias(type_="azure-native:machinelearningcompute/v20170601preview:OperationalizationCluster")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(OperationalizationCluster, __self__).__init__(
            'azure-native:machinelearningcompute/v20170801preview:OperationalizationCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'OperationalizationCluster':
        """
        Get an existing OperationalizationCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = OperationalizationClusterArgs.__new__(OperationalizationClusterArgs)

        __props__.__dict__["app_insights"] = None
        __props__.__dict__["cluster_type"] = None
        __props__.__dict__["container_registry"] = None
        __props__.__dict__["container_service"] = None
        __props__.__dict__["created_on"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["global_service_configuration"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["modified_on"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_errors"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["storage_account"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return OperationalizationCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appInsights")
    def app_insights(self) -> pulumi.Output[Optional['outputs.AppInsightsPropertiesResponse']]:
        """
        AppInsights configuration.
        """
        return pulumi.get(self, "app_insights")

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> pulumi.Output[str]:
        """
        The cluster type.
        """
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="containerRegistry")
    def container_registry(self) -> pulumi.Output[Optional['outputs.ContainerRegistryPropertiesResponse']]:
        """
        Container Registry properties.
        """
        return pulumi.get(self, "container_registry")

    @property
    @pulumi.getter(name="containerService")
    def container_service(self) -> pulumi.Output[Optional['outputs.AcsClusterPropertiesResponse']]:
        """
        Parameters for the Azure Container Service cluster.
        """
        return pulumi.get(self, "container_service")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> pulumi.Output[str]:
        """
        The date and time when the cluster was created.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the cluster.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="globalServiceConfiguration")
    def global_service_configuration(self) -> pulumi.Output[Optional['outputs.GlobalServiceConfigurationResponse']]:
        """
        Contains global configuration for the web services in the cluster.
        """
        return pulumi.get(self, "global_service_configuration")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="modifiedOn")
    def modified_on(self) -> pulumi.Output[str]:
        """
        The date and time when the cluster was last modified.
        """
        return pulumi.get(self, "modified_on")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningErrors")
    def provisioning_errors(self) -> pulumi.Output[Sequence['outputs.ErrorResponseWrapperResponse']]:
        """
        List of provisioning errors reported by the resource provider.
        """
        return pulumi.get(self, "provisioning_errors")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provision state of the cluster. Valid values are Unknown, Updating, Provisioning, Succeeded, and Failed.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="storageAccount")
    def storage_account(self) -> pulumi.Output[Optional['outputs.StorageAccountPropertiesResponse']]:
        """
        Storage Account properties.
        """
        return pulumi.get(self, "storage_account")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Specifies the type of the resource.
        """
        return pulumi.get(self, "type")

