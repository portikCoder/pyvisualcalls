import collections
import logging
import re
from collections import namedtuple
from pathlib import Path
from typing import List

from dataclasses import dataclass

import visualizer
from data_node_holder import DataStructure_ToHoldCallsAndCallees

PY_FUNCTION_PATTERN: str = re.compile(r"(?<=def )(\w+) ?\(([\w: , ]*)(?=\).*[ \[\]\->]*:$)",
                                      flags=re.I | re.M)  # https://regex101.com/r/8xlNZo/1


@dataclass
class Config:
    project_name: str
    project_path: str


def setup(config: Config):
    logging.getLogger().setLevel(logging.DEBUG)


def read_config():
    # return Config("bitbucket-scanner", r"C:\dev\3ppautomation\bitbucket-scanner\src")
    return Config("svl-generator", r"C:\dev\3ppautomation\svl-generator")


def discover_python_project(project_path: str) -> List[Path]:
    project_files = [path for path in Path(project_path).rglob('./[!v][!e][!n]*/*.py') if
                     not re.search('venv.*', path.__str__())]  # if 'venv' not in path
    logging.debug(project_files)
    return project_files


def map_python_file_into(project_file: Path, calls_and_callees_graph: DataStructure_ToHoldCallsAndCallees):
    content: str
    try:
        with open(project_file, 'r')as f:
            content = f.read()
    except (PermissionError, FileNotFoundError, UnicodeDecodeError) as pe_or_fnfe:
        logging.error(f"Could not read '{project_file}'! {pe_or_fnfe}")
        return
    if not content:
        logging.debug(f"File '{project_file}' is empty")
        return

    FunctionDescriptor = namedtuple('FunctionDescriptor', ('name', 'params'))
    functions: List[FunctionDescriptor] = [FunctionDescriptor(name, str(params).split(',')) for name, params in
                                           re.findall(PY_FUNCTION_PATTERN, content)]
    logging.debug(f"(File <-> methods) '{project_file}' <-> {functions}")

    {calls_and_callees_graph.append(project_file, function.name,
                                    DataStructure_ToHoldCallsAndCallees.Node(1, 'child', 'father')) for function in
     functions}


def build_calls_and_callees_graph(project_files: List[Path]) -> DataStructure_ToHoldCallsAndCallees:
    calls_and_callees_graph: DataStructure_ToHoldCallsAndCallees = DataStructure_ToHoldCallsAndCallees(
        collections.defaultdict(lambda: collections.defaultdict(list)))

    for project_file in project_files:
        map_python_file_into(project_file, calls_and_callees_graph)
    return calls_and_callees_graph


analysation = ''


def execute_analyzation_for_python_project(config: Config):
    logging.info(f"Discover the specified python project: {config.project_path}")
    project_files = discover_python_project(config.project_path)
    calls_with_calees: DataStructure_ToHoldCallsAndCallees = build_calls_and_callees_graph(project_files)
    logging.debug(f"Result for calls_with_calees: {calls_with_calees}")

    logging.info("Visualize")
    logging.info("is turned off now...")
    # visualizer.visualize(config.project_name, calls_with_calees)


def main():
    config: Config = read_config()
    setup(config)
    logging.info("Setup done.")
    logging.debug(f"Config's content: {config}")

    execute_analyzation_for_python_project(config)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
