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
    'OrganizationResourcePropertiesOfferDetailArgs',
    'OrganizationResourcePropertiesUserDetailArgs',
]

@pulumi.input_type
class OrganizationResourcePropertiesOfferDetailArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 plan_name: Optional[pulumi.Input[str]] = None,
                 publisher_id: Optional[pulumi.Input[str]] = None,
                 term_unit: Optional[pulumi.Input[str]] = None):
        """
        Confluent offer detail
        :param pulumi.Input[str] id: Offer Id
        :param pulumi.Input[str] plan_id: Offer Plan Id
        :param pulumi.Input[str] plan_name: Offer Plan Name
        :param pulumi.Input[str] publisher_id: Publisher Id
        :param pulumi.Input[str] term_unit: Offer Plan Term unit
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if plan_id is not None:
            pulumi.set(__self__, "plan_id", plan_id)
        if plan_name is not None:
            pulumi.set(__self__, "plan_name", plan_name)
        if publisher_id is not None:
            pulumi.set(__self__, "publisher_id", publisher_id)
        if term_unit is not None:
            pulumi.set(__self__, "term_unit", term_unit)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Offer Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> Optional[pulumi.Input[str]]:
        """
        Offer Plan Id
        """
        return pulumi.get(self, "plan_id")

    @plan_id.setter
    def plan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "plan_id", value)

    @property
    @pulumi.getter(name="planName")
    def plan_name(self) -> Optional[pulumi.Input[str]]:
        """
        Offer Plan Name
        """
        return pulumi.get(self, "plan_name")

    @plan_name.setter
    def plan_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "plan_name", value)

    @property
    @pulumi.getter(name="publisherId")
    def publisher_id(self) -> Optional[pulumi.Input[str]]:
        """
        Publisher Id
        """
        return pulumi.get(self, "publisher_id")

    @publisher_id.setter
    def publisher_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "publisher_id", value)

    @property
    @pulumi.getter(name="termUnit")
    def term_unit(self) -> Optional[pulumi.Input[str]]:
        """
        Offer Plan Term unit
        """
        return pulumi.get(self, "term_unit")

    @term_unit.setter
    def term_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "term_unit", value)


@pulumi.input_type
class OrganizationResourcePropertiesUserDetailArgs:
    def __init__(__self__, *,
                 email_address: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None):
        """
        Subscriber detail
        :param pulumi.Input[str] email_address: Email address
        :param pulumi.Input[str] first_name: First name
        :param pulumi.Input[str] last_name: Last name
        """
        if email_address is not None:
            pulumi.set(__self__, "email_address", email_address)
        if first_name is not None:
            pulumi.set(__self__, "first_name", first_name)
        if last_name is not None:
            pulumi.set(__self__, "last_name", last_name)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> Optional[pulumi.Input[str]]:
        """
        Email address
        """
        return pulumi.get(self, "email_address")

    @email_address.setter
    def email_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_address", value)

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> Optional[pulumi.Input[str]]:
        """
        First name
        """
        return pulumi.get(self, "first_name")

    @first_name.setter
    def first_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "first_name", value)

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> Optional[pulumi.Input[str]]:
        """
        Last name
        """
        return pulumi.get(self, "last_name")

    @last_name.setter
    def last_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_name", value)


