# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetOriginResult',
    'AwaitableGetOriginResult',
    'get_origin',
    'get_origin_output',
]

warnings.warn("""Version 2016-04-02 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetOriginResult:
    """
    CDN origin is the source of the content being delivered via CDN. When the edge nodes represented by an endpoint do not have the requested content cached, they attempt to fetch it from one or more of the configured origins.
    """
    def __init__(__self__, host_name=None, http_port=None, https_port=None, id=None, name=None, provisioning_state=None, resource_state=None, type=None):
        if host_name and not isinstance(host_name, str):
            raise TypeError("Expected argument 'host_name' to be a str")
        pulumi.set(__self__, "host_name", host_name)
        if http_port and not isinstance(http_port, int):
            raise TypeError("Expected argument 'http_port' to be a int")
        pulumi.set(__self__, "http_port", http_port)
        if https_port and not isinstance(https_port, int):
            raise TypeError("Expected argument 'https_port' to be a int")
        pulumi.set(__self__, "https_port", https_port)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_state and not isinstance(resource_state, str):
            raise TypeError("Expected argument 'resource_state' to be a str")
        pulumi.set(__self__, "resource_state", resource_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> str:
        """
        The address of the origin. Domain names, IPv4 addresses, and IPv6 addresses are supported.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="httpPort")
    def http_port(self) -> Optional[int]:
        """
        The value of the HTTP port. Must be between 1 and 65535.
        """
        return pulumi.get(self, "http_port")

    @property
    @pulumi.getter(name="httpsPort")
    def https_port(self) -> Optional[int]:
        """
        The value of the https port. Must be between 1 and 65535.
        """
        return pulumi.get(self, "https_port")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID
        """
        return pulumi.get(self, "id")

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
        Provisioning status of the origin.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> str:
        """
        Resource status of the origin.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetOriginResult(GetOriginResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOriginResult(
            host_name=self.host_name,
            http_port=self.http_port,
            https_port=self.https_port,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            resource_state=self.resource_state,
            type=self.type)


def get_origin(endpoint_name: Optional[str] = None,
               origin_name: Optional[str] = None,
               profile_name: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOriginResult:
    """
    CDN origin is the source of the content being delivered via CDN. When the edge nodes represented by an endpoint do not have the requested content cached, they attempt to fetch it from one or more of the configured origins.


    :param str endpoint_name: Name of the endpoint within the CDN profile.
    :param str origin_name: Name of the origin, an arbitrary value but it needs to be unique under endpoint
    :param str profile_name: Name of the CDN profile within the resource group.
    :param str resource_group_name: Name of the resource group within the Azure subscription.
    """
    pulumi.log.warn("""get_origin is deprecated: Version 2016-04-02 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['endpointName'] = endpoint_name
    __args__['originName'] = origin_name
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:cdn/v20160402:getOrigin', __args__, opts=opts, typ=GetOriginResult).value

    return AwaitableGetOriginResult(
        host_name=__ret__.host_name,
        http_port=__ret__.http_port,
        https_port=__ret__.https_port,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        resource_state=__ret__.resource_state,
        type=__ret__.type)


@_utilities.lift_output_func(get_origin)
def get_origin_output(endpoint_name: Optional[pulumi.Input[str]] = None,
                      origin_name: Optional[pulumi.Input[str]] = None,
                      profile_name: Optional[pulumi.Input[str]] = None,
                      resource_group_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOriginResult]:
    """
    CDN origin is the source of the content being delivered via CDN. When the edge nodes represented by an endpoint do not have the requested content cached, they attempt to fetch it from one or more of the configured origins.


    :param str endpoint_name: Name of the endpoint within the CDN profile.
    :param str origin_name: Name of the origin, an arbitrary value but it needs to be unique under endpoint
    :param str profile_name: Name of the CDN profile within the resource group.
    :param str resource_group_name: Name of the resource group within the Azure subscription.
    """
    pulumi.log.warn("""get_origin is deprecated: Version 2016-04-02 will be removed in v2 of the provider.""")
    ...
