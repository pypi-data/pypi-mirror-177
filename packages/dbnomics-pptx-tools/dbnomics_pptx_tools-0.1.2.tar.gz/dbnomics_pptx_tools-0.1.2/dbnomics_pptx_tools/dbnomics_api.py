from pathlib import Path

import daiquiri
import pandas as pd
from dbnomics import fetch_series
from pandas import DataFrame

from dbnomics_pptx_tools.metadata import PresentationMetadata, SlideMetadata

__all__ = [
    "fetch_presentation_series",
    "load_series_from_cache",
    "save_series_to_cache",
    "select_slide_series",
    "SeriesLoadError",
]

logger = daiquiri.getLogger(__name__)


class SeriesLoadError(Exception):
    def __init__(self, *, cache_dir: Path, series_id: str):
        message = f"Series {series_id!r} was not found in cache directory."
        super().__init__(message)
        self.cache_dir = cache_dir
        self.series_id = series_id


def add_series_id_column(df: DataFrame) -> DataFrame:
    return df.assign(series_id=lambda row: row.provider_code + "/" + row.dataset_code + "/" + row.series_code)


def fetch_presentation_series(presentation_metadata: PresentationMetadata, *, cache_dir: Path, force: bool = False):
    series_ids = sorted(presentation_metadata.get_slide_series_ids())
    logger.debug("Fetching all the series needed for the presentation from DBnomics: %r...", series_ids)
    for series_id in series_ids:
        if is_series_in_cache(series_id, cache_dir=cache_dir) and not force:
            logger.debug("Series %r is already in cache, skipping fetch", series_id)
            continue
        logger.debug("Fetching series %r...", series_id)
        df = fetch_series(series_ids=[series_id])
        df = add_series_id_column(df)
        save_series_to_cache(df, cache_dir=cache_dir, series_id=series_id)
        logger.debug("Series %r was saved to the cache directory", series_id)


def get_series_json_file_name(series_id: str) -> str:
    return series_id.replace("/", "__") + ".json"


def get_series_json_file_path(series_id: str, *, cache_dir: Path) -> Path:
    return cache_dir / get_series_json_file_name(series_id)


def is_series_in_cache(series_id: str, *, cache_dir: Path) -> bool:
    file_path = get_series_json_file_path(series_id, cache_dir=cache_dir)
    return file_path.is_file()


def load_series_from_cache(series_id: str, *, cache_dir: Path) -> DataFrame:
    file_path = get_series_json_file_path(series_id, cache_dir=cache_dir)
    if not file_path.is_file():
        raise SeriesLoadError(cache_dir=cache_dir, series_id=series_id)
    return pd.read_json(
        file_path, convert_dates=["period"], dtype={"original_period": str}, orient="records"  # type: ignore
    )


def save_series_to_cache(series_df: DataFrame, *, cache_dir: Path, series_id: str):
    file_path = get_series_json_file_path(series_id, cache_dir=cache_dir)
    series_df.to_json(file_path, date_format="iso", indent=2, orient="records")


def select_slide_series(presentation_series_df: DataFrame, *, slide_metadata: SlideMetadata):
    slide_series_ids = slide_metadata.get_series_ids()
    return presentation_series_df.query(
        "series_id in @slide_series_ids", local_dict={"slide_series_ids": slide_series_ids}
    )
