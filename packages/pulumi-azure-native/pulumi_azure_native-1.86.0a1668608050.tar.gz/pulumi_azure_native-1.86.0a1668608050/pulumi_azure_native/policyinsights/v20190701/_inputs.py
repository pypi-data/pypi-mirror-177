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

__all__ = [
    'RemediationFiltersArgs',
]

@pulumi.input_type
class RemediationFiltersArgs:
    def __init__(__self__, *,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The filters that will be applied to determine which resources to remediate.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations: The resource locations that will be remediated.
        """
        if locations is not None:
            pulumi.set(__self__, "locations", locations)

    @property
    @pulumi.getter
    def locations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The resource locations that will be remediated.
        """
        return pulumi.get(self, "locations")

    @locations.setter
    def locations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "locations", value)


