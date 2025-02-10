from abc import ABC, abstractmethod
from dataclasses import dataclass
from loguru import logger
import re


@dataclass
class ScriptMetadata:
    readme_start: int
    readme_end: int
    path: str
    content: str


class ScriptMetadataExtractorInterface(ABC):
    @abstractmethod
    def extract(self, readme_content: list[str]) -> list[ScriptMetadata]:
        pass


class ScriptContentReaderInterface(ABC):
    @abstractmethod
    def read(self, script_path: str) -> str:
        pass


class ConcreteScriptMetadataExtractor(ScriptMetadataExtractorInterface):
    def __init__(self) -> None:
        self._code_block_start_regex = r"^.*?:"
        self._code_block_end = ""
        self._path_separator = ":"

    def extract(self, readme_content: list[str]) -> list[ScriptMetadata]:
        scripts = []
        current_block = None

        for row, line in enumerate(readme_content):
            if self._is_code_block_start(line):
                current_block = self._start_new_block(line, row)
            elif self._is_code_block_end(line) and current_block:
                scripts.append(self._finish_current_block(current_block, row, readme_content))
                current_block = None

        return scripts

    def _is_code_block_start(self, line: str) -> bool:
        return re.search(self._code_block_start_regex, line) is not None

    def _is_code_block_end(self, line: str) -> bool:
        return line.strip() == self._code_block_end

    def _start_new_block(self, line: str, row: int) -> dict:
        path = line.split(self._path_separator)[-1].strip()
        return {"start": row, "path": path}

    def _finish_current_block(self, block: dict, end_row: int, readme_content: list[str]) -> ScriptMetadata:
        start_row = block["start"]
        end_row = end_row
        path = block["path"]
        content = "\n".join(readme_content[start_row:end_row+1])
        return ScriptMetadata(readme_start=start_row, readme_end=end_row, path=path, content=content)


class ConcreteScriptContentReader(ScriptContentReaderInterface):
    def read(self, script_path: str) -> str:
        try:
            with open(script_path) as script_file:
                return script_file.read()
        except FileNotFoundError:
            logger.error(f"Error: {script_path} not found. Skipping.")
            return ""


class CodeEmbedder:
    def __init__(
        self,
        readme_paths: list[str],
        script_metadata_extractor: ScriptMetadataExtractorInterface,
        script_content_reader: ScriptContentReaderInterface,
    ) -> None:
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

        script_contents = self._read_script_content(scripts=scripts)
        script_contents.sort(key=lambda x: x.readme_start)
        self._update_readme(
            script_contents=script_contents,
            readme_content=readme_content,
            readme_path=readme_path,
        )

    def _read_readme(self, readme_path: str) -> list[str]:
        if not readme_path.endswith(".md"):
            logger.error("README path must end with .md")
            raise ValueError("README path must end with .md")

        with open(readme_path) as readme_file:
            return readme_file.readlines()

    def _extract_scripts(
        self, readme_content: list[str], readme_path: str
    ) -> list[ScriptMetadata] | None:
        scripts = self._script_metadata_extractor.extract(readme_content=readme_content)
        if not scripts:
            logger.info(f"No script paths found in README in path {readme_path}. Skipping.")
            return None
        logger.info(
            f"""Found script paths in README in path {readme_path}:
            {set(script.path for script in scripts)}"""
        )
        return scripts

    def _read_script_content(self, scripts: list[ScriptMetadata]) -> list[ScriptMetadata]:
        for script in scripts:
            script.content = self._script_content_reader.read(script.path)
        return scripts

    def _update_readme(
        self,
        script_contents: list[ScriptMetadata],
        readme_content: list[str],
        readme_path: str,
    ) -> None:
        updated_readme = []
        readme_content_cursor = 0

        for script in script_contents:
            updated_readme += readme_content[readme_content_cursor : script.readme_start + 1]
            updated_readme += [script.content + "\n"]
            readme_content_cursor = script.readme_end

        updated_readme += readme_content[readme_content_cursor:]

        with open(readme_path, "w") as readme_file:
            readme_file.writelines(updated_readme)