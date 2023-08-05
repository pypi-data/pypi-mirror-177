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

__all__ = ['VpnConnectionInitArgs', 'VpnConnection']

@pulumi.input_type
class VpnConnectionInitArgs:
    def __init__(__self__, *,
                 gateway_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 connection_bandwidth: Optional[pulumi.Input[int]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 enable_internet_security: Optional[pulumi.Input[bool]] = None,
                 enable_rate_limiting: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_vpn_site: Optional[pulumi.Input['SubResourceArgs']] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 vpn_connection_protocol_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]] = None):
        """
        The set of arguments for constructing a VpnConnection resource.
        :param pulumi.Input[str] gateway_name: The name of the gateway.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VpnGateway.
        :param pulumi.Input[int] connection_bandwidth: Expected bandwidth in MBPS.
        :param pulumi.Input[str] connection_name: The name of the connection.
        :param pulumi.Input[bool] enable_bgp: EnableBgp flag
        :param pulumi.Input[bool] enable_internet_security: Enable internet security
        :param pulumi.Input[bool] enable_rate_limiting: EnableBgp flag
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]] ipsec_policies: The IPSec Policies to be considered by this connection.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input['SubResourceArgs'] remote_vpn_site: Id of the connected vpn site.
        :param pulumi.Input[int] routing_weight: routing weight for vpn connection.
        :param pulumi.Input[str] shared_key: SharedKey for the vpn connection.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']] vpn_connection_protocol_type: Connection protocol used for this connection
        """
        pulumi.set(__self__, "gateway_name", gateway_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if connection_bandwidth is not None:
            pulumi.set(__self__, "connection_bandwidth", connection_bandwidth)
        if connection_name is not None:
            pulumi.set(__self__, "connection_name", connection_name)
        if enable_bgp is not None:
            pulumi.set(__self__, "enable_bgp", enable_bgp)
        if enable_internet_security is not None:
            pulumi.set(__self__, "enable_internet_security", enable_internet_security)
        if enable_rate_limiting is not None:
            pulumi.set(__self__, "enable_rate_limiting", enable_rate_limiting)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ipsec_policies is not None:
            pulumi.set(__self__, "ipsec_policies", ipsec_policies)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if remote_vpn_site is not None:
            pulumi.set(__self__, "remote_vpn_site", remote_vpn_site)
        if routing_weight is not None:
            pulumi.set(__self__, "routing_weight", routing_weight)
        if shared_key is not None:
            pulumi.set(__self__, "shared_key", shared_key)
        if vpn_connection_protocol_type is not None:
            pulumi.set(__self__, "vpn_connection_protocol_type", vpn_connection_protocol_type)

    @property
    @pulumi.getter(name="gatewayName")
    def gateway_name(self) -> pulumi.Input[str]:
        """
        The name of the gateway.
        """
        return pulumi.get(self, "gateway_name")

    @gateway_name.setter
    def gateway_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "gateway_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name of the VpnGateway.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="connectionBandwidth")
    def connection_bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        Expected bandwidth in MBPS.
        """
        return pulumi.get(self, "connection_bandwidth")

    @connection_bandwidth.setter
    def connection_bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "connection_bandwidth", value)

    @property
    @pulumi.getter(name="connectionName")
    def connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the connection.
        """
        return pulumi.get(self, "connection_name")

    @connection_name.setter
    def connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_name", value)

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> Optional[pulumi.Input[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_bgp")

    @enable_bgp.setter
    def enable_bgp(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_bgp", value)

    @property
    @pulumi.getter(name="enableInternetSecurity")
    def enable_internet_security(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable internet security
        """
        return pulumi.get(self, "enable_internet_security")

    @enable_internet_security.setter
    def enable_internet_security(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_internet_security", value)

    @property
    @pulumi.getter(name="enableRateLimiting")
    def enable_rate_limiting(self) -> Optional[pulumi.Input[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_rate_limiting")

    @enable_rate_limiting.setter
    def enable_rate_limiting(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_rate_limiting", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="ipsecPolicies")
    def ipsec_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]]:
        """
        The IPSec Policies to be considered by this connection.
        """
        return pulumi.get(self, "ipsec_policies")

    @ipsec_policies.setter
    def ipsec_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]]):
        pulumi.set(self, "ipsec_policies", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="remoteVpnSite")
    def remote_vpn_site(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        Id of the connected vpn site.
        """
        return pulumi.get(self, "remote_vpn_site")

    @remote_vpn_site.setter
    def remote_vpn_site(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "remote_vpn_site", value)

    @property
    @pulumi.getter(name="routingWeight")
    def routing_weight(self) -> Optional[pulumi.Input[int]]:
        """
        routing weight for vpn connection.
        """
        return pulumi.get(self, "routing_weight")

    @routing_weight.setter
    def routing_weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "routing_weight", value)

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> Optional[pulumi.Input[str]]:
        """
        SharedKey for the vpn connection.
        """
        return pulumi.get(self, "shared_key")

    @shared_key.setter
    def shared_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "shared_key", value)

    @property
    @pulumi.getter(name="vpnConnectionProtocolType")
    def vpn_connection_protocol_type(self) -> Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]]:
        """
        Connection protocol used for this connection
        """
        return pulumi.get(self, "vpn_connection_protocol_type")

    @vpn_connection_protocol_type.setter
    def vpn_connection_protocol_type(self, value: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]]):
        pulumi.set(self, "vpn_connection_protocol_type", value)


class VpnConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_bandwidth: Optional[pulumi.Input[int]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 enable_internet_security: Optional[pulumi.Input[bool]] = None,
                 enable_rate_limiting: Optional[pulumi.Input[bool]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_vpn_site: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 vpn_connection_protocol_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]] = None,
                 __props__=None):
        """
        VpnConnection Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] connection_bandwidth: Expected bandwidth in MBPS.
        :param pulumi.Input[str] connection_name: The name of the connection.
        :param pulumi.Input[bool] enable_bgp: EnableBgp flag
        :param pulumi.Input[bool] enable_internet_security: Enable internet security
        :param pulumi.Input[bool] enable_rate_limiting: EnableBgp flag
        :param pulumi.Input[str] gateway_name: The name of the gateway.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]] ipsec_policies: The IPSec Policies to be considered by this connection.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] remote_vpn_site: Id of the connected vpn site.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VpnGateway.
        :param pulumi.Input[int] routing_weight: routing weight for vpn connection.
        :param pulumi.Input[str] shared_key: SharedKey for the vpn connection.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']] vpn_connection_protocol_type: Connection protocol used for this connection
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpnConnectionInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        VpnConnection Resource.

        :param str resource_name: The name of the resource.
        :param VpnConnectionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpnConnectionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_bandwidth: Optional[pulumi.Input[int]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 enable_internet_security: Optional[pulumi.Input[bool]] = None,
                 enable_rate_limiting: Optional[pulumi.Input[bool]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_vpn_site: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 vpn_connection_protocol_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayConnectionProtocol']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VpnConnectionInitArgs.__new__(VpnConnectionInitArgs)

            __props__.__dict__["connection_bandwidth"] = connection_bandwidth
            __props__.__dict__["connection_name"] = connection_name
            __props__.__dict__["enable_bgp"] = enable_bgp
            __props__.__dict__["enable_internet_security"] = enable_internet_security
            __props__.__dict__["enable_rate_limiting"] = enable_rate_limiting
            if gateway_name is None and not opts.urn:
                raise TypeError("Missing required property 'gateway_name'")
            __props__.__dict__["gateway_name"] = gateway_name
            __props__.__dict__["id"] = id
            __props__.__dict__["ipsec_policies"] = ipsec_policies
            __props__.__dict__["name"] = name
            __props__.__dict__["remote_vpn_site"] = remote_vpn_site
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["routing_weight"] = routing_weight
            __props__.__dict__["shared_key"] = shared_key
            __props__.__dict__["vpn_connection_protocol_type"] = vpn_connection_protocol_type
            __props__.__dict__["connection_status"] = None
            __props__.__dict__["egress_bytes_transferred"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["ingress_bytes_transferred"] = None
            __props__.__dict__["provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20180401:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20180601:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20180701:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20180801:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20181101:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20181201:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20190201:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20190401:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20190601:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20190701:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20190801:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20190901:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20191101:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20191201:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20200301:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20200401:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20200501:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20200601:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20200701:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20200801:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20201101:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20210201:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20210301:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20210501:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20210801:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20220101:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20220501:VpnConnection"), pulumi.Alias(type_="azure-native:network/v20220701:VpnConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VpnConnection, __self__).__init__(
            'azure-native:network/v20181001:VpnConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VpnConnection':
        """
        Get an existing VpnConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VpnConnectionInitArgs.__new__(VpnConnectionInitArgs)

        __props__.__dict__["connection_bandwidth"] = None
        __props__.__dict__["connection_status"] = None
        __props__.__dict__["egress_bytes_transferred"] = None
        __props__.__dict__["enable_bgp"] = None
        __props__.__dict__["enable_internet_security"] = None
        __props__.__dict__["enable_rate_limiting"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["ingress_bytes_transferred"] = None
        __props__.__dict__["ipsec_policies"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["remote_vpn_site"] = None
        __props__.__dict__["routing_weight"] = None
        __props__.__dict__["shared_key"] = None
        __props__.__dict__["vpn_connection_protocol_type"] = None
        return VpnConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionBandwidth")
    def connection_bandwidth(self) -> pulumi.Output[Optional[int]]:
        """
        Expected bandwidth in MBPS.
        """
        return pulumi.get(self, "connection_bandwidth")

    @property
    @pulumi.getter(name="connectionStatus")
    def connection_status(self) -> pulumi.Output[str]:
        """
        The connection status.
        """
        return pulumi.get(self, "connection_status")

    @property
    @pulumi.getter(name="egressBytesTransferred")
    def egress_bytes_transferred(self) -> pulumi.Output[float]:
        """
        Egress bytes transferred.
        """
        return pulumi.get(self, "egress_bytes_transferred")

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> pulumi.Output[Optional[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_bgp")

    @property
    @pulumi.getter(name="enableInternetSecurity")
    def enable_internet_security(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable internet security
        """
        return pulumi.get(self, "enable_internet_security")

    @property
    @pulumi.getter(name="enableRateLimiting")
    def enable_rate_limiting(self) -> pulumi.Output[Optional[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_rate_limiting")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="ingressBytesTransferred")
    def ingress_bytes_transferred(self) -> pulumi.Output[float]:
        """
        Ingress bytes transferred.
        """
        return pulumi.get(self, "ingress_bytes_transferred")

    @property
    @pulumi.getter(name="ipsecPolicies")
    def ipsec_policies(self) -> pulumi.Output[Optional[Sequence['outputs.IpsecPolicyResponse']]]:
        """
        The IPSec Policies to be considered by this connection.
        """
        return pulumi.get(self, "ipsec_policies")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="remoteVpnSite")
    def remote_vpn_site(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Id of the connected vpn site.
        """
        return pulumi.get(self, "remote_vpn_site")

    @property
    @pulumi.getter(name="routingWeight")
    def routing_weight(self) -> pulumi.Output[Optional[int]]:
        """
        routing weight for vpn connection.
        """
        return pulumi.get(self, "routing_weight")

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> pulumi.Output[Optional[str]]:
        """
        SharedKey for the vpn connection.
        """
        return pulumi.get(self, "shared_key")

    @property
    @pulumi.getter(name="vpnConnectionProtocolType")
    def vpn_connection_protocol_type(self) -> pulumi.Output[Optional[str]]:
        """
        Connection protocol used for this connection
        """
        return pulumi.get(self, "vpn_connection_protocol_type")

