from pathlib import Path
import shutil

root = Path('.').absolute()
target = root / 'pandas_query_tool'

for t in target.rglob('__pycache__'):
    shutil.rmtree(t)
