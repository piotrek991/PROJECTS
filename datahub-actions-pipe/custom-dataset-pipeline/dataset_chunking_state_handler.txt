"""State handler for dataset semantic chunking stateful ingestion."""

import logging
from typing import Optional, cast

from datahub.ingestion.api.ingestion_job_checkpointing_provider_base import JobId
from datahub.ingestion.source.state.checkpoint import Checkpoint
from datahub.ingestion.source.state.stateful_ingestion_base import (
    StatefulIngestionConfig,
    StatefulIngestionConfigBase,
    StatefulIngestionSourceBase,
)
from datahub.ingestion.source.state.use_case_handler import (
    StatefulIngestionUsecaseHandlerBase,
)
from dataset_chunking_state import DatasetChunkingCheckpointState

logger: logging.Logger = logging.getLogger(__name__)


class DatasetChunkingStatefulIngestionConfig(StatefulIngestionConfig):
    """Configuration for dataset chunking stateful ingestion."""
    pass


class DatasetChunkingStateHandler(
    StatefulIngestionUsecaseHandlerBase[DatasetChunkingCheckpointState]
):
    """State handler for dataset semantic chunking stateful ingestion.
    
    Manages dataset content hash tracking to skip unchanged datasets between runs.
    """

    def __init__(
        self,
        source: StatefulIngestionSourceBase,
        config: StatefulIngestionConfigBase[DatasetChunkingStatefulIngestionConfig],
        pipeline_name: Optional[str],
        run_id: str,
    ):
        self.state_provider = source.state_provider
        self.stateful_ingestion_config: Optional[
            DatasetChunkingStatefulIngestionConfig
        ] = config.stateful_ingestion
        self.pipeline_name = pipeline_name
        self.run_id = run_id
        self.checkpointing_enabled: bool = (
            self.state_provider.is_stateful_ingestion_configured()
        )
        self._job_id = self._init_job_id()
        self.state_provider.register_stateful_ingestion_usecase_handler(self)

    def _ignore_old_state(self) -> bool:
        if (
            self.stateful_ingestion_config is not None
            and self.stateful_ingestion_config.ignore_old_state
        ):
            return True
        return False

    def _ignore_new_state(self) -> bool:
        if (
            self.stateful_ingestion_config is not None
            and self.stateful_ingestion_config.ignore_new_state
        ):
            return True
        return False

    def _init_job_id(self) -> JobId:
        return JobId("dataset_semantic_chunking")

    @property
    def job_id(self) -> JobId:
        return self._job_id

    def is_checkpointing_enabled(self) -> bool:
        return self.checkpointing_enabled

    def create_checkpoint(
        self,
    ) -> Optional[Checkpoint[DatasetChunkingCheckpointState]]:
        if not self.is_checkpointing_enabled() or self._ignore_new_state():
            return None

        assert self.pipeline_name is not None
        return Checkpoint(
            job_name=self.job_id,
            pipeline_name=self.pipeline_name,
            run_id=self.run_id,
            state=DatasetChunkingCheckpointState(),
        )

    def get_current_state(
        self,
    ) -> Optional[DatasetChunkingCheckpointState]:
        """Get the current checkpoint state (being built during this run)."""
        if not self.is_checkpointing_enabled() or self._ignore_new_state():
            return None
        cur_checkpoint = self.state_provider.get_current_checkpoint(self.job_id)
        assert cur_checkpoint is not None
        cur_state = cast(DatasetChunkingCheckpointState, cur_checkpoint.state)
        return cur_state

    def get_last_state(
        self,
    ) -> Optional[DatasetChunkingCheckpointState]:
        """Get the last checkpoint state (from previous run in GMS)."""
        if not self.is_checkpointing_enabled() or self._ignore_old_state():
            return None
        last_checkpoint = self.state_provider.get_last_checkpoint(
            self.job_id, DatasetChunkingCheckpointState
        )
        if last_checkpoint and last_checkpoint.state:
            return cast(DatasetChunkingCheckpointState, last_checkpoint.state)

        return None

    def get_dataset_hash(self, dataset_urn: str) -> Optional[str]:
        """Get the stored content hash for a dataset from the last checkpoint."""
        state = self.get_last_state()
        if state and dataset_urn in state.dataset_state:
            return state.dataset_state[dataset_urn].get("content_hash")
        return None

    def update_dataset_state(
        self, dataset_urn: str, content_hash: str, last_processed: str
    ) -> None:
        """Update the checkpoint state for a dataset."""
        current_state = self.get_current_state()
        if current_state:
            current_state.dataset_state[dataset_urn] = {
                "content_hash": content_hash,
                "last_processed": last_processed,
            }

    def get_event_offset(self, topic: str) -> Optional[str]:
        """Get the stored offset for an event topic."""
        state = self.get_last_state()
        if state:
            return state.event_offsets.get(topic)
        return None

    def update_event_offset(self, topic: str, offset_id: str) -> None:
        """Update the offset for an event topic."""
        current_state = self.get_current_state()
        if current_state:
            current_state.event_offsets[topic] = offset_id
