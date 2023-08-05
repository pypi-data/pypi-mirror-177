# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .arc_setting import *
from .cluster import *
from .extension import *
from .get_arc_setting import *
from .get_cluster import *
from .get_extension import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.azurestackhci.v20200301preview as __v20200301preview
    v20200301preview = __v20200301preview
    import pulumi_azure_native.azurestackhci.v20201001 as __v20201001
    v20201001 = __v20201001
    import pulumi_azure_native.azurestackhci.v20210101preview as __v20210101preview
    v20210101preview = __v20210101preview
    import pulumi_azure_native.azurestackhci.v20210701preview as __v20210701preview
    v20210701preview = __v20210701preview
    import pulumi_azure_native.azurestackhci.v20210901 as __v20210901
    v20210901 = __v20210901
    import pulumi_azure_native.azurestackhci.v20220101 as __v20220101
    v20220101 = __v20220101
    import pulumi_azure_native.azurestackhci.v20220301 as __v20220301
    v20220301 = __v20220301
    import pulumi_azure_native.azurestackhci.v20220501 as __v20220501
    v20220501 = __v20220501
    import pulumi_azure_native.azurestackhci.v20220901 as __v20220901
    v20220901 = __v20220901
    import pulumi_azure_native.azurestackhci.v20221001 as __v20221001
    v20221001 = __v20221001
else:
    v20200301preview = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20200301preview')
    v20201001 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20201001')
    v20210101preview = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20210101preview')
    v20210701preview = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20210701preview')
    v20210901 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20210901')
    v20220101 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20220101')
    v20220301 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20220301')
    v20220501 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20220501')
    v20220901 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20220901')
    v20221001 = _utilities.lazy_import('pulumi_azure_native.azurestackhci.v20221001')

