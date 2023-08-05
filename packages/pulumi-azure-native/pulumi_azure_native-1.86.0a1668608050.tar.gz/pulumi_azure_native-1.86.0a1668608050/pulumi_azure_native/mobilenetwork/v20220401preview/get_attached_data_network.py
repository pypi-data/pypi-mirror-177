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
    'GetAttachedDataNetworkResult',
    'AwaitableGetAttachedDataNetworkResult',
    'get_attached_data_network',
    'get_attached_data_network_output',
]

@pulumi.output_type
class GetAttachedDataNetworkResult:
    """
    Attached data network resource.
    """
    def __init__(__self__, created_at=None, created_by=None, created_by_type=None, dns_addresses=None, id=None, last_modified_at=None, last_modified_by=None, last_modified_by_type=None, location=None, name=None, napt_configuration=None, provisioning_state=None, system_data=None, tags=None, type=None, user_equipment_address_pool_prefix=None, user_equipment_static_address_pool_prefix=None, user_plane_data_interface=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if created_by and not isinstance(created_by, str):
            raise TypeError("Expected argument 'created_by' to be a str")
        pulumi.set(__self__, "created_by", created_by)
        if created_by_type and not isinstance(created_by_type, str):
            raise TypeError("Expected argument 'created_by_type' to be a str")
        pulumi.set(__self__, "created_by_type", created_by_type)
        if dns_addresses and not isinstance(dns_addresses, list):
            raise TypeError("Expected argument 'dns_addresses' to be a list")
        pulumi.set(__self__, "dns_addresses", dns_addresses)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified_at and not isinstance(last_modified_at, str):
            raise TypeError("Expected argument 'last_modified_at' to be a str")
        pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by and not isinstance(last_modified_by, str):
            raise TypeError("Expected argument 'last_modified_by' to be a str")
        pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type and not isinstance(last_modified_by_type, str):
            raise TypeError("Expected argument 'last_modified_by_type' to be a str")
        pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if napt_configuration and not isinstance(napt_configuration, dict):
            raise TypeError("Expected argument 'napt_configuration' to be a dict")
        pulumi.set(__self__, "napt_configuration", napt_configuration)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_equipment_address_pool_prefix and not isinstance(user_equipment_address_pool_prefix, list):
            raise TypeError("Expected argument 'user_equipment_address_pool_prefix' to be a list")
        pulumi.set(__self__, "user_equipment_address_pool_prefix", user_equipment_address_pool_prefix)
        if user_equipment_static_address_pool_prefix and not isinstance(user_equipment_static_address_pool_prefix, list):
            raise TypeError("Expected argument 'user_equipment_static_address_pool_prefix' to be a list")
        pulumi.set(__self__, "user_equipment_static_address_pool_prefix", user_equipment_static_address_pool_prefix)
        if user_plane_data_interface and not isinstance(user_plane_data_interface, dict):
            raise TypeError("Expected argument 'user_plane_data_interface' to be a dict")
        pulumi.set(__self__, "user_plane_data_interface", user_plane_data_interface)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="dnsAddresses")
    def dns_addresses(self) -> Optional[Sequence[str]]:
        """
        The DNS servers to signal to UEs to use for this attached data network.
        """
        return pulumi.get(self, "dns_addresses")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="naptConfiguration")
    def napt_configuration(self) -> Optional['outputs.NaptConfigurationResponse']:
        """
        The network address and port translation (NAPT) configuration.
        If this is not specified, the attached data network will use a default NAPT configuration with NAPT enabled.
        """
        return pulumi.get(self, "napt_configuration")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the attached data network resource.
        """
        return pulumi.get(self, "provisioning_state")

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
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userEquipmentAddressPoolPrefix")
    def user_equipment_address_pool_prefix(self) -> Optional[Sequence[str]]:
        """
        The user equipment (UE) address pool prefixes for the attached data network from which the packet core instance will dynamically assign IP addresses to UEs.
        The packet core instance assigns an IP address to a UE when the UE sets up a PDU session.
         You must define at least one of userEquipmentAddressPoolPrefix and userEquipmentStaticAddressPoolPrefix. If you define both, they must be of the same size.
        """
        return pulumi.get(self, "user_equipment_address_pool_prefix")

    @property
    @pulumi.getter(name="userEquipmentStaticAddressPoolPrefix")
    def user_equipment_static_address_pool_prefix(self) -> Optional[Sequence[str]]:
        """
        The user equipment (UE) address pool prefixes for the attached data network from which the packet core instance will assign static IP addresses to UEs.
        The packet core instance assigns an IP address to a UE when the UE sets up a PDU session. The static IP address for a specific UE is set in StaticIPConfiguration on the corresponding SIM resource.
        At least one of userEquipmentAddressPoolPrefix and userEquipmentStaticAddressPoolPrefix must be defined. If both are defined, they must be of the same size.
        """
        return pulumi.get(self, "user_equipment_static_address_pool_prefix")

    @property
    @pulumi.getter(name="userPlaneDataInterface")
    def user_plane_data_interface(self) -> 'outputs.InterfacePropertiesResponse':
        """
        The user plane interface on the data network. For 5G networks, this is the N6 interface. For 4G networks, this is the SGi interface.
        """
        return pulumi.get(self, "user_plane_data_interface")


class AwaitableGetAttachedDataNetworkResult(GetAttachedDataNetworkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttachedDataNetworkResult(
            created_at=self.created_at,
            created_by=self.created_by,
            created_by_type=self.created_by_type,
            dns_addresses=self.dns_addresses,
            id=self.id,
            last_modified_at=self.last_modified_at,
            last_modified_by=self.last_modified_by,
            last_modified_by_type=self.last_modified_by_type,
            location=self.location,
            name=self.name,
            napt_configuration=self.napt_configuration,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            user_equipment_address_pool_prefix=self.user_equipment_address_pool_prefix,
            user_equipment_static_address_pool_prefix=self.user_equipment_static_address_pool_prefix,
            user_plane_data_interface=self.user_plane_data_interface)


def get_attached_data_network(attached_data_network_name: Optional[str] = None,
                              packet_core_control_plane_name: Optional[str] = None,
                              packet_core_data_plane_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttachedDataNetworkResult:
    """
    Attached data network resource.


    :param str attached_data_network_name: The name of the attached data network.
    :param str packet_core_control_plane_name: The name of the packet core control plane.
    :param str packet_core_data_plane_name: The name of the packet core data plane.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['attachedDataNetworkName'] = attached_data_network_name
    __args__['packetCoreControlPlaneName'] = packet_core_control_plane_name
    __args__['packetCoreDataPlaneName'] = packet_core_data_plane_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:mobilenetwork/v20220401preview:getAttachedDataNetwork', __args__, opts=opts, typ=GetAttachedDataNetworkResult).value

    return AwaitableGetAttachedDataNetworkResult(
        created_at=__ret__.created_at,
        created_by=__ret__.created_by,
        created_by_type=__ret__.created_by_type,
        dns_addresses=__ret__.dns_addresses,
        id=__ret__.id,
        last_modified_at=__ret__.last_modified_at,
        last_modified_by=__ret__.last_modified_by,
        last_modified_by_type=__ret__.last_modified_by_type,
        location=__ret__.location,
        name=__ret__.name,
        napt_configuration=__ret__.napt_configuration,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        user_equipment_address_pool_prefix=__ret__.user_equipment_address_pool_prefix,
        user_equipment_static_address_pool_prefix=__ret__.user_equipment_static_address_pool_prefix,
        user_plane_data_interface=__ret__.user_plane_data_interface)


@_utilities.lift_output_func(get_attached_data_network)
def get_attached_data_network_output(attached_data_network_name: Optional[pulumi.Input[str]] = None,
                                     packet_core_control_plane_name: Optional[pulumi.Input[str]] = None,
                                     packet_core_data_plane_name: Optional[pulumi.Input[str]] = None,
                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttachedDataNetworkResult]:
    """
    Attached data network resource.


    :param str attached_data_network_name: The name of the attached data network.
    :param str packet_core_control_plane_name: The name of the packet core control plane.
    :param str packet_core_data_plane_name: The name of the packet core data plane.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
