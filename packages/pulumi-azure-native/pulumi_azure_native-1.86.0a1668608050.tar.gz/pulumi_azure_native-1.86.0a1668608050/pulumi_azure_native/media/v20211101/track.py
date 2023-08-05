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
from ._enums import *
from ._inputs import *

__all__ = ['TrackArgs', 'Track']

@pulumi.input_type
class TrackArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 asset_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 track: Optional[pulumi.Input[Union['AudioTrackArgs', 'TextTrackArgs', 'VideoTrackArgs']]] = None,
                 track_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Track resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[str] asset_name: The Asset name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[Union['AudioTrackArgs', 'TextTrackArgs', 'VideoTrackArgs']] track: Detailed information about a track in the asset.
        :param pulumi.Input[str] track_name: The Asset Track name.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "asset_name", asset_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if track is not None:
            pulumi.set(__self__, "track", track)
        if track_name is not None:
            pulumi.set(__self__, "track_name", track_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The Media Services account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="assetName")
    def asset_name(self) -> pulumi.Input[str]:
        """
        The Asset name.
        """
        return pulumi.get(self, "asset_name")

    @asset_name.setter
    def asset_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "asset_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def track(self) -> Optional[pulumi.Input[Union['AudioTrackArgs', 'TextTrackArgs', 'VideoTrackArgs']]]:
        """
        Detailed information about a track in the asset.
        """
        return pulumi.get(self, "track")

    @track.setter
    def track(self, value: Optional[pulumi.Input[Union['AudioTrackArgs', 'TextTrackArgs', 'VideoTrackArgs']]]):
        pulumi.set(self, "track", value)

    @property
    @pulumi.getter(name="trackName")
    def track_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Asset Track name.
        """
        return pulumi.get(self, "track_name")

    @track_name.setter
    def track_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "track_name", value)


class Track(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 asset_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 track: Optional[pulumi.Input[Union[pulumi.InputType['AudioTrackArgs'], pulumi.InputType['TextTrackArgs'], pulumi.InputType['VideoTrackArgs']]]] = None,
                 track_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An Asset Track resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[str] asset_name: The Asset name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[Union[pulumi.InputType['AudioTrackArgs'], pulumi.InputType['TextTrackArgs'], pulumi.InputType['VideoTrackArgs']]] track: Detailed information about a track in the asset.
        :param pulumi.Input[str] track_name: The Asset Track name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TrackArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Asset Track resource.

        :param str resource_name: The name of the resource.
        :param TrackArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TrackArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 asset_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 track: Optional[pulumi.Input[Union[pulumi.InputType['AudioTrackArgs'], pulumi.InputType['TextTrackArgs'], pulumi.InputType['VideoTrackArgs']]]] = None,
                 track_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TrackArgs.__new__(TrackArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            if asset_name is None and not opts.urn:
                raise TypeError("Missing required property 'asset_name'")
            __props__.__dict__["asset_name"] = asset_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["track"] = track
            __props__.__dict__["track_name"] = track_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:media:Track"), pulumi.Alias(type_="azure-native:media/v20220801:Track")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Track, __self__).__init__(
            'azure-native:media/v20211101:Track',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Track':
        """
        Get an existing Track resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TrackArgs.__new__(TrackArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["track"] = None
        __props__.__dict__["type"] = None
        return Track(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the asset track.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def track(self) -> pulumi.Output[Optional[Any]]:
        """
        Detailed information about a track in the asset.
        """
        return pulumi.get(self, "track")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

