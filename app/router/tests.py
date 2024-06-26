from typing import List

from fastapi import APIRouter

from app.models.test_case import get_test_cases, run_tests, TestFile, TestCase, TestRunResult

router = APIRouter()


@router.get("/test_cases", response_model=List[TestFile])
async def fetch_test_cases():
    return get_test_cases()


@router.post("/run_tests", response_model=TestRunResult)
async def execute_tests(test_cases: List[TestCase]):
    return run_tests(test_cases)
