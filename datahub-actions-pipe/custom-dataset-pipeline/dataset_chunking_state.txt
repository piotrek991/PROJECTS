"""State classes for dataset semantic chunking stateful ingestion."""

from typing import Dict
import pydantic
from datahub.ingestion.source.state.checkpoint import CheckpointStateBase


class DatasetChunkingCheckpointState(CheckpointStateBase):
    """Checkpoint state for dataset chunking and embedding.
    
    Stores dataset content hashes (batch mode) and event stream offsets (event mode).
    """

    # Dataset content tracking (used in batch mode)
    dataset_state: Dict[str, Dict[str, str]] = pydantic.Field(
        default_factory=dict,
        description="Dataset state mapping URN to content hash and last processed timestamp (batch mode)",
    )

    # Event stream offset tracking (used in event mode)
    event_offsets: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="Maps topic to offset_id for event-driven mode",
    )
