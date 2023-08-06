import pickle
import sys
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, Optional

import inquirer as i
import toml
import typer
from rich import print
from streamlit.web import cli as stcli

import encord_active.app.conf  # pylint: disable=unused-import
from encord_active.app.app_config import CONFIG_PROPERTIES, AppConfig
from encord_active.app.app_print_utils import get_projects_json
from encord_active.app.common.cli_helpers import choose_local_project, get_local_project
from encord_active.app.db.predictions import (
    import_predictions as app_import_predictions,
)
from encord_active.lib.metrics.fetch_prebuilt_metrics import (
    PREBUILT_PROJECT_TO_STORAGE,
    PREBUILT_PROJECTS,
    fetch_metric,
)

APP_NAME = "encord-active"

cli = typer.Typer(
    rich_markup_mode="markdown",
    help="""
All commands in this CLI have a --help option, which will guide you on the way.
If you don't find the information you need here, we recommend that you visit
our main documentation: https://encord-active-docs.web.app
""",
    epilog="""
Made by Encord. Contact Encord here: https://encord.com/contact_us/ to learn more

about our active learning platform for computer vision.
""",
)
config_cli = typer.Typer()
import_cli = typer.Typer()
print_cli = typer.Typer(rich_markup_mode="markdown")
cli.add_typer(config_cli, name="config", help="Configure global settings 🔧")
cli.add_typer(import_cli, name="import", help="Import Projects or Predictions ⬇️")
cli.add_typer(print_cli, name="print")

__PREBUILT_PROJECT_NAMES = list(PREBUILT_PROJECTS.keys())


config = AppConfig(APP_NAME)
state: Dict[str, Any] = {}


@config_cli.command()
def list():
    """
    List Encord Active configuration properties.
    """
    print(toml.dumps(config.contents) or "[bold red]Nothing configured.")


def _check_property(property: str):
    if property not in CONFIG_PROPERTIES:
        print(f"[bold red]`{property}` is not a valid property.")
        print("Valid properties are:")
        print(CONFIG_PROPERTIES)
        exit()


@config_cli.command()
def get(
    property: str = typer.Argument(..., help="Name of the property"),
):
    """
    Print the value of an Encord Active configuration property.
    """
    _check_property(property)
    value = config.contents.get(property)
    print(f"{property} = {value}" or f"[bold red]Property `{property}` not configured.")


@config_cli.command()
def set(
    property: str = typer.Argument(..., help="Name of the property"),
    value: str = typer.Argument(..., help="Value to set"),
):
    """
    Sets an Encord Active configuration property.
    """
    _check_property(property)
    config.contents[property] = value
    config.save()

    print(f"[bold green]Property `{property}` has been set.")


@config_cli.command()
def unset(
    property: str = typer.Argument(..., help="Name of the property"),
):
    """
    Unsets the value of an Encord Active configuration property.
    """
    _check_property(property)
    del config.contents[property]
    config.save()

    print(f"[bold green]Property `{property}` was unset.")


@cli.command()
def download(
    project_name: str = typer.Option(
        None, help=f"Name of the chosen project. Available prebuilt projects: {__PREBUILT_PROJECT_NAMES}."
    ),
):
    """
    Try out Encord Active fast. **Download** an existing dataset to get started. 📁

    * If --project_name is not given as an argument, available prebuilt projects will be listed
     and the user can select one from the menu.
    """
    project_parent_dir = config.get_or_query_project_path()

    if project_name is not None and project_name not in PREBUILT_PROJECTS:
        print("No such project in prebuilt projects.")
        raise typer.Abort()

    if not project_name:
        project_names_with_storage = [p + f" ({PREBUILT_PROJECT_TO_STORAGE[p]})" for p in __PREBUILT_PROJECT_NAMES]
        questions = [i.List("project_name", message="Choose a project", choices=project_names_with_storage)]
        answers = i.prompt(questions)
        if not answers or "project_name" not in answers:
            print("No project was selected.")
            raise typer.Abort()
        project_name = answers["project_name"].split(" ", maxsplit=1)[0]

    # create project folder
    project_dir = project_parent_dir / project_name
    project_dir.mkdir(exist_ok=True)

    fetch_metric(project_name, project_dir)


@import_cli.command(name="predictions")
def import_predictions(
    predictions_path: Path = typer.Argument(
        ...,
        help="Path of the project to which you would like to import the predictions into",
        dir_okay=False,
    ),
):
    """
    **Imports** a predictions file. The predictions should be in a using the `Prediction` model and stored in a pkl file :brain:
    """

    project_dir = choose_local_project(config)
    if not project_dir:
        raise typer.Abort()

    project = get_local_project(project_dir)

    with open(predictions_path, "rb") as f:
        predictions = pickle.load(f)

    app_import_predictions(project, project_dir, predictions)


@import_cli.command(name="project")
def import_project():
    """
    **Imports** a project from Encord 📦
    """
    from encord_active.lib.metrics.import_encord_project import main as import_script

    # TODO: move the setup into a config command.
    # currently the import setup will run every time.
    import_script(config)


@print_cli.command(name="encord-projects")
def print_encord_projects(
    query: Optional[str] = typer.Option(None, help="Optional fuzzy title filter; SQL syntax."),
):
    """
    Print the mapping between \`project_hash\`es of your Encord projects and their titles.

    You can query projects by title with the SQL fuzzy syntax. To look for a title including "validation" you would do:

    > encord-active print encord-projects --query "%validation%"

    """
    json_projects = get_projects_json(config, query)
    if state.get("json_output"):
        Path("./encord-projects.json").write_text(json_projects, encoding="utf-8")
    else:
        print(json_projects)


@print_cli.command(name="ontology")
def print_ontology():
    """
    **Prints** an ontology mapping between the class name to the `featureNodeHash` JSON format.
    """
    project_dir = choose_local_project(config)
    if not project_dir:
        raise typer.Abort()

    project = get_local_project(project_dir)
    objects = project.ontology["objects"]

    ontology = {o["name"].lower(): o["featureNodeHash"] for o in objects}
    json_ontology = json_dumps(ontology, indent=2)

    if state.get("json_output"):
        Path("./ontology.json").write_text(json_ontology, encoding="utf-8")
        print("Stored mapping in [blue]`./ontology.json`")
    else:
        print(json_ontology)


@print_cli.command(name="data-mapping")
def print_data_mapping(limit: int = typer.Option(None, help="Limit the result to the first `limit` data hashes")):
    """
    **Prints** a mapping between `data_hashes` and their corresponding `filename`
    """
    project_dir = choose_local_project(config)
    if not project_dir:
        raise typer.Abort()

    mapping: Dict[str, str] = {}

    for label in (project_dir / "data").iterdir():
        if not label.is_dir() and not (label / "label_row.json").is_file():
            continue

        label_row = json_loads((label / "label_row.json").read_text())
        mapping = {
            **mapping,
            **{data_hash: value["data_title"] for data_hash, value in label_row["data_units"].items()},
        }
        if limit and len(mapping) > limit:
            break

    if limit and limit < len(mapping):
        mapping = {k: v for i, (k, v) in enumerate(mapping.items()) if i < limit}

    json_mapping = json_dumps(mapping, indent=2)

    if state.get("json_output"):
        Path("./data_mapping.json").write_text(json_mapping, encoding="utf-8")
        print("Stored mapping in [blue]`./data_mapping.json`")
    else:
        print(json_mapping)


@print_cli.callback()
def main(json: bool = False):  # pylint: disable=redefined-outer-name
    """
    Print useful information 🖨️
    """
    state["json_output"] = json


@cli.command()
def visualise(
    project_path: Optional[Path] = typer.Argument(
        None,
        help="Path of the project you would like to visualise",
        file_okay=False,
    ),
):
    """
    Launches the application with the provided project ✨
    """
    streamlit_page = (Path(__file__).parent / "streamlit_entrypoint.py").expanduser().absolute()

    project_path = project_path or choose_local_project(config)

    if not project_path:
        raise typer.Abort()

    data_dir = project_path.expanduser().absolute().as_posix()
    sys.argv = ["streamlit", "run", streamlit_page.as_posix(), data_dir]
    sys.exit(stcli.main())  # pylint: disable=no-value-for-parameter


if __name__ == "__main__":
    cli(prog_name=APP_NAME)
