"""Configuration model for Custom Dataset Semantic Ingestion Pipeline."""

from typing import List, Optional
from pydantic import Field
from datahub.configuration.common import ConfigModel
from datahub.ingestion.source.state.stateful_ingestion_base import (
    StatefulIngestionConfigBase,
)
from dataset_chunking_state_handler import (
    DatasetChunkingStatefulIngestionConfig,
)


class DataHubConnectionConfig(ConfigModel):
    """Connection configuration for DataHub GMS."""

    server: str = Field(
        default="http://localhost:8080",
        description="DataHub GMS server endpoint URL",
    )
    token: Optional[str] = Field(
        default=None,
        description="DataHub personal access token if authentication is enabled",
    )
    timeout_seconds: int = Field(
        default=30,
        description="Request timeout in seconds for GraphQL/REST calls",
    )


class EmbeddingConfig(ConfigModel):
    """Embedding provider configuration.

    If provider/model is not specified, it will be automatically fetched
    from DataHub GMS server AppConfig API (semanticSearchConfig).
    """

    provider: Optional[str] = Field(
        default=None,
        description="Embedding provider: 'openai', 'bedrock', 'cohere', or 'local'. Auto-discovered if omitted.",
    )
    model: Optional[str] = Field(
        default=None,
        description="Model ID (e.g., 'text-embedding-3-large', 'cohere.embed-english-v3'). Auto-discovered if omitted.",
    )
    model_embedding_key: Optional[str] = Field(
        default=None,
        description="Elasticsearch index model key (e.g., 'text_embedding_3_large'). Auto-discovered if omitted.",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API key for the provider (or set OPENAI_API_KEY / COHERE_API_KEY in environment)",
    )
    aws_region: Optional[str] = Field(
        default="us-west-2",
        description="AWS Region for AWS Bedrock provider",
    )
    batch_size: int = Field(
        default=25,
        description="Number of chunks to send per embedding API call",
    )
    request_timeout: int = Field(
        default=60,
        description="Timeout for embedding API calls in seconds",
    )


class ChunkingConfig(ConfigModel):
    """Text chunking parameters for datasets."""

    max_characters: int = Field(
        default=1800,
        description="Target maximum characters per chunk (~400 tokens)",
    )
    include_header_in_every_chunk: bool = Field(
        default=True,
        description="If true, prepends the dataset summary header to each column chunk so context is preserved.",
    )


class IncrementalConfig(ConfigModel):
    """Incremental state tracking configuration (local fallback)."""

    enabled: bool = Field(
        default=True,
        description="Enable incremental processing to skip unchanged datasets",
    )
    state_file_path: Optional[str] = Field(
        default=None,
        description="Path to store local fallback state cache JSON file (defaults to ~/.datahub/dataset_semantic_state/{pipeline_name}.json)",
    )
    force_reprocess: bool = Field(
        default=False,
        description="If true, ignores existing state and reprocesses all datasets",
    )


class DatasetSemanticSourceConfig(
    StatefulIngestionConfigBase[DatasetChunkingStatefulIngestionConfig]
):
    """Main configuration for DatasetSemanticSource."""

    datahub: DataHubConnectionConfig = Field(
        default_factory=DataHubConnectionConfig,
        description="DataHub GMS connection configuration",
    )
    embedding: EmbeddingConfig = Field(
        default_factory=EmbeddingConfig,
        description="Embedding model and provider configuration",
    )
    chunking: ChunkingConfig = Field(
        default_factory=ChunkingConfig,
        description="Dataset chunking parameters",
    )
    incremental: IncrementalConfig = Field(
        default_factory=IncrementalConfig,
        description="Incremental state tracking configuration (local fallback)",
    )
    platform_filter: Optional[List[str]] = Field(
        default=None,
        description="Optional list of platforms to include (e.g. ['snowflake', 'bigquery', 'postgres'])",
    )
    env_filter: Optional[List[str]] = Field(
        default=None,
        description="Optional list of environments to include (e.g. ['PROD', 'DEV'])",
    )
    min_text_length: int = Field(
        default=15,
        description="Minimum character length of synthesized dataset text to be eligible for embedding",
    )
    max_datasets: Optional[int] = Field(
        default=None,
        description="Maximum number of datasets to process (useful for testing and debugging)",
    )
