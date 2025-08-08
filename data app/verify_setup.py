import sys
import os
import importlib.util
import subprocess

def check_module(module_name):
    return importlib.util.find_spec(module_name) is not None

print("\n--- DA MVP Environment Verification ---")
print(f"Python version: {sys.version.split()[0]}")
if sys.version_info < (3, 9):
    print("❌ Python 3.9 or higher required.")
else:
    print("✅ Python version is sufficient.")

modules = ["pandas", "sqlalchemy", "streamlit", "plotly", "openpyxl", "xlrd"]
for mod in modules:
    if check_module(mod):
        print(f"✅ {mod} is installed.")
    else:
        print(f"❌ {mod} is NOT installed.")

if os.path.isfile('data/database.db'):
    print("✅ SQLite database file exists.")
else:
    print("❌ SQLite database file does not exist.")

try:
    subprocess.run(["streamlit", "version"], check=True)
    print("✅ Streamlit CLI is available.")
except:
    print("❌ Streamlit CLI is not available. Check your installation.")
