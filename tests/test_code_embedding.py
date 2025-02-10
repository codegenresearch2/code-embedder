import pytest
from typing import List
from pathlib import Path
from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_script_metadata_extractor() -> None:
    test_cases = [
        (
            [":main.py", "print('Hello, World!')", ""],
            [ScriptMetadata(readme_start=0, readme_end=2, path="main.py", section_name=None)],
        ),
        # Add more test cases here...
    ]

    for readme_content, expected in test_cases:
        script_metadata_extractor = ScriptMetadataExtractor()
        result = script_metadata_extractor.extract(readme_content=readme_content)
        assert result == expected

def test_code_embedder_read_script_content() -> None:
    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    scripts = code_embedder._read_script_content(
        scripts=[
            ScriptMetadata(
                readme_start=6, readme_end=7, path="tests/data/example.py", section_name=None
            )
        ]
    )
    assert scripts == [
        ScriptMetadata(
            readme_start=6,
            readme_end=7,
            path="tests/data/example.py",
            content='print("Hello, World! from script")\n',
            section_name=None,
        )
    ]

def test_code_embedder(tmp_path: Path) -> None:
    original_paths = [
        "tests/data/readme0.md",
        "tests/data/readme1.md",
        "tests/data/readme2.md",
    ]
    expected_paths = [
        "tests/data/expected_readme0.md",
        "tests/data/expected_readme1.md",
        "tests/data/expected_readme2.md",
    ]

    # Create a temporary copy of the original file
    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path) as readme_file:
            temp_readme_path.write_text(readme_file.read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path) for temp_readme_path in temp_readme_paths],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    code_embedder()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path) as expected_file, open(temp_readme_path) as updated_file:
            expected_readme_content = expected_file.readlines()
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content


In the revised code, I have:

1. Explicitly defined the return type of the test functions.
2. Simplified the file opening syntax by omitting the mode parameter when reading files.
3. Ensured consistency in variable naming for temporary paths and expected paths.
4. Reviewed the overall structure of the code to align it more closely with the gold code.

These changes should address the feedback received and bring the code even closer to the gold standard.