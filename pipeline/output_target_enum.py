from enum import Enum

from pipeline.defined import graph_to_pdf_pipeline, \
    graph_to_md_file_pipeline, graph_to_html_pipeline, graph_to_plantuml_image
from transform.logseq import LogSeqRenderer

class OutputType(Enum):
    """
    Encodes valid transform types.
    """

    PDF = "pdf"
    PLANTUML = "plantuml"
    MD = "md"
    SINGLE_HTML = "single_html"
    LOGSEQ = "logseq"

    def __str__(self):
        return self.value


def build_file_pipeline(target, concept_store, output_path, render_options):

    match target:
        case OutputType.PLANTUML:
            return graph_to_plantuml_image(concept_store, output_path, render_options)
        case OutputType.PDF:
            return graph_to_pdf_pipeline(concept_store, output_path, render_options)
        case OutputType.MD:
            return graph_to_md_file_pipeline(concept_store, output_path, render_options)
        case OutputType.SINGLE_HTML:
            return graph_to_html_pipeline(concept_store, output_path, render_options)
        case OutputType.LOGSEQ:
            return LogSeqRenderer(concept_store, output_path, render_options)
        case other:
            raise Exception("No Pipeline associated to given output type")

