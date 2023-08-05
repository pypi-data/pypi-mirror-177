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
    'ListSiteIdentifiersAssignedToHostNameResult',
    'AwaitableListSiteIdentifiersAssignedToHostNameResult',
    'list_site_identifiers_assigned_to_host_name',
    'list_site_identifiers_assigned_to_host_name_output',
]

@pulumi.output_type
class ListSiteIdentifiersAssignedToHostNameResult:
    """
    Collection of identifiers.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> str:
        """
        Link to next page of resources.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.IdentifierResponse']:
        """
        Collection of resources.
        """
        return pulumi.get(self, "value")


class AwaitableListSiteIdentifiersAssignedToHostNameResult(ListSiteIdentifiersAssignedToHostNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListSiteIdentifiersAssignedToHostNameResult(
            next_link=self.next_link,
            value=self.value)


def list_site_identifiers_assigned_to_host_name(name: Optional[str] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListSiteIdentifiersAssignedToHostNameResult:
    """
    Collection of identifiers.


    :param str name: Name of the object.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20200901:listSiteIdentifiersAssignedToHostName', __args__, opts=opts, typ=ListSiteIdentifiersAssignedToHostNameResult).value

    return AwaitableListSiteIdentifiersAssignedToHostNameResult(
        next_link=__ret__.next_link,
        value=__ret__.value)


@_utilities.lift_output_func(list_site_identifiers_assigned_to_host_name)
def list_site_identifiers_assigned_to_host_name_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListSiteIdentifiersAssignedToHostNameResult]:
    """
    Collection of identifiers.


    :param str name: Name of the object.
    """
    ...
