THIS IS TO MAKE AN EXECUTABLE FOR YOU APPLICATION

rm -rf venv  # Replace 'venv' with your venv's name if it's different
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt     #Optional pip freeze > requirements.txt
pip install pyinstaller
pyinstaller --onefile appp.py

#######################################################################################################
#Look at the differences with the .spec file that is created and then add the new lines that you find here to the existing one while correcing the paths

# myapp.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['appp.py'],
             pathex=['/path/to/your/app'],
             binaries=[],
             datas=[('/path/to/your/app/templates', 'templates'),
                    ('/path/to/your/app/static', 'static')],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='appp',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )


pyinstaller myapp.spec
####################################################################################
pyinstaller myapp.spec


###################################################################################
If it still doesnt work got to the appp.py and fix the Flask app instance:

import sys
import os

template_dir = os.path.join(sys._MEIPASS, 'templates')
static_dir = os.path.join(sys._MEIPASS, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
#########################################################################################
