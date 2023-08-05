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
    'GetGen2EnvironmentResult',
    'AwaitableGetGen2EnvironmentResult',
    'get_gen2_environment',
    'get_gen2_environment_output',
]

@pulumi.output_type
class GetGen2EnvironmentResult:
    """
    An environment is a set of time-series data available for query, and is the top level Azure Time Series Insights resource. Gen2 environments do not have set data retention limits.
    """
    def __init__(__self__, creation_time=None, data_access_fqdn=None, data_access_id=None, id=None, kind=None, location=None, name=None, provisioning_state=None, sku=None, status=None, storage_configuration=None, tags=None, time_series_id_properties=None, type=None, warm_store_configuration=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if data_access_fqdn and not isinstance(data_access_fqdn, str):
            raise TypeError("Expected argument 'data_access_fqdn' to be a str")
        pulumi.set(__self__, "data_access_fqdn", data_access_fqdn)
        if data_access_id and not isinstance(data_access_id, str):
            raise TypeError("Expected argument 'data_access_id' to be a str")
        pulumi.set(__self__, "data_access_id", data_access_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
        if storage_configuration and not isinstance(storage_configuration, dict):
            raise TypeError("Expected argument 'storage_configuration' to be a dict")
        pulumi.set(__self__, "storage_configuration", storage_configuration)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if time_series_id_properties and not isinstance(time_series_id_properties, list):
            raise TypeError("Expected argument 'time_series_id_properties' to be a list")
        pulumi.set(__self__, "time_series_id_properties", time_series_id_properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if warm_store_configuration and not isinstance(warm_store_configuration, dict):
            raise TypeError("Expected argument 'warm_store_configuration' to be a dict")
        pulumi.set(__self__, "warm_store_configuration", warm_store_configuration)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        The time the resource was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="dataAccessFqdn")
    def data_access_fqdn(self) -> str:
        """
        The fully qualified domain name used to access the environment data, e.g. to query the environment's events or upload reference data for the environment.
        """
        return pulumi.get(self, "data_access_fqdn")

    @property
    @pulumi.getter(name="dataAccessId")
    def data_access_id(self) -> str:
        """
        An id used to access the environment data, e.g. to query the environment's events or upload reference data for the environment.
        """
        return pulumi.get(self, "data_access_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the environment.
        Expected value is 'Gen2'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The sku determines the type of environment, either Gen1 (S1 or S2) or Gen2 (L1). For Gen1 environments the sku determines the capacity of the environment, the ingress rate, and the billing rate.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> 'outputs.EnvironmentStatusResponse':
        """
        An object that represents the status of the environment, and its internal state in the Time Series Insights service.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageConfiguration")
    def storage_configuration(self) -> 'outputs.Gen2StorageConfigurationOutputResponse':
        """
        The storage configuration provides the connection details that allows the Time Series Insights service to connect to the customer storage account that is used to store the environment's data.
        """
        return pulumi.get(self, "storage_configuration")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeSeriesIdProperties")
    def time_series_id_properties(self) -> Sequence['outputs.TimeSeriesIdPropertyResponse']:
        """
        The list of event properties which will be used to define the environment's time series id.
        """
        return pulumi.get(self, "time_series_id_properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="warmStoreConfiguration")
    def warm_store_configuration(self) -> Optional['outputs.WarmStoreConfigurationPropertiesResponse']:
        """
        The warm store configuration provides the details to create a warm store cache that will retain a copy of the environment's data available for faster query.
        """
        return pulumi.get(self, "warm_store_configuration")


class AwaitableGetGen2EnvironmentResult(GetGen2EnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGen2EnvironmentResult(
            creation_time=self.creation_time,
            data_access_fqdn=self.data_access_fqdn,
            data_access_id=self.data_access_id,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            status=self.status,
            storage_configuration=self.storage_configuration,
            tags=self.tags,
            time_series_id_properties=self.time_series_id_properties,
            type=self.type,
            warm_store_configuration=self.warm_store_configuration)


def get_gen2_environment(environment_name: Optional[str] = None,
                         expand: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGen2EnvironmentResult:
    """
    An environment is a set of time-series data available for query, and is the top level Azure Time Series Insights resource. Gen2 environments do not have set data retention limits.


    :param str environment_name: The name of the Time Series Insights environment associated with the specified resource group.
    :param str expand: Setting $expand=status will include the status of the internal services of the environment in the Time Series Insights service.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['environmentName'] = environment_name
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:timeseriesinsights/v20200515:getGen2Environment', __args__, opts=opts, typ=GetGen2EnvironmentResult).value

    return AwaitableGetGen2EnvironmentResult(
        creation_time=__ret__.creation_time,
        data_access_fqdn=__ret__.data_access_fqdn,
        data_access_id=__ret__.data_access_id,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        status=__ret__.status,
        storage_configuration=__ret__.storage_configuration,
        tags=__ret__.tags,
        time_series_id_properties=__ret__.time_series_id_properties,
        type=__ret__.type,
        warm_store_configuration=__ret__.warm_store_configuration)


@_utilities.lift_output_func(get_gen2_environment)
def get_gen2_environment_output(environment_name: Optional[pulumi.Input[str]] = None,
                                expand: Optional[pulumi.Input[Optional[str]]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGen2EnvironmentResult]:
    """
    An environment is a set of time-series data available for query, and is the top level Azure Time Series Insights resource. Gen2 environments do not have set data retention limits.


    :param str environment_name: The name of the Time Series Insights environment associated with the specified resource group.
    :param str expand: Setting $expand=status will include the status of the internal services of the environment in the Time Series Insights service.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    ...
