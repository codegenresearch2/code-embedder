import argparse
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

class ReadmeProcessor:
    def __init__(self, readme_paths):
        self.readme_paths = readme_paths
        self.script_metadata_extractor = ScriptMetadataExtractor()
        self.script_content_reader = ScriptContentReader()

    def process(self):
        code_embedder = CodeEmbedder(
            readme_paths=self.readme_paths,
            script_metadata_extractor=self.script_metadata_extractor,
            script_content_reader=self.script_content_reader,
        )
        code_embedder()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--readme-paths", nargs="+", type=str, help="Paths to Readme files", default=["README.md"]
    )
    args = parser.parse_args()

    processor = ReadmeProcessor(readme_paths=args.readme_paths)
    processor.process()
    logger.info("Code Embedder finished successfully.")


In the rewritten code, I've created a new class `ReadmeProcessor` that encapsulates the logic for processing the README files. This improves modularity and readability by reducing complexity in the main script. The `CodeEmbedder` class from the original code is still used, but it's now initialized and called within the `ReadmeProcessor` class. This simplifies the code structure and makes it easier to understand.