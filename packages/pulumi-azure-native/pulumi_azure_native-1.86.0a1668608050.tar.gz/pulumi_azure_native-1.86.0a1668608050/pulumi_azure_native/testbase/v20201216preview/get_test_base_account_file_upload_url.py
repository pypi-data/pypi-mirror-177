# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetTestBaseAccountFileUploadUrlResult',
    'AwaitableGetTestBaseAccountFileUploadUrlResult',
    'get_test_base_account_file_upload_url',
    'get_test_base_account_file_upload_url_output',
]

@pulumi.output_type
class GetTestBaseAccountFileUploadUrlResult:
    """
    The URL response
    """
    def __init__(__self__, blob_path=None, upload_url=None):
        if blob_path and not isinstance(blob_path, str):
            raise TypeError("Expected argument 'blob_path' to be a str")
        pulumi.set(__self__, "blob_path", blob_path)
        if upload_url and not isinstance(upload_url, str):
            raise TypeError("Expected argument 'upload_url' to be a str")
        pulumi.set(__self__, "upload_url", upload_url)

    @property
    @pulumi.getter(name="blobPath")
    def blob_path(self) -> str:
        """
        The blob path of the uploaded package. It will be used as the 'blobPath' property of PackageResource.
        """
        return pulumi.get(self, "blob_path")

    @property
    @pulumi.getter(name="uploadUrl")
    def upload_url(self) -> str:
        """
        The URL used for uploading the package.
        """
        return pulumi.get(self, "upload_url")


class AwaitableGetTestBaseAccountFileUploadUrlResult(GetTestBaseAccountFileUploadUrlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTestBaseAccountFileUploadUrlResult(
            blob_path=self.blob_path,
            upload_url=self.upload_url)


def get_test_base_account_file_upload_url(blob_name: Optional[str] = None,
                                          resource_group_name: Optional[str] = None,
                                          test_base_account_name: Optional[str] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTestBaseAccountFileUploadUrlResult:
    """
    The URL response


    :param str blob_name: The custom file name of the uploaded blob.
    :param str resource_group_name: The name of the resource group that contains the resource.
    :param str test_base_account_name: The resource name of the Test Base Account.
    """
    __args__ = dict()
    __args__['blobName'] = blob_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['testBaseAccountName'] = test_base_account_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:testbase/v20201216preview:getTestBaseAccountFileUploadUrl', __args__, opts=opts, typ=GetTestBaseAccountFileUploadUrlResult).value

    return AwaitableGetTestBaseAccountFileUploadUrlResult(
        blob_path=__ret__.blob_path,
        upload_url=__ret__.upload_url)


@_utilities.lift_output_func(get_test_base_account_file_upload_url)
def get_test_base_account_file_upload_url_output(blob_name: Optional[pulumi.Input[Optional[str]]] = None,
                                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                                 test_base_account_name: Optional[pulumi.Input[str]] = None,
                                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTestBaseAccountFileUploadUrlResult]:
    """
    The URL response


    :param str blob_name: The custom file name of the uploaded blob.
    :param str resource_group_name: The name of the resource group that contains the resource.
    :param str test_base_account_name: The resource name of the Test Base Account.
    """
    ...
