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
    'GetCertificateResult',
    'AwaitableGetCertificateResult',
    'get_certificate',
    'get_certificate_output',
]

@pulumi.output_type
class GetCertificateResult:
    """
    SSL certificate for an app.
    """
    def __init__(__self__, canonical_name=None, cer_blob=None, domain_validation_method=None, expiration_date=None, friendly_name=None, host_names=None, hosting_environment_profile=None, id=None, issue_date=None, issuer=None, key_vault_id=None, key_vault_secret_name=None, key_vault_secret_status=None, kind=None, location=None, name=None, pfx_blob=None, public_key_hash=None, self_link=None, server_farm_id=None, site_name=None, subject_name=None, tags=None, thumbprint=None, type=None, valid=None):
        if canonical_name and not isinstance(canonical_name, str):
            raise TypeError("Expected argument 'canonical_name' to be a str")
        pulumi.set(__self__, "canonical_name", canonical_name)
        if cer_blob and not isinstance(cer_blob, str):
            raise TypeError("Expected argument 'cer_blob' to be a str")
        pulumi.set(__self__, "cer_blob", cer_blob)
        if domain_validation_method and not isinstance(domain_validation_method, str):
            raise TypeError("Expected argument 'domain_validation_method' to be a str")
        pulumi.set(__self__, "domain_validation_method", domain_validation_method)
        if expiration_date and not isinstance(expiration_date, str):
            raise TypeError("Expected argument 'expiration_date' to be a str")
        pulumi.set(__self__, "expiration_date", expiration_date)
        if friendly_name and not isinstance(friendly_name, str):
            raise TypeError("Expected argument 'friendly_name' to be a str")
        pulumi.set(__self__, "friendly_name", friendly_name)
        if host_names and not isinstance(host_names, list):
            raise TypeError("Expected argument 'host_names' to be a list")
        pulumi.set(__self__, "host_names", host_names)
        if hosting_environment_profile and not isinstance(hosting_environment_profile, dict):
            raise TypeError("Expected argument 'hosting_environment_profile' to be a dict")
        pulumi.set(__self__, "hosting_environment_profile", hosting_environment_profile)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if issue_date and not isinstance(issue_date, str):
            raise TypeError("Expected argument 'issue_date' to be a str")
        pulumi.set(__self__, "issue_date", issue_date)
        if issuer and not isinstance(issuer, str):
            raise TypeError("Expected argument 'issuer' to be a str")
        pulumi.set(__self__, "issuer", issuer)
        if key_vault_id and not isinstance(key_vault_id, str):
            raise TypeError("Expected argument 'key_vault_id' to be a str")
        pulumi.set(__self__, "key_vault_id", key_vault_id)
        if key_vault_secret_name and not isinstance(key_vault_secret_name, str):
            raise TypeError("Expected argument 'key_vault_secret_name' to be a str")
        pulumi.set(__self__, "key_vault_secret_name", key_vault_secret_name)
        if key_vault_secret_status and not isinstance(key_vault_secret_status, str):
            raise TypeError("Expected argument 'key_vault_secret_status' to be a str")
        pulumi.set(__self__, "key_vault_secret_status", key_vault_secret_status)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if pfx_blob and not isinstance(pfx_blob, str):
            raise TypeError("Expected argument 'pfx_blob' to be a str")
        pulumi.set(__self__, "pfx_blob", pfx_blob)
        if public_key_hash and not isinstance(public_key_hash, str):
            raise TypeError("Expected argument 'public_key_hash' to be a str")
        pulumi.set(__self__, "public_key_hash", public_key_hash)
        if self_link and not isinstance(self_link, str):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, "self_link", self_link)
        if server_farm_id and not isinstance(server_farm_id, str):
            raise TypeError("Expected argument 'server_farm_id' to be a str")
        pulumi.set(__self__, "server_farm_id", server_farm_id)
        if site_name and not isinstance(site_name, str):
            raise TypeError("Expected argument 'site_name' to be a str")
        pulumi.set(__self__, "site_name", site_name)
        if subject_name and not isinstance(subject_name, str):
            raise TypeError("Expected argument 'subject_name' to be a str")
        pulumi.set(__self__, "subject_name", subject_name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if thumbprint and not isinstance(thumbprint, str):
            raise TypeError("Expected argument 'thumbprint' to be a str")
        pulumi.set(__self__, "thumbprint", thumbprint)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if valid and not isinstance(valid, bool):
            raise TypeError("Expected argument 'valid' to be a bool")
        pulumi.set(__self__, "valid", valid)

    @property
    @pulumi.getter(name="canonicalName")
    def canonical_name(self) -> Optional[str]:
        """
        CNAME of the certificate to be issued via free certificate
        """
        return pulumi.get(self, "canonical_name")

    @property
    @pulumi.getter(name="cerBlob")
    def cer_blob(self) -> str:
        """
        Raw bytes of .cer file
        """
        return pulumi.get(self, "cer_blob")

    @property
    @pulumi.getter(name="domainValidationMethod")
    def domain_validation_method(self) -> Optional[str]:
        """
        Method of domain validation for free cert
        """
        return pulumi.get(self, "domain_validation_method")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> str:
        """
        Certificate expiration date.
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> str:
        """
        Friendly name of the certificate.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> Optional[Sequence[str]]:
        """
        Host names the certificate applies to.
        """
        return pulumi.get(self, "host_names")

    @property
    @pulumi.getter(name="hostingEnvironmentProfile")
    def hosting_environment_profile(self) -> 'outputs.HostingEnvironmentProfileResponse':
        """
        Specification for the App Service Environment to use for the certificate.
        """
        return pulumi.get(self, "hosting_environment_profile")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="issueDate")
    def issue_date(self) -> str:
        """
        Certificate issue Date.
        """
        return pulumi.get(self, "issue_date")

    @property
    @pulumi.getter
    def issuer(self) -> str:
        """
        Certificate issuer.
        """
        return pulumi.get(self, "issuer")

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> Optional[str]:
        """
        Key Vault Csm resource Id.
        """
        return pulumi.get(self, "key_vault_id")

    @property
    @pulumi.getter(name="keyVaultSecretName")
    def key_vault_secret_name(self) -> Optional[str]:
        """
        Key Vault secret name.
        """
        return pulumi.get(self, "key_vault_secret_name")

    @property
    @pulumi.getter(name="keyVaultSecretStatus")
    def key_vault_secret_status(self) -> str:
        """
        Status of the Key Vault secret.
        """
        return pulumi.get(self, "key_vault_secret_status")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pfxBlob")
    def pfx_blob(self) -> Optional[str]:
        """
        Pfx blob.
        """
        return pulumi.get(self, "pfx_blob")

    @property
    @pulumi.getter(name="publicKeyHash")
    def public_key_hash(self) -> str:
        """
        Public key hash.
        """
        return pulumi.get(self, "public_key_hash")

    @property
    @pulumi.getter(name="selfLink")
    def self_link(self) -> str:
        """
        Self link.
        """
        return pulumi.get(self, "self_link")

    @property
    @pulumi.getter(name="serverFarmId")
    def server_farm_id(self) -> Optional[str]:
        """
        Resource ID of the associated App Service plan, formatted as: "/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}".
        """
        return pulumi.get(self, "server_farm_id")

    @property
    @pulumi.getter(name="siteName")
    def site_name(self) -> str:
        """
        App name.
        """
        return pulumi.get(self, "site_name")

    @property
    @pulumi.getter(name="subjectName")
    def subject_name(self) -> str:
        """
        Subject name of the certificate.
        """
        return pulumi.get(self, "subject_name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def thumbprint(self) -> str:
        """
        Certificate thumbprint.
        """
        return pulumi.get(self, "thumbprint")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def valid(self) -> bool:
        """
        Is the certificate valid?.
        """
        return pulumi.get(self, "valid")


class AwaitableGetCertificateResult(GetCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificateResult(
            canonical_name=self.canonical_name,
            cer_blob=self.cer_blob,
            domain_validation_method=self.domain_validation_method,
            expiration_date=self.expiration_date,
            friendly_name=self.friendly_name,
            host_names=self.host_names,
            hosting_environment_profile=self.hosting_environment_profile,
            id=self.id,
            issue_date=self.issue_date,
            issuer=self.issuer,
            key_vault_id=self.key_vault_id,
            key_vault_secret_name=self.key_vault_secret_name,
            key_vault_secret_status=self.key_vault_secret_status,
            kind=self.kind,
            location=self.location,
            name=self.name,
            pfx_blob=self.pfx_blob,
            public_key_hash=self.public_key_hash,
            self_link=self.self_link,
            server_farm_id=self.server_farm_id,
            site_name=self.site_name,
            subject_name=self.subject_name,
            tags=self.tags,
            thumbprint=self.thumbprint,
            type=self.type,
            valid=self.valid)


def get_certificate(name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCertificateResult:
    """
    SSL certificate for an app.


    :param str name: Name of the certificate.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20210201:getCertificate', __args__, opts=opts, typ=GetCertificateResult).value

    return AwaitableGetCertificateResult(
        canonical_name=__ret__.canonical_name,
        cer_blob=__ret__.cer_blob,
        domain_validation_method=__ret__.domain_validation_method,
        expiration_date=__ret__.expiration_date,
        friendly_name=__ret__.friendly_name,
        host_names=__ret__.host_names,
        hosting_environment_profile=__ret__.hosting_environment_profile,
        id=__ret__.id,
        issue_date=__ret__.issue_date,
        issuer=__ret__.issuer,
        key_vault_id=__ret__.key_vault_id,
        key_vault_secret_name=__ret__.key_vault_secret_name,
        key_vault_secret_status=__ret__.key_vault_secret_status,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        pfx_blob=__ret__.pfx_blob,
        public_key_hash=__ret__.public_key_hash,
        self_link=__ret__.self_link,
        server_farm_id=__ret__.server_farm_id,
        site_name=__ret__.site_name,
        subject_name=__ret__.subject_name,
        tags=__ret__.tags,
        thumbprint=__ret__.thumbprint,
        type=__ret__.type,
        valid=__ret__.valid)


@_utilities.lift_output_func(get_certificate)
def get_certificate_output(name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCertificateResult]:
    """
    SSL certificate for an app.


    :param str name: Name of the certificate.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
