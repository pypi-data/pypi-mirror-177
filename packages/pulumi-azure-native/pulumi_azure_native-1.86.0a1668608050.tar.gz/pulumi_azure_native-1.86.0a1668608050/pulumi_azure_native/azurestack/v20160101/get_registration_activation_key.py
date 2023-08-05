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
    'GetRegistrationActivationKeyResult',
    'AwaitableGetRegistrationActivationKeyResult',
    'get_registration_activation_key',
    'get_registration_activation_key_output',
]

@pulumi.output_type
class GetRegistrationActivationKeyResult:
    """
    The resource containing the Azure Stack activation key.
    """
    def __init__(__self__, activation_key=None):
        if activation_key and not isinstance(activation_key, str):
            raise TypeError("Expected argument 'activation_key' to be a str")
        pulumi.set(__self__, "activation_key", activation_key)

    @property
    @pulumi.getter(name="activationKey")
    def activation_key(self) -> Optional[str]:
        """
        Azure Stack activation key.
        """
        return pulumi.get(self, "activation_key")


class AwaitableGetRegistrationActivationKeyResult(GetRegistrationActivationKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistrationActivationKeyResult(
            activation_key=self.activation_key)


def get_registration_activation_key(registration_name: Optional[str] = None,
                                    resource_group: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegistrationActivationKeyResult:
    """
    The resource containing the Azure Stack activation key.


    :param str registration_name: Name of the Azure Stack registration.
    :param str resource_group: Name of the resource group.
    """
    __args__ = dict()
    __args__['registrationName'] = registration_name
    __args__['resourceGroup'] = resource_group
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:azurestack/v20160101:getRegistrationActivationKey', __args__, opts=opts, typ=GetRegistrationActivationKeyResult).value

    return AwaitableGetRegistrationActivationKeyResult(
        activation_key=__ret__.activation_key)


@_utilities.lift_output_func(get_registration_activation_key)
def get_registration_activation_key_output(registration_name: Optional[pulumi.Input[str]] = None,
                                           resource_group: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegistrationActivationKeyResult]:
    """
    The resource containing the Azure Stack activation key.


    :param str registration_name: Name of the Azure Stack registration.
    :param str resource_group: Name of the resource group.
    """
    ...
