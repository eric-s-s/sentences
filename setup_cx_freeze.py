from cx_Freeze import setup, Executable
import sys
import os


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

DLLS = ''
for directory in sys.path:
    if directory.endswith('DLLs'):
        DLLS = directory
# original_python = os.path.dirname(DLLS)
# os.environ['TCL_LIBRARY'] = os.path.join(original_python, 'tcl', 'tcl8.6')
# os.environ['TK_LIBRARY'] = os.path.join(original_python, 'tcl', 'tk8.6')


options = {
    'build_exe': {
        'include_files': [
            os.path.join(DLLS, 'tk86t.dll'),
            os.path.join(DLLS, 'tcl86t.dll'),
         ],
        'excludes': ['PyQt5']
    },
}


base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('sentences/gui/go_delete_me.py',  # TODO change this
               base=base,
               shortcutName='It\'s GO TIME!',
               shortcutDir='DesktopFolder',
               icon='sentences/data/go_time.ico',
               )
]

setup(name='test_cx',
      version='1.4',
      description='a simple cx_freeze test',
      options=options,
      executables=executables,

      keywords='',
      url='http://github.com/eric-s-s/sound_test',
      author='Eric Shaw',
      author_email='shaweric01@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          "Operating System :: Windows",
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ],
      packages=['sentences', 'sentences.words', 'sentences.gui'],

      package_data={
          '': ['data/*.csv', 'data/*.cfg', 'data/*.ico']
      },
      install_requires=['reportlab'],
      include_package_data=True,
      zip_safe=False
      )
