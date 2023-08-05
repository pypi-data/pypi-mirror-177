# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AddressSpaceArgs',
    'EncryptionArgs',
    'IdentityDataArgs',
    'PrivateEndpointConnectionPropertiesArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'SkuArgs',
    'VirtualNetworkPeeringPropertiesFormatDatabricksVirtualNetworkArgs',
    'VirtualNetworkPeeringPropertiesFormatRemoteVirtualNetworkArgs',
    'WorkspaceCustomBooleanParameterArgs',
    'WorkspaceCustomParametersArgs',
    'WorkspaceCustomStringParameterArgs',
    'WorkspaceEncryptionParameterArgs',
    'WorkspaceProviderAuthorizationArgs',
]

@pulumi.input_type
class AddressSpaceArgs:
    def __init__(__self__, *,
                 address_prefixes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        AddressSpace contains an array of IP address ranges that can be used by subnets of the virtual network.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] address_prefixes: A list of address blocks reserved for this virtual network in CIDR notation.
        """
        if address_prefixes is not None:
            pulumi.set(__self__, "address_prefixes", address_prefixes)

    @property
    @pulumi.getter(name="addressPrefixes")
    def address_prefixes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of address blocks reserved for this virtual network in CIDR notation.
        """
        return pulumi.get(self, "address_prefixes")

    @address_prefixes.setter
    def address_prefixes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "address_prefixes", value)


@pulumi.input_type
class EncryptionArgs:
    def __init__(__self__, *,
                 key_name: Optional[pulumi.Input[str]] = None,
                 key_source: Optional[pulumi.Input[Union[str, 'KeySource']]] = None,
                 key_vault_uri: Optional[pulumi.Input[str]] = None,
                 key_version: Optional[pulumi.Input[str]] = None):
        """
        The object that contains details of encryption used on the workspace.
        :param pulumi.Input[str] key_name: The name of KeyVault key.
        :param pulumi.Input[Union[str, 'KeySource']] key_source: The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault
        :param pulumi.Input[str] key_vault_uri: The Uri of KeyVault.
        :param pulumi.Input[str] key_version: The version of KeyVault key.
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_source is None:
            key_source = 'Default'
        if key_source is not None:
            pulumi.set(__self__, "key_source", key_source)
        if key_vault_uri is not None:
            pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of KeyVault key.
        """
        return pulumi.get(self, "key_name")

    @key_name.setter
    def key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_name", value)

    @property
    @pulumi.getter(name="keySource")
    def key_source(self) -> Optional[pulumi.Input[Union[str, 'KeySource']]]:
        """
        The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault
        """
        return pulumi.get(self, "key_source")

    @key_source.setter
    def key_source(self, value: Optional[pulumi.Input[Union[str, 'KeySource']]]):
        pulumi.set(self, "key_source", value)

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The Uri of KeyVault.
        """
        return pulumi.get(self, "key_vault_uri")

    @key_vault_uri.setter
    def key_vault_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_uri", value)

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of KeyVault key.
        """
        return pulumi.get(self, "key_version")

    @key_version.setter
    def key_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_version", value)


@pulumi.input_type
class IdentityDataArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[Union[str, 'IdentityType']]):
        """
        Identity for the resource.
        :param pulumi.Input[Union[str, 'IdentityType']] type: The identity type.
        """
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'IdentityType']]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'IdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class PrivateEndpointConnectionPropertiesArgs:
    def __init__(__self__, *,
                 private_link_service_connection_state: pulumi.Input['PrivateLinkServiceConnectionStateArgs']):
        """
        The properties of a private endpoint connection
        :param pulumi.Input['PrivateLinkServiceConnectionStateArgs'] private_link_service_connection_state: Private endpoint connection state
        """
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> pulumi.Input['PrivateLinkServiceConnectionStateArgs']:
        """
        Private endpoint connection state
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: pulumi.Input['PrivateLinkServiceConnectionStateArgs']):
        pulumi.set(self, "private_link_service_connection_state", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 status: pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']],
                 action_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None):
        """
        The current state of a private endpoint connection
        :param pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']] status: The status of a private endpoint connection
        :param pulumi.Input[str] action_required: Actions required for a private endpoint connection
        :param pulumi.Input[str] description: The description for the current state of a private endpoint connection
        """
        pulumi.set(__self__, "status", status)
        if action_required is not None:
            pulumi.set(__self__, "action_required", action_required)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']]:
        """
        The status of a private endpoint connection
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="actionRequired")
    def action_required(self) -> Optional[pulumi.Input[str]]:
        """
        Actions required for a private endpoint connection
        """
        return pulumi.get(self, "action_required")

    @action_required.setter
    def action_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for the current state of a private endpoint connection
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 tier: Optional[pulumi.Input[str]] = None):
        """
        SKU for the resource.
        :param pulumi.Input[str] name: The SKU name.
        :param pulumi.Input[str] tier: The SKU tier.
        """
        pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The SKU name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU tier.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class VirtualNetworkPeeringPropertiesFormatDatabricksVirtualNetworkArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None):
        """
         The remote virtual network should be in the same region. See here to learn more (https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering).
        :param pulumi.Input[str] id: The Id of the databricks virtual network.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of the databricks virtual network.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class VirtualNetworkPeeringPropertiesFormatRemoteVirtualNetworkArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None):
        """
         The remote virtual network should be in the same region. See here to learn more (https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering).
        :param pulumi.Input[str] id: The Id of the remote virtual network.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of the remote virtual network.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class WorkspaceCustomBooleanParameterArgs:
    def __init__(__self__, *,
                 value: pulumi.Input[bool]):
        """
        The value which should be used for this field.
        :param pulumi.Input[bool] value: The value which should be used for this field.
        """
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[bool]:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[bool]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class WorkspaceCustomParametersArgs:
    def __init__(__self__, *,
                 aml_workspace_id: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 custom_private_subnet_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 custom_public_subnet_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 custom_virtual_network_id: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 enable_no_public_ip: Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']] = None,
                 encryption: Optional[pulumi.Input['WorkspaceEncryptionParameterArgs']] = None,
                 load_balancer_backend_pool_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 load_balancer_id: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 nat_gateway_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 prepare_encryption: Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']] = None,
                 public_ip_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 require_infrastructure_encryption: Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']] = None,
                 storage_account_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 storage_account_sku_name: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None,
                 vnet_address_prefix: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']] = None):
        """
        Custom Parameters used for Cluster Creation.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] aml_workspace_id: The ID of a Azure Machine Learning workspace to link with Databricks workspace
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] custom_private_subnet_name: The name of the Private Subnet within the Virtual Network
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] custom_public_subnet_name: The name of a Public Subnet within the Virtual Network
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] custom_virtual_network_id: The ID of a Virtual Network where this Databricks Cluster should be created
        :param pulumi.Input['WorkspaceCustomBooleanParameterArgs'] enable_no_public_ip: Should the Public IP be Disabled?
        :param pulumi.Input['WorkspaceEncryptionParameterArgs'] encryption: Contains the encryption details for Customer-Managed Key (CMK) enabled workspace.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] load_balancer_backend_pool_name: Name of the outbound Load Balancer Backend Pool for Secure Cluster Connectivity (No Public IP).
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] load_balancer_id: Resource URI of Outbound Load balancer for Secure Cluster Connectivity (No Public IP) workspace.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] nat_gateway_name: Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets.
        :param pulumi.Input['WorkspaceCustomBooleanParameterArgs'] prepare_encryption: Prepare the workspace for encryption. Enables the Managed Identity for managed storage account.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] public_ip_name: Name of the Public IP for No Public IP workspace with managed vNet.
        :param pulumi.Input['WorkspaceCustomBooleanParameterArgs'] require_infrastructure_encryption: A boolean indicating whether or not the DBFS root file system will be enabled with secondary layer of encryption with platform managed keys for data at rest.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] storage_account_name: Default DBFS storage account name.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] storage_account_sku_name: Storage account SKU name, ex: Standard_GRS, Standard_LRS. Refer https://aka.ms/storageskus for valid inputs.
        :param pulumi.Input['WorkspaceCustomStringParameterArgs'] vnet_address_prefix: Address prefix for Managed virtual network. Default value for this input is 10.139.
        """
        if aml_workspace_id is not None:
            pulumi.set(__self__, "aml_workspace_id", aml_workspace_id)
        if custom_private_subnet_name is not None:
            pulumi.set(__self__, "custom_private_subnet_name", custom_private_subnet_name)
        if custom_public_subnet_name is not None:
            pulumi.set(__self__, "custom_public_subnet_name", custom_public_subnet_name)
        if custom_virtual_network_id is not None:
            pulumi.set(__self__, "custom_virtual_network_id", custom_virtual_network_id)
        if enable_no_public_ip is not None:
            pulumi.set(__self__, "enable_no_public_ip", enable_no_public_ip)
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)
        if load_balancer_backend_pool_name is not None:
            pulumi.set(__self__, "load_balancer_backend_pool_name", load_balancer_backend_pool_name)
        if load_balancer_id is not None:
            pulumi.set(__self__, "load_balancer_id", load_balancer_id)
        if nat_gateway_name is not None:
            pulumi.set(__self__, "nat_gateway_name", nat_gateway_name)
        if prepare_encryption is not None:
            pulumi.set(__self__, "prepare_encryption", prepare_encryption)
        if public_ip_name is not None:
            pulumi.set(__self__, "public_ip_name", public_ip_name)
        if require_infrastructure_encryption is not None:
            pulumi.set(__self__, "require_infrastructure_encryption", require_infrastructure_encryption)
        if storage_account_name is not None:
            pulumi.set(__self__, "storage_account_name", storage_account_name)
        if storage_account_sku_name is not None:
            pulumi.set(__self__, "storage_account_sku_name", storage_account_sku_name)
        if vnet_address_prefix is not None:
            pulumi.set(__self__, "vnet_address_prefix", vnet_address_prefix)

    @property
    @pulumi.getter(name="amlWorkspaceId")
    def aml_workspace_id(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        The ID of a Azure Machine Learning workspace to link with Databricks workspace
        """
        return pulumi.get(self, "aml_workspace_id")

    @aml_workspace_id.setter
    def aml_workspace_id(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "aml_workspace_id", value)

    @property
    @pulumi.getter(name="customPrivateSubnetName")
    def custom_private_subnet_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        The name of the Private Subnet within the Virtual Network
        """
        return pulumi.get(self, "custom_private_subnet_name")

    @custom_private_subnet_name.setter
    def custom_private_subnet_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "custom_private_subnet_name", value)

    @property
    @pulumi.getter(name="customPublicSubnetName")
    def custom_public_subnet_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        The name of a Public Subnet within the Virtual Network
        """
        return pulumi.get(self, "custom_public_subnet_name")

    @custom_public_subnet_name.setter
    def custom_public_subnet_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "custom_public_subnet_name", value)

    @property
    @pulumi.getter(name="customVirtualNetworkId")
    def custom_virtual_network_id(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        The ID of a Virtual Network where this Databricks Cluster should be created
        """
        return pulumi.get(self, "custom_virtual_network_id")

    @custom_virtual_network_id.setter
    def custom_virtual_network_id(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "custom_virtual_network_id", value)

    @property
    @pulumi.getter(name="enableNoPublicIp")
    def enable_no_public_ip(self) -> Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']]:
        """
        Should the Public IP be Disabled?
        """
        return pulumi.get(self, "enable_no_public_ip")

    @enable_no_public_ip.setter
    def enable_no_public_ip(self, value: Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']]):
        pulumi.set(self, "enable_no_public_ip", value)

    @property
    @pulumi.getter
    def encryption(self) -> Optional[pulumi.Input['WorkspaceEncryptionParameterArgs']]:
        """
        Contains the encryption details for Customer-Managed Key (CMK) enabled workspace.
        """
        return pulumi.get(self, "encryption")

    @encryption.setter
    def encryption(self, value: Optional[pulumi.Input['WorkspaceEncryptionParameterArgs']]):
        pulumi.set(self, "encryption", value)

    @property
    @pulumi.getter(name="loadBalancerBackendPoolName")
    def load_balancer_backend_pool_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Name of the outbound Load Balancer Backend Pool for Secure Cluster Connectivity (No Public IP).
        """
        return pulumi.get(self, "load_balancer_backend_pool_name")

    @load_balancer_backend_pool_name.setter
    def load_balancer_backend_pool_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "load_balancer_backend_pool_name", value)

    @property
    @pulumi.getter(name="loadBalancerId")
    def load_balancer_id(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Resource URI of Outbound Load balancer for Secure Cluster Connectivity (No Public IP) workspace.
        """
        return pulumi.get(self, "load_balancer_id")

    @load_balancer_id.setter
    def load_balancer_id(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "load_balancer_id", value)

    @property
    @pulumi.getter(name="natGatewayName")
    def nat_gateway_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets.
        """
        return pulumi.get(self, "nat_gateway_name")

    @nat_gateway_name.setter
    def nat_gateway_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "nat_gateway_name", value)

    @property
    @pulumi.getter(name="prepareEncryption")
    def prepare_encryption(self) -> Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']]:
        """
        Prepare the workspace for encryption. Enables the Managed Identity for managed storage account.
        """
        return pulumi.get(self, "prepare_encryption")

    @prepare_encryption.setter
    def prepare_encryption(self, value: Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']]):
        pulumi.set(self, "prepare_encryption", value)

    @property
    @pulumi.getter(name="publicIpName")
    def public_ip_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Name of the Public IP for No Public IP workspace with managed vNet.
        """
        return pulumi.get(self, "public_ip_name")

    @public_ip_name.setter
    def public_ip_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "public_ip_name", value)

    @property
    @pulumi.getter(name="requireInfrastructureEncryption")
    def require_infrastructure_encryption(self) -> Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']]:
        """
        A boolean indicating whether or not the DBFS root file system will be enabled with secondary layer of encryption with platform managed keys for data at rest.
        """
        return pulumi.get(self, "require_infrastructure_encryption")

    @require_infrastructure_encryption.setter
    def require_infrastructure_encryption(self, value: Optional[pulumi.Input['WorkspaceCustomBooleanParameterArgs']]):
        pulumi.set(self, "require_infrastructure_encryption", value)

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Default DBFS storage account name.
        """
        return pulumi.get(self, "storage_account_name")

    @storage_account_name.setter
    def storage_account_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "storage_account_name", value)

    @property
    @pulumi.getter(name="storageAccountSkuName")
    def storage_account_sku_name(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Storage account SKU name, ex: Standard_GRS, Standard_LRS. Refer https://aka.ms/storageskus for valid inputs.
        """
        return pulumi.get(self, "storage_account_sku_name")

    @storage_account_sku_name.setter
    def storage_account_sku_name(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "storage_account_sku_name", value)

    @property
    @pulumi.getter(name="vnetAddressPrefix")
    def vnet_address_prefix(self) -> Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]:
        """
        Address prefix for Managed virtual network. Default value for this input is 10.139.
        """
        return pulumi.get(self, "vnet_address_prefix")

    @vnet_address_prefix.setter
    def vnet_address_prefix(self, value: Optional[pulumi.Input['WorkspaceCustomStringParameterArgs']]):
        pulumi.set(self, "vnet_address_prefix", value)


@pulumi.input_type
class WorkspaceCustomStringParameterArgs:
    def __init__(__self__, *,
                 value: pulumi.Input[str]):
        """
        The Value.
        :param pulumi.Input[str] value: The value which should be used for this field.
        """
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class WorkspaceEncryptionParameterArgs:
    def __init__(__self__, *,
                 value: Optional[pulumi.Input['EncryptionArgs']] = None):
        """
        The object that contains details of encryption used on the workspace.
        :param pulumi.Input['EncryptionArgs'] value: The value which should be used for this field.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input['EncryptionArgs']]:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input['EncryptionArgs']]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class WorkspaceProviderAuthorizationArgs:
    def __init__(__self__, *,
                 principal_id: pulumi.Input[str],
                 role_definition_id: pulumi.Input[str]):
        """
        The workspace provider authorization.
        :param pulumi.Input[str] principal_id: The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources.
        :param pulumi.Input[str] role_definition_id: The provider's role definition identifier. This role will define all the permissions that the provider must have on the workspace's container resource group. This role definition cannot have permission to delete the resource group.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> pulumi.Input[str]:
        """
        The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> pulumi.Input[str]:
        """
        The provider's role definition identifier. This role will define all the permissions that the provider must have on the workspace's container resource group. This role definition cannot have permission to delete the resource group.
        """
        return pulumi.get(self, "role_definition_id")

    @role_definition_id.setter
    def role_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_definition_id", value)


