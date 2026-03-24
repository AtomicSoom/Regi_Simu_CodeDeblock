import subprocess
import sys
import os

# chemin vers ton script Streamlit
script_path = os.path.join(os.path.dirname(__file__), "SendToServerOSC.py")

# lance Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])