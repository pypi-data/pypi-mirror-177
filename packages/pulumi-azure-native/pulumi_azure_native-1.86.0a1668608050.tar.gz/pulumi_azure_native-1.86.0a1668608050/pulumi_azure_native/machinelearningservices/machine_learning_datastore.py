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
from ._enums import *

__all__ = ['MachineLearningDatastoreArgs', 'MachineLearningDatastore']

@pulumi.input_type
class MachineLearningDatastoreArgs:
    def __init__(__self__, *,
                 data_store_type: pulumi.Input[Union[str, 'DatastoreTypeArm']],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 account_key: Optional[pulumi.Input[str]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 adls_resource_group: Optional[pulumi.Input[str]] = None,
                 adls_subscription_id: Optional[pulumi.Input[str]] = None,
                 authority_url: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 datastore_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint: Optional[pulumi.Input[str]] = None,
                 enforce_ssl: Optional[pulumi.Input[bool]] = None,
                 file_system: Optional[pulumi.Input[str]] = None,
                 include_secret: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_url: Optional[pulumi.Input[str]] = None,
                 sas_token: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 skip_validation: Optional[pulumi.Input[bool]] = None,
                 storage_account_resource_group: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None,
                 store_name: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 workspace_system_assigned_identity: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a MachineLearningDatastore resource.
        :param pulumi.Input[Union[str, 'DatastoreTypeArm']] data_store_type: Specifies datastore type.
        :param pulumi.Input[str] resource_group_name: Name of the resource group in which workspace is located.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        :param pulumi.Input[str] account_key: Account Key of storage account.
        :param pulumi.Input[str] account_name: The name of the storage account.
        :param pulumi.Input[str] adls_resource_group: The resource group the ADLS store belongs to. Defaults to selected resource group.
        :param pulumi.Input[str] adls_subscription_id: The ID of the subscription the ADLS store belongs to. Defaults to selected subscription.
        :param pulumi.Input[str] authority_url: Authority url used to authenticate the user.
        :param pulumi.Input[str] client_id: The service principal's client/application ID.
        :param pulumi.Input[str] client_secret: The service principal's secret.
        :param pulumi.Input[str] container_name: The name of the azure blob container.
        :param pulumi.Input[str] database_name: The database name.
        :param pulumi.Input[str] datastore_name: The Datastore name.
        :param pulumi.Input[str] description: The description of the datastore.
        :param pulumi.Input[str] endpoint: The endpoint of the server.
        :param pulumi.Input[bool] enforce_ssl: This sets the ssl value of the server. Defaults to true if not set.
        :param pulumi.Input[str] file_system: The file system name of the ADLS Gen2.
        :param pulumi.Input[bool] include_secret: Include datastore secret in response.
        :param pulumi.Input[str] name: The name of the datastore.
        :param pulumi.Input[str] password: The password.
        :param pulumi.Input[str] port: The port number.
        :param pulumi.Input[str] protocol: The protocol to be used
        :param pulumi.Input[str] resource_url: Determines what operations will be performed.
        :param pulumi.Input[str] sas_token: Sas Token of storage account.
        :param pulumi.Input[str] server_name: The SQL/MySQL/PostgreSQL server name
        :param pulumi.Input[str] share_name: The name of the file share.
        :param pulumi.Input[bool] skip_validation: Skip validation that ensures data can be loaded from the dataset before registration.
        :param pulumi.Input[str] storage_account_resource_group: The resource group of the storage account. Defaults to selected resource group
        :param pulumi.Input[str] storage_account_subscription_id: The subscription ID of the storage account. Defaults to selected subscription
        :param pulumi.Input[str] store_name: The ADLS store name.
        :param pulumi.Input[str] tenant_id: The service principal Tenant ID.
        :param pulumi.Input[str] user_id: The user ID.
        :param pulumi.Input[str] user_name: The username of the database user.
        :param pulumi.Input[bool] workspace_system_assigned_identity: If set to true, datastore support data access authenticated with Workspace MSI.
        """
        pulumi.set(__self__, "data_store_type", data_store_type)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if account_key is not None:
            pulumi.set(__self__, "account_key", account_key)
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if adls_resource_group is not None:
            pulumi.set(__self__, "adls_resource_group", adls_resource_group)
        if adls_subscription_id is not None:
            pulumi.set(__self__, "adls_subscription_id", adls_subscription_id)
        if authority_url is not None:
            pulumi.set(__self__, "authority_url", authority_url)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if container_name is not None:
            pulumi.set(__self__, "container_name", container_name)
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if datastore_name is not None:
            pulumi.set(__self__, "datastore_name", datastore_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if enforce_ssl is None:
            enforce_ssl = True
        if enforce_ssl is not None:
            pulumi.set(__self__, "enforce_ssl", enforce_ssl)
        if file_system is not None:
            pulumi.set(__self__, "file_system", file_system)
        if include_secret is None:
            include_secret = True
        if include_secret is not None:
            pulumi.set(__self__, "include_secret", include_secret)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if resource_url is not None:
            pulumi.set(__self__, "resource_url", resource_url)
        if sas_token is not None:
            pulumi.set(__self__, "sas_token", sas_token)
        if server_name is not None:
            pulumi.set(__self__, "server_name", server_name)
        if share_name is not None:
            pulumi.set(__self__, "share_name", share_name)
        if skip_validation is not None:
            pulumi.set(__self__, "skip_validation", skip_validation)
        if storage_account_resource_group is not None:
            pulumi.set(__self__, "storage_account_resource_group", storage_account_resource_group)
        if storage_account_subscription_id is not None:
            pulumi.set(__self__, "storage_account_subscription_id", storage_account_subscription_id)
        if store_name is not None:
            pulumi.set(__self__, "store_name", store_name)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)
        if workspace_system_assigned_identity is not None:
            pulumi.set(__self__, "workspace_system_assigned_identity", workspace_system_assigned_identity)

    @property
    @pulumi.getter(name="dataStoreType")
    def data_store_type(self) -> pulumi.Input[Union[str, 'DatastoreTypeArm']]:
        """
        Specifies datastore type.
        """
        return pulumi.get(self, "data_store_type")

    @data_store_type.setter
    def data_store_type(self, value: pulumi.Input[Union[str, 'DatastoreTypeArm']]):
        pulumi.set(self, "data_store_type", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group in which workspace is located.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        Name of Azure Machine Learning workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="accountKey")
    def account_key(self) -> Optional[pulumi.Input[str]]:
        """
        Account Key of storage account.
        """
        return pulumi.get(self, "account_key")

    @account_key.setter
    def account_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_key", value)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the storage account.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="adlsResourceGroup")
    def adls_resource_group(self) -> Optional[pulumi.Input[str]]:
        """
        The resource group the ADLS store belongs to. Defaults to selected resource group.
        """
        return pulumi.get(self, "adls_resource_group")

    @adls_resource_group.setter
    def adls_resource_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "adls_resource_group", value)

    @property
    @pulumi.getter(name="adlsSubscriptionId")
    def adls_subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the subscription the ADLS store belongs to. Defaults to selected subscription.
        """
        return pulumi.get(self, "adls_subscription_id")

    @adls_subscription_id.setter
    def adls_subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "adls_subscription_id", value)

    @property
    @pulumi.getter(name="authorityUrl")
    def authority_url(self) -> Optional[pulumi.Input[str]]:
        """
        Authority url used to authenticate the user.
        """
        return pulumi.get(self, "authority_url")

    @authority_url.setter
    def authority_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authority_url", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The service principal's client/application ID.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The service principal's secret.
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the azure blob container.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        The database name.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="datastoreName")
    def datastore_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Datastore name.
        """
        return pulumi.get(self, "datastore_name")

    @datastore_name.setter
    def datastore_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "datastore_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the datastore.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The endpoint of the server.
        """
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint", value)

    @property
    @pulumi.getter(name="enforceSSL")
    def enforce_ssl(self) -> Optional[pulumi.Input[bool]]:
        """
        This sets the ssl value of the server. Defaults to true if not set.
        """
        return pulumi.get(self, "enforce_ssl")

    @enforce_ssl.setter
    def enforce_ssl(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enforce_ssl", value)

    @property
    @pulumi.getter(name="fileSystem")
    def file_system(self) -> Optional[pulumi.Input[str]]:
        """
        The file system name of the ADLS Gen2.
        """
        return pulumi.get(self, "file_system")

    @file_system.setter
    def file_system(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system", value)

    @property
    @pulumi.getter(name="includeSecret")
    def include_secret(self) -> Optional[pulumi.Input[bool]]:
        """
        Include datastore secret in response.
        """
        return pulumi.get(self, "include_secret")

    @include_secret.setter
    def include_secret(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_secret", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the datastore.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[str]]:
        """
        The port number.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol to be used
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="resourceUrl")
    def resource_url(self) -> Optional[pulumi.Input[str]]:
        """
        Determines what operations will be performed.
        """
        return pulumi.get(self, "resource_url")

    @resource_url.setter
    def resource_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_url", value)

    @property
    @pulumi.getter(name="sasToken")
    def sas_token(self) -> Optional[pulumi.Input[str]]:
        """
        Sas Token of storage account.
        """
        return pulumi.get(self, "sas_token")

    @sas_token.setter
    def sas_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sas_token", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> Optional[pulumi.Input[str]]:
        """
        The SQL/MySQL/PostgreSQL server name
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the file share.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "share_name", value)

    @property
    @pulumi.getter(name="skipValidation")
    def skip_validation(self) -> Optional[pulumi.Input[bool]]:
        """
        Skip validation that ensures data can be loaded from the dataset before registration.
        """
        return pulumi.get(self, "skip_validation")

    @skip_validation.setter
    def skip_validation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_validation", value)

    @property
    @pulumi.getter(name="storageAccountResourceGroup")
    def storage_account_resource_group(self) -> Optional[pulumi.Input[str]]:
        """
        The resource group of the storage account. Defaults to selected resource group
        """
        return pulumi.get(self, "storage_account_resource_group")

    @storage_account_resource_group.setter
    def storage_account_resource_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_resource_group", value)

    @property
    @pulumi.getter(name="storageAccountSubscriptionId")
    def storage_account_subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The subscription ID of the storage account. Defaults to selected subscription
        """
        return pulumi.get(self, "storage_account_subscription_id")

    @storage_account_subscription_id.setter
    def storage_account_subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_subscription_id", value)

    @property
    @pulumi.getter(name="storeName")
    def store_name(self) -> Optional[pulumi.Input[str]]:
        """
        The ADLS store name.
        """
        return pulumi.get(self, "store_name")

    @store_name.setter
    def store_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "store_name", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The service principal Tenant ID.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The user ID.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The username of the database user.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)

    @property
    @pulumi.getter(name="workspaceSystemAssignedIdentity")
    def workspace_system_assigned_identity(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, datastore support data access authenticated with Workspace MSI.
        """
        return pulumi.get(self, "workspace_system_assigned_identity")

    @workspace_system_assigned_identity.setter
    def workspace_system_assigned_identity(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "workspace_system_assigned_identity", value)


class MachineLearningDatastore(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_key: Optional[pulumi.Input[str]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 adls_resource_group: Optional[pulumi.Input[str]] = None,
                 adls_subscription_id: Optional[pulumi.Input[str]] = None,
                 authority_url: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 data_store_type: Optional[pulumi.Input[Union[str, 'DatastoreTypeArm']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 datastore_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint: Optional[pulumi.Input[str]] = None,
                 enforce_ssl: Optional[pulumi.Input[bool]] = None,
                 file_system: Optional[pulumi.Input[str]] = None,
                 include_secret: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_url: Optional[pulumi.Input[str]] = None,
                 sas_token: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 skip_validation: Optional[pulumi.Input[bool]] = None,
                 storage_account_resource_group: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None,
                 store_name: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 workspace_system_assigned_identity: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Machine Learning datastore object wrapped into ARM resource envelope.
        API Version: 2020-05-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_key: Account Key of storage account.
        :param pulumi.Input[str] account_name: The name of the storage account.
        :param pulumi.Input[str] adls_resource_group: The resource group the ADLS store belongs to. Defaults to selected resource group.
        :param pulumi.Input[str] adls_subscription_id: The ID of the subscription the ADLS store belongs to. Defaults to selected subscription.
        :param pulumi.Input[str] authority_url: Authority url used to authenticate the user.
        :param pulumi.Input[str] client_id: The service principal's client/application ID.
        :param pulumi.Input[str] client_secret: The service principal's secret.
        :param pulumi.Input[str] container_name: The name of the azure blob container.
        :param pulumi.Input[Union[str, 'DatastoreTypeArm']] data_store_type: Specifies datastore type.
        :param pulumi.Input[str] database_name: The database name.
        :param pulumi.Input[str] datastore_name: The Datastore name.
        :param pulumi.Input[str] description: The description of the datastore.
        :param pulumi.Input[str] endpoint: The endpoint of the server.
        :param pulumi.Input[bool] enforce_ssl: This sets the ssl value of the server. Defaults to true if not set.
        :param pulumi.Input[str] file_system: The file system name of the ADLS Gen2.
        :param pulumi.Input[bool] include_secret: Include datastore secret in response.
        :param pulumi.Input[str] name: The name of the datastore.
        :param pulumi.Input[str] password: The password.
        :param pulumi.Input[str] port: The port number.
        :param pulumi.Input[str] protocol: The protocol to be used
        :param pulumi.Input[str] resource_group_name: Name of the resource group in which workspace is located.
        :param pulumi.Input[str] resource_url: Determines what operations will be performed.
        :param pulumi.Input[str] sas_token: Sas Token of storage account.
        :param pulumi.Input[str] server_name: The SQL/MySQL/PostgreSQL server name
        :param pulumi.Input[str] share_name: The name of the file share.
        :param pulumi.Input[bool] skip_validation: Skip validation that ensures data can be loaded from the dataset before registration.
        :param pulumi.Input[str] storage_account_resource_group: The resource group of the storage account. Defaults to selected resource group
        :param pulumi.Input[str] storage_account_subscription_id: The subscription ID of the storage account. Defaults to selected subscription
        :param pulumi.Input[str] store_name: The ADLS store name.
        :param pulumi.Input[str] tenant_id: The service principal Tenant ID.
        :param pulumi.Input[str] user_id: The user ID.
        :param pulumi.Input[str] user_name: The username of the database user.
        :param pulumi.Input[str] workspace_name: Name of Azure Machine Learning workspace.
        :param pulumi.Input[bool] workspace_system_assigned_identity: If set to true, datastore support data access authenticated with Workspace MSI.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MachineLearningDatastoreArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Machine Learning datastore object wrapped into ARM resource envelope.
        API Version: 2020-05-01-preview.

        :param str resource_name: The name of the resource.
        :param MachineLearningDatastoreArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MachineLearningDatastoreArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_key: Optional[pulumi.Input[str]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 adls_resource_group: Optional[pulumi.Input[str]] = None,
                 adls_subscription_id: Optional[pulumi.Input[str]] = None,
                 authority_url: Optional[pulumi.Input[str]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 data_store_type: Optional[pulumi.Input[Union[str, 'DatastoreTypeArm']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 datastore_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 endpoint: Optional[pulumi.Input[str]] = None,
                 enforce_ssl: Optional[pulumi.Input[bool]] = None,
                 file_system: Optional[pulumi.Input[str]] = None,
                 include_secret: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_url: Optional[pulumi.Input[str]] = None,
                 sas_token: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 skip_validation: Optional[pulumi.Input[bool]] = None,
                 storage_account_resource_group: Optional[pulumi.Input[str]] = None,
                 storage_account_subscription_id: Optional[pulumi.Input[str]] = None,
                 store_name: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 workspace_system_assigned_identity: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MachineLearningDatastoreArgs.__new__(MachineLearningDatastoreArgs)

            __props__.__dict__["account_key"] = account_key
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["adls_resource_group"] = adls_resource_group
            __props__.__dict__["adls_subscription_id"] = adls_subscription_id
            __props__.__dict__["authority_url"] = authority_url
            __props__.__dict__["client_id"] = client_id
            __props__.__dict__["client_secret"] = client_secret
            __props__.__dict__["container_name"] = container_name
            if data_store_type is None and not opts.urn:
                raise TypeError("Missing required property 'data_store_type'")
            __props__.__dict__["data_store_type"] = data_store_type
            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["datastore_name"] = datastore_name
            __props__.__dict__["description"] = description
            __props__.__dict__["endpoint"] = endpoint
            if enforce_ssl is None:
                enforce_ssl = True
            __props__.__dict__["enforce_ssl"] = enforce_ssl
            __props__.__dict__["file_system"] = file_system
            if include_secret is None:
                include_secret = True
            __props__.__dict__["include_secret"] = include_secret
            __props__.__dict__["name"] = name
            __props__.__dict__["password"] = password
            __props__.__dict__["port"] = port
            __props__.__dict__["protocol"] = protocol
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_url"] = resource_url
            __props__.__dict__["sas_token"] = sas_token
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["share_name"] = share_name
            __props__.__dict__["skip_validation"] = skip_validation
            __props__.__dict__["storage_account_resource_group"] = storage_account_resource_group
            __props__.__dict__["storage_account_subscription_id"] = storage_account_subscription_id
            __props__.__dict__["store_name"] = store_name
            __props__.__dict__["tenant_id"] = tenant_id
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["user_name"] = user_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["workspace_system_assigned_identity"] = workspace_system_assigned_identity
            __props__.__dict__["identity"] = None
            __props__.__dict__["location"] = None
            __props__.__dict__["properties"] = None
            __props__.__dict__["sku"] = None
            __props__.__dict__["tags"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:machinelearningservices/v20200501preview:MachineLearningDatastore"), pulumi.Alias(type_="azure-native:machinelearningservices/v20210301preview:MachineLearningDatastore"), pulumi.Alias(type_="azure-native:machinelearningservices/v20220201preview:MachineLearningDatastore"), pulumi.Alias(type_="azure-native:machinelearningservices/v20220501:MachineLearningDatastore"), pulumi.Alias(type_="azure-native:machinelearningservices/v20220601preview:MachineLearningDatastore"), pulumi.Alias(type_="azure-native:machinelearningservices/v20221001:MachineLearningDatastore"), pulumi.Alias(type_="azure-native:machinelearningservices/v20221001preview:MachineLearningDatastore")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MachineLearningDatastore, __self__).__init__(
            'azure-native:machinelearningservices:MachineLearningDatastore',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MachineLearningDatastore':
        """
        Get an existing MachineLearningDatastore resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MachineLearningDatastoreArgs.__new__(MachineLearningDatastoreArgs)

        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return MachineLearningDatastore(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.DatastoreResponse']:
        """
        Datastore properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the workspace.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Specifies the type of the resource.
        """
        return pulumi.get(self, "type")

