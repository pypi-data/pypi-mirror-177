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
    'PolicyVariableColumnArgs',
    'PolicyVariableValueColumnValueArgs',
]

@pulumi.input_type
class PolicyVariableColumnArgs:
    def __init__(__self__, *,
                 column_name: pulumi.Input[str]):
        """
        The variable column.
        :param pulumi.Input[str] column_name: The name of this policy variable column.
        """
        pulumi.set(__self__, "column_name", column_name)

    @property
    @pulumi.getter(name="columnName")
    def column_name(self) -> pulumi.Input[str]:
        """
        The name of this policy variable column.
        """
        return pulumi.get(self, "column_name")

    @column_name.setter
    def column_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "column_name", value)


@pulumi.input_type
class PolicyVariableValueColumnValueArgs:
    def __init__(__self__, *,
                 column_name: pulumi.Input[str],
                 column_value: Any):
        """
        The name value tuple for this variable value column.
        :param pulumi.Input[str] column_name: Column name for the variable value
        :param Any column_value: Column value for the variable value; this can be an integer, double, boolean, null or a string.
        """
        pulumi.set(__self__, "column_name", column_name)
        pulumi.set(__self__, "column_value", column_value)

    @property
    @pulumi.getter(name="columnName")
    def column_name(self) -> pulumi.Input[str]:
        """
        Column name for the variable value
        """
        return pulumi.get(self, "column_name")

    @column_name.setter
    def column_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "column_name", value)

    @property
    @pulumi.getter(name="columnValue")
    def column_value(self) -> Any:
        """
        Column value for the variable value; this can be an integer, double, boolean, null or a string.
        """
        return pulumi.get(self, "column_value")

    @column_value.setter
    def column_value(self, value: Any):
        pulumi.set(self, "column_value", value)


