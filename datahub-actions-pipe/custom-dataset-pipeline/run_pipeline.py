#!/usr/bin/env python3
"""Standalone runner for the Custom Dataset Semantic Ingestion Pipeline.

Run directly via:
    python run_pipeline.py --server http://localhost:8080 --openai-key sk-...
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add current directory to sys.path so modules can be imported
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from datahub.ingestion.run.pipeline import Pipeline
from custom_dataset_config import (
    ChunkingConfig,
    DataHubConnectionConfig,
    DatasetSemanticSourceConfig,
    EmbeddingConfig,
    IncrementalConfig,
)
from custom_dataset_source import DatasetSemanticSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("dataset-semantic-runner")


def main():
    parser = argparse.ArgumentParser(
        description="Run Dataset Semantic Search Ingestion Pipeline"
    )
    parser.add_argument(
        "--server",
        default=os.environ.get("DATAHUB_GMS_URL", "http://localhost:8080"),
        help="DataHub GMS server URL (default: http://localhost:8080)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("DATAHUB_GMS_TOKEN", None),
        help="DataHub Personal Access Token (if auth is enabled)",
    )
    parser.add_argument(
        "--openai-key",
        default=os.environ.get("OPENAI_API_KEY", None),
        help="OpenAI API Key (default: from OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--model",
        default="text-embedding-3-large",
        help="Embedding model ID (default: text-embedding-3-large)",
    )
    parser.add_argument(
        "--provider",
        default="openai",
        help="Embedding provider: openai, bedrock, cohere, or local (default: openai)",
    )
    parser.add_argument(
        "--platforms",
        nargs="*",
        default=None,
        help="Optional platforms to filter (e.g. snowflake bigquery)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of datasets to process (for testing)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reprocess all datasets (ignore incremental cache)",
    )

    args = parser.parse_args()

    pipeline_config = {
        "source": {
            "type": "custom_dataset_source.DatasetSemanticSource",
            "config": {
                "datahub": {
                    "server": args.server,
                    "token": args.token,
                },
                "embedding": {
                    "provider": args.provider,
                    "model": args.model,
                    "api_key": args.openai_key,
                },
                "platform_filter": args.platforms,
                "max_datasets": args.limit,
                "incremental": {
                    "enabled": True,
                    "force_reprocess": args.force,
                },
            },
        },
        "sink": {
            "type": "datahub-rest",
            "config": {
                "server": args.server,
                "token": args.token,
            },
        },
    }

    logger.info("Initializing Dataset Semantic Ingestion Pipeline...")
    pipeline = Pipeline.create(pipeline_config)

    logger.info("Running pipeline...")
    pipeline.run()
    pipeline.pretty_print_summary()

    if pipeline.has_failures():
        logger.error("Pipeline finished with failures.")
        sys.exit(1)
    else:
        logger.info("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
