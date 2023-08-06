import logging
from pathlib import Path
from typing import Optional

import daiquiri
import typer
import yaml  # type: ignore
from pptx import Presentation as open_presentation
from pptx.presentation import Presentation
from typer import FileBinaryRead, FileBinaryWrite, Typer

from dbnomics_pptx_tools.dbnomics_api import SeriesLoadError, fetch_presentation_series
from dbnomics_pptx_tools.metadata import PresentationMetadata
from dbnomics_pptx_tools.module_utils import load_python_module_from_path
from dbnomics_pptx_tools.slides import delete_other_slides, update_slides

app = Typer()

logger = daiquiri.getLogger(__name__)


DBNOMICS_API_CACHE_DIR_NAME = "dbnomics_api_cache"


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def main(verbose: bool = typer.Option(False, "-v")):
    """
    DBnomics PowerPoint (pptx) tools.
    """
    daiquiri.setup()
    if verbose:
        daiquiri.set_default_log_levels([(__package__, logging.DEBUG)])


def parse_range(value: str) -> set[int]:
    """Parse ranges like "1-10,3,4,23-47"."""
    result: set[int] = set()
    for part in value.split(","):
        x = part.split("-")
        result.update(range(int(x[0]), int(x[-1]) + 1))
    return result


def parse_range_option(expr: str) -> set[int]:
    try:
        return parse_range(expr)
    except Exception:
        raise typer.BadParameter(f"Could not parse range: {expr}")


@app.command()
def fetch(
    metadata_file: Path = typer.Argument(..., exists=True, readable=True),
    dbnomics_api_cache_dir: Path = typer.Option(DBNOMICS_API_CACHE_DIR_NAME),
    force: bool = typer.Option(False),
):
    dbnomics_api_cache_dir.mkdir(exist_ok=True)

    presentation_metadata = load_presentation_metadata(metadata_file)
    fetch_presentation_series(presentation_metadata, cache_dir=dbnomics_api_cache_dir, force=force)


@app.command()
def update(
    input_pptx_file: FileBinaryRead,
    output_pptx_file: FileBinaryWrite,
    adhoc_tables_module_path: Optional[Path] = typer.Option(
        None, "--adhoc-tables-module", exists=True, readable=True, dir_okay=False
    ),
    dbnomics_api_cache_dir: Path = typer.Option(DBNOMICS_API_CACHE_DIR_NAME, exists=True, readable=True, dir_okay=True),
    metadata_file: Optional[Path] = typer.Option(None, exists=True, readable=True),
    only_slides_expr: Optional[str] = typer.Option(None, "--slides"),
    save_processed_slides_only: bool = False,
):
    """
    Update DBnomics data in a PowerPoint (pptx) presentation.
    """
    only_slides = None
    if only_slides_expr is not None:
        logger.debug("Will process slides %s", only_slides_expr)
        only_slides = parse_range_option(only_slides_expr)

    if save_processed_slides_only and only_slides is None:
        raise typer.BadParameter("--save-processed-slides-only must be used with --slides")

    logger.debug("Loading presentation from %r...", str(input_pptx_file.name))
    prs: Presentation = open_presentation(input_pptx_file)

    if metadata_file is None:
        metadata_file = Path(input_pptx_file.name).with_suffix(".yaml")
        logger.debug(
            "Metadata file not passed as an option, using file named after the presentation, with '.yaml' suffix"
        )

    presentation_metadata = load_presentation_metadata(metadata_file)

    adhoc_tables_module = (
        load_python_module_from_path(adhoc_tables_module_path, module_name="adhoc_tables")
        if adhoc_tables_module_path is not None
        else None
    )

    try:
        update_slides(
            prs,
            adhoc_tables_module=adhoc_tables_module,
            dbnomics_api_cache_dir=dbnomics_api_cache_dir,
            only_slides=only_slides,
            presentation_metadata=presentation_metadata,
        )
    except SeriesLoadError as exc:
        typer.echo(f'{str(exc)} Hint: run the "fetch" command first.')
        raise typer.Exit(1)

    if save_processed_slides_only:
        assert only_slides is not None
        delete_other_slides(prs, only_slides=only_slides)

    logger.debug("Saving presentation to %r...", str(output_pptx_file.name))
    prs.save(output_pptx_file)


def load_presentation_metadata(metadata_file: Path) -> PresentationMetadata:
    logger.debug("Loading presentation metadata from %r...", str(metadata_file))
    presentation_metadata_data = yaml.safe_load(metadata_file.read_text())
    return PresentationMetadata.parse_obj(presentation_metadata_data)


if __name__ == "__main__":
    app()
