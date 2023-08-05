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

__all__ = ['BlobServicePropertiesArgs', 'BlobServiceProperties']

@pulumi.input_type
class BlobServicePropertiesArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 automatic_snapshot_policy_enabled: Optional[pulumi.Input[bool]] = None,
                 blob_services_name: Optional[pulumi.Input[str]] = None,
                 change_feed: Optional[pulumi.Input['ChangeFeedArgs']] = None,
                 container_delete_retention_policy: Optional[pulumi.Input['DeleteRetentionPolicyArgs']] = None,
                 cors: Optional[pulumi.Input['CorsRulesArgs']] = None,
                 default_service_version: Optional[pulumi.Input[str]] = None,
                 delete_retention_policy: Optional[pulumi.Input['DeleteRetentionPolicyArgs']] = None,
                 is_versioning_enabled: Optional[pulumi.Input[bool]] = None,
                 last_access_time_tracking_policy: Optional[pulumi.Input['LastAccessTimeTrackingPolicyArgs']] = None,
                 restore_policy: Optional[pulumi.Input['RestorePolicyPropertiesArgs']] = None):
        """
        The set of arguments for constructing a BlobServiceProperties resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[bool] automatic_snapshot_policy_enabled: Deprecated in favor of isVersioningEnabled property.
        :param pulumi.Input[str] blob_services_name: The name of the blob Service within the specified storage account. Blob Service Name must be 'default'
        :param pulumi.Input['ChangeFeedArgs'] change_feed: The blob service properties for change feed events.
        :param pulumi.Input['DeleteRetentionPolicyArgs'] container_delete_retention_policy: The blob service properties for container soft delete.
        :param pulumi.Input['CorsRulesArgs'] cors: Specifies CORS rules for the Blob service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the Blob service.
        :param pulumi.Input[str] default_service_version: DefaultServiceVersion indicates the default version to use for requests to the Blob service if an incoming request’s version is not specified. Possible values include version 2008-10-27 and all more recent versions.
        :param pulumi.Input['DeleteRetentionPolicyArgs'] delete_retention_policy: The blob service properties for blob soft delete.
        :param pulumi.Input[bool] is_versioning_enabled: Versioning is enabled if set to true.
        :param pulumi.Input['LastAccessTimeTrackingPolicyArgs'] last_access_time_tracking_policy: The blob service property to configure last access time based tracking policy.
        :param pulumi.Input['RestorePolicyPropertiesArgs'] restore_policy: The blob service properties for blob restore policy.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if automatic_snapshot_policy_enabled is not None:
            pulumi.set(__self__, "automatic_snapshot_policy_enabled", automatic_snapshot_policy_enabled)
        if blob_services_name is not None:
            pulumi.set(__self__, "blob_services_name", blob_services_name)
        if change_feed is not None:
            pulumi.set(__self__, "change_feed", change_feed)
        if container_delete_retention_policy is not None:
            pulumi.set(__self__, "container_delete_retention_policy", container_delete_retention_policy)
        if cors is not None:
            pulumi.set(__self__, "cors", cors)
        if default_service_version is not None:
            pulumi.set(__self__, "default_service_version", default_service_version)
        if delete_retention_policy is not None:
            pulumi.set(__self__, "delete_retention_policy", delete_retention_policy)
        if is_versioning_enabled is not None:
            pulumi.set(__self__, "is_versioning_enabled", is_versioning_enabled)
        if last_access_time_tracking_policy is not None:
            pulumi.set(__self__, "last_access_time_tracking_policy", last_access_time_tracking_policy)
        if restore_policy is not None:
            pulumi.set(__self__, "restore_policy", restore_policy)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the user's subscription. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="automaticSnapshotPolicyEnabled")
    def automatic_snapshot_policy_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Deprecated in favor of isVersioningEnabled property.
        """
        return pulumi.get(self, "automatic_snapshot_policy_enabled")

    @automatic_snapshot_policy_enabled.setter
    def automatic_snapshot_policy_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "automatic_snapshot_policy_enabled", value)

    @property
    @pulumi.getter(name="blobServicesName")
    def blob_services_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the blob Service within the specified storage account. Blob Service Name must be 'default'
        """
        return pulumi.get(self, "blob_services_name")

    @blob_services_name.setter
    def blob_services_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "blob_services_name", value)

    @property
    @pulumi.getter(name="changeFeed")
    def change_feed(self) -> Optional[pulumi.Input['ChangeFeedArgs']]:
        """
        The blob service properties for change feed events.
        """
        return pulumi.get(self, "change_feed")

    @change_feed.setter
    def change_feed(self, value: Optional[pulumi.Input['ChangeFeedArgs']]):
        pulumi.set(self, "change_feed", value)

    @property
    @pulumi.getter(name="containerDeleteRetentionPolicy")
    def container_delete_retention_policy(self) -> Optional[pulumi.Input['DeleteRetentionPolicyArgs']]:
        """
        The blob service properties for container soft delete.
        """
        return pulumi.get(self, "container_delete_retention_policy")

    @container_delete_retention_policy.setter
    def container_delete_retention_policy(self, value: Optional[pulumi.Input['DeleteRetentionPolicyArgs']]):
        pulumi.set(self, "container_delete_retention_policy", value)

    @property
    @pulumi.getter
    def cors(self) -> Optional[pulumi.Input['CorsRulesArgs']]:
        """
        Specifies CORS rules for the Blob service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the Blob service.
        """
        return pulumi.get(self, "cors")

    @cors.setter
    def cors(self, value: Optional[pulumi.Input['CorsRulesArgs']]):
        pulumi.set(self, "cors", value)

    @property
    @pulumi.getter(name="defaultServiceVersion")
    def default_service_version(self) -> Optional[pulumi.Input[str]]:
        """
        DefaultServiceVersion indicates the default version to use for requests to the Blob service if an incoming request’s version is not specified. Possible values include version 2008-10-27 and all more recent versions.
        """
        return pulumi.get(self, "default_service_version")

    @default_service_version.setter
    def default_service_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_service_version", value)

    @property
    @pulumi.getter(name="deleteRetentionPolicy")
    def delete_retention_policy(self) -> Optional[pulumi.Input['DeleteRetentionPolicyArgs']]:
        """
        The blob service properties for blob soft delete.
        """
        return pulumi.get(self, "delete_retention_policy")

    @delete_retention_policy.setter
    def delete_retention_policy(self, value: Optional[pulumi.Input['DeleteRetentionPolicyArgs']]):
        pulumi.set(self, "delete_retention_policy", value)

    @property
    @pulumi.getter(name="isVersioningEnabled")
    def is_versioning_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Versioning is enabled if set to true.
        """
        return pulumi.get(self, "is_versioning_enabled")

    @is_versioning_enabled.setter
    def is_versioning_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_versioning_enabled", value)

    @property
    @pulumi.getter(name="lastAccessTimeTrackingPolicy")
    def last_access_time_tracking_policy(self) -> Optional[pulumi.Input['LastAccessTimeTrackingPolicyArgs']]:
        """
        The blob service property to configure last access time based tracking policy.
        """
        return pulumi.get(self, "last_access_time_tracking_policy")

    @last_access_time_tracking_policy.setter
    def last_access_time_tracking_policy(self, value: Optional[pulumi.Input['LastAccessTimeTrackingPolicyArgs']]):
        pulumi.set(self, "last_access_time_tracking_policy", value)

    @property
    @pulumi.getter(name="restorePolicy")
    def restore_policy(self) -> Optional[pulumi.Input['RestorePolicyPropertiesArgs']]:
        """
        The blob service properties for blob restore policy.
        """
        return pulumi.get(self, "restore_policy")

    @restore_policy.setter
    def restore_policy(self, value: Optional[pulumi.Input['RestorePolicyPropertiesArgs']]):
        pulumi.set(self, "restore_policy", value)


class BlobServiceProperties(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 automatic_snapshot_policy_enabled: Optional[pulumi.Input[bool]] = None,
                 blob_services_name: Optional[pulumi.Input[str]] = None,
                 change_feed: Optional[pulumi.Input[pulumi.InputType['ChangeFeedArgs']]] = None,
                 container_delete_retention_policy: Optional[pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']]] = None,
                 cors: Optional[pulumi.Input[pulumi.InputType['CorsRulesArgs']]] = None,
                 default_service_version: Optional[pulumi.Input[str]] = None,
                 delete_retention_policy: Optional[pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']]] = None,
                 is_versioning_enabled: Optional[pulumi.Input[bool]] = None,
                 last_access_time_tracking_policy: Optional[pulumi.Input[pulumi.InputType['LastAccessTimeTrackingPolicyArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restore_policy: Optional[pulumi.Input[pulumi.InputType['RestorePolicyPropertiesArgs']]] = None,
                 __props__=None):
        """
        The properties of a storage account’s Blob service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[bool] automatic_snapshot_policy_enabled: Deprecated in favor of isVersioningEnabled property.
        :param pulumi.Input[str] blob_services_name: The name of the blob Service within the specified storage account. Blob Service Name must be 'default'
        :param pulumi.Input[pulumi.InputType['ChangeFeedArgs']] change_feed: The blob service properties for change feed events.
        :param pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']] container_delete_retention_policy: The blob service properties for container soft delete.
        :param pulumi.Input[pulumi.InputType['CorsRulesArgs']] cors: Specifies CORS rules for the Blob service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the Blob service.
        :param pulumi.Input[str] default_service_version: DefaultServiceVersion indicates the default version to use for requests to the Blob service if an incoming request’s version is not specified. Possible values include version 2008-10-27 and all more recent versions.
        :param pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']] delete_retention_policy: The blob service properties for blob soft delete.
        :param pulumi.Input[bool] is_versioning_enabled: Versioning is enabled if set to true.
        :param pulumi.Input[pulumi.InputType['LastAccessTimeTrackingPolicyArgs']] last_access_time_tracking_policy: The blob service property to configure last access time based tracking policy.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['RestorePolicyPropertiesArgs']] restore_policy: The blob service properties for blob restore policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BlobServicePropertiesArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The properties of a storage account’s Blob service.

        :param str resource_name: The name of the resource.
        :param BlobServicePropertiesArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BlobServicePropertiesArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 automatic_snapshot_policy_enabled: Optional[pulumi.Input[bool]] = None,
                 blob_services_name: Optional[pulumi.Input[str]] = None,
                 change_feed: Optional[pulumi.Input[pulumi.InputType['ChangeFeedArgs']]] = None,
                 container_delete_retention_policy: Optional[pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']]] = None,
                 cors: Optional[pulumi.Input[pulumi.InputType['CorsRulesArgs']]] = None,
                 default_service_version: Optional[pulumi.Input[str]] = None,
                 delete_retention_policy: Optional[pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']]] = None,
                 is_versioning_enabled: Optional[pulumi.Input[bool]] = None,
                 last_access_time_tracking_policy: Optional[pulumi.Input[pulumi.InputType['LastAccessTimeTrackingPolicyArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restore_policy: Optional[pulumi.Input[pulumi.InputType['RestorePolicyPropertiesArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BlobServicePropertiesArgs.__new__(BlobServicePropertiesArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["automatic_snapshot_policy_enabled"] = automatic_snapshot_policy_enabled
            __props__.__dict__["blob_services_name"] = blob_services_name
            __props__.__dict__["change_feed"] = change_feed
            __props__.__dict__["container_delete_retention_policy"] = container_delete_retention_policy
            __props__.__dict__["cors"] = cors
            __props__.__dict__["default_service_version"] = default_service_version
            __props__.__dict__["delete_retention_policy"] = delete_retention_policy
            __props__.__dict__["is_versioning_enabled"] = is_versioning_enabled
            __props__.__dict__["last_access_time_tracking_policy"] = last_access_time_tracking_policy
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["restore_policy"] = restore_policy
            __props__.__dict__["name"] = None
            __props__.__dict__["sku"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:storage:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20180701:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20181101:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20190401:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20190601:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20200801preview:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20210201:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20210401:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20210601:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20210801:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20210901:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20220501:BlobServiceProperties"), pulumi.Alias(type_="azure-native:storage/v20220901:BlobServiceProperties")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BlobServiceProperties, __self__).__init__(
            'azure-native:storage/v20210101:BlobServiceProperties',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BlobServiceProperties':
        """
        Get an existing BlobServiceProperties resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BlobServicePropertiesArgs.__new__(BlobServicePropertiesArgs)

        __props__.__dict__["automatic_snapshot_policy_enabled"] = None
        __props__.__dict__["change_feed"] = None
        __props__.__dict__["container_delete_retention_policy"] = None
        __props__.__dict__["cors"] = None
        __props__.__dict__["default_service_version"] = None
        __props__.__dict__["delete_retention_policy"] = None
        __props__.__dict__["is_versioning_enabled"] = None
        __props__.__dict__["last_access_time_tracking_policy"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["restore_policy"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["type"] = None
        return BlobServiceProperties(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="automaticSnapshotPolicyEnabled")
    def automatic_snapshot_policy_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Deprecated in favor of isVersioningEnabled property.
        """
        return pulumi.get(self, "automatic_snapshot_policy_enabled")

    @property
    @pulumi.getter(name="changeFeed")
    def change_feed(self) -> pulumi.Output[Optional['outputs.ChangeFeedResponse']]:
        """
        The blob service properties for change feed events.
        """
        return pulumi.get(self, "change_feed")

    @property
    @pulumi.getter(name="containerDeleteRetentionPolicy")
    def container_delete_retention_policy(self) -> pulumi.Output[Optional['outputs.DeleteRetentionPolicyResponse']]:
        """
        The blob service properties for container soft delete.
        """
        return pulumi.get(self, "container_delete_retention_policy")

    @property
    @pulumi.getter
    def cors(self) -> pulumi.Output[Optional['outputs.CorsRulesResponse']]:
        """
        Specifies CORS rules for the Blob service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the Blob service.
        """
        return pulumi.get(self, "cors")

    @property
    @pulumi.getter(name="defaultServiceVersion")
    def default_service_version(self) -> pulumi.Output[Optional[str]]:
        """
        DefaultServiceVersion indicates the default version to use for requests to the Blob service if an incoming request’s version is not specified. Possible values include version 2008-10-27 and all more recent versions.
        """
        return pulumi.get(self, "default_service_version")

    @property
    @pulumi.getter(name="deleteRetentionPolicy")
    def delete_retention_policy(self) -> pulumi.Output[Optional['outputs.DeleteRetentionPolicyResponse']]:
        """
        The blob service properties for blob soft delete.
        """
        return pulumi.get(self, "delete_retention_policy")

    @property
    @pulumi.getter(name="isVersioningEnabled")
    def is_versioning_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Versioning is enabled if set to true.
        """
        return pulumi.get(self, "is_versioning_enabled")

    @property
    @pulumi.getter(name="lastAccessTimeTrackingPolicy")
    def last_access_time_tracking_policy(self) -> pulumi.Output[Optional['outputs.LastAccessTimeTrackingPolicyResponse']]:
        """
        The blob service property to configure last access time based tracking policy.
        """
        return pulumi.get(self, "last_access_time_tracking_policy")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="restorePolicy")
    def restore_policy(self) -> pulumi.Output[Optional['outputs.RestorePolicyPropertiesResponse']]:
        """
        The blob service properties for blob restore policy.
        """
        return pulumi.get(self, "restore_policy")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        Sku name and tier.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

