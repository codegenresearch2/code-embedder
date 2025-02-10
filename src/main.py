import argparse
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--readme-paths", nargs="+", type=str, help="Paths to Readme files", default=["README.md"]
    )
    args = parser.parse_args()

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()

    code_embedder = CodeEmbedder(
        readme_paths=args.readme_paths,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    code_embedder()
    logger.info("Code Embedder finished successfully.")


In the revised code, I've moved the argument parsing to the beginning of the main block, before the instantiation of any classes. I've also added `nargs="+"` to the `--readme-paths` argument definition to allow for multiple paths. The default value for `--readme-paths` is now a list containing the default path `"README.md"`. The main logic of the script is encapsulated within the `if __name__ == "__main__":` block.