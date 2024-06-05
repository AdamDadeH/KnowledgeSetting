import argparse

import os

from concept_store.concept_graph_store import ConceptGraph
from concept_store.concept_store import ConceptStore
from loading import build_local_content_repo

from pipeline.output_target_enum import OutputType, build_file_pipeline
from transform.pdf import LinearRendererOptions

import time


def render_single(concept_store: ConceptStore,
                  graph_store: ConceptGraph,
                  output_path: str,
                  target_type,
                  known=None,
                  targets=None):
    """
    End to end rendering from yaml to final transform.

    :param concept_store:
    :param graph_store:
    :param output_path:
    :param target_type:
    :param known:
    :param targets:
    :return:
    """

    content_dag = graph_store

    # Selecting only those nodes that are required for our goal.
    if targets is not None:
        if known is None:
            known = []
        content_dag = content_dag.subset_by_known_and_goals(known, targets)

    # right now this hides configuration of transform - which we do want to expose
    to_sub = []

    render_options = LinearRendererOptions(to_sub)
    renderer = build_file_pipeline(target_type, concept_store, output_path, render_options)

    #infer what to remove
    #to_sub = [k for (k, v) in content_dag.usage_count() if v < 2]

    renderer.execute(content_dag.dependency_graph)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output_type", type=OutputType, choices=list(OutputType))
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--input", nargs="+")
    parser.add_argument("--output")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--known", nargs="+")
    parser.add_argument("--goal", nargs="+")
    parser.add_argument("--continuous", action="store_true")
    args = parser.parse_args()

    if args.continuous:

        def get_file_state(files):
            """Retrieve the current state of the files as a dictionary mapping file names to modification times."""
            state = {}
            for file in files:
                if os.path.isfile(file):
                    state[file] = os.path.getmtime(file)
            return state


        def poll_files(files, interval=1):
            """Continuously poll a list of files for any changes."""
            # Initialize the last known state of each file
            last_state = get_file_state(files)

            try:
                while True:
                    time.sleep(interval)
                    current_state = get_file_state(files)
                    if current_state != last_state:
                        compare_states(last_state, current_state)
                        last_state = current_state
            except KeyboardInterrupt:
                print("Stopped polling.")


        def compare_states(old_state, new_state):
            """Compare old and new states of files, and print differences."""
            old_files = set(old_state.keys())
            new_files = set(new_state.keys())
            modified = {file for file in old_files & new_files if old_state[file] != new_state[file]}

            if modified:
                print("Modified files: ", modified)
                render_single(
                    args.input,
                    args.output,
                    args.output_type,
                    args.known,
                    args.goal,
                )


        poll_files(args.input)

        """
        class MyHandler(FileSystemEventHandler):
            def on_modified(self, event):
                print("Modified")
                print(event)
                render_single(
                    args.input,
                    args.output,
                    args.output_type,
                    args.known,
                    args.goal,
                )

        event_handler = MyHandler()
        observer = Observer()

        for path in args.input:
            # Schedules watching of a given path
            observer.schedule(event_handler, path)
            print("adding {} to scheduler".format(path))
        # start observer
        observer.start()

        try:
            while True:
                # poll every second
                time.sleep(1)
        except KeyboardInterrupt:
            observer.unschedule_all()
            # stop observer if interrupted
            observer.stop()
            # Wait until the thread terminates before exit
        observer.join()
        """
    else:

        concept_store, graph_store = build_local_content_repo(args.input)
        render_single(concept_store,
                      graph_store,
                      args.output,
                      args.output_type,
                      args.known,
                      args.goal)
