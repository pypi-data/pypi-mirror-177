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

__all__ = ['ContainerGroupArgs', 'ContainerGroup']

@pulumi.input_type
class ContainerGroupArgs:
    def __init__(__self__, *,
                 containers: pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]],
                 os_type: pulumi.Input[Union[str, 'OperatingSystemTypes']],
                 resource_group_name: pulumi.Input[str],
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]]] = None,
                 ip_address: Optional[pulumi.Input['IpAddressArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]]] = None):
        """
        The set of arguments for constructing a ContainerGroup resource.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]] containers: The containers within the container group.
        :param pulumi.Input[Union[str, 'OperatingSystemTypes']] os_type: The operating system type required by the containers in the container group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] container_group_name: The name of the container group.
        :param pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]] image_registry_credentials: The image registry credentials by which the container group is created from.
        :param pulumi.Input['IpAddressArgs'] ip_address: The IP address type of the container group.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']] restart_policy: Restart policy for all containers within the container group. 
               - `Always` Always restart
               - `OnFailure` Restart on failure
               - `Never` Never restart
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]] volumes: The list of volumes that can be mounted by containers in this container group.
        """
        pulumi.set(__self__, "containers", containers)
        pulumi.set(__self__, "os_type", os_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if container_group_name is not None:
            pulumi.set(__self__, "container_group_name", container_group_name)
        if image_registry_credentials is not None:
            pulumi.set(__self__, "image_registry_credentials", image_registry_credentials)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if restart_policy is not None:
            pulumi.set(__self__, "restart_policy", restart_policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if volumes is not None:
            pulumi.set(__self__, "volumes", volumes)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]]:
        """
        The containers within the container group.
        """
        return pulumi.get(self, "containers")

    @containers.setter
    def containers(self, value: pulumi.Input[Sequence[pulumi.Input['ContainerArgs']]]):
        pulumi.set(self, "containers", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Input[Union[str, 'OperatingSystemTypes']]:
        """
        The operating system type required by the containers in the container group.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: pulumi.Input[Union[str, 'OperatingSystemTypes']]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="containerGroupName")
    def container_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container group.
        """
        return pulumi.get(self, "container_group_name")

    @container_group_name.setter
    def container_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_group_name", value)

    @property
    @pulumi.getter(name="imageRegistryCredentials")
    def image_registry_credentials(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]]]:
        """
        The image registry credentials by which the container group is created from.
        """
        return pulumi.get(self, "image_registry_credentials")

    @image_registry_credentials.setter
    def image_registry_credentials(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ImageRegistryCredentialArgs']]]]):
        pulumi.set(self, "image_registry_credentials", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input['IpAddressArgs']]:
        """
        The IP address type of the container group.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input['IpAddressArgs']]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]]:
        """
        Restart policy for all containers within the container group. 
        - `Always` Always restart
        - `OnFailure` Restart on failure
        - `Never` Never restart
        """
        return pulumi.get(self, "restart_policy")

    @restart_policy.setter
    def restart_policy(self, value: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]]):
        pulumi.set(self, "restart_policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def volumes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]]]:
        """
        The list of volumes that can be mounted by containers in this container group.
        """
        return pulumi.get(self, "volumes")

    @volumes.setter
    def volumes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeArgs']]]]):
        pulumi.set(self, "volumes", value)


warnings.warn("""Version 2018-02-01-preview will be removed in v2 of the provider.""", DeprecationWarning)


class ContainerGroup(pulumi.CustomResource):
    warnings.warn("""Version 2018-02-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]]] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]]] = None,
                 ip_address: Optional[pulumi.Input[pulumi.InputType['IpAddressArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OperatingSystemTypes']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]]] = None,
                 __props__=None):
        """
        A container group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_group_name: The name of the container group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]] containers: The containers within the container group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]] image_registry_credentials: The image registry credentials by which the container group is created from.
        :param pulumi.Input[pulumi.InputType['IpAddressArgs']] ip_address: The IP address type of the container group.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Union[str, 'OperatingSystemTypes']] os_type: The operating system type required by the containers in the container group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']] restart_policy: Restart policy for all containers within the container group. 
               - `Always` Always restart
               - `OnFailure` Restart on failure
               - `Never` Never restart
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]] volumes: The list of volumes that can be mounted by containers in this container group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A container group.

        :param str resource_name: The name of the resource.
        :param ContainerGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]]] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]]] = None,
                 ip_address: Optional[pulumi.Input[pulumi.InputType['IpAddressArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OperatingSystemTypes']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""ContainerGroup is deprecated: Version 2018-02-01-preview will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContainerGroupArgs.__new__(ContainerGroupArgs)

            __props__.__dict__["container_group_name"] = container_group_name
            if containers is None and not opts.urn:
                raise TypeError("Missing required property 'containers'")
            __props__.__dict__["containers"] = containers
            __props__.__dict__["image_registry_credentials"] = image_registry_credentials
            __props__.__dict__["ip_address"] = ip_address
            __props__.__dict__["location"] = location
            if os_type is None and not opts.urn:
                raise TypeError("Missing required property 'os_type'")
            __props__.__dict__["os_type"] = os_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["restart_policy"] = restart_policy
            __props__.__dict__["tags"] = tags
            __props__.__dict__["volumes"] = volumes
            __props__.__dict__["instance_view"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerinstance:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20170801preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20171001preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20171201preview:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180401:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180601:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20180901:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20181001:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20191201:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20201101:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20210301:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20210701:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20210901:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20211001:ContainerGroup"), pulumi.Alias(type_="azure-native:containerinstance/v20220901:ContainerGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ContainerGroup, __self__).__init__(
            'azure-native:containerinstance/v20180201preview:ContainerGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ContainerGroup':
        """
        Get an existing ContainerGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ContainerGroupArgs.__new__(ContainerGroupArgs)

        __props__.__dict__["containers"] = None
        __props__.__dict__["image_registry_credentials"] = None
        __props__.__dict__["instance_view"] = None
        __props__.__dict__["ip_address"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["os_type"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["restart_policy"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["volumes"] = None
        return ContainerGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Output[Sequence['outputs.ContainerResponse']]:
        """
        The containers within the container group.
        """
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter(name="imageRegistryCredentials")
    def image_registry_credentials(self) -> pulumi.Output[Optional[Sequence['outputs.ImageRegistryCredentialResponse']]]:
        """
        The image registry credentials by which the container group is created from.
        """
        return pulumi.get(self, "image_registry_credentials")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> pulumi.Output['outputs.ContainerGroupResponseInstanceView']:
        """
        The instance view of the container group. Only valid in response.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[Optional['outputs.IpAddressResponse']]:
        """
        The IP address type of the container group.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[str]:
        """
        The operating system type required by the containers in the container group.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the container group. This only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Restart policy for all containers within the container group. 
        - `Always` Always restart
        - `OnFailure` Restart on failure
        - `Never` Never restart
        """
        return pulumi.get(self, "restart_policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def volumes(self) -> pulumi.Output[Optional[Sequence['outputs.VolumeResponse']]]:
        """
        The list of volumes that can be mounted by containers in this container group.
        """
        return pulumi.get(self, "volumes")

