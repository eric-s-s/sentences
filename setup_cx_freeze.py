from cx_Freeze import setup, Executable
import sys
import os


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


options = {
    'build_exe': {
        'include_files': [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
         ],
    },
}


base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('sentences/tkinter/go.py', base=base, shortcutName='GOOOOO')
]

setup(name='test_cx',
      version='1.1',
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
      packages=['sentences', 'sentences.words', 'sentences.tkinter'],

      package_data={
          '': ['data/*.csv', 'data/*.cfg']
      },
      install_requires=['reportlab', 'cx_freeze'],
      include_package_data=True,
      zip_safe=False
      )





