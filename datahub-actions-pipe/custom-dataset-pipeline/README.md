# Custom Dataset Semantic Search Ingestion Pipeline

A production-ready DataHub ingestion pipeline for indexing **Dataset entities** and their **schema metadata** into DataHub's Semantic Search vector index (`datasetindex_v2_semantic`).

---

## Architecture Overview

This pipeline mirrors the design of [`datahub-documents`](file:///d:/datahub/datahub/metadata-ingestion/src/datahub/ingestion/source/datahub_documents/datahub_documents_source.py):

```
 ┌─────────────┐     1. Query Datasets & Schemas      ┌───────────────────────────┐
 │ DataHub GMS │◀─────────────────────────────────────│   DatasetSemanticSource   │
 └──────┬──────┘                                      └─────────────┬─────────────┘
        │                                                           │
        │ 2. Return Descriptions, Columns, Tags, Terms              │ 3. Chunk Elements
        └──────────────────────────────────────────────────────────▶│    (Preserve columns)
                                                                    │
                                                                    │ 4. Batch API Embeddings
                                                                    ▼
                                                      ┌───────────────────────────┐
                                                      │    Embedding Provider     │
                                                      │ (OpenAI / Bedrock/Cohere) │
                                                      └─────────────┬─────────────┘
                                                                    │
                                                                    │ 5. Returns Float Vectors
                                                                    ▼
 ┌─────────────┐     6. Emit SemanticContent MCP      ┌───────────────────────────┐
 │ DataHub GMS │◀─────────────────────────────────────│     DatahubRestSink       │
 └──────┬──────┘                                      └───────────────────────────┘
        │
        │ 7. GMS Dual-Writes to datasetindex_v2_semantic
        ▼
 ┌────────────────────────────────────────────────────┐
 │  OpenSearch / Elasticsearch (k-NN Vector Search)   │
 └────────────────────────────────────────────────────┘
```

---

## 1. Prerequisites (GMS Setup)

Before running the pipeline, ensure your DataHub instance is configured to support semantic search on datasets:

### A. Add `semanticContent` to `dataset` in `entity-registry.yml`
In your [`entity-registry.yml`](file:///d:/datahub/datahub/metadata-models/src/main/resources/entity-registry.yml), add `- semanticContent` under `dataset`:
```yaml
entities:
  - name: dataset
    aspects:
      - datasetProperties
      - schemaMetadata
      - documentation
      - semanticContent    # <-- Required
```

### B. Configure GMS Environment Variables
In your `docker-compose.yml` or Helm chart for `datahub-gms`:
```yaml
environment:
  - ENTITY_REGISTRY_CONFIG_PATH=/datahub/datahub-gms/resources/entity-registry.yml
  - ELASTICSEARCH_SEMANTIC_SEARCH_ENABLED=true
  - ELASTICSEARCH_SEMANTIC_SEARCH_ENTITIES=document,dataset
  - EMBEDDING_PROVIDER_TYPE=openai
  - OPENAI_API_KEY=sk-...
  - OPENAI_EMBEDDING_MODEL=text-embedding-3-large
```

---

## 2. Installation

Install dependencies:
```bash
pip install "acryl-datahub" "openai" "pydantic"
```

---

## 3. Running the Pipeline

### Method A: Using DataHub Ingestion CLI & Recipe (Recommended)

1. Set your OpenAI API key (or Bedrock/Cohere credentials):
   ```bash
   export OPENAI_API_KEY="sk-your-openai-key"
   export DATAHUB_GMS_URL="http://localhost:8080"
   ```

2. Run the recipe:
   ```bash
   cd custom-dataset-pipeline
   datahub ingest -c dataset_semantic_recipe.yml
   ```

---

### Method B: Using the Standalone Python Runner

```bash
python custom-dataset-pipeline/run_pipeline.py \
  --server http://localhost:8080 \
  --openai-key "sk-your-openai-key" \
  --model "text-embedding-3-large"
```

**Useful Runner Options:**
- `--limit 10`: Only process the first 10 datasets (for testing).
- `--platforms snowflake bigquery`: Filter to specific platforms.
- `--force`: Force recalculate all embeddings, ignoring incremental state.

---

### Method C: Running via DataHub UI (Managed Ingestion)

1. Mount the `custom-dataset-pipeline` folder into the `datahub-actions` container in `docker-compose.yml`:
   ```yaml
   datahub-actions:
     image: acryldata/datahub-actions:latest
     environment:
       - PYTHONPATH=/etc/datahub/custom_plugins
     volumes:
       - ./custom-dataset-pipeline:/etc/datahub/custom_plugins:ro
   ```
2. In DataHub UI $\rightarrow$ **Ingestion** $\rightarrow$ **Create New Source** $\rightarrow$ **Custom Recipe (YAML)**:
   - Paste the contents of [`dataset_semantic_recipe.yml`](file:///d:/datahub/datahub/custom-dataset-pipeline/dataset_semantic_recipe.yml).
   - In **Advanced Settings** $\rightarrow$ **Extra Pip Requirements**, add `openai`.
   - Click **Save & Run**.

---

## 4. Verification & Diagnostics

### 1. Test Semantic Search via CLI
```bash
datahub search query "customer transaction table with billing status" --semantic
```

### 2. Test via GraphQL API
```graphql
query SearchDatasetSemantic {
  semanticSearchAcrossEntities(
    input: {
      query: "sales revenue transactions"
      types: [DATASET]
      count: 10
    }
  ) {
    total
    searchResults {
      score
      entity {
        urn
        type
        ... on Dataset {
          name
          properties {
            description
          }
        }
      }
    }
  }
}
```

### 3. Check Elasticsearch Index directly
```bash
curl "http://localhost:9200/datasetindex_v2_semantic/_search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "exists": { "field": "embeddings.text_embedding_3_large" }
    }
  }'
```
