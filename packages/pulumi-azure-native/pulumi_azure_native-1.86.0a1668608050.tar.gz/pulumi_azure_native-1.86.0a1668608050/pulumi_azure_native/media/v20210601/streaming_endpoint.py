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
from ._inputs import *

__all__ = ['StreamingEndpointArgs', 'StreamingEndpoint']

@pulumi.input_type
class StreamingEndpointArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 scale_units: pulumi.Input[int],
                 access_control: Optional[pulumi.Input['StreamingEndpointAccessControlArgs']] = None,
                 auto_start: Optional[pulumi.Input[bool]] = None,
                 availability_set_name: Optional[pulumi.Input[str]] = None,
                 cdn_enabled: Optional[pulumi.Input[bool]] = None,
                 cdn_profile: Optional[pulumi.Input[str]] = None,
                 cdn_provider: Optional[pulumi.Input[str]] = None,
                 cross_site_access_policies: Optional[pulumi.Input['CrossSiteAccessPoliciesArgs']] = None,
                 custom_host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_cache_age: Optional[pulumi.Input[float]] = None,
                 streaming_endpoint_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a StreamingEndpoint resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[int] scale_units: The number of scale units. Use the Scale operation to adjust this value.
        :param pulumi.Input['StreamingEndpointAccessControlArgs'] access_control: The access control definition of the streaming endpoint.
        :param pulumi.Input[bool] auto_start: The flag indicates if the resource should be automatically started on creation.
        :param pulumi.Input[str] availability_set_name: This feature is deprecated, do not set a value for this property.
        :param pulumi.Input[bool] cdn_enabled: The CDN enabled flag.
        :param pulumi.Input[str] cdn_profile: The CDN profile name.
        :param pulumi.Input[str] cdn_provider: The CDN provider name.
        :param pulumi.Input['CrossSiteAccessPoliciesArgs'] cross_site_access_policies: The streaming endpoint access policies.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] custom_host_names: The custom host names of the streaming endpoint
        :param pulumi.Input[str] description: The streaming endpoint description.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[float] max_cache_age: Max cache age
        :param pulumi.Input[str] streaming_endpoint_name: The name of the streaming endpoint, maximum length is 24.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "scale_units", scale_units)
        if access_control is not None:
            pulumi.set(__self__, "access_control", access_control)
        if auto_start is not None:
            pulumi.set(__self__, "auto_start", auto_start)
        if availability_set_name is not None:
            pulumi.set(__self__, "availability_set_name", availability_set_name)
        if cdn_enabled is not None:
            pulumi.set(__self__, "cdn_enabled", cdn_enabled)
        if cdn_profile is not None:
            pulumi.set(__self__, "cdn_profile", cdn_profile)
        if cdn_provider is not None:
            pulumi.set(__self__, "cdn_provider", cdn_provider)
        if cross_site_access_policies is not None:
            pulumi.set(__self__, "cross_site_access_policies", cross_site_access_policies)
        if custom_host_names is not None:
            pulumi.set(__self__, "custom_host_names", custom_host_names)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if max_cache_age is not None:
            pulumi.set(__self__, "max_cache_age", max_cache_age)
        if streaming_endpoint_name is not None:
            pulumi.set(__self__, "streaming_endpoint_name", streaming_endpoint_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter(name="scaleUnits")
    def scale_units(self) -> pulumi.Input[int]:
        """
        The number of scale units. Use the Scale operation to adjust this value.
        """
        return pulumi.get(self, "scale_units")

    @scale_units.setter
    def scale_units(self, value: pulumi.Input[int]):
        pulumi.set(self, "scale_units", value)

    @property
    @pulumi.getter(name="accessControl")
    def access_control(self) -> Optional[pulumi.Input['StreamingEndpointAccessControlArgs']]:
        """
        The access control definition of the streaming endpoint.
        """
        return pulumi.get(self, "access_control")

    @access_control.setter
    def access_control(self, value: Optional[pulumi.Input['StreamingEndpointAccessControlArgs']]):
        pulumi.set(self, "access_control", value)

    @property
    @pulumi.getter(name="autoStart")
    def auto_start(self) -> Optional[pulumi.Input[bool]]:
        """
        The flag indicates if the resource should be automatically started on creation.
        """
        return pulumi.get(self, "auto_start")

    @auto_start.setter
    def auto_start(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_start", value)

    @property
    @pulumi.getter(name="availabilitySetName")
    def availability_set_name(self) -> Optional[pulumi.Input[str]]:
        """
        This feature is deprecated, do not set a value for this property.
        """
        return pulumi.get(self, "availability_set_name")

    @availability_set_name.setter
    def availability_set_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_set_name", value)

    @property
    @pulumi.getter(name="cdnEnabled")
    def cdn_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        The CDN enabled flag.
        """
        return pulumi.get(self, "cdn_enabled")

    @cdn_enabled.setter
    def cdn_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cdn_enabled", value)

    @property
    @pulumi.getter(name="cdnProfile")
    def cdn_profile(self) -> Optional[pulumi.Input[str]]:
        """
        The CDN profile name.
        """
        return pulumi.get(self, "cdn_profile")

    @cdn_profile.setter
    def cdn_profile(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cdn_profile", value)

    @property
    @pulumi.getter(name="cdnProvider")
    def cdn_provider(self) -> Optional[pulumi.Input[str]]:
        """
        The CDN provider name.
        """
        return pulumi.get(self, "cdn_provider")

    @cdn_provider.setter
    def cdn_provider(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cdn_provider", value)

    @property
    @pulumi.getter(name="crossSiteAccessPolicies")
    def cross_site_access_policies(self) -> Optional[pulumi.Input['CrossSiteAccessPoliciesArgs']]:
        """
        The streaming endpoint access policies.
        """
        return pulumi.get(self, "cross_site_access_policies")

    @cross_site_access_policies.setter
    def cross_site_access_policies(self, value: Optional[pulumi.Input['CrossSiteAccessPoliciesArgs']]):
        pulumi.set(self, "cross_site_access_policies", value)

    @property
    @pulumi.getter(name="customHostNames")
    def custom_host_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The custom host names of the streaming endpoint
        """
        return pulumi.get(self, "custom_host_names")

    @custom_host_names.setter
    def custom_host_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "custom_host_names", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The streaming endpoint description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maxCacheAge")
    def max_cache_age(self) -> Optional[pulumi.Input[float]]:
        """
        Max cache age
        """
        return pulumi.get(self, "max_cache_age")

    @max_cache_age.setter
    def max_cache_age(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_cache_age", value)

    @property
    @pulumi.getter(name="streamingEndpointName")
    def streaming_endpoint_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the streaming endpoint, maximum length is 24.
        """
        return pulumi.get(self, "streaming_endpoint_name")

    @streaming_endpoint_name.setter
    def streaming_endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "streaming_endpoint_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class StreamingEndpoint(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_control: Optional[pulumi.Input[pulumi.InputType['StreamingEndpointAccessControlArgs']]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 auto_start: Optional[pulumi.Input[bool]] = None,
                 availability_set_name: Optional[pulumi.Input[str]] = None,
                 cdn_enabled: Optional[pulumi.Input[bool]] = None,
                 cdn_profile: Optional[pulumi.Input[str]] = None,
                 cdn_provider: Optional[pulumi.Input[str]] = None,
                 cross_site_access_policies: Optional[pulumi.Input[pulumi.InputType['CrossSiteAccessPoliciesArgs']]] = None,
                 custom_host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_cache_age: Optional[pulumi.Input[float]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scale_units: Optional[pulumi.Input[int]] = None,
                 streaming_endpoint_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The streaming endpoint.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StreamingEndpointAccessControlArgs']] access_control: The access control definition of the streaming endpoint.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[bool] auto_start: The flag indicates if the resource should be automatically started on creation.
        :param pulumi.Input[str] availability_set_name: This feature is deprecated, do not set a value for this property.
        :param pulumi.Input[bool] cdn_enabled: The CDN enabled flag.
        :param pulumi.Input[str] cdn_profile: The CDN profile name.
        :param pulumi.Input[str] cdn_provider: The CDN provider name.
        :param pulumi.Input[pulumi.InputType['CrossSiteAccessPoliciesArgs']] cross_site_access_policies: The streaming endpoint access policies.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] custom_host_names: The custom host names of the streaming endpoint
        :param pulumi.Input[str] description: The streaming endpoint description.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[float] max_cache_age: Max cache age
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[int] scale_units: The number of scale units. Use the Scale operation to adjust this value.
        :param pulumi.Input[str] streaming_endpoint_name: The name of the streaming endpoint, maximum length is 24.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StreamingEndpointArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The streaming endpoint.

        :param str resource_name: The name of the resource.
        :param StreamingEndpointArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StreamingEndpointArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_control: Optional[pulumi.Input[pulumi.InputType['StreamingEndpointAccessControlArgs']]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 auto_start: Optional[pulumi.Input[bool]] = None,
                 availability_set_name: Optional[pulumi.Input[str]] = None,
                 cdn_enabled: Optional[pulumi.Input[bool]] = None,
                 cdn_profile: Optional[pulumi.Input[str]] = None,
                 cdn_provider: Optional[pulumi.Input[str]] = None,
                 cross_site_access_policies: Optional[pulumi.Input[pulumi.InputType['CrossSiteAccessPoliciesArgs']]] = None,
                 custom_host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_cache_age: Optional[pulumi.Input[float]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scale_units: Optional[pulumi.Input[int]] = None,
                 streaming_endpoint_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StreamingEndpointArgs.__new__(StreamingEndpointArgs)

            __props__.__dict__["access_control"] = access_control
            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["auto_start"] = auto_start
            __props__.__dict__["availability_set_name"] = availability_set_name
            __props__.__dict__["cdn_enabled"] = cdn_enabled
            __props__.__dict__["cdn_profile"] = cdn_profile
            __props__.__dict__["cdn_provider"] = cdn_provider
            __props__.__dict__["cross_site_access_policies"] = cross_site_access_policies
            __props__.__dict__["custom_host_names"] = custom_host_names
            __props__.__dict__["description"] = description
            __props__.__dict__["location"] = location
            __props__.__dict__["max_cache_age"] = max_cache_age
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if scale_units is None and not opts.urn:
                raise TypeError("Missing required property 'scale_units'")
            __props__.__dict__["scale_units"] = scale_units
            __props__.__dict__["streaming_endpoint_name"] = streaming_endpoint_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["created"] = None
            __props__.__dict__["free_trial_end_time"] = None
            __props__.__dict__["host_name"] = None
            __props__.__dict__["last_modified"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:media:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20180330preview:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20180601preview:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20180701:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20190501preview:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20200501:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20211101:StreamingEndpoint"), pulumi.Alias(type_="azure-native:media/v20220801:StreamingEndpoint")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StreamingEndpoint, __self__).__init__(
            'azure-native:media/v20210601:StreamingEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StreamingEndpoint':
        """
        Get an existing StreamingEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StreamingEndpointArgs.__new__(StreamingEndpointArgs)

        __props__.__dict__["access_control"] = None
        __props__.__dict__["availability_set_name"] = None
        __props__.__dict__["cdn_enabled"] = None
        __props__.__dict__["cdn_profile"] = None
        __props__.__dict__["cdn_provider"] = None
        __props__.__dict__["created"] = None
        __props__.__dict__["cross_site_access_policies"] = None
        __props__.__dict__["custom_host_names"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["free_trial_end_time"] = None
        __props__.__dict__["host_name"] = None
        __props__.__dict__["last_modified"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["max_cache_age"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_state"] = None
        __props__.__dict__["scale_units"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return StreamingEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessControl")
    def access_control(self) -> pulumi.Output[Optional['outputs.StreamingEndpointAccessControlResponse']]:
        """
        The access control definition of the streaming endpoint.
        """
        return pulumi.get(self, "access_control")

    @property
    @pulumi.getter(name="availabilitySetName")
    def availability_set_name(self) -> pulumi.Output[Optional[str]]:
        """
        This feature is deprecated, do not set a value for this property.
        """
        return pulumi.get(self, "availability_set_name")

    @property
    @pulumi.getter(name="cdnEnabled")
    def cdn_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        The CDN enabled flag.
        """
        return pulumi.get(self, "cdn_enabled")

    @property
    @pulumi.getter(name="cdnProfile")
    def cdn_profile(self) -> pulumi.Output[Optional[str]]:
        """
        The CDN profile name.
        """
        return pulumi.get(self, "cdn_profile")

    @property
    @pulumi.getter(name="cdnProvider")
    def cdn_provider(self) -> pulumi.Output[Optional[str]]:
        """
        The CDN provider name.
        """
        return pulumi.get(self, "cdn_provider")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        The exact time the streaming endpoint was created.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="crossSiteAccessPolicies")
    def cross_site_access_policies(self) -> pulumi.Output[Optional['outputs.CrossSiteAccessPoliciesResponse']]:
        """
        The streaming endpoint access policies.
        """
        return pulumi.get(self, "cross_site_access_policies")

    @property
    @pulumi.getter(name="customHostNames")
    def custom_host_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The custom host names of the streaming endpoint
        """
        return pulumi.get(self, "custom_host_names")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The streaming endpoint description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="freeTrialEndTime")
    def free_trial_end_time(self) -> pulumi.Output[str]:
        """
        The free trial expiration time.
        """
        return pulumi.get(self, "free_trial_end_time")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        The streaming endpoint host name.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> pulumi.Output[str]:
        """
        The exact time the streaming endpoint was last modified.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxCacheAge")
    def max_cache_age(self) -> pulumi.Output[Optional[float]]:
        """
        Max cache age
        """
        return pulumi.get(self, "max_cache_age")

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
        The provisioning state of the streaming endpoint.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        The resource state of the streaming endpoint.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter(name="scaleUnits")
    def scale_units(self) -> pulumi.Output[int]:
        """
        The number of scale units. Use the Scale operation to adjust this value.
        """
        return pulumi.get(self, "scale_units")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

