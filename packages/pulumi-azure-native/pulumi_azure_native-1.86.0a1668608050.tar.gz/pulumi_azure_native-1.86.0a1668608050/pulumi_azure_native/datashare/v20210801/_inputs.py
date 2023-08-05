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
    'IdentityArgs',
    'TableLevelSharingPropertiesArgs',
]

@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input[Union[str, 'Type']]] = None):
        """
        Identity of resource
        :param pulumi.Input[Union[str, 'Type']] type: Identity Type
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'Type']]]:
        """
        Identity Type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'Type']]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class TableLevelSharingPropertiesArgs:
    def __init__(__self__, *,
                 external_tables_to_exclude: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 external_tables_to_include: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 materialized_views_to_exclude: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 materialized_views_to_include: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tables_to_exclude: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tables_to_include: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Table level sharing properties dto for kusto data set properties
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_tables_to_exclude: External tables to be excluded in the data set
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_tables_to_include: External tables to be included in the data set
        :param pulumi.Input[Sequence[pulumi.Input[str]]] materialized_views_to_exclude: Materialized views to be excluded in the data set
        :param pulumi.Input[Sequence[pulumi.Input[str]]] materialized_views_to_include: Materialized views to be included in the data set
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tables_to_exclude: Tables to be excluded in the data set
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tables_to_include: Tables to be included in the data set
        """
        if external_tables_to_exclude is not None:
            pulumi.set(__self__, "external_tables_to_exclude", external_tables_to_exclude)
        if external_tables_to_include is not None:
            pulumi.set(__self__, "external_tables_to_include", external_tables_to_include)
        if materialized_views_to_exclude is not None:
            pulumi.set(__self__, "materialized_views_to_exclude", materialized_views_to_exclude)
        if materialized_views_to_include is not None:
            pulumi.set(__self__, "materialized_views_to_include", materialized_views_to_include)
        if tables_to_exclude is not None:
            pulumi.set(__self__, "tables_to_exclude", tables_to_exclude)
        if tables_to_include is not None:
            pulumi.set(__self__, "tables_to_include", tables_to_include)

    @property
    @pulumi.getter(name="externalTablesToExclude")
    def external_tables_to_exclude(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        External tables to be excluded in the data set
        """
        return pulumi.get(self, "external_tables_to_exclude")

    @external_tables_to_exclude.setter
    def external_tables_to_exclude(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "external_tables_to_exclude", value)

    @property
    @pulumi.getter(name="externalTablesToInclude")
    def external_tables_to_include(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        External tables to be included in the data set
        """
        return pulumi.get(self, "external_tables_to_include")

    @external_tables_to_include.setter
    def external_tables_to_include(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "external_tables_to_include", value)

    @property
    @pulumi.getter(name="materializedViewsToExclude")
    def materialized_views_to_exclude(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Materialized views to be excluded in the data set
        """
        return pulumi.get(self, "materialized_views_to_exclude")

    @materialized_views_to_exclude.setter
    def materialized_views_to_exclude(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "materialized_views_to_exclude", value)

    @property
    @pulumi.getter(name="materializedViewsToInclude")
    def materialized_views_to_include(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Materialized views to be included in the data set
        """
        return pulumi.get(self, "materialized_views_to_include")

    @materialized_views_to_include.setter
    def materialized_views_to_include(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "materialized_views_to_include", value)

    @property
    @pulumi.getter(name="tablesToExclude")
    def tables_to_exclude(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tables to be excluded in the data set
        """
        return pulumi.get(self, "tables_to_exclude")

    @tables_to_exclude.setter
    def tables_to_exclude(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tables_to_exclude", value)

    @property
    @pulumi.getter(name="tablesToInclude")
    def tables_to_include(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Tables to be included in the data set
        """
        return pulumi.get(self, "tables_to_include")

    @tables_to_include.setter
    def tables_to_include(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tables_to_include", value)


