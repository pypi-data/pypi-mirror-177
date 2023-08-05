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

__all__ = [
    'GetStorageAccountResult',
    'AwaitableGetStorageAccountResult',
    'get_storage_account',
    'get_storage_account_output',
]

warnings.warn("""Version 2015-05-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetStorageAccountResult:
    """
    The storage account.
    """
    def __init__(__self__, account_type=None, creation_time=None, custom_domain=None, id=None, last_geo_failover_time=None, location=None, name=None, primary_endpoints=None, primary_location=None, provisioning_state=None, secondary_endpoints=None, secondary_location=None, status_of_primary=None, status_of_secondary=None, tags=None, type=None):
        if account_type and not isinstance(account_type, str):
            raise TypeError("Expected argument 'account_type' to be a str")
        pulumi.set(__self__, "account_type", account_type)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if custom_domain and not isinstance(custom_domain, dict):
            raise TypeError("Expected argument 'custom_domain' to be a dict")
        pulumi.set(__self__, "custom_domain", custom_domain)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_geo_failover_time and not isinstance(last_geo_failover_time, str):
            raise TypeError("Expected argument 'last_geo_failover_time' to be a str")
        pulumi.set(__self__, "last_geo_failover_time", last_geo_failover_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if primary_endpoints and not isinstance(primary_endpoints, dict):
            raise TypeError("Expected argument 'primary_endpoints' to be a dict")
        pulumi.set(__self__, "primary_endpoints", primary_endpoints)
        if primary_location and not isinstance(primary_location, str):
            raise TypeError("Expected argument 'primary_location' to be a str")
        pulumi.set(__self__, "primary_location", primary_location)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if secondary_endpoints and not isinstance(secondary_endpoints, dict):
            raise TypeError("Expected argument 'secondary_endpoints' to be a dict")
        pulumi.set(__self__, "secondary_endpoints", secondary_endpoints)
        if secondary_location and not isinstance(secondary_location, str):
            raise TypeError("Expected argument 'secondary_location' to be a str")
        pulumi.set(__self__, "secondary_location", secondary_location)
        if status_of_primary and not isinstance(status_of_primary, str):
            raise TypeError("Expected argument 'status_of_primary' to be a str")
        pulumi.set(__self__, "status_of_primary", status_of_primary)
        if status_of_secondary and not isinstance(status_of_secondary, str):
            raise TypeError("Expected argument 'status_of_secondary' to be a str")
        pulumi.set(__self__, "status_of_secondary", status_of_secondary)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> Optional[str]:
        """
        Gets the type of the storage account.
        """
        return pulumi.get(self, "account_type")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        Gets the creation date and time of the storage account in UTC.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="customDomain")
    def custom_domain(self) -> Optional['outputs.CustomDomainResponse']:
        """
        Gets the user assigned custom domain assigned to this storage account.
        """
        return pulumi.get(self, "custom_domain")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastGeoFailoverTime")
    def last_geo_failover_time(self) -> Optional[str]:
        """
        Gets the timestamp of the most recent instance of a failover to the secondary location. Only the most recent timestamp is retained. This element is not returned if there has never been a failover instance. Only available if the accountType is StandardGRS or StandardRAGRS.
        """
        return pulumi.get(self, "last_geo_failover_time")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="primaryEndpoints")
    def primary_endpoints(self) -> Optional['outputs.EndpointsResponse']:
        """
        Gets the URLs that are used to perform a retrieval of a public blob, queue or table object.Note that StandardZRS and PremiumLRS accounts only return the blob endpoint.
        """
        return pulumi.get(self, "primary_endpoints")

    @property
    @pulumi.getter(name="primaryLocation")
    def primary_location(self) -> Optional[str]:
        """
        Gets the location of the primary for the storage account.
        """
        return pulumi.get(self, "primary_location")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Gets the status of the storage account at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="secondaryEndpoints")
    def secondary_endpoints(self) -> Optional['outputs.EndpointsResponse']:
        """
        Gets the URLs that are used to perform a retrieval of a public blob, queue or table object from the secondary location of the storage account. Only available if the accountType is StandardRAGRS.
        """
        return pulumi.get(self, "secondary_endpoints")

    @property
    @pulumi.getter(name="secondaryLocation")
    def secondary_location(self) -> Optional[str]:
        """
        Gets the location of the geo replicated secondary for the storage account. Only available if the accountType is StandardGRS or StandardRAGRS.
        """
        return pulumi.get(self, "secondary_location")

    @property
    @pulumi.getter(name="statusOfPrimary")
    def status_of_primary(self) -> Optional[str]:
        """
        Gets the status indicating whether the primary location of the storage account is available or unavailable.
        """
        return pulumi.get(self, "status_of_primary")

    @property
    @pulumi.getter(name="statusOfSecondary")
    def status_of_secondary(self) -> Optional[str]:
        """
        Gets the status indicating whether the secondary location of the storage account is available or unavailable. Only available if the accountType is StandardGRS or StandardRAGRS.
        """
        return pulumi.get(self, "status_of_secondary")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetStorageAccountResult(GetStorageAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageAccountResult(
            account_type=self.account_type,
            creation_time=self.creation_time,
            custom_domain=self.custom_domain,
            id=self.id,
            last_geo_failover_time=self.last_geo_failover_time,
            location=self.location,
            name=self.name,
            primary_endpoints=self.primary_endpoints,
            primary_location=self.primary_location,
            provisioning_state=self.provisioning_state,
            secondary_endpoints=self.secondary_endpoints,
            secondary_location=self.secondary_location,
            status_of_primary=self.status_of_primary,
            status_of_secondary=self.status_of_secondary,
            tags=self.tags,
            type=self.type)


def get_storage_account(account_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStorageAccountResult:
    """
    The storage account.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.  
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    pulumi.log.warn("""get_storage_account is deprecated: Version 2015-05-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:storage/v20150501preview:getStorageAccount', __args__, opts=opts, typ=GetStorageAccountResult).value

    return AwaitableGetStorageAccountResult(
        account_type=__ret__.account_type,
        creation_time=__ret__.creation_time,
        custom_domain=__ret__.custom_domain,
        id=__ret__.id,
        last_geo_failover_time=__ret__.last_geo_failover_time,
        location=__ret__.location,
        name=__ret__.name,
        primary_endpoints=__ret__.primary_endpoints,
        primary_location=__ret__.primary_location,
        provisioning_state=__ret__.provisioning_state,
        secondary_endpoints=__ret__.secondary_endpoints,
        secondary_location=__ret__.secondary_location,
        status_of_primary=__ret__.status_of_primary,
        status_of_secondary=__ret__.status_of_secondary,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_storage_account)
def get_storage_account_output(account_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStorageAccountResult]:
    """
    The storage account.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.  
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    pulumi.log.warn("""get_storage_account is deprecated: Version 2015-05-01-preview will be removed in v2 of the provider.""")
    ...
