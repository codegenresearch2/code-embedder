import re
from dataclasses import dataclass
from typing import List
from loguru import logger

@dataclass
class ScriptMetadata:
    readme_start: int
    readme_end: int
    path: str
    content: str

class ScriptMetadataExtractor:
    def __init__(self, content: str) -> None:
        self.content = content

    def extract_metadata(self, readme_content: List[str]) -> List[ScriptMetadata]:
        scripts = []
        current_block = None
        code_block_start_regex = r"^.*?:"
        code_block_end = ""
        path_separator = ":"

        for row, line in enumerate(readme_content):
            if re.search(code_block_start_regex, line) is not None:
                path = line.split(path_separator)[-1].strip()
                current_block = {"start": row, "path": path}
            elif line.strip() == code_block_end and current_block:
                scripts.append(ScriptMetadata(
                    readme_start=current_block["start"],
                    readme_end=row,
                    path=current_block["path"],
                    content=self.content
                ))
                current_block = None

        return scripts

class ScriptContentReader:
    def read_script_content(self, scripts: List[ScriptMetadata]) -> List[ScriptMetadata]:
        script_contents = []

        for script in scripts:
            try:
                with open(script.path) as script_file:
                    script.content = script_file.read()

                script_contents.append(script)

            except FileNotFoundError:
                logger.error(f"Error: {script.path} not found. Skipping.")

        return script_contents

class CodeEmbedder:
    def __init__(self, readme_paths: List[str], script_metadata_extractor: ScriptMetadataExtractor, script_content_reader: ScriptContentReader) -> None:
        self._readme_paths = readme_paths
        self._script_metadata_extractor = script_metadata_extractor
        self._script_content_reader = script_content_reader

    def __call__(self) -> None:
        for readme_path in self._readme_paths:
            self._process_readme(readme_path)

    def _process_readme(self, readme_path: str) -> None:
        readme_content = self._read_readme(readme_path)
        if not readme_content:
            logger.info(f"Empty README in path {readme_path}. Skipping.")
            return

        scripts = self._extract_scripts(readme_content=readme_content, readme_path=readme_path)
        if not scripts:
            return

        scripts = self._read_script_content(scripts=scripts)
        self._update_readme(scripts=scripts, readme_content=readme_content, readme_path=readme_path)

    def _read_readme(self, readme_path: str) -> List[str]:
        if not readme_path.endswith(".md"):
            logger.error("README path must end with .md")
            raise ValueError("README path must end with .md")

        with open(readme_path) as readme_file:
            return readme_file.readlines()

    def _extract_scripts(self, readme_content: List[str], readme_path: str) -> List[ScriptMetadata] | None:
        scripts = self._script_metadata_extractor.extract_metadata(readme_content=readme_content)
        if not scripts:
            logger.info(f"No script paths found in README in path {readme_path}. Skipping.")
            return None
        logger.info(f"Found script paths in README in path {readme_path}: {set(script.path for script in scripts)}")
        return scripts

    def _read_script_content(self, scripts: List[ScriptMetadata]) -> List[ScriptMetadata]:
        return self._script_content_reader.read_script_content(scripts=scripts)

    def _update_readme(self, scripts: List[ScriptMetadata], readme_content: List[str], readme_path: str) -> None:
        scripts.sort(key=lambda x: x.readme_start)
        updated_readme = []
        readme_content_cursor = 0

        for script in scripts:
            updated_readme += readme_content[readme_content_cursor : script.readme_start + 1]
            updated_readme += script.content + "\n"
            readme_content_cursor = script.readme_end

        updated_readme += readme_content[readme_content_cursor:]

        with open(readme_path, "w") as readme_file:
            readme_file.writelines(updated_readme)