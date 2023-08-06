from __future__ import annotations

from enum import Enum
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

__all__ = ["DataLabelPosition", "PresentationMetadata", "SlideMetadata"]


class DataLabelPosition(Enum):
    LAST_POINT = "last_point"


ChartName: TypeAlias = str
SeriesId: TypeAlias = str
SlideName: TypeAlias = str
TableLocation: TypeAlias = str


class TopLevelSeriesSpec(BaseModel):
    name: str


class ChartOrTableSeriesSpec(BaseModel):
    id: str
    name: str | None = None
    tag: str | None = None

    def get_name(self, *, presentation_metadata: PresentationMetadata) -> str | None:
        name = self.name
        if name is not None:
            return name
        series_spec = presentation_metadata.series.get(self.id)
        if series_spec is None:
            return None
        return series_spec.name

    def has_tag(self, tag: str | None) -> bool:
        return tag == self.tag


class TableSpec(BaseModel):
    series: list[SeriesId | ChartOrTableSeriesSpec]

    def find_series_id_by_name(
        self, series_name: str, *, presentation_metadata: PresentationMetadata, tag: str | None = None
    ) -> str | None:
        for series_id_or_spec in self.series:
            series_spec = self._to_series_spec(series_id_or_spec, presentation_metadata=presentation_metadata)
            if series_spec.name is None:
                continue
            if series_spec.name == series_name and series_spec.has_tag(tag):
                return series_spec.id
        return None

    def get_series_ids(self) -> set[str]:
        return {
            series_id_or_spec.id if isinstance(series_id_or_spec, ChartOrTableSeriesSpec) else series_id_or_spec
            for series_id_or_spec in self.series
        }

    def _get_presentation_series_spec_name(
        self, series_id: SeriesId, *, presentation_metadata: PresentationMetadata
    ) -> str | None:
        presentation_series_spec = presentation_metadata.series.get(series_id)
        if presentation_series_spec is None:
            return None
        return presentation_series_spec.name

    def _to_series_spec(
        self, series_id_or_spec: SeriesId | ChartOrTableSeriesSpec, *, presentation_metadata: PresentationMetadata
    ) -> ChartOrTableSeriesSpec:
        if isinstance(series_id_or_spec, ChartOrTableSeriesSpec):
            series_spec = series_id_or_spec
            if series_spec.name is not None:
                return series_id_or_spec
            presentation_series_spec_name = self._get_presentation_series_spec_name(
                series_spec.id, presentation_metadata=presentation_metadata
            )
            return series_spec.copy(update={"name": presentation_series_spec_name})

        series_id = series_id_or_spec
        presentation_series_spec_name = self._get_presentation_series_spec_name(
            series_id, presentation_metadata=presentation_metadata
        )
        return ChartOrTableSeriesSpec(id=series_id, name=presentation_series_spec_name)


DataLabelPositionT: TypeAlias = Literal["last_point"]


class ChartSpec(TableSpec):
    data_labels: list[DataLabelPositionT] = Field(default_factory=list)


class SlideMetadata(BaseModel):
    charts: dict[ChartName, ChartSpec] = Field(default_factory=dict)
    tables: dict[TableLocation, TableSpec] = Field(default_factory=dict)

    def get_series_ids(self) -> set[str]:
        series_ids = set()
        for chart_spec in self.charts.values():
            series_ids |= set(chart_spec.get_series_ids())
        for table_spec in self.tables.values():
            series_ids |= set(table_spec.get_series_ids())
        return series_ids


class PresentationMetadata(BaseModel):
    series: dict[SeriesId, TopLevelSeriesSpec] = Field(default_factory=dict)
    slides: dict[SlideName, SlideMetadata]

    def get_slide_series_ids(self) -> set[str]:
        result = set()
        for slide in self.slides.values():
            result |= slide.get_series_ids()
        return result
