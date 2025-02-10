import argparse
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--readme-paths", nargs="+", help="Paths to Readme files", default=["README.md"]
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


In the revised code, I've adjusted the argument parsing for `--readme-paths` to accept multiple values using `nargs="+"`. This allows for the input of multiple README file paths, making the code more flexible. I've also ensured that the instantiation of `ScriptMetadataExtractor` and `ScriptContentReader` occurs after the argument parsing and before the `CodeEmbedder` instantiation, as suggested by the oracle's feedback. The main block is structured correctly, with the `if __name__ == "__main__":` encapsulating the logic that follows it.