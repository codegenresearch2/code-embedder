import pytest
from typing import List
from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_script_metadata_extractor():
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

def test_code_embedder_read_script_content():
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

def test_code_embedder(tmp_path):
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
    temp_readme_paths = [str(tmp_path / f"readme{i}.md") for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path, 'r') as readme_file:
            with open(temp_readme_path, 'w') as temp_file:
                temp_file.write(readme_file.read())

    code_embedder = CodeEmbedder(
        readme_paths=temp_readme_paths,
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    code_embedder()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path, 'r') as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path, 'r') as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content


In the revised code, I have:

1. Ensured that the import statements are consistent with the gold code.
2. Reviewed the structure of the test functions to match the logical flow and organization of the gold code.
3. Updated the temporary file handling to match the gold code's approach.
4. Double-checked the assertions to ensure they are structured similarly to those in the gold code.
5. Ensured consistency in naming to maintain clarity and readability.

These changes should address the feedback received and bring the code even closer to the gold standard.