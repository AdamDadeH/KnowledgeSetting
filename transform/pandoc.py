import subprocess

from transform.transform import BaseRenderer


class PandocTransform(BaseRenderer):

    def __init__(self, output_path, output_file_extension):
        self.output_path = output_path
        self.output_file_extension = output_file_extension

    def execute(self, data):
        """
        Input path should be pointer to markdown on disk.

        :param data:
        :return:
        """
        try:
            res = subprocess.run(
                [
                    "pandoc",
                    data,
                    "-o",
                    self.output_path + "." + self.output_file_extension,
                    "-V",
                    "documentclass=tufte-book",
                ],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return self.output_path
        except subprocess.CalledProcessError as e:
            # Handle the subprocess-specific error
            error_message = f"Command '{' '.join(e.cmd)}' returned non-zero exit status {e.returncode}."
            detailed_error = f"stderr: {e.stderr}"
            # Log or print detailed error information
            print(error_message)
            print(detailed_error)
            # Optionally, re-raise the error with detailed information or handle it as needed
            raise RuntimeError(f"{error_message}\n{detailed_error}") from None
        print(f"returncode = {res.returncode}")
        if res.returncode != 0:
            # there was an error, we assume the traceback was printed to stderr
            print("there was an error :\n")
            print(res.stderr.decode("utf-8"))

class PandocMdToHtml(PandocTransform):

    def __init__(self, output_path):
        super().__init__(output_path, "html")


class PandocMdToPdf(PandocTransform):

    def __init__(self, output_path):
        super().__init__(output_path, "pdf")
