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

from typing import (
    List,
    Optional,
)

from fireopal.types import Credentials

from .base import fire_opal_workflow


@fire_opal_workflow("validate_input_circuits_workflow")
def validate(
    circuits: List[str],
    credentials: Optional[Credentials] = None,
    backend: Optional[str] = None,
):
    """
    Fire Opal function to validate input circuits.

    Parameters
    ----------
    circuits : List[str]
        A list of quantum circuit in the form QASM string. You can use Qiskit to
        generate these strings.
    credentials : Credentials, optional
        The credentials for running circuits on an IBM backend. This dictionary should
        contain key-value entries with keys `token`, `project`, `hub`, and `group`.
    backend : str, optional
        The backend device that should be used to run circuits.
    """
    return {
        "circuits": circuits,
        "credentials": credentials,
        "backend": backend,
    }
