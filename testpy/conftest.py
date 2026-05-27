import sys
import os

# testpy/ の親ディレクトリ（プロジェクトルート）を import path に追加
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
