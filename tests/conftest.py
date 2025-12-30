import sys
import os

# Robustly add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"\nDEBUG CONFTEST: Added {src_path} to sys.path\nCurrent path: {sys.path[:3]}...")
