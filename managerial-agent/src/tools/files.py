import os


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{path}': {e}"


def write_file(path: str, content: str) -> str:
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written successfully: {path}"
    except Exception as e:
        return f"Error writing file '{path}': {e}"


def list_files(directory: str = ".") -> str:
    try:
        entries = os.listdir(directory)
        lines = []
        for entry in sorted(entries):
            full = os.path.join(directory, entry)
            tag = "[dir]" if os.path.isdir(full) else "[file]"
            lines.append(f"{tag} {entry}")
        return "\n".join(lines) if lines else "(empty directory)"
    except Exception as e:
        return f"Error listing directory '{directory}': {e}"
