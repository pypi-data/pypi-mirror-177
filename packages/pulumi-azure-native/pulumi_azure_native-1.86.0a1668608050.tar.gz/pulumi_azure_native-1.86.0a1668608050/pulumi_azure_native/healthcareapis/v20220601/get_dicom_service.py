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
    'GetDicomServiceResult',
    'AwaitableGetDicomServiceResult',
    'get_dicom_service',
    'get_dicom_service_output',
]

@pulumi.output_type
class GetDicomServiceResult:
    """
    The description of Dicom Service
    """
    def __init__(__self__, authentication_configuration=None, cors_configuration=None, etag=None, id=None, identity=None, location=None, name=None, private_endpoint_connections=None, provisioning_state=None, public_network_access=None, service_url=None, system_data=None, tags=None, type=None):
        if authentication_configuration and not isinstance(authentication_configuration, dict):
            raise TypeError("Expected argument 'authentication_configuration' to be a dict")
        pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if cors_configuration and not isinstance(cors_configuration, dict):
            raise TypeError("Expected argument 'cors_configuration' to be a dict")
        pulumi.set(__self__, "cors_configuration", cors_configuration)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
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
        if service_url and not isinstance(service_url, str):
            raise TypeError("Expected argument 'service_url' to be a str")
        pulumi.set(__self__, "service_url", service_url)
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
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional['outputs.DicomServiceAuthenticationConfigurationResponse']:
        """
        Dicom Service authentication configuration.
        """
        return pulumi.get(self, "authentication_configuration")

    @property
    @pulumi.getter(name="corsConfiguration")
    def cors_configuration(self) -> Optional['outputs.CorsConfigurationResponse']:
        """
        Dicom Service Cors configuration.
        """
        return pulumi.get(self, "cors_configuration")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        An etag associated with the resource, used for optimistic concurrency when editing it.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ServiceManagedIdentityResponseIdentity']:
        """
        Setting indicating whether the service has a managed identity associated with it.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        """
        The list of private endpoint connections that are set up for this resource.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> str:
        """
        Control permission for data plane traffic coming from public networks while private endpoint is enabled.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="serviceUrl")
    def service_url(self) -> str:
        """
        The url of the Dicom Services.
        """
        return pulumi.get(self, "service_url")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
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
        The resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetDicomServiceResult(GetDicomServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDicomServiceResult(
            authentication_configuration=self.authentication_configuration,
            cors_configuration=self.cors_configuration,
            etag=self.etag,
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            public_network_access=self.public_network_access,
            service_url=self.service_url,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_dicom_service(dicom_service_name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      workspace_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDicomServiceResult:
    """
    The description of Dicom Service


    :param str dicom_service_name: The name of DICOM Service resource.
    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str workspace_name: The name of workspace resource.
    """
    __args__ = dict()
    __args__['dicomServiceName'] = dicom_service_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:healthcareapis/v20220601:getDicomService', __args__, opts=opts, typ=GetDicomServiceResult).value

    return AwaitableGetDicomServiceResult(
        authentication_configuration=__ret__.authentication_configuration,
        cors_configuration=__ret__.cors_configuration,
        etag=__ret__.etag,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        public_network_access=__ret__.public_network_access,
        service_url=__ret__.service_url,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_dicom_service)
def get_dicom_service_output(dicom_service_name: Optional[pulumi.Input[str]] = None,
                             resource_group_name: Optional[pulumi.Input[str]] = None,
                             workspace_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDicomServiceResult]:
    """
    The description of Dicom Service


    :param str dicom_service_name: The name of DICOM Service resource.
    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str workspace_name: The name of workspace resource.
    """
    ...
