import os, shutil

from src.utils.logger import log

FILE_NAMES_TO_REMOVE = [
    "__pycache__",
]

FILE_EXTENSIONS_TO_REMOVE = []

FILE_NAMES_TO_IGNORE = ["venv"]


def clean_folder(folder: str | None = ".") -> None:
    for content in os.scandir(folder):
        if content.name not in FILE_NAMES_TO_IGNORE:

            if content.is_file():
                name, ext = os.path.splitext(content.name)
                ext = ext.lstrip(".")
                if (
                    ext in FILE_EXTENSIONS_TO_REMOVE
                    or content.name in FILE_NAMES_TO_REMOVE
                ):
                    os.remove(content.path)
                    log(msg=f"removed {content.path}", prepend="clean", color="green")

            elif content.is_dir():
                if content.name in FILE_NAMES_TO_REMOVE:
                    shutil.rmtree(content.path)
                    log(msg=f"removed {content.path}", prepend="clean", color="green")
                else:
                    clean_folder(content.path)


if __name__ == "__main__":
    clean_folder()
