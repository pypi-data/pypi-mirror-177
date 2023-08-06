# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from dataclasses import dataclass

# pylint:disable=too-few-public-methods


@dataclass
class Credentials:
    """
    Credentials for running circuits on an IBM backend.
    For more information on the fields, see:
    https://quantum-computing.ibm.com/lab/docs/iql/manage/account/ibmq

    Parameters
    ----------
    token : str
        An IBM account API token.
    project : str
        The IBM project.
    hub : str
        The IBM hub.
    group : str
        The IBM group.
    """

    token: str
    project: str
    hub: str
    group: str
