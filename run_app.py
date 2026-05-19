import os
import subprocess
import sys
import webbrowser
import time

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_path, "app.py")

    if not os.path.exists(app_path):
        print("ERROR: app.py was not found.")
        input("Press Enter to close...")
        return

    subprocess.Popen([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.headless=false"
    ])

    time.sleep(3)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    main()