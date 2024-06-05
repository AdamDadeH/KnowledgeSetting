from transform.transform import BaseRenderer

class GraphToMarkdown(BaseRenderer):
    """ """

    def __init__(self, substitution_handler, content_repo):
        self.substitution_handler = substitution_handler
        self.content_repo = content_repo

    def newline(self):
        return "\n\n"

    def content_to_md(self, content):
        """

        :param content:
        :param display_rule:
        :return:
        """
        output = "**{}**: {}".format(content.get_type(), content.get_title())
        output += self.newline()
        output += self.substitution_handler.substitute(content.get_concept())
        output += self.newline()
        output += self.errors_to_md(content.errors)
        return output

    def errors_to_md(self, errors):
        """
        :return:
        """
        output = ""
        for e in errors.errors:
            output += "Error: {}\n\n".format(e)
        for w in errors.warnings:
            output += "Warning: {}\n\n".format(w)
        return output

    def execute(self, sequenced):
        """

        :param sequenced:
        :param concept_store:
        :return:
        """
        output = ""
        for k in sequenced:
            output += self.content_to_md(
                self.content_repo.get_concept_or_default(k)
            )
        return output
