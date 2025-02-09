import pytest
from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def test_code_embedder():
    code_embedder = CodeEmbedder(
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader()
    )

    # Test cases for script metadata extraction
    readme_content_1 = [":main.py", "print('Hello, World!')", ""]
    expected_1 = [ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content="")]
    result_1 = code_embedder.extract_script_metadata(readme_content=readme_content_1)
    assert result_1 == expected_1

    readme_content_2 = ["", "print('Hello, World!')", ""]
    expected_2 = []
    result_2 = code_embedder.extract_script_metadata(readme_content=readme_content_2)
    assert result_2 == expected_2

    readme_content_3 = []
    expected_3 = []
    result_3 = code_embedder.extract_script_metadata(readme_content=readme_content_3)
    assert result_3 == expected_3

    readme_content_4 = ["", "print('Hello, World!')", ""]
    expected_4 = []
    result_4 = code_embedder.extract_script_metadata(readme_content=readme_content_4)
    assert result_4 == expected_4

    readme_content_5 = [
        ":main.py",
        "print('Hello, World!')",
        "",
        ":example.py",
        "import os",
        "print('Hello, World!')",
        "",
        "",
        "print('Do not replace')",
        ""
    ]
    expected_5 = [
        ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content=""),
        ScriptMetadata(readme_start=3, readme_end=6, path="example.py", content="")
    ]
    result_5 = code_embedder.extract_script_metadata(readme_content=readme_content_5)
    assert result_5 == expected_5

    # Test reading script content
    scripts = [
        ScriptMetadata(readme_start=6, readme_end=7, path="tests/data/example.py", content="")
    ]
    updated_scripts = code_embedder._read_script_content(scripts=scripts)
    assert updated_scripts == [
        ScriptMetadata(
            readme_start=6,
            readme_end=7,
            path="tests/data/example.py",
            content='print("Hello, World! from script")\n'
        )
    ]

    # Test embedding code
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
        with open(expected_path) as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path) as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content