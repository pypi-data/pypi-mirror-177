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
    'GetVirtualRouterPeeringResult',
    'AwaitableGetVirtualRouterPeeringResult',
    'get_virtual_router_peering',
    'get_virtual_router_peering_output',
]

@pulumi.output_type
class GetVirtualRouterPeeringResult:
    """
    Virtual Router Peering resource.
    """
    def __init__(__self__, etag=None, id=None, name=None, peer_asn=None, peer_ip=None, provisioning_state=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if peer_asn and not isinstance(peer_asn, float):
            raise TypeError("Expected argument 'peer_asn' to be a float")
        pulumi.set(__self__, "peer_asn", peer_asn)
        if peer_ip and not isinstance(peer_ip, str):
            raise TypeError("Expected argument 'peer_ip' to be a str")
        pulumi.set(__self__, "peer_ip", peer_ip)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the virtual router peering that is unique within a virtual router.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peerAsn")
    def peer_asn(self) -> Optional[float]:
        """
        Peer ASN.
        """
        return pulumi.get(self, "peer_asn")

    @property
    @pulumi.getter(name="peerIp")
    def peer_ip(self) -> Optional[str]:
        """
        Peer IP.
        """
        return pulumi.get(self, "peer_ip")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Peering type.
        """
        return pulumi.get(self, "type")


class AwaitableGetVirtualRouterPeeringResult(GetVirtualRouterPeeringResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualRouterPeeringResult(
            etag=self.etag,
            id=self.id,
            name=self.name,
            peer_asn=self.peer_asn,
            peer_ip=self.peer_ip,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_virtual_router_peering(peering_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               virtual_router_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualRouterPeeringResult:
    """
    Virtual Router Peering resource.


    :param str peering_name: The name of the Virtual Router Peering.
    :param str resource_group_name: The name of the resource group.
    :param str virtual_router_name: The name of the Virtual Router.
    """
    __args__ = dict()
    __args__['peeringName'] = peering_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualRouterName'] = virtual_router_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20210801:getVirtualRouterPeering', __args__, opts=opts, typ=GetVirtualRouterPeeringResult).value

    return AwaitableGetVirtualRouterPeeringResult(
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        peer_asn=__ret__.peer_asn,
        peer_ip=__ret__.peer_ip,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)


@_utilities.lift_output_func(get_virtual_router_peering)
def get_virtual_router_peering_output(peering_name: Optional[pulumi.Input[str]] = None,
                                      resource_group_name: Optional[pulumi.Input[str]] = None,
                                      virtual_router_name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualRouterPeeringResult]:
    """
    Virtual Router Peering resource.


    :param str peering_name: The name of the Virtual Router Peering.
    :param str resource_group_name: The name of the resource group.
    :param str virtual_router_name: The name of the Virtual Router.
    """
    ...
