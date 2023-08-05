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
    'GetNotificationChannelResult',
    'AwaitableGetNotificationChannelResult',
    'get_notification_channel',
    'get_notification_channel_output',
]

warnings.warn("""Version 2016-05-15 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetNotificationChannelResult:
    """
    A notification.
    """
    def __init__(__self__, created_date=None, description=None, events=None, id=None, location=None, name=None, provisioning_state=None, tags=None, type=None, unique_identifier=None, web_hook_url=None):
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if events and not isinstance(events, list):
            raise TypeError("Expected argument 'events' to be a list")
        pulumi.set(__self__, "events", events)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unique_identifier and not isinstance(unique_identifier, str):
            raise TypeError("Expected argument 'unique_identifier' to be a str")
        pulumi.set(__self__, "unique_identifier", unique_identifier)
        if web_hook_url and not isinstance(web_hook_url, str):
            raise TypeError("Expected argument 'web_hook_url' to be a str")
        pulumi.set(__self__, "web_hook_url", web_hook_url)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The creation date of the notification channel.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of notification.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def events(self) -> Optional[Sequence['outputs.EventResponse']]:
        """
        The list of event for which this notification is enabled.
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uniqueIdentifier")
    def unique_identifier(self) -> Optional[str]:
        """
        The unique immutable identifier of a resource (Guid).
        """
        return pulumi.get(self, "unique_identifier")

    @property
    @pulumi.getter(name="webHookUrl")
    def web_hook_url(self) -> Optional[str]:
        """
        The webhook URL to send notifications to.
        """
        return pulumi.get(self, "web_hook_url")


class AwaitableGetNotificationChannelResult(GetNotificationChannelResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNotificationChannelResult(
            created_date=self.created_date,
            description=self.description,
            events=self.events,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type,
            unique_identifier=self.unique_identifier,
            web_hook_url=self.web_hook_url)


def get_notification_channel(expand: Optional[str] = None,
                             lab_name: Optional[str] = None,
                             name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNotificationChannelResult:
    """
    A notification.


    :param str expand: Specify the $expand query. Example: 'properties($select=webHookUrl)'
    :param str lab_name: The name of the lab.
    :param str name: The name of the notificationChannel.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_notification_channel is deprecated: Version 2016-05-15 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['expand'] = expand
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:devtestlab/v20160515:getNotificationChannel', __args__, opts=opts, typ=GetNotificationChannelResult).value

    return AwaitableGetNotificationChannelResult(
        created_date=__ret__.created_date,
        description=__ret__.description,
        events=__ret__.events,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type,
        unique_identifier=__ret__.unique_identifier,
        web_hook_url=__ret__.web_hook_url)


@_utilities.lift_output_func(get_notification_channel)
def get_notification_channel_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                    lab_name: Optional[pulumi.Input[str]] = None,
                                    name: Optional[pulumi.Input[str]] = None,
                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNotificationChannelResult]:
    """
    A notification.


    :param str expand: Specify the $expand query. Example: 'properties($select=webHookUrl)'
    :param str lab_name: The name of the lab.
    :param str name: The name of the notificationChannel.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_notification_channel is deprecated: Version 2016-05-15 will be removed in v2 of the provider.""")
    ...
