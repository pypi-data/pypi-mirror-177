from pathlib import Path

import pytest

from infiniaml_idp_client._cli.typed_dict_code_gen import generate

from ..conftest import Config

DATA_PATH = Path(__file__).parent / ".." / "data"


@pytest.mark.skip(reason="Needs work")
@pytest.mark.parametrize(
    "openapi_file, py_file", [("openapi_1.json", "models_1.py"), ("openapi_2.json", "models_2.py")]
)
def test_generate_project_models(openapi_file: str, py_file: str, config: Config):
    openapi_file_path = DATA_PATH / openapi_file
    py_file_path = DATA_PATH / py_file

    with openapi_file_path.open("r") as input, py_file_path.open("r") as expected_output:
        output = generate(input.read())
        assert expected_output.read() == output.clean()
