import subprocess

from source.inline_handler import SubstitutionHandler
from transform.pandoc import PandocMdToHtml, PandocMdToPdf
from transform.markdown import GraphToMarkdown
from transform.pdf import IllegalCharCheck, UnmatchedBracket
from pipeline.pipeline import Pipeline
from transform.plantuml import GraphToPlantUml, PlantUmlToImage
from transform.sequencer import Sequencer, SpectralSortSequencer
from transform.string import StringToFile




def graph_to_md_pipeline(content_repo, render_options=None):
    inline_handler = SubstitutionHandler(render_options.to_substitute, content_repo)
    pipeline = Pipeline()
    pipeline.add_stage(SpectralSortSequencer())
    pipeline.add_stage(GraphToMarkdown(inline_handler, content_repo))
    pipeline.add_stage(IllegalCharCheck("∆"))
    pipeline.add_stage(UnmatchedBracket("$", "$"))
    return pipeline

def graph_to_md_file_pipeline(content_repo, output_path, render_options):
    pipeline = graph_to_md_pipeline(content_repo, render_options)
    pipeline.add_stage(StringToFile(output_path + ".md"))
    return pipeline

def graph_to_html_pipeline(content_repo, output_path, render_options):
    pipeline = graph_to_md_file_pipeline(content_repo, output_path, render_options)
    pipeline.add_stage(PandocMdToHtml(output_path))
    return pipeline

def graph_to_pdf_pipeline(content_repo, output_path, render_options):
    pipeline = graph_to_md_file_pipeline(content_repo, output_path, render_options)
    pipeline.add_stage(PandocMdToPdf(output_path))
    return pipeline

def graph_to_plantuml_image(content_repo, output_path, render_options):
    pipeline = Pipeline()
    pipeline.add_stage(GraphToPlantUml())
    pipeline.add_stage(StringToFile(output_path + ".puml"))
    pipeline.add_stage(PlantUmlToImage())
    return pipeline