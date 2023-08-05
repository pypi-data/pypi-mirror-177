# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ApiOperationArgs', 'ApiOperation']

@pulumi.input_type
class ApiOperationArgs:
    def __init__(__self__, *,
                 api_id: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 method: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 url_template: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 operation_id: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[str]] = None,
                 request: Optional[pulumi.Input['RequestContractArgs']] = None,
                 responses: Optional[pulumi.Input[Sequence[pulumi.Input['ResponseContractArgs']]]] = None,
                 template_parameters: Optional[pulumi.Input[Sequence[pulumi.Input['ParameterContractArgs']]]] = None):
        """
        The set of arguments for constructing a ApiOperation resource.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        :param pulumi.Input[str] display_name: Operation Name.
        :param pulumi.Input[str] method: A Valid HTTP Operation Method. Typical Http Methods like GET, PUT, POST but not limited by only them.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] url_template: Relative URL template identifying the target resource for this operation. May include parameters. Example: /customers/{cid}/orders/{oid}/?date={date}
        :param pulumi.Input[str] description: Description of the operation. May include HTML formatting tags.
        :param pulumi.Input[str] operation_id: Operation identifier within an API. Must be unique in the current API Management service instance.
        :param pulumi.Input[str] policies: Operation Policies
        :param pulumi.Input['RequestContractArgs'] request: An entity containing request details.
        :param pulumi.Input[Sequence[pulumi.Input['ResponseContractArgs']]] responses: Array of Operation responses.
        :param pulumi.Input[Sequence[pulumi.Input['ParameterContractArgs']]] template_parameters: Collection of URL template parameters.
        """
        pulumi.set(__self__, "api_id", api_id)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "method", method)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "service_name", service_name)
        pulumi.set(__self__, "url_template", url_template)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if operation_id is not None:
            pulumi.set(__self__, "operation_id", operation_id)
        if policies is not None:
            pulumi.set(__self__, "policies", policies)
        if request is not None:
            pulumi.set(__self__, "request", request)
        if responses is not None:
            pulumi.set(__self__, "responses", responses)
        if template_parameters is not None:
            pulumi.set(__self__, "template_parameters", template_parameters)

    @property
    @pulumi.getter(name="apiId")
    def api_id(self) -> pulumi.Input[str]:
        """
        API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        """
        return pulumi.get(self, "api_id")

    @api_id.setter
    def api_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Operation Name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def method(self) -> pulumi.Input[str]:
        """
        A Valid HTTP Operation Method. Typical Http Methods like GET, PUT, POST but not limited by only them.
        """
        return pulumi.get(self, "method")

    @method.setter
    def method(self, value: pulumi.Input[str]):
        pulumi.set(self, "method", value)

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
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter(name="urlTemplate")
    def url_template(self) -> pulumi.Input[str]:
        """
        Relative URL template identifying the target resource for this operation. May include parameters. Example: /customers/{cid}/orders/{oid}/?date={date}
        """
        return pulumi.get(self, "url_template")

    @url_template.setter
    def url_template(self, value: pulumi.Input[str]):
        pulumi.set(self, "url_template", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the operation. May include HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="operationId")
    def operation_id(self) -> Optional[pulumi.Input[str]]:
        """
        Operation identifier within an API. Must be unique in the current API Management service instance.
        """
        return pulumi.get(self, "operation_id")

    @operation_id.setter
    def operation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "operation_id", value)

    @property
    @pulumi.getter
    def policies(self) -> Optional[pulumi.Input[str]]:
        """
        Operation Policies
        """
        return pulumi.get(self, "policies")

    @policies.setter
    def policies(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policies", value)

    @property
    @pulumi.getter
    def request(self) -> Optional[pulumi.Input['RequestContractArgs']]:
        """
        An entity containing request details.
        """
        return pulumi.get(self, "request")

    @request.setter
    def request(self, value: Optional[pulumi.Input['RequestContractArgs']]):
        pulumi.set(self, "request", value)

    @property
    @pulumi.getter
    def responses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResponseContractArgs']]]]:
        """
        Array of Operation responses.
        """
        return pulumi.get(self, "responses")

    @responses.setter
    def responses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResponseContractArgs']]]]):
        pulumi.set(self, "responses", value)

    @property
    @pulumi.getter(name="templateParameters")
    def template_parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ParameterContractArgs']]]]:
        """
        Collection of URL template parameters.
        """
        return pulumi.get(self, "template_parameters")

    @template_parameters.setter
    def template_parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ParameterContractArgs']]]]):
        pulumi.set(self, "template_parameters", value)


class ApiOperation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 method: Optional[pulumi.Input[str]] = None,
                 operation_id: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[str]] = None,
                 request: Optional[pulumi.Input[pulumi.InputType['RequestContractArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 responses: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResponseContractArgs']]]]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 template_parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ParameterContractArgs']]]]] = None,
                 url_template: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Api Operation details.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        :param pulumi.Input[str] description: Description of the operation. May include HTML formatting tags.
        :param pulumi.Input[str] display_name: Operation Name.
        :param pulumi.Input[str] method: A Valid HTTP Operation Method. Typical Http Methods like GET, PUT, POST but not limited by only them.
        :param pulumi.Input[str] operation_id: Operation identifier within an API. Must be unique in the current API Management service instance.
        :param pulumi.Input[str] policies: Operation Policies
        :param pulumi.Input[pulumi.InputType['RequestContractArgs']] request: An entity containing request details.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResponseContractArgs']]]] responses: Array of Operation responses.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ParameterContractArgs']]]] template_parameters: Collection of URL template parameters.
        :param pulumi.Input[str] url_template: Relative URL template identifying the target resource for this operation. May include parameters. Example: /customers/{cid}/orders/{oid}/?date={date}
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApiOperationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Api Operation details.
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param ApiOperationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApiOperationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 method: Optional[pulumi.Input[str]] = None,
                 operation_id: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[str]] = None,
                 request: Optional[pulumi.Input[pulumi.InputType['RequestContractArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 responses: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResponseContractArgs']]]]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 template_parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ParameterContractArgs']]]]] = None,
                 url_template: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiOperationArgs.__new__(ApiOperationArgs)

            if api_id is None and not opts.urn:
                raise TypeError("Missing required property 'api_id'")
            __props__.__dict__["api_id"] = api_id
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if method is None and not opts.urn:
                raise TypeError("Missing required property 'method'")
            __props__.__dict__["method"] = method
            __props__.__dict__["operation_id"] = operation_id
            __props__.__dict__["policies"] = policies
            __props__.__dict__["request"] = request
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["responses"] = responses
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            __props__.__dict__["template_parameters"] = template_parameters
            if url_template is None and not opts.urn:
                raise TypeError("Missing required property 'url_template'")
            __props__.__dict__["url_template"] = url_template
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:apimanagement/v20160707:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20161010:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20170301:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20180101:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20180601preview:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20190101:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20191201:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20191201preview:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20200601preview:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20201201:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20210101preview:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20210401preview:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20210801:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20211201preview:ApiOperation"), pulumi.Alias(type_="azure-native:apimanagement/v20220401preview:ApiOperation")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApiOperation, __self__).__init__(
            'azure-native:apimanagement:ApiOperation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApiOperation':
        """
        Get an existing ApiOperation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApiOperationArgs.__new__(ApiOperationArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["method"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policies"] = None
        __props__.__dict__["request"] = None
        __props__.__dict__["responses"] = None
        __props__.__dict__["template_parameters"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["url_template"] = None
        return ApiOperation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the operation. May include HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Operation Name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def method(self) -> pulumi.Output[str]:
        """
        A Valid HTTP Operation Method. Typical Http Methods like GET, PUT, POST but not limited by only them.
        """
        return pulumi.get(self, "method")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policies(self) -> pulumi.Output[Optional[str]]:
        """
        Operation Policies
        """
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter
    def request(self) -> pulumi.Output[Optional['outputs.RequestContractResponse']]:
        """
        An entity containing request details.
        """
        return pulumi.get(self, "request")

    @property
    @pulumi.getter
    def responses(self) -> pulumi.Output[Optional[Sequence['outputs.ResponseContractResponse']]]:
        """
        Array of Operation responses.
        """
        return pulumi.get(self, "responses")

    @property
    @pulumi.getter(name="templateParameters")
    def template_parameters(self) -> pulumi.Output[Optional[Sequence['outputs.ParameterContractResponse']]]:
        """
        Collection of URL template parameters.
        """
        return pulumi.get(self, "template_parameters")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="urlTemplate")
    def url_template(self) -> pulumi.Output[str]:
        """
        Relative URL template identifying the target resource for this operation. May include parameters. Example: /customers/{cid}/orders/{oid}/?date={date}
        """
        return pulumi.get(self, "url_template")

