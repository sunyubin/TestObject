from pydantic import BaseModel
from typing import List, Dict
import os
import subprocess


class TestCase(BaseModel):
    file: str
    name: str


class TestFile(BaseModel):
    file: str
    cases: List[TestCase]


class TestRunResult(BaseModel):
    test_cases: List[TestCase]
    output: str


def get_test_cases(test_dir: str = None) -> List[TestFile]:
    if test_dir is None:
        test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../tests"))
    if not os.path.exists(test_dir):
        raise RuntimeError(f"Directory '{test_dir}' does not exist")

    test_files = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                file_path = os.path.join(root, file)
                test_cases = []
                with open(file_path, 'r') as f:
                    for line in f:
                        if line.strip().startswith("def test_"):
                            test_name = line.split('(')[0].strip()[4:]
                            test_cases.append(TestCase(file=file_path, name=test_name))
                test_files.append(TestFile(file=file_path, cases=test_cases))
    return test_files


def run_tests(test_cases: List[TestCase]) -> TestRunResult:
    test_files = [test_case.file for test_case in test_cases]
    command = ["pytest", "-v"] + test_files
    result = subprocess.run(command, capture_output=True, text=True)
    return TestRunResult(test_cases=test_cases, output=result.stdout)
