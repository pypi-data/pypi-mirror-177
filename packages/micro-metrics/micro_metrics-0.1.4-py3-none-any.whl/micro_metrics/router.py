# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Execute Orchestrator with Parameters """


import os

from baseblock import FileIO

from micro_metrics.bp import Orchestrator


def run(input_directory: str,
        output_file: str) -> str:
    metrics = Orchestrator().run(input_directory)
    output_path = FileIO.join_cwd(os.path.dirname(output_file))
    FileIO.exists_or_create(output_path)
    FileIO.write_json(metrics, output_file)


def main(input_directory, output_file):
    run(input_directory, output_file)


if __name__ == "__main__":
    import plac

    plac.call(main)
