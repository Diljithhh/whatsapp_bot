import uvicorn
import os
import sys
from pathlib import Path

def start():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    # Get port from environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Use 0.0.0.0 instead of 127.0.0.1 to bind to all interfaces
    uvicorn.run(
        "automate_media.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=[str(project_root)]
    )

if __name__ == "__main__":
    start()

