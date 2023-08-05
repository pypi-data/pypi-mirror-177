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
    'GetDscConfigurationResult',
    'AwaitableGetDscConfigurationResult',
    'get_dsc_configuration',
    'get_dsc_configuration_output',
]

@pulumi.output_type
class GetDscConfigurationResult:
    """
    Definition of the configuration type.
    """
    def __init__(__self__, creation_time=None, description=None, etag=None, id=None, job_count=None, last_modified_time=None, location=None, log_verbose=None, name=None, node_configuration_count=None, parameters=None, provisioning_state=None, source=None, state=None, tags=None, type=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if job_count and not isinstance(job_count, int):
            raise TypeError("Expected argument 'job_count' to be a int")
        pulumi.set(__self__, "job_count", job_count)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if log_verbose and not isinstance(log_verbose, bool):
            raise TypeError("Expected argument 'log_verbose' to be a bool")
        pulumi.set(__self__, "log_verbose", log_verbose)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if node_configuration_count and not isinstance(node_configuration_count, int):
            raise TypeError("Expected argument 'node_configuration_count' to be a int")
        pulumi.set(__self__, "node_configuration_count", node_configuration_count)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if source and not isinstance(source, dict):
            raise TypeError("Expected argument 'source' to be a dict")
        pulumi.set(__self__, "source", source)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        Gets or sets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Gets or sets the etag of the resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="jobCount")
    def job_count(self) -> Optional[int]:
        """
        Gets or sets the job count of the configuration.
        """
        return pulumi.get(self, "job_count")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[str]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The Azure Region where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logVerbose")
    def log_verbose(self) -> Optional[bool]:
        """
        Gets or sets verbose log option.
        """
        return pulumi.get(self, "log_verbose")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nodeConfigurationCount")
    def node_configuration_count(self) -> Optional[int]:
        """
        Gets the number of compiled node configurations.
        """
        return pulumi.get(self, "node_configuration_count")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, 'outputs.DscConfigurationParameterResponse']]:
        """
        Gets or sets the configuration parameters.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Gets or sets the provisioning state of the configuration.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def source(self) -> Optional['outputs.ContentSourceResponse']:
        """
        Gets or sets the source.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        Gets or sets the state of the configuration.
        """
        return pulumi.get(self, "state")

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
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetDscConfigurationResult(GetDscConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDscConfigurationResult(
            creation_time=self.creation_time,
            description=self.description,
            etag=self.etag,
            id=self.id,
            job_count=self.job_count,
            last_modified_time=self.last_modified_time,
            location=self.location,
            log_verbose=self.log_verbose,
            name=self.name,
            node_configuration_count=self.node_configuration_count,
            parameters=self.parameters,
            provisioning_state=self.provisioning_state,
            source=self.source,
            state=self.state,
            tags=self.tags,
            type=self.type)


def get_dsc_configuration(automation_account_name: Optional[str] = None,
                          configuration_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDscConfigurationResult:
    """
    Definition of the configuration type.


    :param str automation_account_name: The name of the automation account.
    :param str configuration_name: The configuration name.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['automationAccountName'] = automation_account_name
    __args__['configurationName'] = configuration_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:automation/v20151031:getDscConfiguration', __args__, opts=opts, typ=GetDscConfigurationResult).value

    return AwaitableGetDscConfigurationResult(
        creation_time=__ret__.creation_time,
        description=__ret__.description,
        etag=__ret__.etag,
        id=__ret__.id,
        job_count=__ret__.job_count,
        last_modified_time=__ret__.last_modified_time,
        location=__ret__.location,
        log_verbose=__ret__.log_verbose,
        name=__ret__.name,
        node_configuration_count=__ret__.node_configuration_count,
        parameters=__ret__.parameters,
        provisioning_state=__ret__.provisioning_state,
        source=__ret__.source,
        state=__ret__.state,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_dsc_configuration)
def get_dsc_configuration_output(automation_account_name: Optional[pulumi.Input[str]] = None,
                                 configuration_name: Optional[pulumi.Input[str]] = None,
                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDscConfigurationResult]:
    """
    Definition of the configuration type.


    :param str automation_account_name: The name of the automation account.
    :param str configuration_name: The configuration name.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    ...
