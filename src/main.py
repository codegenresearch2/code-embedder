import argparse
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--readme-paths", type=str, help="Paths to Readme files", default="README.md"
    )
    args = parser.parse_args()

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()

    code_embedder = CodeEmbedder(
        readme_paths=[args.readme_paths],
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    code_embedder()
    logger.info("Code Embedder finished successfully.")


In the revised code, I've specified the type for the `--readme-paths` argument as `type=str` and adjusted the default value to be a single string `"README.md"`. I've also ensured that the argument parsing occurs before the instantiation of any classes. The main block is structured correctly, with the `if __name__ == "__main__":` encapsulating all the logic that follows it, including the argument parsing.