import pytest
from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor

# Implement the `from_readme_content` method in the `ScriptMetadata` class
class ScriptMetadata:
    def __init__(self, readme_start, readme_end, path, content=""):
        self.readme_start = readme_start
        self.readme_end = readme_end
        self.path = path
        self.content = content

    @staticmethod
    def from_readme_content(readme_content):
        metadata_list = []
        for i, line in enumerate(readme_content):
            if line.startswith(":"):
                start = i
                while not readme_content[i].startswith(""):
                    i += 1
                end = i
                path = readme_content[start].split(":")[1].strip()
                content = "\n".join(readme_content[start+1:end])
                metadata_list.append(ScriptMetadata(readme_start=start, readme_end=end, path=path, content=content))
        return metadata_list

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
        "one_tagged_script_one_untagged_script",
        "two_tagged_scripts_one_untagged_script",
    ],
)
def test_script_path_extractor(
    readme_content: list[str], expected: list[ScriptMetadata]
) -> None:
    script_path_extractor = ScriptMetadata.from_readme_content(readme_content)
    result = script_path_extractor
    assert result == expected

# Define the `_read_script_content` method in the `CodeEmbedder` class
class CodeEmbedder:
    def __init__(self, readme_paths, script_content_reader, script_metadata_extractor):
        self.readme_paths = readme_paths
        self.script_content_reader = script_content_reader
        self.script_metadata_extractor = script_metadata_extractor

    def _read_script_content(self, scripts):
        script_contents = []
        for script in scripts:
            content = self.script_content_reader.read(script.path)
            script_contents.append(ScriptMetadata(readme_start=script.readme_start, readme_end=script.readme_end, path=script.path, content=content))
        return script_contents

    def __call__(self):
        for readme_path in self.readme_paths:
            with open(readme_path) as readme_file:
                readme_content = readme_file.readlines()
            scripts = ScriptMetadata.from_readme_content(readme_content)
            updated_scripts = self._read_script_content(scripts)
            with open(readme_path, 'w') as readme_file:
                for script in updated_scripts:
                    readme_content[script.readme_start:script.readme_end+1] = [f":{script.path}\n{script.content}\n"]
                readme_file.writelines(readme_content)

def test_code_embedder_read_script_content() -> None:
    script_content_reader = ScriptContentReader()
    script_metadata_extractor = ScriptMetadataExtractor()
    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_content_reader=script_content_reader,
        script_metadata_extractor=script_metadata_extractor,
    )

    scripts = [
        ScriptMetadata(readme_start=6, readme_end=7, path="tests/data/example.py", content="")
    ]
    result = code_embedder._read_script_content(scripts)
    assert result == [
        ScriptMetadata(
            readme_start=6,
            readme_end=7,
            path="tests/data/example.py",
            content='print("Hello, World! from script")\n',
        )
    ]

def test_code_embedder(tmp_path) -> None:
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

    script_content_reader = ScriptContentReader()
    script_metadata_extractor = ScriptMetadataExtractor()
    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path) for temp_readme_path in temp_readme_paths],
        script_content_reader=script_content_reader,
        script_metadata_extractor=script_metadata_extractor,
    )

    code_embedder()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path) as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path) as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content