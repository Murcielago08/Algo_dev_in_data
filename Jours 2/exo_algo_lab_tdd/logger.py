import time
import os

class SimpleLogger:
    """Logger simple : garde les logs en mémoire et écrit dans un fichier."""
    def __init__(self):
        self.records = []

    def log(self, level: str, message: str):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] {level.upper()}: {message}"
        self.records.append(entry)

    def write_to_file(self, path: str, mode='a'):
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        with open(path, mode, encoding='utf-8') as f:
            for r in self.records:
                f.write(r + '\n')

    def clear(self):
        self.records.clear()
