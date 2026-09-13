from pathlib import Path
from typing import TypedDict


TEST_CASE_DIRECTORY = Path(__file__).parent / "testCases"


class JSSPProblem(TypedDict):
    jobs: int
    machines: int
    schedule: list[list[int]]


def get_test_cases() -> list[Path]:
    return sorted(TEST_CASE_DIRECTORY.glob("*.txt"))


def get_test_case_dimensions(file_path: Path) -> tuple[int, int]:
    values = file_path.read_text(encoding="utf-8").split()

    jobs, machines = map(int, values[:2])

    return jobs, machines


def read_JSSP(file_path: str) -> JSSPProblem:
    values = Path(file_path).read_text(encoding="utf-8").split()

    if len(values) < 2:
        raise ValueError("The file must define the number of jobs and machines.")

    try:
        jobs, machines = map(int, values[:2])
        schedule = list(map(int, values[2:]))
    except ValueError as error:
        raise ValueError("The file must contain only integers.") from error

    if jobs < 0 or machines < 0:
        raise ValueError("jobs and machines must be non-negative.")

    columns = 2 * machines

    expected_schedule_values = jobs * columns

    if len(schedule) != expected_schedule_values:
        raise ValueError(
            "Expected " + str(expected_schedule_values) + " schedule values, "
            "but found " + str(len(schedule)) + "."
        )

    JSSP = [
        schedule[index * columns : (index + 1) * columns]
        for index in range(jobs)
    ]

    return {
        "jobs": jobs,
        "machines": machines,
        "schedule": JSSP,
    }