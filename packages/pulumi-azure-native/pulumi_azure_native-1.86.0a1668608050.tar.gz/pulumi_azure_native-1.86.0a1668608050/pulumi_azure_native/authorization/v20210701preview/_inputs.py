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
    'AccessReviewInstanceArgs',
    'AccessReviewReviewerArgs',
]

@pulumi.input_type
class AccessReviewInstanceArgs:
    def __init__(__self__, *,
                 backup_reviewers: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]] = None,
                 end_date_time: Optional[pulumi.Input[str]] = None,
                 reviewers: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]] = None,
                 start_date_time: Optional[pulumi.Input[str]] = None):
        """
        Access Review Instance.
        :param pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]] backup_reviewers: This is the collection of backup reviewers.
        :param pulumi.Input[str] end_date_time: The DateTime when the review instance is scheduled to end.
        :param pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]] reviewers: This is the collection of reviewers.
        :param pulumi.Input[str] start_date_time: The DateTime when the review instance is scheduled to be start.
        """
        if backup_reviewers is not None:
            pulumi.set(__self__, "backup_reviewers", backup_reviewers)
        if end_date_time is not None:
            pulumi.set(__self__, "end_date_time", end_date_time)
        if reviewers is not None:
            pulumi.set(__self__, "reviewers", reviewers)
        if start_date_time is not None:
            pulumi.set(__self__, "start_date_time", start_date_time)

    @property
    @pulumi.getter(name="backupReviewers")
    def backup_reviewers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]:
        """
        This is the collection of backup reviewers.
        """
        return pulumi.get(self, "backup_reviewers")

    @backup_reviewers.setter
    def backup_reviewers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]):
        pulumi.set(self, "backup_reviewers", value)

    @property
    @pulumi.getter(name="endDateTime")
    def end_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        The DateTime when the review instance is scheduled to end.
        """
        return pulumi.get(self, "end_date_time")

    @end_date_time.setter
    def end_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_date_time", value)

    @property
    @pulumi.getter
    def reviewers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]:
        """
        This is the collection of reviewers.
        """
        return pulumi.get(self, "reviewers")

    @reviewers.setter
    def reviewers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]):
        pulumi.set(self, "reviewers", value)

    @property
    @pulumi.getter(name="startDateTime")
    def start_date_time(self) -> Optional[pulumi.Input[str]]:
        """
        The DateTime when the review instance is scheduled to be start.
        """
        return pulumi.get(self, "start_date_time")

    @start_date_time.setter
    def start_date_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_date_time", value)


@pulumi.input_type
class AccessReviewReviewerArgs:
    def __init__(__self__, *,
                 principal_id: Optional[pulumi.Input[str]] = None):
        """
        Descriptor for what needs to be reviewed
        :param pulumi.Input[str] principal_id: The id of the reviewer(user/servicePrincipal)
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the reviewer(user/servicePrincipal)
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)


