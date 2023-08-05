# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'CheckpointResponse',
    'CloudCapacityResponse',
    'ExtendedLocationResponse',
    'HardwareProfileResponse',
    'NetworkInterfacesResponse',
    'NetworkProfileResponse',
    'OsProfileResponse',
    'StorageProfileResponse',
    'StorageQoSPolicyDetailsResponse',
    'StorageQoSPolicyResponse',
    'SystemDataResponse',
    'VMMServerPropertiesResponseCredentials',
    'VirtualDiskResponse',
    'VirtualMachinePropertiesResponseAvailabilitySets',
]

@pulumi.output_type
class CheckpointResponse(dict):
    """
    Defines the resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "checkpointID":
            suggest = "checkpoint_id"
        elif key == "parentCheckpointID":
            suggest = "parent_checkpoint_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CheckpointResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CheckpointResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CheckpointResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 checkpoint_id: Optional[str] = None,
                 description: Optional[str] = None,
                 name: Optional[str] = None,
                 parent_checkpoint_id: Optional[str] = None):
        """
        Defines the resource properties.
        :param str checkpoint_id: Gets ID of the checkpoint.
        :param str description: Gets description of the checkpoint.
        :param str name: Gets name of the checkpoint.
        :param str parent_checkpoint_id: Gets ID of parent of the checkpoint.
        """
        if checkpoint_id is not None:
            pulumi.set(__self__, "checkpoint_id", checkpoint_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if parent_checkpoint_id is not None:
            pulumi.set(__self__, "parent_checkpoint_id", parent_checkpoint_id)

    @property
    @pulumi.getter(name="checkpointID")
    def checkpoint_id(self) -> Optional[str]:
        """
        Gets ID of the checkpoint.
        """
        return pulumi.get(self, "checkpoint_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Gets description of the checkpoint.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets name of the checkpoint.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentCheckpointID")
    def parent_checkpoint_id(self) -> Optional[str]:
        """
        Gets ID of parent of the checkpoint.
        """
        return pulumi.get(self, "parent_checkpoint_id")


@pulumi.output_type
class CloudCapacityResponse(dict):
    """
    Cloud Capacity model
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cpuCount":
            suggest = "cpu_count"
        elif key == "memoryMB":
            suggest = "memory_mb"
        elif key == "vmCount":
            suggest = "vm_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CloudCapacityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CloudCapacityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CloudCapacityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cpu_count: Optional[float] = None,
                 memory_mb: Optional[float] = None,
                 vm_count: Optional[float] = None):
        """
        Cloud Capacity model
        :param float cpu_count: CPUCount specifies the maximum number of CPUs that can be allocated in the cloud.
        :param float memory_mb: MemoryMB specifies a memory usage limit in megabytes.
        :param float vm_count: VMCount gives the max number of VMs that can be deployed in the cloud.
        """
        if cpu_count is not None:
            pulumi.set(__self__, "cpu_count", cpu_count)
        if memory_mb is not None:
            pulumi.set(__self__, "memory_mb", memory_mb)
        if vm_count is not None:
            pulumi.set(__self__, "vm_count", vm_count)

    @property
    @pulumi.getter(name="cpuCount")
    def cpu_count(self) -> Optional[float]:
        """
        CPUCount specifies the maximum number of CPUs that can be allocated in the cloud.
        """
        return pulumi.get(self, "cpu_count")

    @property
    @pulumi.getter(name="memoryMB")
    def memory_mb(self) -> Optional[float]:
        """
        MemoryMB specifies a memory usage limit in megabytes.
        """
        return pulumi.get(self, "memory_mb")

    @property
    @pulumi.getter(name="vmCount")
    def vm_count(self) -> Optional[float]:
        """
        VMCount gives the max number of VMs that can be deployed in the cloud.
        """
        return pulumi.get(self, "vm_count")


@pulumi.output_type
class ExtendedLocationResponse(dict):
    """
    The extended location.
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 type: Optional[str] = None):
        """
        The extended location.
        :param str name: The extended location name.
        :param str type: The extended location type.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The extended location name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The extended location type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class HardwareProfileResponse(dict):
    """
    Defines the resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cpuCount":
            suggest = "cpu_count"
        elif key == "dynamicMemoryEnabled":
            suggest = "dynamic_memory_enabled"
        elif key == "dynamicMemoryMaxMB":
            suggest = "dynamic_memory_max_mb"
        elif key == "dynamicMemoryMinMB":
            suggest = "dynamic_memory_min_mb"
        elif key == "isHighlyAvailable":
            suggest = "is_highly_available"
        elif key == "limitCpuForMigration":
            suggest = "limit_cpu_for_migration"
        elif key == "memoryMB":
            suggest = "memory_mb"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in HardwareProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        HardwareProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        HardwareProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cpu_count: Optional[int] = None,
                 dynamic_memory_enabled: Optional[str] = None,
                 dynamic_memory_max_mb: Optional[int] = None,
                 dynamic_memory_min_mb: Optional[int] = None,
                 is_highly_available: Optional[str] = None,
                 limit_cpu_for_migration: Optional[str] = None,
                 memory_mb: Optional[int] = None):
        """
        Defines the resource properties.
        :param int cpu_count: Gets or sets the number of vCPUs for the vm.
        :param str dynamic_memory_enabled: Gets or sets a value indicating whether to enable dynamic memory or not.
        :param int dynamic_memory_max_mb: Gets or sets the max dynamic memory for the vm.
        :param int dynamic_memory_min_mb: Gets or sets the min dynamic memory for the vm.
        :param str is_highly_available: Gets highly available property.
        :param str limit_cpu_for_migration: Gets or sets a value indicating whether to enable processor compatibility mode for live migration of VMs.
        :param int memory_mb: MemoryMB is the size of a virtual machine's memory, in MB.
        """
        if cpu_count is not None:
            pulumi.set(__self__, "cpu_count", cpu_count)
        if dynamic_memory_enabled is not None:
            pulumi.set(__self__, "dynamic_memory_enabled", dynamic_memory_enabled)
        if dynamic_memory_max_mb is not None:
            pulumi.set(__self__, "dynamic_memory_max_mb", dynamic_memory_max_mb)
        if dynamic_memory_min_mb is not None:
            pulumi.set(__self__, "dynamic_memory_min_mb", dynamic_memory_min_mb)
        if is_highly_available is not None:
            pulumi.set(__self__, "is_highly_available", is_highly_available)
        if limit_cpu_for_migration is not None:
            pulumi.set(__self__, "limit_cpu_for_migration", limit_cpu_for_migration)
        if memory_mb is not None:
            pulumi.set(__self__, "memory_mb", memory_mb)

    @property
    @pulumi.getter(name="cpuCount")
    def cpu_count(self) -> Optional[int]:
        """
        Gets or sets the number of vCPUs for the vm.
        """
        return pulumi.get(self, "cpu_count")

    @property
    @pulumi.getter(name="dynamicMemoryEnabled")
    def dynamic_memory_enabled(self) -> Optional[str]:
        """
        Gets or sets a value indicating whether to enable dynamic memory or not.
        """
        return pulumi.get(self, "dynamic_memory_enabled")

    @property
    @pulumi.getter(name="dynamicMemoryMaxMB")
    def dynamic_memory_max_mb(self) -> Optional[int]:
        """
        Gets or sets the max dynamic memory for the vm.
        """
        return pulumi.get(self, "dynamic_memory_max_mb")

    @property
    @pulumi.getter(name="dynamicMemoryMinMB")
    def dynamic_memory_min_mb(self) -> Optional[int]:
        """
        Gets or sets the min dynamic memory for the vm.
        """
        return pulumi.get(self, "dynamic_memory_min_mb")

    @property
    @pulumi.getter(name="isHighlyAvailable")
    def is_highly_available(self) -> Optional[str]:
        """
        Gets highly available property.
        """
        return pulumi.get(self, "is_highly_available")

    @property
    @pulumi.getter(name="limitCpuForMigration")
    def limit_cpu_for_migration(self) -> Optional[str]:
        """
        Gets or sets a value indicating whether to enable processor compatibility mode for live migration of VMs.
        """
        return pulumi.get(self, "limit_cpu_for_migration")

    @property
    @pulumi.getter(name="memoryMB")
    def memory_mb(self) -> Optional[int]:
        """
        MemoryMB is the size of a virtual machine's memory, in MB.
        """
        return pulumi.get(self, "memory_mb")


@pulumi.output_type
class NetworkInterfacesResponse(dict):
    """
    Network Interface model
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayName":
            suggest = "display_name"
        elif key == "ipv4Addresses":
            suggest = "ipv4_addresses"
        elif key == "ipv6Addresses":
            suggest = "ipv6_addresses"
        elif key == "networkName":
            suggest = "network_name"
        elif key == "ipv4AddressType":
            suggest = "ipv4_address_type"
        elif key == "ipv6AddressType":
            suggest = "ipv6_address_type"
        elif key == "macAddress":
            suggest = "mac_address"
        elif key == "macAddressType":
            suggest = "mac_address_type"
        elif key == "nicId":
            suggest = "nic_id"
        elif key == "virtualNetworkId":
            suggest = "virtual_network_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkInterfacesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkInterfacesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkInterfacesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 display_name: str,
                 ipv4_addresses: Sequence[str],
                 ipv6_addresses: Sequence[str],
                 network_name: str,
                 ipv4_address_type: Optional[str] = None,
                 ipv6_address_type: Optional[str] = None,
                 mac_address: Optional[str] = None,
                 mac_address_type: Optional[str] = None,
                 name: Optional[str] = None,
                 nic_id: Optional[str] = None,
                 virtual_network_id: Optional[str] = None):
        """
        Network Interface model
        :param str display_name: Gets the display name of the network interface as shown in the vmmServer. This is the fallback label for a NIC when the name is not set.
        :param Sequence[str] ipv4_addresses: Gets or sets the nic ipv4 addresses.
        :param Sequence[str] ipv6_addresses: Gets or sets the nic ipv6 addresses.
        :param str network_name: Gets or sets the name of the virtual network in vmmServer that the nic is connected to.
        :param str ipv4_address_type: Gets or sets the ipv4 address type.
        :param str ipv6_address_type: Gets or sets the ipv6 address type.
        :param str mac_address: Gets or sets the nic MAC address.
        :param str mac_address_type: Gets or sets the mac address type.
        :param str name: Gets or sets the name of the network interface.
        :param str nic_id: Gets or sets the nic id.
        :param str virtual_network_id: Gets or sets the ARM Id of the Microsoft.ScVmm/virtualNetwork resource to connect the nic.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "ipv4_addresses", ipv4_addresses)
        pulumi.set(__self__, "ipv6_addresses", ipv6_addresses)
        pulumi.set(__self__, "network_name", network_name)
        if ipv4_address_type is not None:
            pulumi.set(__self__, "ipv4_address_type", ipv4_address_type)
        if ipv6_address_type is not None:
            pulumi.set(__self__, "ipv6_address_type", ipv6_address_type)
        if mac_address is not None:
            pulumi.set(__self__, "mac_address", mac_address)
        if mac_address_type is not None:
            pulumi.set(__self__, "mac_address_type", mac_address_type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if nic_id is not None:
            pulumi.set(__self__, "nic_id", nic_id)
        if virtual_network_id is not None:
            pulumi.set(__self__, "virtual_network_id", virtual_network_id)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Gets the display name of the network interface as shown in the vmmServer. This is the fallback label for a NIC when the name is not set.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="ipv4Addresses")
    def ipv4_addresses(self) -> Sequence[str]:
        """
        Gets or sets the nic ipv4 addresses.
        """
        return pulumi.get(self, "ipv4_addresses")

    @property
    @pulumi.getter(name="ipv6Addresses")
    def ipv6_addresses(self) -> Sequence[str]:
        """
        Gets or sets the nic ipv6 addresses.
        """
        return pulumi.get(self, "ipv6_addresses")

    @property
    @pulumi.getter(name="networkName")
    def network_name(self) -> str:
        """
        Gets or sets the name of the virtual network in vmmServer that the nic is connected to.
        """
        return pulumi.get(self, "network_name")

    @property
    @pulumi.getter(name="ipv4AddressType")
    def ipv4_address_type(self) -> Optional[str]:
        """
        Gets or sets the ipv4 address type.
        """
        return pulumi.get(self, "ipv4_address_type")

    @property
    @pulumi.getter(name="ipv6AddressType")
    def ipv6_address_type(self) -> Optional[str]:
        """
        Gets or sets the ipv6 address type.
        """
        return pulumi.get(self, "ipv6_address_type")

    @property
    @pulumi.getter(name="macAddress")
    def mac_address(self) -> Optional[str]:
        """
        Gets or sets the nic MAC address.
        """
        return pulumi.get(self, "mac_address")

    @property
    @pulumi.getter(name="macAddressType")
    def mac_address_type(self) -> Optional[str]:
        """
        Gets or sets the mac address type.
        """
        return pulumi.get(self, "mac_address_type")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the name of the network interface.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nicId")
    def nic_id(self) -> Optional[str]:
        """
        Gets or sets the nic id.
        """
        return pulumi.get(self, "nic_id")

    @property
    @pulumi.getter(name="virtualNetworkId")
    def virtual_network_id(self) -> Optional[str]:
        """
        Gets or sets the ARM Id of the Microsoft.ScVmm/virtualNetwork resource to connect the nic.
        """
        return pulumi.get(self, "virtual_network_id")


@pulumi.output_type
class NetworkProfileResponse(dict):
    """
    Defines the resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "networkInterfaces":
            suggest = "network_interfaces"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 network_interfaces: Optional[Sequence['outputs.NetworkInterfacesResponse']] = None):
        """
        Defines the resource properties.
        :param Sequence['NetworkInterfacesResponse'] network_interfaces: Gets or sets the list of network interfaces associated with the virtual machine.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[Sequence['outputs.NetworkInterfacesResponse']]:
        """
        Gets or sets the list of network interfaces associated with the virtual machine.
        """
        return pulumi.get(self, "network_interfaces")


@pulumi.output_type
class OsProfileResponse(dict):
    """
    Defines the resource properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "osName":
            suggest = "os_name"
        elif key == "osType":
            suggest = "os_type"
        elif key == "computerName":
            suggest = "computer_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OsProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OsProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OsProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 os_name: str,
                 os_type: str,
                 computer_name: Optional[str] = None):
        """
        Defines the resource properties.
        :param str os_name: Gets or sets os name.
        :param str os_type: Gets or sets the type of the os.
        :param str computer_name: Gets or sets computer name.
        """
        pulumi.set(__self__, "os_name", os_name)
        pulumi.set(__self__, "os_type", os_type)
        if computer_name is not None:
            pulumi.set(__self__, "computer_name", computer_name)

    @property
    @pulumi.getter(name="osName")
    def os_name(self) -> str:
        """
        Gets or sets os name.
        """
        return pulumi.get(self, "os_name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> str:
        """
        Gets or sets the type of the os.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="computerName")
    def computer_name(self) -> Optional[str]:
        """
        Gets or sets computer name.
        """
        return pulumi.get(self, "computer_name")


@pulumi.output_type
class StorageProfileResponse(dict):
    """
    Defines the resource properties.
    """
    def __init__(__self__, *,
                 disks: Optional[Sequence['outputs.VirtualDiskResponse']] = None):
        """
        Defines the resource properties.
        :param Sequence['VirtualDiskResponse'] disks: Gets or sets the list of virtual disks associated with the virtual machine.
        """
        if disks is not None:
            pulumi.set(__self__, "disks", disks)

    @property
    @pulumi.getter
    def disks(self) -> Optional[Sequence['outputs.VirtualDiskResponse']]:
        """
        Gets or sets the list of virtual disks associated with the virtual machine.
        """
        return pulumi.get(self, "disks")


@pulumi.output_type
class StorageQoSPolicyDetailsResponse(dict):
    """
    The StorageQoSPolicyDetails definition.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 name: Optional[str] = None):
        """
        The StorageQoSPolicyDetails definition.
        :param str id: The ID of the QoS policy.
        :param str name: The name of the policy.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the QoS policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class StorageQoSPolicyResponse(dict):
    """
    The StorageQoSPolicy definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bandwidthLimit":
            suggest = "bandwidth_limit"
        elif key == "iopsMaximum":
            suggest = "iops_maximum"
        elif key == "iopsMinimum":
            suggest = "iops_minimum"
        elif key == "policyId":
            suggest = "policy_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StorageQoSPolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StorageQoSPolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StorageQoSPolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bandwidth_limit: Optional[float] = None,
                 id: Optional[str] = None,
                 iops_maximum: Optional[float] = None,
                 iops_minimum: Optional[float] = None,
                 name: Optional[str] = None,
                 policy_id: Optional[str] = None):
        """
        The StorageQoSPolicy definition.
        :param float bandwidth_limit: The Bandwidth Limit for internet traffic.
        :param str id: The ID of the QoS policy.
        :param float iops_maximum: The maximum IO operations per second.
        :param float iops_minimum: The minimum IO operations per second.
        :param str name: The name of the policy.
        :param str policy_id: The underlying policy.
        """
        if bandwidth_limit is not None:
            pulumi.set(__self__, "bandwidth_limit", bandwidth_limit)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if iops_maximum is not None:
            pulumi.set(__self__, "iops_maximum", iops_maximum)
        if iops_minimum is not None:
            pulumi.set(__self__, "iops_minimum", iops_minimum)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)

    @property
    @pulumi.getter(name="bandwidthLimit")
    def bandwidth_limit(self) -> Optional[float]:
        """
        The Bandwidth Limit for internet traffic.
        """
        return pulumi.get(self, "bandwidth_limit")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the QoS policy.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="iopsMaximum")
    def iops_maximum(self) -> Optional[float]:
        """
        The maximum IO operations per second.
        """
        return pulumi.get(self, "iops_maximum")

    @property
    @pulumi.getter(name="iopsMinimum")
    def iops_minimum(self) -> Optional[float]:
        """
        The minimum IO operations per second.
        """
        return pulumi.get(self, "iops_minimum")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[str]:
        """
        The underlying policy.
        """
        return pulumi.get(self, "policy_id")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

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


@pulumi.output_type
class VMMServerPropertiesResponseCredentials(dict):
    """
    Credentials to connect to VMMServer.
    """
    def __init__(__self__, *,
                 username: Optional[str] = None):
        """
        Credentials to connect to VMMServer.
        :param str username: Username to use to connect to VMMServer.
        """
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username to use to connect to VMMServer.
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class VirtualDiskResponse(dict):
    """
    Virtual disk model
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayName":
            suggest = "display_name"
        elif key == "maxDiskSizeGB":
            suggest = "max_disk_size_gb"
        elif key == "vhdFormatType":
            suggest = "vhd_format_type"
        elif key == "volumeType":
            suggest = "volume_type"
        elif key == "busType":
            suggest = "bus_type"
        elif key == "createDiffDisk":
            suggest = "create_diff_disk"
        elif key == "diskId":
            suggest = "disk_id"
        elif key == "diskSizeGB":
            suggest = "disk_size_gb"
        elif key == "storageQoSPolicy":
            suggest = "storage_qo_s_policy"
        elif key == "templateDiskId":
            suggest = "template_disk_id"
        elif key == "vhdType":
            suggest = "vhd_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VirtualDiskResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VirtualDiskResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VirtualDiskResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 display_name: str,
                 max_disk_size_gb: int,
                 vhd_format_type: str,
                 volume_type: str,
                 bus: Optional[int] = None,
                 bus_type: Optional[str] = None,
                 create_diff_disk: Optional[str] = None,
                 disk_id: Optional[str] = None,
                 disk_size_gb: Optional[int] = None,
                 lun: Optional[int] = None,
                 name: Optional[str] = None,
                 storage_qo_s_policy: Optional['outputs.StorageQoSPolicyDetailsResponse'] = None,
                 template_disk_id: Optional[str] = None,
                 vhd_type: Optional[str] = None):
        """
        Virtual disk model
        :param str display_name: Gets the display name of the virtual disk as shown in the vmmServer. This is the fallback label for a disk when the name is not set.
        :param int max_disk_size_gb: Gets or sets the max disk size.
        :param str vhd_format_type: Gets the disk vhd format type.
        :param str volume_type: Gets or sets the disk volume type.
        :param int bus: Gets or sets the disk bus.
        :param str bus_type: Gets or sets the disk bus type.
        :param str create_diff_disk: Gets or sets a value indicating diff disk.
        :param str disk_id: Gets or sets the disk id.
        :param int disk_size_gb: Gets or sets the disk total size.
        :param int lun: Gets or sets the disk lun.
        :param str name: Gets or sets the name of the disk.
        :param 'StorageQoSPolicyDetailsResponse' storage_qo_s_policy: The QoS policy for the disk.
        :param str template_disk_id: Gets or sets the disk id in the template.
        :param str vhd_type: Gets or sets the disk vhd type.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "max_disk_size_gb", max_disk_size_gb)
        pulumi.set(__self__, "vhd_format_type", vhd_format_type)
        pulumi.set(__self__, "volume_type", volume_type)
        if bus is not None:
            pulumi.set(__self__, "bus", bus)
        if bus_type is not None:
            pulumi.set(__self__, "bus_type", bus_type)
        if create_diff_disk is not None:
            pulumi.set(__self__, "create_diff_disk", create_diff_disk)
        if disk_id is not None:
            pulumi.set(__self__, "disk_id", disk_id)
        if disk_size_gb is not None:
            pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if lun is not None:
            pulumi.set(__self__, "lun", lun)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if storage_qo_s_policy is not None:
            pulumi.set(__self__, "storage_qo_s_policy", storage_qo_s_policy)
        if template_disk_id is not None:
            pulumi.set(__self__, "template_disk_id", template_disk_id)
        if vhd_type is not None:
            pulumi.set(__self__, "vhd_type", vhd_type)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Gets the display name of the virtual disk as shown in the vmmServer. This is the fallback label for a disk when the name is not set.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="maxDiskSizeGB")
    def max_disk_size_gb(self) -> int:
        """
        Gets or sets the max disk size.
        """
        return pulumi.get(self, "max_disk_size_gb")

    @property
    @pulumi.getter(name="vhdFormatType")
    def vhd_format_type(self) -> str:
        """
        Gets the disk vhd format type.
        """
        return pulumi.get(self, "vhd_format_type")

    @property
    @pulumi.getter(name="volumeType")
    def volume_type(self) -> str:
        """
        Gets or sets the disk volume type.
        """
        return pulumi.get(self, "volume_type")

    @property
    @pulumi.getter
    def bus(self) -> Optional[int]:
        """
        Gets or sets the disk bus.
        """
        return pulumi.get(self, "bus")

    @property
    @pulumi.getter(name="busType")
    def bus_type(self) -> Optional[str]:
        """
        Gets or sets the disk bus type.
        """
        return pulumi.get(self, "bus_type")

    @property
    @pulumi.getter(name="createDiffDisk")
    def create_diff_disk(self) -> Optional[str]:
        """
        Gets or sets a value indicating diff disk.
        """
        return pulumi.get(self, "create_diff_disk")

    @property
    @pulumi.getter(name="diskId")
    def disk_id(self) -> Optional[str]:
        """
        Gets or sets the disk id.
        """
        return pulumi.get(self, "disk_id")

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> Optional[int]:
        """
        Gets or sets the disk total size.
        """
        return pulumi.get(self, "disk_size_gb")

    @property
    @pulumi.getter
    def lun(self) -> Optional[int]:
        """
        Gets or sets the disk lun.
        """
        return pulumi.get(self, "lun")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the name of the disk.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="storageQoSPolicy")
    def storage_qo_s_policy(self) -> Optional['outputs.StorageQoSPolicyDetailsResponse']:
        """
        The QoS policy for the disk.
        """
        return pulumi.get(self, "storage_qo_s_policy")

    @property
    @pulumi.getter(name="templateDiskId")
    def template_disk_id(self) -> Optional[str]:
        """
        Gets or sets the disk id in the template.
        """
        return pulumi.get(self, "template_disk_id")

    @property
    @pulumi.getter(name="vhdType")
    def vhd_type(self) -> Optional[str]:
        """
        Gets or sets the disk vhd type.
        """
        return pulumi.get(self, "vhd_type")


@pulumi.output_type
class VirtualMachinePropertiesResponseAvailabilitySets(dict):
    """
    Availability Set model
    """
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 name: Optional[str] = None):
        """
        Availability Set model
        :param str id: Gets the ARM Id of the microsoft.scvmm/availabilitySets resource.
        :param str name: Gets or sets the name of the availability set.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Gets the ARM Id of the microsoft.scvmm/availabilitySets resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the name of the availability set.
        """
        return pulumi.get(self, "name")


