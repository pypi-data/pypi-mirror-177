# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AccountResourcePropertiesArgs',
    'CorsRuleArgs',
    'EndpointAuthenticationArgs',
    'ModelingInputDataArgs',
    'ModelingResourcePropertiesArgs',
    'ServiceEndpointResourcePropertiesArgs',
]

@pulumi.input_type
class AccountResourcePropertiesArgs:
    def __init__(__self__, *,
                 configuration: Optional[pulumi.Input[Union[str, 'AccountConfiguration']]] = None,
                 cors: Optional[pulumi.Input[Sequence[pulumi.Input['CorsRuleArgs']]]] = None,
                 endpoint_authentications: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointAuthenticationArgs']]]] = None,
                 reports_connection_string: Optional[pulumi.Input[str]] = None):
        """
        Account resource properties.
        :param pulumi.Input[Union[str, 'AccountConfiguration']] configuration: Account configuration. This can only be set at RecommendationsService Account creation.
        :param pulumi.Input[Sequence[pulumi.Input['CorsRuleArgs']]] cors: The list of CORS details.
        :param pulumi.Input[Sequence[pulumi.Input['EndpointAuthenticationArgs']]] endpoint_authentications: The list of service endpoints authentication details.
        :param pulumi.Input[str] reports_connection_string: Connection string to write Accounts reports to.
        """
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if cors is not None:
            pulumi.set(__self__, "cors", cors)
        if endpoint_authentications is not None:
            pulumi.set(__self__, "endpoint_authentications", endpoint_authentications)
        if reports_connection_string is not None:
            pulumi.set(__self__, "reports_connection_string", reports_connection_string)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input[Union[str, 'AccountConfiguration']]]:
        """
        Account configuration. This can only be set at RecommendationsService Account creation.
        """
        return pulumi.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input[Union[str, 'AccountConfiguration']]]):
        pulumi.set(self, "configuration", value)

    @property
    @pulumi.getter
    def cors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CorsRuleArgs']]]]:
        """
        The list of CORS details.
        """
        return pulumi.get(self, "cors")

    @cors.setter
    def cors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CorsRuleArgs']]]]):
        pulumi.set(self, "cors", value)

    @property
    @pulumi.getter(name="endpointAuthentications")
    def endpoint_authentications(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EndpointAuthenticationArgs']]]]:
        """
        The list of service endpoints authentication details.
        """
        return pulumi.get(self, "endpoint_authentications")

    @endpoint_authentications.setter
    def endpoint_authentications(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointAuthenticationArgs']]]]):
        pulumi.set(self, "endpoint_authentications", value)

    @property
    @pulumi.getter(name="reportsConnectionString")
    def reports_connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        Connection string to write Accounts reports to.
        """
        return pulumi.get(self, "reports_connection_string")

    @reports_connection_string.setter
    def reports_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reports_connection_string", value)


@pulumi.input_type
class CorsRuleArgs:
    def __init__(__self__, *,
                 allowed_origins: pulumi.Input[Sequence[pulumi.Input[str]]],
                 allowed_headers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 allowed_methods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 exposed_headers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 max_age_in_seconds: Optional[pulumi.Input[int]] = None):
        """
        CORS details.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_origins: The origin domains that are permitted to make a request against the service via CORS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_headers: The request headers that the origin domain may specify on the CORS request.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_methods: The methods (HTTP request verbs) that the origin domain may use for a CORS request.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exposed_headers: The response headers to expose to CORS clients.
        :param pulumi.Input[int] max_age_in_seconds: The number of seconds that the client/browser should cache a preflight response.
        """
        pulumi.set(__self__, "allowed_origins", allowed_origins)
        if allowed_headers is not None:
            pulumi.set(__self__, "allowed_headers", allowed_headers)
        if allowed_methods is not None:
            pulumi.set(__self__, "allowed_methods", allowed_methods)
        if exposed_headers is not None:
            pulumi.set(__self__, "exposed_headers", exposed_headers)
        if max_age_in_seconds is not None:
            pulumi.set(__self__, "max_age_in_seconds", max_age_in_seconds)

    @property
    @pulumi.getter(name="allowedOrigins")
    def allowed_origins(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The origin domains that are permitted to make a request against the service via CORS.
        """
        return pulumi.get(self, "allowed_origins")

    @allowed_origins.setter
    def allowed_origins(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "allowed_origins", value)

    @property
    @pulumi.getter(name="allowedHeaders")
    def allowed_headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The request headers that the origin domain may specify on the CORS request.
        """
        return pulumi.get(self, "allowed_headers")

    @allowed_headers.setter
    def allowed_headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_headers", value)

    @property
    @pulumi.getter(name="allowedMethods")
    def allowed_methods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The methods (HTTP request verbs) that the origin domain may use for a CORS request.
        """
        return pulumi.get(self, "allowed_methods")

    @allowed_methods.setter
    def allowed_methods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_methods", value)

    @property
    @pulumi.getter(name="exposedHeaders")
    def exposed_headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The response headers to expose to CORS clients.
        """
        return pulumi.get(self, "exposed_headers")

    @exposed_headers.setter
    def exposed_headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exposed_headers", value)

    @property
    @pulumi.getter(name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        The number of seconds that the client/browser should cache a preflight response.
        """
        return pulumi.get(self, "max_age_in_seconds")

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_age_in_seconds", value)


@pulumi.input_type
class EndpointAuthenticationArgs:
    def __init__(__self__, *,
                 aad_tenant_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 principal_type: Optional[pulumi.Input[Union[str, 'PrincipalType']]] = None):
        """
        Service endpoints authentication details.
        :param pulumi.Input[str] aad_tenant_id: AAD tenant ID.
        :param pulumi.Input[str] principal_id: AAD principal ID.
        :param pulumi.Input[Union[str, 'PrincipalType']] principal_type: AAD principal type.
        """
        if aad_tenant_id is not None:
            pulumi.set(__self__, "aad_tenant_id", aad_tenant_id)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if principal_type is not None:
            pulumi.set(__self__, "principal_type", principal_type)

    @property
    @pulumi.getter(name="aadTenantID")
    def aad_tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        AAD tenant ID.
        """
        return pulumi.get(self, "aad_tenant_id")

    @aad_tenant_id.setter
    def aad_tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aad_tenant_id", value)

    @property
    @pulumi.getter(name="principalID")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        AAD principal ID.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> Optional[pulumi.Input[Union[str, 'PrincipalType']]]:
        """
        AAD principal type.
        """
        return pulumi.get(self, "principal_type")

    @principal_type.setter
    def principal_type(self, value: Optional[pulumi.Input[Union[str, 'PrincipalType']]]):
        pulumi.set(self, "principal_type", value)


@pulumi.input_type
class ModelingInputDataArgs:
    def __init__(__self__, *,
                 connection_string: Optional[pulumi.Input[str]] = None):
        """
        The configuration to raw CDM data to be used as Modeling resource input.
        :param pulumi.Input[str] connection_string: Connection string to raw input data.
        """
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        Connection string to raw input data.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_string", value)


@pulumi.input_type
class ModelingResourcePropertiesArgs:
    def __init__(__self__, *,
                 features: Optional[pulumi.Input[Union[str, 'ModelingFeatures']]] = None,
                 frequency: Optional[pulumi.Input[Union[str, 'ModelingFrequency']]] = None,
                 input_data: Optional[pulumi.Input['ModelingInputDataArgs']] = None,
                 size: Optional[pulumi.Input[Union[str, 'ModelingSize']]] = None):
        """
        Modeling resource properties.
        :param pulumi.Input[Union[str, 'ModelingFeatures']] features: Modeling features controls the set of supported scenarios\\models being computed. This can only be set at Modeling creation.
        :param pulumi.Input[Union[str, 'ModelingFrequency']] frequency: Modeling frequency controls the modeling compute frequency.
        :param pulumi.Input['ModelingInputDataArgs'] input_data: The configuration to raw CDM data to be used as Modeling resource input.
        :param pulumi.Input[Union[str, 'ModelingSize']] size: Modeling size controls the maximum supported input data size.
        """
        if features is not None:
            pulumi.set(__self__, "features", features)
        if frequency is not None:
            pulumi.set(__self__, "frequency", frequency)
        if input_data is not None:
            pulumi.set(__self__, "input_data", input_data)
        if size is not None:
            pulumi.set(__self__, "size", size)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Union[str, 'ModelingFeatures']]]:
        """
        Modeling features controls the set of supported scenarios\\models being computed. This can only be set at Modeling creation.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Union[str, 'ModelingFeatures']]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter
    def frequency(self) -> Optional[pulumi.Input[Union[str, 'ModelingFrequency']]]:
        """
        Modeling frequency controls the modeling compute frequency.
        """
        return pulumi.get(self, "frequency")

    @frequency.setter
    def frequency(self, value: Optional[pulumi.Input[Union[str, 'ModelingFrequency']]]):
        pulumi.set(self, "frequency", value)

    @property
    @pulumi.getter(name="inputData")
    def input_data(self) -> Optional[pulumi.Input['ModelingInputDataArgs']]:
        """
        The configuration to raw CDM data to be used as Modeling resource input.
        """
        return pulumi.get(self, "input_data")

    @input_data.setter
    def input_data(self, value: Optional[pulumi.Input['ModelingInputDataArgs']]):
        pulumi.set(self, "input_data", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[Union[str, 'ModelingSize']]]:
        """
        Modeling size controls the maximum supported input data size.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[Union[str, 'ModelingSize']]]):
        pulumi.set(self, "size", value)


@pulumi.input_type
class ServiceEndpointResourcePropertiesArgs:
    def __init__(__self__, *,
                 pre_allocated_capacity: Optional[pulumi.Input[int]] = None):
        """
        ServiceEndpoint resource properties.
        :param pulumi.Input[int] pre_allocated_capacity: ServiceEndpoint pre-allocated capacity controls the maximum requests-per-second allowed for that endpoint. Only applicable when Account configuration is Capacity.
        """
        if pre_allocated_capacity is not None:
            pulumi.set(__self__, "pre_allocated_capacity", pre_allocated_capacity)

    @property
    @pulumi.getter(name="preAllocatedCapacity")
    def pre_allocated_capacity(self) -> Optional[pulumi.Input[int]]:
        """
        ServiceEndpoint pre-allocated capacity controls the maximum requests-per-second allowed for that endpoint. Only applicable when Account configuration is Capacity.
        """
        return pulumi.get(self, "pre_allocated_capacity")

    @pre_allocated_capacity.setter
    def pre_allocated_capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "pre_allocated_capacity", value)


