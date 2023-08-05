# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['ApplicationArgs', 'Application']

@pulumi.input_type
class ApplicationArgs:
    def __init__(__self__, *,
                 application_group_name: pulumi.Input[str],
                 command_line_setting: pulumi.Input[Union[str, 'CommandLineSetting']],
                 resource_group_name: pulumi.Input[str],
                 application_name: Optional[pulumi.Input[str]] = None,
                 application_type: Optional[pulumi.Input[Union[str, 'RemoteApplicationType']]] = None,
                 command_line_arguments: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 file_path: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 icon_index: Optional[pulumi.Input[int]] = None,
                 icon_path: Optional[pulumi.Input[str]] = None,
                 msix_package_application_id: Optional[pulumi.Input[str]] = None,
                 msix_package_family_name: Optional[pulumi.Input[str]] = None,
                 show_in_portal: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Application resource.
        :param pulumi.Input[str] application_group_name: The name of the application group
        :param pulumi.Input[Union[str, 'CommandLineSetting']] command_line_setting: Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] application_name: The name of the application within the specified application group
        :param pulumi.Input[Union[str, 'RemoteApplicationType']] application_type: Resource Type of Application.
        :param pulumi.Input[str] command_line_arguments: Command Line Arguments for Application.
        :param pulumi.Input[str] description: Description of Application.
        :param pulumi.Input[str] file_path: Specifies a path for the executable file for the application.
        :param pulumi.Input[str] friendly_name: Friendly name of Application.
        :param pulumi.Input[int] icon_index: Index of the icon.
        :param pulumi.Input[str] icon_path: Path to icon.
        :param pulumi.Input[str] msix_package_application_id: Specifies the package application Id for MSIX applications
        :param pulumi.Input[str] msix_package_family_name: Specifies the package family name for MSIX applications
        :param pulumi.Input[bool] show_in_portal: Specifies whether to show the RemoteApp program in the RD Web Access server.
        """
        pulumi.set(__self__, "application_group_name", application_group_name)
        pulumi.set(__self__, "command_line_setting", command_line_setting)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if application_name is not None:
            pulumi.set(__self__, "application_name", application_name)
        if application_type is not None:
            pulumi.set(__self__, "application_type", application_type)
        if command_line_arguments is not None:
            pulumi.set(__self__, "command_line_arguments", command_line_arguments)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if file_path is not None:
            pulumi.set(__self__, "file_path", file_path)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if icon_index is not None:
            pulumi.set(__self__, "icon_index", icon_index)
        if icon_path is not None:
            pulumi.set(__self__, "icon_path", icon_path)
        if msix_package_application_id is not None:
            pulumi.set(__self__, "msix_package_application_id", msix_package_application_id)
        if msix_package_family_name is not None:
            pulumi.set(__self__, "msix_package_family_name", msix_package_family_name)
        if show_in_portal is not None:
            pulumi.set(__self__, "show_in_portal", show_in_portal)

    @property
    @pulumi.getter(name="applicationGroupName")
    def application_group_name(self) -> pulumi.Input[str]:
        """
        The name of the application group
        """
        return pulumi.get(self, "application_group_name")

    @application_group_name.setter
    def application_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_group_name", value)

    @property
    @pulumi.getter(name="commandLineSetting")
    def command_line_setting(self) -> pulumi.Input[Union[str, 'CommandLineSetting']]:
        """
        Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
        """
        return pulumi.get(self, "command_line_setting")

    @command_line_setting.setter
    def command_line_setting(self, value: pulumi.Input[Union[str, 'CommandLineSetting']]):
        pulumi.set(self, "command_line_setting", value)

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
    @pulumi.getter(name="applicationName")
    def application_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application within the specified application group
        """
        return pulumi.get(self, "application_name")

    @application_name.setter
    def application_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_name", value)

    @property
    @pulumi.getter(name="applicationType")
    def application_type(self) -> Optional[pulumi.Input[Union[str, 'RemoteApplicationType']]]:
        """
        Resource Type of Application.
        """
        return pulumi.get(self, "application_type")

    @application_type.setter
    def application_type(self, value: Optional[pulumi.Input[Union[str, 'RemoteApplicationType']]]):
        pulumi.set(self, "application_type", value)

    @property
    @pulumi.getter(name="commandLineArguments")
    def command_line_arguments(self) -> Optional[pulumi.Input[str]]:
        """
        Command Line Arguments for Application.
        """
        return pulumi.get(self, "command_line_arguments")

    @command_line_arguments.setter
    def command_line_arguments(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "command_line_arguments", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of Application.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="filePath")
    def file_path(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a path for the executable file for the application.
        """
        return pulumi.get(self, "file_path")

    @file_path.setter
    def file_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_path", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly name of Application.
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="iconIndex")
    def icon_index(self) -> Optional[pulumi.Input[int]]:
        """
        Index of the icon.
        """
        return pulumi.get(self, "icon_index")

    @icon_index.setter
    def icon_index(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "icon_index", value)

    @property
    @pulumi.getter(name="iconPath")
    def icon_path(self) -> Optional[pulumi.Input[str]]:
        """
        Path to icon.
        """
        return pulumi.get(self, "icon_path")

    @icon_path.setter
    def icon_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "icon_path", value)

    @property
    @pulumi.getter(name="msixPackageApplicationId")
    def msix_package_application_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the package application Id for MSIX applications
        """
        return pulumi.get(self, "msix_package_application_id")

    @msix_package_application_id.setter
    def msix_package_application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "msix_package_application_id", value)

    @property
    @pulumi.getter(name="msixPackageFamilyName")
    def msix_package_family_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the package family name for MSIX applications
        """
        return pulumi.get(self, "msix_package_family_name")

    @msix_package_family_name.setter
    def msix_package_family_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "msix_package_family_name", value)

    @property
    @pulumi.getter(name="showInPortal")
    def show_in_portal(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to show the RemoteApp program in the RD Web Access server.
        """
        return pulumi.get(self, "show_in_portal")

    @show_in_portal.setter
    def show_in_portal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "show_in_portal", value)


warnings.warn("""Version 2020-09-21-preview will be removed in v2 of the provider.""", DeprecationWarning)


class Application(pulumi.CustomResource):
    warnings.warn("""Version 2020-09-21-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 application_type: Optional[pulumi.Input[Union[str, 'RemoteApplicationType']]] = None,
                 command_line_arguments: Optional[pulumi.Input[str]] = None,
                 command_line_setting: Optional[pulumi.Input[Union[str, 'CommandLineSetting']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 file_path: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 icon_index: Optional[pulumi.Input[int]] = None,
                 icon_path: Optional[pulumi.Input[str]] = None,
                 msix_package_application_id: Optional[pulumi.Input[str]] = None,
                 msix_package_family_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 show_in_portal: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Schema for Application properties.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_group_name: The name of the application group
        :param pulumi.Input[str] application_name: The name of the application within the specified application group
        :param pulumi.Input[Union[str, 'RemoteApplicationType']] application_type: Resource Type of Application.
        :param pulumi.Input[str] command_line_arguments: Command Line Arguments for Application.
        :param pulumi.Input[Union[str, 'CommandLineSetting']] command_line_setting: Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
        :param pulumi.Input[str] description: Description of Application.
        :param pulumi.Input[str] file_path: Specifies a path for the executable file for the application.
        :param pulumi.Input[str] friendly_name: Friendly name of Application.
        :param pulumi.Input[int] icon_index: Index of the icon.
        :param pulumi.Input[str] icon_path: Path to icon.
        :param pulumi.Input[str] msix_package_application_id: Specifies the package application Id for MSIX applications
        :param pulumi.Input[str] msix_package_family_name: Specifies the package family name for MSIX applications
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[bool] show_in_portal: Specifies whether to show the RemoteApp program in the RD Web Access server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Schema for Application properties.

        :param str resource_name: The name of the resource.
        :param ApplicationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 application_type: Optional[pulumi.Input[Union[str, 'RemoteApplicationType']]] = None,
                 command_line_arguments: Optional[pulumi.Input[str]] = None,
                 command_line_setting: Optional[pulumi.Input[Union[str, 'CommandLineSetting']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 file_path: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 icon_index: Optional[pulumi.Input[int]] = None,
                 icon_path: Optional[pulumi.Input[str]] = None,
                 msix_package_application_id: Optional[pulumi.Input[str]] = None,
                 msix_package_family_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 show_in_portal: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        pulumi.log.warn("""Application is deprecated: Version 2020-09-21-preview will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationArgs.__new__(ApplicationArgs)

            if application_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_group_name'")
            __props__.__dict__["application_group_name"] = application_group_name
            __props__.__dict__["application_name"] = application_name
            __props__.__dict__["application_type"] = application_type
            __props__.__dict__["command_line_arguments"] = command_line_arguments
            if command_line_setting is None and not opts.urn:
                raise TypeError("Missing required property 'command_line_setting'")
            __props__.__dict__["command_line_setting"] = command_line_setting
            __props__.__dict__["description"] = description
            __props__.__dict__["file_path"] = file_path
            __props__.__dict__["friendly_name"] = friendly_name
            __props__.__dict__["icon_index"] = icon_index
            __props__.__dict__["icon_path"] = icon_path
            __props__.__dict__["msix_package_application_id"] = msix_package_application_id
            __props__.__dict__["msix_package_family_name"] = msix_package_family_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["show_in_portal"] = show_in_portal
            __props__.__dict__["icon_content"] = None
            __props__.__dict__["icon_hash"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:desktopvirtualization:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20190123preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20190924preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20191210preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20201019preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20201102preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20201110preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20210114preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20210201preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20210309preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20210401preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20210712:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20210903preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20220210preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20220401preview:Application"), pulumi.Alias(type_="azure-native:desktopvirtualization/v20220909:Application")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Application, __self__).__init__(
            'azure-native:desktopvirtualization/v20200921preview:Application',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Application':
        """
        Get an existing Application resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationArgs.__new__(ApplicationArgs)

        __props__.__dict__["application_type"] = None
        __props__.__dict__["command_line_arguments"] = None
        __props__.__dict__["command_line_setting"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["file_path"] = None
        __props__.__dict__["friendly_name"] = None
        __props__.__dict__["icon_content"] = None
        __props__.__dict__["icon_hash"] = None
        __props__.__dict__["icon_index"] = None
        __props__.__dict__["icon_path"] = None
        __props__.__dict__["msix_package_application_id"] = None
        __props__.__dict__["msix_package_family_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["show_in_portal"] = None
        __props__.__dict__["type"] = None
        return Application(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationType")
    def application_type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Type of Application.
        """
        return pulumi.get(self, "application_type")

    @property
    @pulumi.getter(name="commandLineArguments")
    def command_line_arguments(self) -> pulumi.Output[Optional[str]]:
        """
        Command Line Arguments for Application.
        """
        return pulumi.get(self, "command_line_arguments")

    @property
    @pulumi.getter(name="commandLineSetting")
    def command_line_setting(self) -> pulumi.Output[str]:
        """
        Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
        """
        return pulumi.get(self, "command_line_setting")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of Application.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="filePath")
    def file_path(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a path for the executable file for the application.
        """
        return pulumi.get(self, "file_path")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Friendly name of Application.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="iconContent")
    def icon_content(self) -> pulumi.Output[str]:
        """
        the icon a 64 bit string as a byte array.
        """
        return pulumi.get(self, "icon_content")

    @property
    @pulumi.getter(name="iconHash")
    def icon_hash(self) -> pulumi.Output[str]:
        """
        Hash of the icon.
        """
        return pulumi.get(self, "icon_hash")

    @property
    @pulumi.getter(name="iconIndex")
    def icon_index(self) -> pulumi.Output[Optional[int]]:
        """
        Index of the icon.
        """
        return pulumi.get(self, "icon_index")

    @property
    @pulumi.getter(name="iconPath")
    def icon_path(self) -> pulumi.Output[Optional[str]]:
        """
        Path to icon.
        """
        return pulumi.get(self, "icon_path")

    @property
    @pulumi.getter(name="msixPackageApplicationId")
    def msix_package_application_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the package application Id for MSIX applications
        """
        return pulumi.get(self, "msix_package_application_id")

    @property
    @pulumi.getter(name="msixPackageFamilyName")
    def msix_package_family_name(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the package family name for MSIX applications
        """
        return pulumi.get(self, "msix_package_family_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="showInPortal")
    def show_in_portal(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to show the RemoteApp program in the RD Web Access server.
        """
        return pulumi.get(self, "show_in_portal")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

