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

__all__ = ['KubernetesRoleArgs', 'KubernetesRole']

@pulumi.input_type
class KubernetesRoleArgs:
    def __init__(__self__, *,
                 device_name: pulumi.Input[str],
                 host_platform: pulumi.Input[Union[str, 'PlatformType']],
                 kind: pulumi.Input[str],
                 kubernetes_cluster_info: pulumi.Input['KubernetesClusterInfoArgs'],
                 kubernetes_role_resources: pulumi.Input['KubernetesRoleResourcesArgs'],
                 resource_group_name: pulumi.Input[str],
                 role_status: pulumi.Input[Union[str, 'RoleStatus']],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a KubernetesRole resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Union[str, 'PlatformType']] host_platform: Host OS supported by the Kubernetes role.
        :param pulumi.Input[str] kind: Role type.
               Expected value is 'Kubernetes'.
        :param pulumi.Input['KubernetesClusterInfoArgs'] kubernetes_cluster_info: Kubernetes cluster configuration
        :param pulumi.Input['KubernetesRoleResourcesArgs'] kubernetes_role_resources: Kubernetes role resources
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'RoleStatus']] role_status: Role status.
        :param pulumi.Input[str] name: The role name.
        """
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "host_platform", host_platform)
        pulumi.set(__self__, "kind", 'Kubernetes')
        pulumi.set(__self__, "kubernetes_cluster_info", kubernetes_cluster_info)
        pulumi.set(__self__, "kubernetes_role_resources", kubernetes_role_resources)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "role_status", role_status)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="deviceName")
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, "device_name")

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_name", value)

    @property
    @pulumi.getter(name="hostPlatform")
    def host_platform(self) -> pulumi.Input[Union[str, 'PlatformType']]:
        """
        Host OS supported by the Kubernetes role.
        """
        return pulumi.get(self, "host_platform")

    @host_platform.setter
    def host_platform(self, value: pulumi.Input[Union[str, 'PlatformType']]):
        pulumi.set(self, "host_platform", value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        Role type.
        Expected value is 'Kubernetes'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="kubernetesClusterInfo")
    def kubernetes_cluster_info(self) -> pulumi.Input['KubernetesClusterInfoArgs']:
        """
        Kubernetes cluster configuration
        """
        return pulumi.get(self, "kubernetes_cluster_info")

    @kubernetes_cluster_info.setter
    def kubernetes_cluster_info(self, value: pulumi.Input['KubernetesClusterInfoArgs']):
        pulumi.set(self, "kubernetes_cluster_info", value)

    @property
    @pulumi.getter(name="kubernetesRoleResources")
    def kubernetes_role_resources(self) -> pulumi.Input['KubernetesRoleResourcesArgs']:
        """
        Kubernetes role resources
        """
        return pulumi.get(self, "kubernetes_role_resources")

    @kubernetes_role_resources.setter
    def kubernetes_role_resources(self, value: pulumi.Input['KubernetesRoleResourcesArgs']):
        pulumi.set(self, "kubernetes_role_resources", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="roleStatus")
    def role_status(self) -> pulumi.Input[Union[str, 'RoleStatus']]:
        """
        Role status.
        """
        return pulumi.get(self, "role_status")

    @role_status.setter
    def role_status(self, value: pulumi.Input[Union[str, 'RoleStatus']]):
        pulumi.set(self, "role_status", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The role name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class KubernetesRole(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 host_platform: Optional[pulumi.Input[Union[str, 'PlatformType']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kubernetes_cluster_info: Optional[pulumi.Input[pulumi.InputType['KubernetesClusterInfoArgs']]] = None,
                 kubernetes_role_resources: Optional[pulumi.Input[pulumi.InputType['KubernetesRoleResourcesArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_status: Optional[pulumi.Input[Union[str, 'RoleStatus']]] = None,
                 __props__=None):
        """
        Kubernetes role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Union[str, 'PlatformType']] host_platform: Host OS supported by the Kubernetes role.
        :param pulumi.Input[str] kind: Role type.
               Expected value is 'Kubernetes'.
        :param pulumi.Input[pulumi.InputType['KubernetesClusterInfoArgs']] kubernetes_cluster_info: Kubernetes cluster configuration
        :param pulumi.Input[pulumi.InputType['KubernetesRoleResourcesArgs']] kubernetes_role_resources: Kubernetes role resources
        :param pulumi.Input[str] name: The role name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'RoleStatus']] role_status: Role status.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: KubernetesRoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Kubernetes role.

        :param str resource_name: The name of the resource.
        :param KubernetesRoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KubernetesRoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 host_platform: Optional[pulumi.Input[Union[str, 'PlatformType']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kubernetes_cluster_info: Optional[pulumi.Input[pulumi.InputType['KubernetesClusterInfoArgs']]] = None,
                 kubernetes_role_resources: Optional[pulumi.Input[pulumi.InputType['KubernetesRoleResourcesArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_status: Optional[pulumi.Input[Union[str, 'RoleStatus']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KubernetesRoleArgs.__new__(KubernetesRoleArgs)

            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            if host_platform is None and not opts.urn:
                raise TypeError("Missing required property 'host_platform'")
            __props__.__dict__["host_platform"] = host_platform
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = 'Kubernetes'
            if kubernetes_cluster_info is None and not opts.urn:
                raise TypeError("Missing required property 'kubernetes_cluster_info'")
            __props__.__dict__["kubernetes_cluster_info"] = kubernetes_cluster_info
            if kubernetes_role_resources is None and not opts.urn:
                raise TypeError("Missing required property 'kubernetes_role_resources'")
            __props__.__dict__["kubernetes_role_resources"] = kubernetes_role_resources
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if role_status is None and not opts.urn:
                raise TypeError("Missing required property 'role_status'")
            __props__.__dict__["role_status"] = role_status
            __props__.__dict__["host_platform_type"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databoxedge:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190301:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190701:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20190801:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200501preview:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210201:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210201preview:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210601:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20210601preview:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20220301:KubernetesRole"), pulumi.Alias(type_="azure-native:databoxedge/v20220401preview:KubernetesRole")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(KubernetesRole, __self__).__init__(
            'azure-native:databoxedge/v20200901preview:KubernetesRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'KubernetesRole':
        """
        Get an existing KubernetesRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = KubernetesRoleArgs.__new__(KubernetesRoleArgs)

        __props__.__dict__["host_platform"] = None
        __props__.__dict__["host_platform_type"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["kubernetes_cluster_info"] = None
        __props__.__dict__["kubernetes_role_resources"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["role_status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return KubernetesRole(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hostPlatform")
    def host_platform(self) -> pulumi.Output[str]:
        """
        Host OS supported by the Kubernetes role.
        """
        return pulumi.get(self, "host_platform")

    @property
    @pulumi.getter(name="hostPlatformType")
    def host_platform_type(self) -> pulumi.Output[str]:
        """
        Platform where the runtime is hosted.
        """
        return pulumi.get(self, "host_platform_type")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Role type.
        Expected value is 'Kubernetes'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="kubernetesClusterInfo")
    def kubernetes_cluster_info(self) -> pulumi.Output['outputs.KubernetesClusterInfoResponse']:
        """
        Kubernetes cluster configuration
        """
        return pulumi.get(self, "kubernetes_cluster_info")

    @property
    @pulumi.getter(name="kubernetesRoleResources")
    def kubernetes_role_resources(self) -> pulumi.Output['outputs.KubernetesRoleResourcesResponse']:
        """
        Kubernetes role resources
        """
        return pulumi.get(self, "kubernetes_role_resources")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        State of Kubernetes deployment
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="roleStatus")
    def role_status(self) -> pulumi.Output[str]:
        """
        Role status.
        """
        return pulumi.get(self, "role_status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Role configured on ASE resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

