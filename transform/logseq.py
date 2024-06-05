import os

from transform.transform import BaseRenderer


class LogSeqRenderer(BaseRenderer):
    """
    Should write out a file per content with name decided by content_id
    then with a specified mapping from record/content to file format.
    """

    def __init__(self, content_repo, output_path, render_options=None):
        self.output_path = output_path
        self.content_repo = content_repo
        super().__init__(render_options)

    def dependencies_as_backlink(self, k):
        print(k)
        relations = self.content_repo.get_relations(k)
        print(relations)
        dependencies = relations.get("depends_on", [])
        output = ""
        for dep in dependencies:
            output += f"[[{dep}]]\n"
        return output

    def single_file_content(self, key):
        return self.content_repo.get_concept_or_default(key).get_concept()

    def execute(self,
               content_dag):
        os.mkdir(self.output_path)
        for k in list(content_dag):
            with open(f"{self.output_path}/{k}.md", "a") as outfile:
                dependency_text = self.dependencies_as_backlink(k)
                outfile.write(dependency_text + "\n" + self.single_file_content(k))
