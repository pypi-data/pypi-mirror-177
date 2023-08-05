# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .get_machine import *
from .get_machine_extension import *
from .get_private_endpoint_connection import *
from .get_private_link_scope import *
from .get_private_link_scoped_resource import *
from .machine import *
from .machine_extension import *
from .private_endpoint_connection import *
from .private_link_scope import *
from .private_link_scoped_resource import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.hybridcompute.v20190318preview as __v20190318preview
    v20190318preview = __v20190318preview
    import pulumi_azure_native.hybridcompute.v20190802preview as __v20190802preview
    v20190802preview = __v20190802preview
    import pulumi_azure_native.hybridcompute.v20191212 as __v20191212
    v20191212 = __v20191212
    import pulumi_azure_native.hybridcompute.v20200730preview as __v20200730preview
    v20200730preview = __v20200730preview
    import pulumi_azure_native.hybridcompute.v20200802 as __v20200802
    v20200802 = __v20200802
    import pulumi_azure_native.hybridcompute.v20200815preview as __v20200815preview
    v20200815preview = __v20200815preview
    import pulumi_azure_native.hybridcompute.v20210128preview as __v20210128preview
    v20210128preview = __v20210128preview
    import pulumi_azure_native.hybridcompute.v20210325preview as __v20210325preview
    v20210325preview = __v20210325preview
    import pulumi_azure_native.hybridcompute.v20210422preview as __v20210422preview
    v20210422preview = __v20210422preview
    import pulumi_azure_native.hybridcompute.v20210517preview as __v20210517preview
    v20210517preview = __v20210517preview
    import pulumi_azure_native.hybridcompute.v20210520 as __v20210520
    v20210520 = __v20210520
    import pulumi_azure_native.hybridcompute.v20210610preview as __v20210610preview
    v20210610preview = __v20210610preview
    import pulumi_azure_native.hybridcompute.v20211210preview as __v20211210preview
    v20211210preview = __v20211210preview
    import pulumi_azure_native.hybridcompute.v20220310 as __v20220310
    v20220310 = __v20220310
    import pulumi_azure_native.hybridcompute.v20220510preview as __v20220510preview
    v20220510preview = __v20220510preview
    import pulumi_azure_native.hybridcompute.v20220811preview as __v20220811preview
    v20220811preview = __v20220811preview
else:
    v20190318preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20190318preview')
    v20190802preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20190802preview')
    v20191212 = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20191212')
    v20200730preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20200730preview')
    v20200802 = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20200802')
    v20200815preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20200815preview')
    v20210128preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20210128preview')
    v20210325preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20210325preview')
    v20210422preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20210422preview')
    v20210517preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20210517preview')
    v20210520 = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20210520')
    v20210610preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20210610preview')
    v20211210preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20211210preview')
    v20220310 = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20220310')
    v20220510preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20220510preview')
    v20220811preview = _utilities.lazy_import('pulumi_azure_native.hybridcompute.v20220811preview')

