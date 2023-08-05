# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .budget import *
from .get_budget import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.consumption.v20171230preview as __v20171230preview
    v20171230preview = __v20171230preview
    import pulumi_azure_native.consumption.v20180131 as __v20180131
    v20180131 = __v20180131
    import pulumi_azure_native.consumption.v20180331 as __v20180331
    v20180331 = __v20180331
    import pulumi_azure_native.consumption.v20180630 as __v20180630
    v20180630 = __v20180630
    import pulumi_azure_native.consumption.v20180831 as __v20180831
    v20180831 = __v20180831
    import pulumi_azure_native.consumption.v20181001 as __v20181001
    v20181001 = __v20181001
    import pulumi_azure_native.consumption.v20190101 as __v20190101
    v20190101 = __v20190101
    import pulumi_azure_native.consumption.v20190401preview as __v20190401preview
    v20190401preview = __v20190401preview
    import pulumi_azure_native.consumption.v20190501 as __v20190501
    v20190501 = __v20190501
    import pulumi_azure_native.consumption.v20190501preview as __v20190501preview
    v20190501preview = __v20190501preview
    import pulumi_azure_native.consumption.v20190601 as __v20190601
    v20190601 = __v20190601
    import pulumi_azure_native.consumption.v20191001 as __v20191001
    v20191001 = __v20191001
    import pulumi_azure_native.consumption.v20191101 as __v20191101
    v20191101 = __v20191101
    import pulumi_azure_native.consumption.v20210501 as __v20210501
    v20210501 = __v20210501
    import pulumi_azure_native.consumption.v20211001 as __v20211001
    v20211001 = __v20211001
else:
    v20171230preview = _utilities.lazy_import('pulumi_azure_native.consumption.v20171230preview')
    v20180131 = _utilities.lazy_import('pulumi_azure_native.consumption.v20180131')
    v20180331 = _utilities.lazy_import('pulumi_azure_native.consumption.v20180331')
    v20180630 = _utilities.lazy_import('pulumi_azure_native.consumption.v20180630')
    v20180831 = _utilities.lazy_import('pulumi_azure_native.consumption.v20180831')
    v20181001 = _utilities.lazy_import('pulumi_azure_native.consumption.v20181001')
    v20190101 = _utilities.lazy_import('pulumi_azure_native.consumption.v20190101')
    v20190401preview = _utilities.lazy_import('pulumi_azure_native.consumption.v20190401preview')
    v20190501 = _utilities.lazy_import('pulumi_azure_native.consumption.v20190501')
    v20190501preview = _utilities.lazy_import('pulumi_azure_native.consumption.v20190501preview')
    v20190601 = _utilities.lazy_import('pulumi_azure_native.consumption.v20190601')
    v20191001 = _utilities.lazy_import('pulumi_azure_native.consumption.v20191001')
    v20191101 = _utilities.lazy_import('pulumi_azure_native.consumption.v20191101')
    v20210501 = _utilities.lazy_import('pulumi_azure_native.consumption.v20210501')
    v20211001 = _utilities.lazy_import('pulumi_azure_native.consumption.v20211001')

