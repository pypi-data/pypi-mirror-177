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
    'GetConfigurationStoreResult',
    'AwaitableGetConfigurationStoreResult',
    'get_configuration_store',
    'get_configuration_store_output',
]

@pulumi.output_type
class GetConfigurationStoreResult:
    """
    The configuration store along with all resource properties. The Configuration Store will have all information to begin utilizing it.
    """
    def __init__(__self__, creation_date=None, disable_local_auth=None, enable_purge_protection=None, encryption=None, endpoint=None, id=None, identity=None, location=None, name=None, private_endpoint_connections=None, provisioning_state=None, public_network_access=None, sku=None, soft_delete_retention_in_days=None, system_data=None, tags=None, type=None):
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if disable_local_auth and not isinstance(disable_local_auth, bool):
            raise TypeError("Expected argument 'disable_local_auth' to be a bool")
        pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if enable_purge_protection and not isinstance(enable_purge_protection, bool):
            raise TypeError("Expected argument 'enable_purge_protection' to be a bool")
        pulumi.set(__self__, "enable_purge_protection", enable_purge_protection)
        if encryption and not isinstance(encryption, dict):
            raise TypeError("Expected argument 'encryption' to be a dict")
        pulumi.set(__self__, "encryption", encryption)
        if endpoint and not isinstance(endpoint, str):
            raise TypeError("Expected argument 'endpoint' to be a str")
        pulumi.set(__self__, "endpoint", endpoint)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if public_network_access and not isinstance(public_network_access, str):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, "public_network_access", public_network_access)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if soft_delete_retention_in_days and not isinstance(soft_delete_retention_in_days, int):
            raise TypeError("Expected argument 'soft_delete_retention_in_days' to be a int")
        pulumi.set(__self__, "soft_delete_retention_in_days", soft_delete_retention_in_days)
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
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        The creation date of configuration store.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[bool]:
        """
        Disables all authentication methods other than AAD authentication.
        """
        return pulumi.get(self, "disable_local_auth")

    @property
    @pulumi.getter(name="enablePurgeProtection")
    def enable_purge_protection(self) -> Optional[bool]:
        """
        Property specifying whether protection against purge is enabled for this configuration store.
        """
        return pulumi.get(self, "enable_purge_protection")

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.EncryptionPropertiesResponse']:
        """
        The encryption settings of the configuration store.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def endpoint(self) -> str:
        """
        The DNS endpoint where the configuration store API will be available.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ResourceIdentityResponse']:
        """
        The managed identity information, if configured.
        """
        return pulumi.get(self, "identity")

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
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionReferenceResponse']:
        """
        The list of private endpoint connections that are set up for this resource.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the configuration store.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[str]:
        """
        Control permission for data plane traffic coming from public networks while private endpoint is enabled.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The sku of the configuration store.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="softDeleteRetentionInDays")
    def soft_delete_retention_in_days(self) -> Optional[int]:
        """
        The amount of time in days that the configuration store will be retained when it is soft deleted.
        """
        return pulumi.get(self, "soft_delete_retention_in_days")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Resource system metadata.
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


class AwaitableGetConfigurationStoreResult(GetConfigurationStoreResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationStoreResult(
            creation_date=self.creation_date,
            disable_local_auth=self.disable_local_auth,
            enable_purge_protection=self.enable_purge_protection,
            encryption=self.encryption,
            endpoint=self.endpoint,
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            public_network_access=self.public_network_access,
            sku=self.sku,
            soft_delete_retention_in_days=self.soft_delete_retention_in_days,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_configuration_store(config_store_name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationStoreResult:
    """
    The configuration store along with all resource properties. The Configuration Store will have all information to begin utilizing it.


    :param str config_store_name: The name of the configuration store.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    __args__ = dict()
    __args__['configStoreName'] = config_store_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:appconfiguration/v20211001preview:getConfigurationStore', __args__, opts=opts, typ=GetConfigurationStoreResult).value

    return AwaitableGetConfigurationStoreResult(
        creation_date=__ret__.creation_date,
        disable_local_auth=__ret__.disable_local_auth,
        enable_purge_protection=__ret__.enable_purge_protection,
        encryption=__ret__.encryption,
        endpoint=__ret__.endpoint,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        public_network_access=__ret__.public_network_access,
        sku=__ret__.sku,
        soft_delete_retention_in_days=__ret__.soft_delete_retention_in_days,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_configuration_store)
def get_configuration_store_output(config_store_name: Optional[pulumi.Input[str]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConfigurationStoreResult]:
    """
    The configuration store along with all resource properties. The Configuration Store will have all information to begin utilizing it.


    :param str config_store_name: The name of the configuration store.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    ...
