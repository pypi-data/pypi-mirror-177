# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetTrafficManagerUserMetricsKeyResult',
    'AwaitableGetTrafficManagerUserMetricsKeyResult',
    'get_traffic_manager_user_metrics_key',
]

@pulumi.output_type
class GetTrafficManagerUserMetricsKeyResult:
    """
    Class representing Traffic Manager User Metrics.
    """
    def __init__(__self__, id=None, key=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The key returned by the User Metrics operation.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the resource. Ex- Microsoft.Network/trafficManagerProfiles.
        """
        return pulumi.get(self, "type")


class AwaitableGetTrafficManagerUserMetricsKeyResult(GetTrafficManagerUserMetricsKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTrafficManagerUserMetricsKeyResult(
            id=self.id,
            key=self.key,
            name=self.name,
            type=self.type)


def get_traffic_manager_user_metrics_key(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTrafficManagerUserMetricsKeyResult:
    """
    Class representing Traffic Manager User Metrics.
    API Version: 2018-08-01.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network:getTrafficManagerUserMetricsKey', __args__, opts=opts, typ=GetTrafficManagerUserMetricsKeyResult).value

    return AwaitableGetTrafficManagerUserMetricsKeyResult(
        id=__ret__.id,
        key=__ret__.key,
        name=__ret__.name,
        type=__ret__.type)
