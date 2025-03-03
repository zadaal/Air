import subprocess
import PyInstaller.__main__
PyInstaller.__main__.run([
    'main_import_envi_data.py',
    '--onefile',
    '--icon=air_icon.ico',
    '--windowed'
])

"""
command = [
    "pyinstaller",
    "--onefile",
    "--icon=air_icon.ico",
    "main_import_envi_data.py"
]
subprocess.run(command, check=True)
"""