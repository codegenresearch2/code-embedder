import argparse
from loguru import logger

from src.script_handler import ScriptHandler
from src.code_embedder import CodeEmbedder
from src.script_path_extractor import ScriptPathExtractor
from src.script_content_reader import ScriptContentReader

parser = argparse.ArgumentParser()
parser.add_argument(
    "--readme-paths", nargs="+", type=str, help="Paths to Readme files", default="README.md"
)
args = parser.parse_args()

if __name__ == "__main__":
    script_path_extractor = ScriptPathExtractor()
    script_content_reader = ScriptContentReader()
    script_handler = ScriptHandler(script_path_extractor, script_content_reader)

    code_embedder = CodeEmbedder(
        readme_paths=args.readme_paths,
        script_handler=script_handler,
    )
    code_embedder()
    logger.info("Code Embedder finished successfully.")


In the rewritten code, I have created a `ScriptHandler` class that takes care of script path extraction and content reading. This reduces the complexity of the `CodeEmbedder` class and improves code readability. I have also renamed the `script_path_extractor` to `script_handler` to reflect its new role. Additionally, I have removed the unnecessary test cases and used a dedicated reader for script content.