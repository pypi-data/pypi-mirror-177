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
    'GetSecurityConnectorResult',
    'AwaitableGetSecurityConnectorResult',
    'get_security_connector',
    'get_security_connector_output',
]

@pulumi.output_type
class GetSecurityConnectorResult:
    """
    The security connector resource.
    """
    def __init__(__self__, cloud_name=None, etag=None, hierarchy_identifier=None, id=None, kind=None, location=None, name=None, offerings=None, organizational_data=None, system_data=None, tags=None, type=None):
        if cloud_name and not isinstance(cloud_name, str):
            raise TypeError("Expected argument 'cloud_name' to be a str")
        pulumi.set(__self__, "cloud_name", cloud_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if hierarchy_identifier and not isinstance(hierarchy_identifier, str):
            raise TypeError("Expected argument 'hierarchy_identifier' to be a str")
        pulumi.set(__self__, "hierarchy_identifier", hierarchy_identifier)
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
        if offerings and not isinstance(offerings, list):
            raise TypeError("Expected argument 'offerings' to be a list")
        pulumi.set(__self__, "offerings", offerings)
        if organizational_data and not isinstance(organizational_data, dict):
            raise TypeError("Expected argument 'organizational_data' to be a dict")
        pulumi.set(__self__, "organizational_data", organizational_data)
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
    @pulumi.getter(name="cloudName")
    def cloud_name(self) -> Optional[str]:
        """
        The multi cloud resource's cloud name.
        """
        return pulumi.get(self, "cloud_name")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Entity tag is used for comparing two or more entities from the same requested resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hierarchyIdentifier")
    def hierarchy_identifier(self) -> Optional[str]:
        """
        The multi cloud resource identifier (account id in case of AWS connector).
        """
        return pulumi.get(self, "hierarchy_identifier")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of the resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Location where the resource is stored
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
    @pulumi.getter
    def offerings(self) -> Optional[Sequence[Any]]:
        """
        A collection of offerings for the security connector.
        """
        return pulumi.get(self, "offerings")

    @property
    @pulumi.getter(name="organizationalData")
    def organizational_data(self) -> Optional['outputs.SecurityConnectorPropertiesResponseOrganizationalData']:
        """
        The multi cloud account's organizational data
        """
        return pulumi.get(self, "organizational_data")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        A list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetSecurityConnectorResult(GetSecurityConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityConnectorResult(
            cloud_name=self.cloud_name,
            etag=self.etag,
            hierarchy_identifier=self.hierarchy_identifier,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            offerings=self.offerings,
            organizational_data=self.organizational_data,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_security_connector(resource_group_name: Optional[str] = None,
                           security_connector_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityConnectorResult:
    """
    The security connector resource.


    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    :param str security_connector_name: The security connector name.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['securityConnectorName'] = security_connector_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:security/v20210701preview:getSecurityConnector', __args__, opts=opts, typ=GetSecurityConnectorResult).value

    return AwaitableGetSecurityConnectorResult(
        cloud_name=__ret__.cloud_name,
        etag=__ret__.etag,
        hierarchy_identifier=__ret__.hierarchy_identifier,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        offerings=__ret__.offerings,
        organizational_data=__ret__.organizational_data,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_security_connector)
def get_security_connector_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                  security_connector_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecurityConnectorResult]:
    """
    The security connector resource.


    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    :param str security_connector_name: The security connector name.
    """
    ...
