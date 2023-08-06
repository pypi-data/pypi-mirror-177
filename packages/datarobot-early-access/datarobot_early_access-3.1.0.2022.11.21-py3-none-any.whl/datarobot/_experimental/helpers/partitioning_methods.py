#
# Copyright 2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.

from typing import Any

from datarobot.helpers.partitioning_methods import (
    DatetimePartitioning as datarobot_datetime_partitioning,
)
from datarobot.helpers.partitioning_methods import DatetimePartitioningSpecification


class DatetimePartitioning(
    datarobot_datetime_partitioning
):  # pylint: disable=missing-class-docstring
    @classmethod
    def datetime_partitioning_log_retrieve(
        cls, project_id: str, datetime_partitioning_id: str
    ) -> Any:
        """Retrieve the datetime partitioning log content for an optimized datetime partitioning.

        The Datetime Partitioning Log provides details about the partitioning process for an OTV
        or Time Series project.

        Parameters
        ----------
        project_id : str
            project id of the project associated with the datetime partitioning.
        datetime_partitioning_id : str
            id of the optimized datetime partitioning
        """
        url = (
            f"projects/{project_id}/optimizedDatetimePartitionings/{datetime_partitioning_id}/"
            "datetimePartitioningLog/file/"
        )
        response = cls._client.get(url)
        return response.text

    @classmethod
    def get_input_data(
        cls, project_id: str, datetime_partitioning_id: str
    ) -> DatetimePartitioningSpecification:
        """Retrieve the input used to create an Optimized DatetimePartitioning from a project for
        the specified datetime_partitioning_id. A datetime_partitioning_id is created by using the
        :meth:`generate_optimized<datarobot.DatetimePartitioning.generate_optimized>` function.

        Parameters
        ----------
        project_id : str
            the id of the project to retrieve partitioning for
        datetime_partitioning_id : ObjectId
            the ObjectId associated with the project to retrieve from mongo

        Returns
        -------
        DatetimePartitioningInput : the input to optimized datetime partitioning
        """
        url = "projects/{}/optimizedDatetimePartitionings/{}/datetimePartitioningInput/".format(
            project_id, datetime_partitioning_id
        )
        response = cls._client.get(url)
        return DatetimePartitioningSpecification.from_server_data(  # type: ignore[no-untyped-call, no-any-return]
            response.json()
        )
