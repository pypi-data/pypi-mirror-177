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

__all__ = ['PrivateCloudArgs', 'PrivateCloud']

@pulumi.input_type
class PrivateCloudArgs:
    def __init__(__self__, *,
                 management_cluster: pulumi.Input['ManagementClusterArgs'],
                 network_block: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 sku: pulumi.Input['SkuArgs'],
                 identity_sources: Optional[pulumi.Input[Sequence[pulumi.Input['IdentitySourceArgs']]]] = None,
                 internet: Optional[pulumi.Input[Union[str, 'InternetEnum']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 nsxt_password: Optional[pulumi.Input[str]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vcenter_password: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PrivateCloud resource.
        :param pulumi.Input['ManagementClusterArgs'] management_cluster: The default cluster used for management
        :param pulumi.Input[str] network_block: The block of addresses should be unique across VNet in your subscription as well as on-premise. Make sure the CIDR format is conformed to (A.B.C.D/X) where A,B,C,D are between 0 and 255, and X is between 0 and 22
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input['SkuArgs'] sku: The private cloud SKU
        :param pulumi.Input[Sequence[pulumi.Input['IdentitySourceArgs']]] identity_sources: vCenter Single Sign On Identity Sources
        :param pulumi.Input[Union[str, 'InternetEnum']] internet: Connectivity to internet is enabled or disabled
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] nsxt_password: Optionally, set the NSX-T Manager password when the private cloud is created
        :param pulumi.Input[str] private_cloud_name: Name of the private cloud
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] vcenter_password: Optionally, set the vCenter admin password when the private cloud is created
        """
        pulumi.set(__self__, "management_cluster", management_cluster)
        pulumi.set(__self__, "network_block", network_block)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku", sku)
        if identity_sources is not None:
            pulumi.set(__self__, "identity_sources", identity_sources)
        if internet is None:
            internet = 'Disabled'
        if internet is not None:
            pulumi.set(__self__, "internet", internet)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if nsxt_password is not None:
            pulumi.set(__self__, "nsxt_password", nsxt_password)
        if private_cloud_name is not None:
            pulumi.set(__self__, "private_cloud_name", private_cloud_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vcenter_password is not None:
            pulumi.set(__self__, "vcenter_password", vcenter_password)

    @property
    @pulumi.getter(name="managementCluster")
    def management_cluster(self) -> pulumi.Input['ManagementClusterArgs']:
        """
        The default cluster used for management
        """
        return pulumi.get(self, "management_cluster")

    @management_cluster.setter
    def management_cluster(self, value: pulumi.Input['ManagementClusterArgs']):
        pulumi.set(self, "management_cluster", value)

    @property
    @pulumi.getter(name="networkBlock")
    def network_block(self) -> pulumi.Input[str]:
        """
        The block of addresses should be unique across VNet in your subscription as well as on-premise. Make sure the CIDR format is conformed to (A.B.C.D/X) where A,B,C,D are between 0 and 255, and X is between 0 and 22
        """
        return pulumi.get(self, "network_block")

    @network_block.setter
    def network_block(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_block", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        The private cloud SKU
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="identitySources")
    def identity_sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IdentitySourceArgs']]]]:
        """
        vCenter Single Sign On Identity Sources
        """
        return pulumi.get(self, "identity_sources")

    @identity_sources.setter
    def identity_sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IdentitySourceArgs']]]]):
        pulumi.set(self, "identity_sources", value)

    @property
    @pulumi.getter
    def internet(self) -> Optional[pulumi.Input[Union[str, 'InternetEnum']]]:
        """
        Connectivity to internet is enabled or disabled
        """
        return pulumi.get(self, "internet")

    @internet.setter
    def internet(self, value: Optional[pulumi.Input[Union[str, 'InternetEnum']]]):
        pulumi.set(self, "internet", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="nsxtPassword")
    def nsxt_password(self) -> Optional[pulumi.Input[str]]:
        """
        Optionally, set the NSX-T Manager password when the private cloud is created
        """
        return pulumi.get(self, "nsxt_password")

    @nsxt_password.setter
    def nsxt_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nsxt_password", value)

    @property
    @pulumi.getter(name="privateCloudName")
    def private_cloud_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the private cloud
        """
        return pulumi.get(self, "private_cloud_name")

    @private_cloud_name.setter
    def private_cloud_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_cloud_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vcenterPassword")
    def vcenter_password(self) -> Optional[pulumi.Input[str]]:
        """
        Optionally, set the vCenter admin password when the private cloud is created
        """
        return pulumi.get(self, "vcenter_password")

    @vcenter_password.setter
    def vcenter_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vcenter_password", value)


class PrivateCloud(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity_sources: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IdentitySourceArgs']]]]] = None,
                 internet: Optional[pulumi.Input[Union[str, 'InternetEnum']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 management_cluster: Optional[pulumi.Input[pulumi.InputType['ManagementClusterArgs']]] = None,
                 network_block: Optional[pulumi.Input[str]] = None,
                 nsxt_password: Optional[pulumi.Input[str]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vcenter_password: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A private cloud resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IdentitySourceArgs']]]] identity_sources: vCenter Single Sign On Identity Sources
        :param pulumi.Input[Union[str, 'InternetEnum']] internet: Connectivity to internet is enabled or disabled
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[pulumi.InputType['ManagementClusterArgs']] management_cluster: The default cluster used for management
        :param pulumi.Input[str] network_block: The block of addresses should be unique across VNet in your subscription as well as on-premise. Make sure the CIDR format is conformed to (A.B.C.D/X) where A,B,C,D are between 0 and 255, and X is between 0 and 22
        :param pulumi.Input[str] nsxt_password: Optionally, set the NSX-T Manager password when the private cloud is created
        :param pulumi.Input[str] private_cloud_name: Name of the private cloud
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The private cloud SKU
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] vcenter_password: Optionally, set the vCenter admin password when the private cloud is created
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateCloudArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A private cloud resource

        :param str resource_name: The name of the resource.
        :param PrivateCloudArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateCloudArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity_sources: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IdentitySourceArgs']]]]] = None,
                 internet: Optional[pulumi.Input[Union[str, 'InternetEnum']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 management_cluster: Optional[pulumi.Input[pulumi.InputType['ManagementClusterArgs']]] = None,
                 network_block: Optional[pulumi.Input[str]] = None,
                 nsxt_password: Optional[pulumi.Input[str]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vcenter_password: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateCloudArgs.__new__(PrivateCloudArgs)

            __props__.__dict__["identity_sources"] = identity_sources
            if internet is None:
                internet = 'Disabled'
            __props__.__dict__["internet"] = internet
            __props__.__dict__["location"] = location
            if management_cluster is None and not opts.urn:
                raise TypeError("Missing required property 'management_cluster'")
            __props__.__dict__["management_cluster"] = management_cluster
            if network_block is None and not opts.urn:
                raise TypeError("Missing required property 'network_block'")
            __props__.__dict__["network_block"] = network_block
            __props__.__dict__["nsxt_password"] = nsxt_password
            __props__.__dict__["private_cloud_name"] = private_cloud_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vcenter_password"] = vcenter_password
            __props__.__dict__["circuit"] = None
            __props__.__dict__["endpoints"] = None
            __props__.__dict__["management_network"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["nsxt_certificate_thumbprint"] = None
            __props__.__dict__["provisioning_network"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["vcenter_certificate_thumbprint"] = None
            __props__.__dict__["vmotion_network"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:avs:PrivateCloud"), pulumi.Alias(type_="azure-native:avs/v20200717preview:PrivateCloud"), pulumi.Alias(type_="azure-native:avs/v20210101preview:PrivateCloud"), pulumi.Alias(type_="azure-native:avs/v20210601:PrivateCloud"), pulumi.Alias(type_="azure-native:avs/v20211201:PrivateCloud"), pulumi.Alias(type_="azure-native:avs/v20220501:PrivateCloud")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateCloud, __self__).__init__(
            'azure-native:avs/v20200320:PrivateCloud',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateCloud':
        """
        Get an existing PrivateCloud resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrivateCloudArgs.__new__(PrivateCloudArgs)

        __props__.__dict__["circuit"] = None
        __props__.__dict__["endpoints"] = None
        __props__.__dict__["identity_sources"] = None
        __props__.__dict__["internet"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["management_cluster"] = None
        __props__.__dict__["management_network"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_block"] = None
        __props__.__dict__["nsxt_certificate_thumbprint"] = None
        __props__.__dict__["nsxt_password"] = None
        __props__.__dict__["provisioning_network"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vcenter_certificate_thumbprint"] = None
        __props__.__dict__["vcenter_password"] = None
        __props__.__dict__["vmotion_network"] = None
        return PrivateCloud(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def circuit(self) -> pulumi.Output[Optional['outputs.CircuitResponse']]:
        """
        An ExpressRoute Circuit
        """
        return pulumi.get(self, "circuit")

    @property
    @pulumi.getter
    def endpoints(self) -> pulumi.Output['outputs.EndpointsResponse']:
        """
        The endpoints
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter(name="identitySources")
    def identity_sources(self) -> pulumi.Output[Optional[Sequence['outputs.IdentitySourceResponse']]]:
        """
        vCenter Single Sign On Identity Sources
        """
        return pulumi.get(self, "identity_sources")

    @property
    @pulumi.getter
    def internet(self) -> pulumi.Output[Optional[str]]:
        """
        Connectivity to internet is enabled or disabled
        """
        return pulumi.get(self, "internet")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managementCluster")
    def management_cluster(self) -> pulumi.Output['outputs.ManagementClusterResponse']:
        """
        The default cluster used for management
        """
        return pulumi.get(self, "management_cluster")

    @property
    @pulumi.getter(name="managementNetwork")
    def management_network(self) -> pulumi.Output[str]:
        """
        Network used to access vCenter Server and NSX-T Manager
        """
        return pulumi.get(self, "management_network")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkBlock")
    def network_block(self) -> pulumi.Output[str]:
        """
        The block of addresses should be unique across VNet in your subscription as well as on-premise. Make sure the CIDR format is conformed to (A.B.C.D/X) where A,B,C,D are between 0 and 255, and X is between 0 and 22
        """
        return pulumi.get(self, "network_block")

    @property
    @pulumi.getter(name="nsxtCertificateThumbprint")
    def nsxt_certificate_thumbprint(self) -> pulumi.Output[str]:
        """
        Thumbprint of the NSX-T Manager SSL certificate
        """
        return pulumi.get(self, "nsxt_certificate_thumbprint")

    @property
    @pulumi.getter(name="nsxtPassword")
    def nsxt_password(self) -> pulumi.Output[Optional[str]]:
        """
        Optionally, set the NSX-T Manager password when the private cloud is created
        """
        return pulumi.get(self, "nsxt_password")

    @property
    @pulumi.getter(name="provisioningNetwork")
    def provisioning_network(self) -> pulumi.Output[str]:
        """
        Used for virtual machine cold migration, cloning, and snapshot migration
        """
        return pulumi.get(self, "provisioning_network")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        The private cloud SKU
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vcenterCertificateThumbprint")
    def vcenter_certificate_thumbprint(self) -> pulumi.Output[str]:
        """
        Thumbprint of the vCenter Server SSL certificate
        """
        return pulumi.get(self, "vcenter_certificate_thumbprint")

    @property
    @pulumi.getter(name="vcenterPassword")
    def vcenter_password(self) -> pulumi.Output[Optional[str]]:
        """
        Optionally, set the vCenter admin password when the private cloud is created
        """
        return pulumi.get(self, "vcenter_password")

    @property
    @pulumi.getter(name="vmotionNetwork")
    def vmotion_network(self) -> pulumi.Output[str]:
        """
        Used for live migration of virtual machines
        """
        return pulumi.get(self, "vmotion_network")

