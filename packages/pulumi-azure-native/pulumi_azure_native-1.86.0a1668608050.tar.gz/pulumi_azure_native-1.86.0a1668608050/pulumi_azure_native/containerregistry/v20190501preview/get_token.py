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
    'GetTokenResult',
    'AwaitableGetTokenResult',
    'get_token',
    'get_token_output',
]

@pulumi.output_type
class GetTokenResult:
    """
    An object that represents a token for a container registry.
    """
    def __init__(__self__, creation_date=None, credentials=None, id=None, name=None, provisioning_state=None, scope_map_id=None, status=None, system_data=None, type=None):
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if credentials and not isinstance(credentials, dict):
            raise TypeError("Expected argument 'credentials' to be a dict")
        pulumi.set(__self__, "credentials", credentials)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if scope_map_id and not isinstance(scope_map_id, str):
            raise TypeError("Expected argument 'scope_map_id' to be a str")
        pulumi.set(__self__, "scope_map_id", scope_map_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        The creation date of scope map.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def credentials(self) -> Optional['outputs.TokenCredentialsPropertiesResponse']:
        """
        The credentials that can be used for authenticating the token.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="scopeMapId")
    def scope_map_id(self) -> Optional[str]:
        """
        The resource ID of the scope map to which the token will be associated with.
        """
        return pulumi.get(self, "scope_map_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the token example enabled or disabled.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetTokenResult(GetTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTokenResult(
            creation_date=self.creation_date,
            credentials=self.credentials,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            scope_map_id=self.scope_map_id,
            status=self.status,
            system_data=self.system_data,
            type=self.type)


def get_token(registry_name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              token_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTokenResult:
    """
    An object that represents a token for a container registry.


    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    :param str token_name: The name of the token.
    """
    __args__ = dict()
    __args__['registryName'] = registry_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tokenName'] = token_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:containerregistry/v20190501preview:getToken', __args__, opts=opts, typ=GetTokenResult).value

    return AwaitableGetTokenResult(
        creation_date=__ret__.creation_date,
        credentials=__ret__.credentials,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        scope_map_id=__ret__.scope_map_id,
        status=__ret__.status,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_token)
def get_token_output(registry_name: Optional[pulumi.Input[str]] = None,
                     resource_group_name: Optional[pulumi.Input[str]] = None,
                     token_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTokenResult]:
    """
    An object that represents a token for a container registry.


    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    :param str token_name: The name of the token.
    """
    ...
