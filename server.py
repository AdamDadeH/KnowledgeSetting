from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import glob

import json

from concept_store.concept_store import ConceptStore
from concept_store.local_concept_store import LocalConceptStore
from concept_store.local_graph_store import NxConceptGraph
from loading import build_local_content_repo
from pipeline.defined import graph_to_md_pipeline
from source.source import FileListSource
from source.yaml import YamlFile
from transform.pdf import LinearRendererOptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Concept(BaseModel):
    id: int
    name: str
    content: str


# Instantiate your stores and services
concept_store = LocalConceptStore()
graph_store = NxConceptGraph()

@app.on_event("startup")
async def load_data():
    # Load your data here
    logger.info("Loading Data")

    base_path = "/Users/ahenderson/Google Drive/personal-curiosity/3-knowledge-base/math_bracketed/"
    files = glob.glob(base_path + '*.yaml')
    inputs = files
    logger.info(f"Files to load: {inputs}")
    source = FileListSource(inputs, YamlFile)
    source.load_to(concept_store, graph_store)

@app.get("/api/concepts/{id}")
async def get_concept(id: str):
    concept = concept_store.get_concept(id)
    if concept:
        return concept
    raise HTTPException(status_code=404, detail="Concept not found")

class GraphQuery(BaseModel):
    source_ids: list[str]
    target_ids: list[str]
    output_format: str


@app.post("/api/query-graph")
async def query_graph(query: GraphQuery):
    sources = query.source_ids
    targets = query.target_ids
    format = query.output_format

    render_options = LinearRendererOptions([])
    subgraph = graph_store.get_unique_ancestors_subgraph(sources, targets)
    result = graph_to_md_pipeline(concept_store, render_options).execute(subgraph)

    if result is None:
        raise HTTPException(status_code=404, detail="No results found for given query")
    return result

