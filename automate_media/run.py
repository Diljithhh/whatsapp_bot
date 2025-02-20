import uvicorn
import os
import sys
from pathlib import Path

def start():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    uvicorn.run(
        "automate_media.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root)]
    )

if __name__ == "__main__":
    start()

