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
    'CreateFirewallRuleWithAccountParametersArgs',
    'CreateTrustedIdProviderWithAccountParametersArgs',
    'CreateVirtualNetworkRuleWithAccountParametersArgs',
    'EncryptionConfigArgs',
    'EncryptionIdentityArgs',
    'KeyVaultMetaInfoArgs',
]

@pulumi.input_type
class CreateFirewallRuleWithAccountParametersArgs:
    def __init__(__self__, *,
                 end_ip_address: pulumi.Input[str],
                 name: pulumi.Input[str],
                 start_ip_address: pulumi.Input[str]):
        """
        The parameters used to create a new firewall rule while creating a new Data Lake Store account.
        :param pulumi.Input[str] end_ip_address: The end IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        :param pulumi.Input[str] name: The unique name of the firewall rule to create.
        :param pulumi.Input[str] start_ip_address: The start IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        """
        pulumi.set(__self__, "end_ip_address", end_ip_address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "start_ip_address", start_ip_address)

    @property
    @pulumi.getter(name="endIpAddress")
    def end_ip_address(self) -> pulumi.Input[str]:
        """
        The end IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        """
        return pulumi.get(self, "end_ip_address")

    @end_ip_address.setter
    def end_ip_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "end_ip_address", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the firewall rule to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="startIpAddress")
    def start_ip_address(self) -> pulumi.Input[str]:
        """
        The start IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        """
        return pulumi.get(self, "start_ip_address")

    @start_ip_address.setter
    def start_ip_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "start_ip_address", value)


@pulumi.input_type
class CreateTrustedIdProviderWithAccountParametersArgs:
    def __init__(__self__, *,
                 id_provider: pulumi.Input[str],
                 name: pulumi.Input[str]):
        """
        The parameters used to create a new trusted identity provider while creating a new Data Lake Store account.
        :param pulumi.Input[str] id_provider: The URL of this trusted identity provider.
        :param pulumi.Input[str] name: The unique name of the trusted identity provider to create.
        """
        pulumi.set(__self__, "id_provider", id_provider)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="idProvider")
    def id_provider(self) -> pulumi.Input[str]:
        """
        The URL of this trusted identity provider.
        """
        return pulumi.get(self, "id_provider")

    @id_provider.setter
    def id_provider(self, value: pulumi.Input[str]):
        pulumi.set(self, "id_provider", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the trusted identity provider to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class CreateVirtualNetworkRuleWithAccountParametersArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 subnet_id: pulumi.Input[str]):
        """
        The parameters used to create a new virtual network rule while creating a new Data Lake Store account.
        :param pulumi.Input[str] name: The unique name of the virtual network rule to create.
        :param pulumi.Input[str] subnet_id: The resource identifier for the subnet.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the virtual network rule to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The resource identifier for the subnet.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)


@pulumi.input_type
class EncryptionConfigArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['EncryptionConfigType'],
                 key_vault_meta_info: Optional[pulumi.Input['KeyVaultMetaInfoArgs']] = None):
        """
        The encryption configuration for the account.
        :param pulumi.Input['EncryptionConfigType'] type: The type of encryption configuration being used. Currently the only supported types are 'UserManaged' and 'ServiceManaged'.
        :param pulumi.Input['KeyVaultMetaInfoArgs'] key_vault_meta_info: The Key Vault information for connecting to user managed encryption keys.
        """
        pulumi.set(__self__, "type", type)
        if key_vault_meta_info is not None:
            pulumi.set(__self__, "key_vault_meta_info", key_vault_meta_info)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['EncryptionConfigType']:
        """
        The type of encryption configuration being used. Currently the only supported types are 'UserManaged' and 'ServiceManaged'.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['EncryptionConfigType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="keyVaultMetaInfo")
    def key_vault_meta_info(self) -> Optional[pulumi.Input['KeyVaultMetaInfoArgs']]:
        """
        The Key Vault information for connecting to user managed encryption keys.
        """
        return pulumi.get(self, "key_vault_meta_info")

    @key_vault_meta_info.setter
    def key_vault_meta_info(self, value: Optional[pulumi.Input['KeyVaultMetaInfoArgs']]):
        pulumi.set(self, "key_vault_meta_info", value)


@pulumi.input_type
class EncryptionIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['EncryptionIdentityType']):
        """
        The encryption identity properties.
        :param pulumi.Input['EncryptionIdentityType'] type: The type of encryption being used. Currently the only supported type is 'SystemAssigned'.
        """
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['EncryptionIdentityType']:
        """
        The type of encryption being used. Currently the only supported type is 'SystemAssigned'.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['EncryptionIdentityType']):
        pulumi.set(self, "type", value)


@pulumi.input_type
class KeyVaultMetaInfoArgs:
    def __init__(__self__, *,
                 encryption_key_name: pulumi.Input[str],
                 encryption_key_version: pulumi.Input[str],
                 key_vault_resource_id: pulumi.Input[str]):
        """
        Metadata information used by account encryption.
        :param pulumi.Input[str] encryption_key_name: The name of the user managed encryption key.
        :param pulumi.Input[str] encryption_key_version: The version of the user managed encryption key.
        :param pulumi.Input[str] key_vault_resource_id: The resource identifier for the user managed Key Vault being used to encrypt.
        """
        pulumi.set(__self__, "encryption_key_name", encryption_key_name)
        pulumi.set(__self__, "encryption_key_version", encryption_key_version)
        pulumi.set(__self__, "key_vault_resource_id", key_vault_resource_id)

    @property
    @pulumi.getter(name="encryptionKeyName")
    def encryption_key_name(self) -> pulumi.Input[str]:
        """
        The name of the user managed encryption key.
        """
        return pulumi.get(self, "encryption_key_name")

    @encryption_key_name.setter
    def encryption_key_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "encryption_key_name", value)

    @property
    @pulumi.getter(name="encryptionKeyVersion")
    def encryption_key_version(self) -> pulumi.Input[str]:
        """
        The version of the user managed encryption key.
        """
        return pulumi.get(self, "encryption_key_version")

    @encryption_key_version.setter
    def encryption_key_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "encryption_key_version", value)

    @property
    @pulumi.getter(name="keyVaultResourceId")
    def key_vault_resource_id(self) -> pulumi.Input[str]:
        """
        The resource identifier for the user managed Key Vault being used to encrypt.
        """
        return pulumi.get(self, "key_vault_resource_id")

    @key_vault_resource_id.setter
    def key_vault_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_vault_resource_id", value)


