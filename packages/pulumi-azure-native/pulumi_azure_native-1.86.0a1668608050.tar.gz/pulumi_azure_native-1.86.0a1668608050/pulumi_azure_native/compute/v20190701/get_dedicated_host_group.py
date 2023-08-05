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
    'GetDedicatedHostGroupResult',
    'AwaitableGetDedicatedHostGroupResult',
    'get_dedicated_host_group',
    'get_dedicated_host_group_output',
]

warnings.warn("""Version 2019-07-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetDedicatedHostGroupResult:
    """
    Specifies information about the dedicated host group that the dedicated hosts should be assigned to. <br><br> Currently, a dedicated host can only be added to a dedicated host group at creation time. An existing dedicated host cannot be added to another dedicated host group.
    """
    def __init__(__self__, hosts=None, id=None, location=None, name=None, platform_fault_domain_count=None, tags=None, type=None, zones=None):
        if hosts and not isinstance(hosts, list):
            raise TypeError("Expected argument 'hosts' to be a list")
        pulumi.set(__self__, "hosts", hosts)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform_fault_domain_count and not isinstance(platform_fault_domain_count, int):
            raise TypeError("Expected argument 'platform_fault_domain_count' to be a int")
        pulumi.set(__self__, "platform_fault_domain_count", platform_fault_domain_count)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def hosts(self) -> Sequence['outputs.SubResourceReadOnlyResponse']:
        """
        A list of references to all dedicated hosts in the dedicated host group.
        """
        return pulumi.get(self, "hosts")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

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
    @pulumi.getter(name="platformFaultDomainCount")
    def platform_fault_domain_count(self) -> int:
        """
        Number of fault domains that the host group can span.
        """
        return pulumi.get(self, "platform_fault_domain_count")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        Availability Zone to use for this host group. Only single zone is supported. The zone can be assigned only during creation. If not provided, the group supports all zones in the region. If provided, enforces each host in the group to be in the same zone.
        """
        return pulumi.get(self, "zones")


class AwaitableGetDedicatedHostGroupResult(GetDedicatedHostGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDedicatedHostGroupResult(
            hosts=self.hosts,
            id=self.id,
            location=self.location,
            name=self.name,
            platform_fault_domain_count=self.platform_fault_domain_count,
            tags=self.tags,
            type=self.type,
            zones=self.zones)


def get_dedicated_host_group(host_group_name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDedicatedHostGroupResult:
    """
    Specifies information about the dedicated host group that the dedicated hosts should be assigned to. <br><br> Currently, a dedicated host can only be added to a dedicated host group at creation time. An existing dedicated host cannot be added to another dedicated host group.


    :param str host_group_name: The name of the dedicated host group.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_dedicated_host_group is deprecated: Version 2019-07-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['hostGroupName'] = host_group_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20190701:getDedicatedHostGroup', __args__, opts=opts, typ=GetDedicatedHostGroupResult).value

    return AwaitableGetDedicatedHostGroupResult(
        hosts=__ret__.hosts,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        platform_fault_domain_count=__ret__.platform_fault_domain_count,
        tags=__ret__.tags,
        type=__ret__.type,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_dedicated_host_group)
def get_dedicated_host_group_output(host_group_name: Optional[pulumi.Input[str]] = None,
                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDedicatedHostGroupResult]:
    """
    Specifies information about the dedicated host group that the dedicated hosts should be assigned to. <br><br> Currently, a dedicated host can only be added to a dedicated host group at creation time. An existing dedicated host cannot be added to another dedicated host group.


    :param str host_group_name: The name of the dedicated host group.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_dedicated_host_group is deprecated: Version 2019-07-01 will be removed in v2 of the provider.""")
    ...
