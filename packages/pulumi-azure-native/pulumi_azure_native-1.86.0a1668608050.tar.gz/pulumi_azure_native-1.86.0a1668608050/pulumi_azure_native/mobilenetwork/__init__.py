# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .attached_data_network import *
from .data_network import *
from .get_attached_data_network import *
from .get_data_network import *
from .get_mobile_network import *
from .get_packet_core_control_plane import *
from .get_packet_core_data_plane import *
from .get_service import *
from .get_sim import *
from .get_sim_group import *
from .get_sim_policy import *
from .get_site import *
from .get_slice import *
from .list_mobile_network_sim_ids import *
from .mobile_network import *
from .packet_core_control_plane import *
from .packet_core_data_plane import *
from .service import *
from .sim import *
from .sim_group import *
from .sim_policy import *
from .site import *
from .slice import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.mobilenetwork.v20220301preview as __v20220301preview
    v20220301preview = __v20220301preview
    import pulumi_azure_native.mobilenetwork.v20220401preview as __v20220401preview
    v20220401preview = __v20220401preview
else:
    v20220301preview = _utilities.lazy_import('pulumi_azure_native.mobilenetwork.v20220301preview')
    v20220401preview = _utilities.lazy_import('pulumi_azure_native.mobilenetwork.v20220401preview')

