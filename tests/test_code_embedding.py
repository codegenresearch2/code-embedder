import pytest
from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor

@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (
            [":main.py", "print('Hello, World!')", ""],
            [ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content="")],
        ),
        (["", "print('Hello, World!')", ""], []),
        ([], []),
        (["", "print('Hello, World!')", ""], []),
        (
            [
                ":example.py",
                "import os",
                "print('Hello, World!')",
                "",
                "",
                "print('Do not replace')",
                "",
            ],
            [ScriptMetadata(readme_start=0, readme_end=3, path="example.py", content="")],
        ),
        (
            [
                ":main.py",
                "print('Hello, World!')",
                "",
                ":example.py",
                "import os",
                "print('Hello, World!')",
                "",
                "",
                "print('Do not replace')",
                "",
            ],
            [
                ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content=""),
                ScriptMetadata(readme_start=3, readme_end=6, path="example.py", content="")],
        ),
    ],
    ids=[
        "one_tagged_script",
        "one_untagged_script",
        "empty_readme",
        "one_untagged_script_language_specified",
        "two_tagged_scripts_one_untagged_script",
        "two_tagged_scripts_one_untagged_script_additional",  # Added ID to match the number of parameter sets
    ],
)
def test_script_path_extractor(readme_content: list[str], expected: list[ScriptMetadata]) -> None:
    script_path_extractor = ScriptMetadata.from_readme_content(readme_content)
    result = script_path_extractor.extract()
    assert result == expected

def test_code_embedder(tmp_path) -> None:
    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )

    code_embedder()

    # Additional assertions can be added here to verify the expected behavior of the code_embedder function