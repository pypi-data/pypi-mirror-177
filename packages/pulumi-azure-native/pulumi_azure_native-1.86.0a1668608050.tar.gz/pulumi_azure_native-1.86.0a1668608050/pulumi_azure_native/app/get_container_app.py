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

__all__ = [
    'GetContainerAppResult',
    'AwaitableGetContainerAppResult',
    'get_container_app',
    'get_container_app_output',
]

@pulumi.output_type
class GetContainerAppResult:
    """
    Container App.
    """
    def __init__(__self__, configuration=None, custom_domain_verification_id=None, id=None, identity=None, latest_revision_fqdn=None, latest_revision_name=None, location=None, managed_environment_id=None, name=None, outbound_ip_addresses=None, provisioning_state=None, system_data=None, tags=None, template=None, type=None):
        if configuration and not isinstance(configuration, dict):
            raise TypeError("Expected argument 'configuration' to be a dict")
        pulumi.set(__self__, "configuration", configuration)
        if custom_domain_verification_id and not isinstance(custom_domain_verification_id, str):
            raise TypeError("Expected argument 'custom_domain_verification_id' to be a str")
        pulumi.set(__self__, "custom_domain_verification_id", custom_domain_verification_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if latest_revision_fqdn and not isinstance(latest_revision_fqdn, str):
            raise TypeError("Expected argument 'latest_revision_fqdn' to be a str")
        pulumi.set(__self__, "latest_revision_fqdn", latest_revision_fqdn)
        if latest_revision_name and not isinstance(latest_revision_name, str):
            raise TypeError("Expected argument 'latest_revision_name' to be a str")
        pulumi.set(__self__, "latest_revision_name", latest_revision_name)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_environment_id and not isinstance(managed_environment_id, str):
            raise TypeError("Expected argument 'managed_environment_id' to be a str")
        pulumi.set(__self__, "managed_environment_id", managed_environment_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if outbound_ip_addresses and not isinstance(outbound_ip_addresses, list):
            raise TypeError("Expected argument 'outbound_ip_addresses' to be a list")
        pulumi.set(__self__, "outbound_ip_addresses", outbound_ip_addresses)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if template and not isinstance(template, dict):
            raise TypeError("Expected argument 'template' to be a dict")
        pulumi.set(__self__, "template", template)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def configuration(self) -> Optional['outputs.ConfigurationResponse']:
        """
        Non versioned Container App configuration properties.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter(name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> str:
        """
        Id used to verify domain name ownership
        """
        return pulumi.get(self, "custom_domain_verification_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ManagedServiceIdentityResponse']:
        """
        managed identities for the Container App to interact with other Azure services without maintaining any secrets or credentials in code.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="latestRevisionFqdn")
    def latest_revision_fqdn(self) -> str:
        """
        Fully Qualified Domain Name of the latest revision of the Container App.
        """
        return pulumi.get(self, "latest_revision_fqdn")

    @property
    @pulumi.getter(name="latestRevisionName")
    def latest_revision_name(self) -> str:
        """
        Name of the latest revision of the Container App.
        """
        return pulumi.get(self, "latest_revision_name")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedEnvironmentId")
    def managed_environment_id(self) -> Optional[str]:
        """
        Resource ID of the Container App's environment.
        """
        return pulumi.get(self, "managed_environment_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> Sequence[str]:
        """
        Outbound IP Addresses for container app.
        """
        return pulumi.get(self, "outbound_ip_addresses")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Container App.
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
    def template(self) -> Optional['outputs.TemplateResponse']:
        """
        Container App versioned application definition.
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetContainerAppResult(GetContainerAppResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetContainerAppResult(
            configuration=self.configuration,
            custom_domain_verification_id=self.custom_domain_verification_id,
            id=self.id,
            identity=self.identity,
            latest_revision_fqdn=self.latest_revision_fqdn,
            latest_revision_name=self.latest_revision_name,
            location=self.location,
            managed_environment_id=self.managed_environment_id,
            name=self.name,
            outbound_ip_addresses=self.outbound_ip_addresses,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            template=self.template,
            type=self.type)


def get_container_app(container_app_name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetContainerAppResult:
    """
    Container App.
    API Version: 2022-03-01.


    :param str container_app_name: Name of the Container App.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['containerAppName'] = container_app_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:app:getContainerApp', __args__, opts=opts, typ=GetContainerAppResult).value

    return AwaitableGetContainerAppResult(
        configuration=__ret__.configuration,
        custom_domain_verification_id=__ret__.custom_domain_verification_id,
        id=__ret__.id,
        identity=__ret__.identity,
        latest_revision_fqdn=__ret__.latest_revision_fqdn,
        latest_revision_name=__ret__.latest_revision_name,
        location=__ret__.location,
        managed_environment_id=__ret__.managed_environment_id,
        name=__ret__.name,
        outbound_ip_addresses=__ret__.outbound_ip_addresses,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        template=__ret__.template,
        type=__ret__.type)


@_utilities.lift_output_func(get_container_app)
def get_container_app_output(container_app_name: Optional[pulumi.Input[str]] = None,
                             resource_group_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetContainerAppResult]:
    """
    Container App.
    API Version: 2022-03-01.


    :param str container_app_name: Name of the Container App.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
