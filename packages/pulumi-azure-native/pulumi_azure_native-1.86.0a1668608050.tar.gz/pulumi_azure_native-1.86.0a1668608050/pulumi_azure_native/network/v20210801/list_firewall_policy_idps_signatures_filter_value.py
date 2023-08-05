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
    'ListFirewallPolicyIdpsSignaturesFilterValueResult',
    'AwaitableListFirewallPolicyIdpsSignaturesFilterValueResult',
    'list_firewall_policy_idps_signatures_filter_value',
    'list_firewall_policy_idps_signatures_filter_value_output',
]

@pulumi.output_type
class ListFirewallPolicyIdpsSignaturesFilterValueResult:
    """
    Describes the list of all possible values for a specific filter value
    """
    def __init__(__self__, filter_values=None):
        if filter_values and not isinstance(filter_values, list):
            raise TypeError("Expected argument 'filter_values' to be a list")
        pulumi.set(__self__, "filter_values", filter_values)

    @property
    @pulumi.getter(name="filterValues")
    def filter_values(self) -> Optional[Sequence[str]]:
        """
        Describes the possible values
        """
        return pulumi.get(self, "filter_values")


class AwaitableListFirewallPolicyIdpsSignaturesFilterValueResult(ListFirewallPolicyIdpsSignaturesFilterValueResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListFirewallPolicyIdpsSignaturesFilterValueResult(
            filter_values=self.filter_values)


def list_firewall_policy_idps_signatures_filter_value(filter_name: Optional[str] = None,
                                                      firewall_policy_name: Optional[str] = None,
                                                      resource_group_name: Optional[str] = None,
                                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListFirewallPolicyIdpsSignaturesFilterValueResult:
    """
    Describes the list of all possible values for a specific filter value


    :param str filter_name: Describes the name of the column which values will be returned
    :param str firewall_policy_name: The name of the Firewall Policy.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['filterName'] = filter_name
    __args__['firewallPolicyName'] = firewall_policy_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20210801:listFirewallPolicyIdpsSignaturesFilterValue', __args__, opts=opts, typ=ListFirewallPolicyIdpsSignaturesFilterValueResult).value

    return AwaitableListFirewallPolicyIdpsSignaturesFilterValueResult(
        filter_values=__ret__.filter_values)


@_utilities.lift_output_func(list_firewall_policy_idps_signatures_filter_value)
def list_firewall_policy_idps_signatures_filter_value_output(filter_name: Optional[pulumi.Input[Optional[str]]] = None,
                                                             firewall_policy_name: Optional[pulumi.Input[str]] = None,
                                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListFirewallPolicyIdpsSignaturesFilterValueResult]:
    """
    Describes the list of all possible values for a specific filter value


    :param str filter_name: Describes the name of the column which values will be returned
    :param str firewall_policy_name: The name of the Firewall Policy.
    :param str resource_group_name: The name of the resource group.
    """
    ...
