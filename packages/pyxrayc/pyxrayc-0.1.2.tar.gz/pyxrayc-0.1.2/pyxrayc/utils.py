import shutil


def get_executable_path(name: str) -> str:
    return shutil.which(name)
