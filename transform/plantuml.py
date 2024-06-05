import subprocess

from transform.transform import BaseRenderer


class GraphToPlantUml(BaseRenderer):

    def __init__(self):
        self.defined = set()
        self.uml = ""

    def execute(self, graph):
        return self.generate_md(graph)

    def add_node(self, node_name):
        cleaned_node_name = node_name.replace(".", "_")
        if cleaned_node_name not in self.defined:
            self.uml += "class {}\n".format(cleaned_node_name)
            self.defined.add(cleaned_node_name)
        return cleaned_node_name

    def add_edge(self, edge):
        source = self.add_node(edge[0])
        target = self.add_node(edge[1])
        self.uml += "{} --> {}\n".format(source, target)

    def generate_md(self, content_dag):
        self.uml = "@startuml\n"
        for edge in content_dag.edges.data():
            self.add_edge(edge)
        self.uml += "@enduml\n"
        return self.uml

class PlantUmlToImage(BaseRenderer):

    def execute(self, data):
        subprocess.run(["plantuml", "-stdrpt:1", "-teps", data])

