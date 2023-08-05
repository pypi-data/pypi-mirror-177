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

__all__ = ['ProfileArgs', 'Profile']

@pulumi.input_type
class ProfileArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sku: pulumi.Input['SkuArgs'],
                 location: Optional[pulumi.Input[str]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Profile resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the Azure subscription.
        :param pulumi.Input['SkuArgs'] sku: The SKU (pricing tier) of the CDN profile.
        :param pulumi.Input[str] location: Profile location
        :param pulumi.Input[str] profile_name: Name of the CDN profile within the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Profile tags
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku", sku)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if profile_name is not None:
            pulumi.set(__self__, "profile_name", profile_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        The SKU (pricing tier) of the CDN profile.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Profile location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="profileName")
    def profile_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the CDN profile within the resource group.
        """
        return pulumi.get(self, "profile_name")

    @profile_name.setter
    def profile_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "profile_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Profile tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Version 2016-04-02 will be removed in v2 of the provider.""", DeprecationWarning)


class Profile(pulumi.CustomResource):
    warnings.warn("""Version 2016-04-02 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        CDN profile represents the top level resource and the entry point into the CDN API. This allows users to set up a logical grouping of endpoints in addition to creating shared configuration settings and selecting pricing tiers and providers.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: Profile location
        :param pulumi.Input[str] profile_name: Name of the CDN profile within the resource group.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the Azure subscription.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The SKU (pricing tier) of the CDN profile.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Profile tags
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProfileArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        CDN profile represents the top level resource and the entry point into the CDN API. This allows users to set up a logical grouping of endpoints in addition to creating shared configuration settings and selecting pricing tiers and providers.

        :param str resource_name: The name of the resource.
        :param ProfileArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProfileArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""Profile is deprecated: Version 2016-04-02 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProfileArgs.__new__(ProfileArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["profile_name"] = profile_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:cdn:Profile"), pulumi.Alias(type_="azure-native:cdn/v20150601:Profile"), pulumi.Alias(type_="azure-native:cdn/v20161002:Profile"), pulumi.Alias(type_="azure-native:cdn/v20170402:Profile"), pulumi.Alias(type_="azure-native:cdn/v20171012:Profile"), pulumi.Alias(type_="azure-native:cdn/v20190415:Profile"), pulumi.Alias(type_="azure-native:cdn/v20190615:Profile"), pulumi.Alias(type_="azure-native:cdn/v20190615preview:Profile"), pulumi.Alias(type_="azure-native:cdn/v20191231:Profile"), pulumi.Alias(type_="azure-native:cdn/v20200331:Profile"), pulumi.Alias(type_="azure-native:cdn/v20200415:Profile"), pulumi.Alias(type_="azure-native:cdn/v20200901:Profile"), pulumi.Alias(type_="azure-native:cdn/v20210601:Profile"), pulumi.Alias(type_="azure-native:cdn/v20220501preview:Profile"), pulumi.Alias(type_="azure-native:cdn/v20221101preview:Profile")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Profile, __self__).__init__(
            'azure-native:cdn/v20160402:Profile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Profile':
        """
        Get an existing Profile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ProfileArgs.__new__(ProfileArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Profile(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning status of the profile.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        Resource status of the profile.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The SKU (pricing tier) of the CDN profile.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

