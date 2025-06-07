import json
import os

import supervisely as sly
from dotenv import load_dotenv

TASK_DESCR = "task_for_demo"
SKIPPABLE_STATUSES = ["stopped", "error"]

if sly.is_development():
    load_dotenv(os.path.expanduser("~/supervisely-demo.env"))
    load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
active_agent_id = sly.env.agent_id()

api: sly.Api = sly.Api.from_env()
sly.logger.info(
    f"API instance created for team_id={team_id}, workspace_id={workspace_id}, "
    f"Agent ID={active_agent_id}."
)

stopping_session = os.getenv("modal.state.stoppingSession", "false").lower() == "true"
if stopping_session:
    sly.logger.info(
        "The app is launched in stopping session mode. Will find all the tasks "
        "and stop them."
    )

images_modal = os.getenv("modal.state.images", "false").lower() == "true"
videos_modal = os.getenv("modal.state.videos", "false").lower() == "true"
volumes_modal = os.getenv("modal.state.volumes", "false").lower() == "true"
pointclouds_modal = os.getenv("modal.state.pointclouds", "false").lower() == "true"

all_entities = [
    ("images", images_modal),
    ("videos", videos_modal),
    ("volumes", volumes_modal),
    ("pointclouds", pointclouds_modal),
]

sly.logger.info(
    f"Configuration loaded: images_modal={images_modal}, videos_modal={videos_modal}, "
    f"volumes_modal={volumes_modal}, pointclouds_modal={pointclouds_modal}."
)

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
presets_json = os.path.join(parent_dir, "presets.json")
if not os.path.exists(presets_json):
    raise FileNotFoundError(
        f"Presets file not found: {presets_json}. "
        "Please ensure the presets.json file is in the current working directory."
    )

with open(presets_json, "r") as file:
    presets = json.load(file)
sly.logger.info(f"Presets loaded from {presets_json}.")

active_module_ids = []

for entity_name, entity_activated in all_entities:
    if entity_activated:
        entity_module_ids = presets.get(entity_name, [])
        active_module_ids.extend(entity_module_ids)

# Filter out duplicates from the list of active module IDs.
active_module_ids = list(set(active_module_ids))

sly.logger.info(
    f"Module IDs loaded: {active_module_ids}. These modules will be used to launch tasks."
)
