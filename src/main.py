from typing import List

import supervisely as sly

from src.config import (
    SKIPPABLE_STATUSES,
    TASK_DESCR,
    active_agent_id,
    active_module_ids,
    api,
    stopping_session,
    workspace_id,
)


def launch_tasks(
    module_ids: List[int],
    agent_id: int,
    workspace_id: int,
    description: str,
) -> None:
    """Launch tasks for the specified modules in the given workspace.

    :param module_ids: List of module IDs to launch tasks for.
    :type module_ids: List[int]
    :param agent_id: ID of the agent to launch tasks on.
    :type agent_id: int
    :param workspace_id: ID of the workspace to launch tasks in.
    :type workspace_id: int
    :param description: Description for the tasks being launched.
    :type description: str
    """
    for module_id in module_ids:
        task_info = api.task.start(
            agent_id=agent_id,
            module_id=module_id,
            workspace_id=workspace_id,
            description=description,
        )

        sly.logger.info(
            f"Task started: {task_info.get('id')} for module_id={module_id}."
        )
    sly.logger.info(
        f"All tasks launched for agent_id={agent_id} in workspace_id={workspace_id}."
    )


def find_and_stop_tasks(workspace_id: int, description: str) -> None:
    """
    Find and stop all tasks in the specified workspace with the given description.

    :param workspace_id: ID of the workspace to search for tasks.
    :type workspace_id: int
    :param description: Description of the tasks to stop.
    :type description: str
    """
    tasks = api.task.get_list(workspace_id=workspace_id)
    for task in tasks:
        if task.get("description") == description:
            if task.get("status") in SKIPPABLE_STATUSES:
                continue
            task_id = task.get("id")
            try:
                api.task.stop(task_id)
                sly.logger.info(f"Task {task_id} stopped successfully.")
            except Exception as e:
                sly.logger.warning(f"Failed to stop task {task_id}: {e}")


if __name__ == "__main__":
    if stopping_session:
        sly.logger.info("App is in stopping mode, will not launch new tasks.")
        find_and_stop_tasks(workspace_id=workspace_id, description=TASK_DESCR)

    else:
        sly.logger.info("Launching tasks for active modules.")
        if not active_module_ids:
            sly.logger.warning("No active modules found. Exiting.")
        else:
            launch_tasks(
                module_ids=active_module_ids,
                agent_id=active_agent_id,
                workspace_id=workspace_id,
                description=TASK_DESCR,
            )
