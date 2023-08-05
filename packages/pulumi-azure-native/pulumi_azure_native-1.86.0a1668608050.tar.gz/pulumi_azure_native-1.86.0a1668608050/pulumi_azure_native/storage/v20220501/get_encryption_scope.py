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
    'GetEncryptionScopeResult',
    'AwaitableGetEncryptionScopeResult',
    'get_encryption_scope',
    'get_encryption_scope_output',
]

@pulumi.output_type
class GetEncryptionScopeResult:
    """
    The Encryption Scope resource.
    """
    def __init__(__self__, creation_time=None, id=None, key_vault_properties=None, last_modified_time=None, name=None, require_infrastructure_encryption=None, source=None, state=None, type=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key_vault_properties and not isinstance(key_vault_properties, dict):
            raise TypeError("Expected argument 'key_vault_properties' to be a dict")
        pulumi.set(__self__, "key_vault_properties", key_vault_properties)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if require_infrastructure_encryption and not isinstance(require_infrastructure_encryption, bool):
            raise TypeError("Expected argument 'require_infrastructure_encryption' to be a bool")
        pulumi.set(__self__, "require_infrastructure_encryption", require_infrastructure_encryption)
        if source and not isinstance(source, str):
            raise TypeError("Expected argument 'source' to be a str")
        pulumi.set(__self__, "source", source)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Gets the creation date and time of the encryption scope in UTC.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional['outputs.EncryptionScopeKeyVaultPropertiesResponse']:
        """
        The key vault properties for the encryption scope. This is a required field if encryption scope 'source' attribute is set to 'Microsoft.KeyVault'.
        """
        return pulumi.get(self, "key_vault_properties")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> str:
        """
        Gets the last modification date and time of the encryption scope in UTC.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requireInfrastructureEncryption")
    def require_infrastructure_encryption(self) -> Optional[bool]:
        """
        A boolean indicating whether or not the service applies a secondary layer of encryption with platform managed keys for data at rest.
        """
        return pulumi.get(self, "require_infrastructure_encryption")

    @property
    @pulumi.getter
    def source(self) -> Optional[str]:
        """
        The provider for the encryption scope. Possible values (case-insensitive):  Microsoft.Storage, Microsoft.KeyVault.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the encryption scope. Possible values (case-insensitive):  Enabled, Disabled.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetEncryptionScopeResult(GetEncryptionScopeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEncryptionScopeResult(
            creation_time=self.creation_time,
            id=self.id,
            key_vault_properties=self.key_vault_properties,
            last_modified_time=self.last_modified_time,
            name=self.name,
            require_infrastructure_encryption=self.require_infrastructure_encryption,
            source=self.source,
            state=self.state,
            type=self.type)


def get_encryption_scope(account_name: Optional[str] = None,
                         encryption_scope_name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEncryptionScopeResult:
    """
    The Encryption Scope resource.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str encryption_scope_name: The name of the encryption scope within the specified storage account. Encryption scope names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['encryptionScopeName'] = encryption_scope_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:storage/v20220501:getEncryptionScope', __args__, opts=opts, typ=GetEncryptionScopeResult).value

    return AwaitableGetEncryptionScopeResult(
        creation_time=__ret__.creation_time,
        id=__ret__.id,
        key_vault_properties=__ret__.key_vault_properties,
        last_modified_time=__ret__.last_modified_time,
        name=__ret__.name,
        require_infrastructure_encryption=__ret__.require_infrastructure_encryption,
        source=__ret__.source,
        state=__ret__.state,
        type=__ret__.type)


@_utilities.lift_output_func(get_encryption_scope)
def get_encryption_scope_output(account_name: Optional[pulumi.Input[str]] = None,
                                encryption_scope_name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEncryptionScopeResult]:
    """
    The Encryption Scope resource.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str encryption_scope_name: The name of the encryption scope within the specified storage account. Encryption scope names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    ...
