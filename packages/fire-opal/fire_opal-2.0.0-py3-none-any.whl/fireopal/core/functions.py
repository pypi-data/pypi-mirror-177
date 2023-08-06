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

from functools import wraps
from typing import Callable


def start_core_workflow(get_config: Callable, workflow: str):
    """Decorator for a function which will execute a workflow.
    The decorated function should return the data to be used
    during workflow execution. When being used in a client
    package, it is recommended to use a partial to provide
    a default value for `get_config` e.g.

    fire_opal_workflow = partial(
        start_core_workflow,
        get_fire_opal_config
    )

    @fire_opal_workflow("execute")
    def execute(...):

    Parameters
    ----------
    get_config : Callable
        Returns a `CoreClientSettings` instance. The configured
        router will be used to execute the workflow.
    workflow : str
        The registered name of the workflow to be executed.
    """

    def decorator(func: Callable):
        @wraps(func)
        def customized_decorator(*args, **kwargs):
            data = func(*args, **kwargs)
            config = get_config()
            router = config.get_router()
            result = router(workflow, data)
            return result

        return customized_decorator

    return decorator
