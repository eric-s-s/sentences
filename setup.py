from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='sentences',
      version='2.3',
      description='sentence generator',
      long_description=readme(),
      keywords='',
      url='http://github.com/eric-s-s/sound_test',
      author='Eric Shaw',
      author_email='shaweric01@gmail.com',
      license='MIT',
      classifiers=[
        'Development Status :: 4 - Beta',
        "Operating System :: Windows",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
      ],
      packages=['sentences', 'sentences.words', 'sentences.backend', 'sentences.gui'],
      entry_points={
          'console_scripts': ['gen_pdf = sentences.guimain:main_app'],
      },
      package_data={
          '': ['data/*.csv', 'data/default.cfg', 'data/*.txt', 'data/*.ico']
      },
      install_requires=['reportlab'],
      include_package_data=True,
      zip_safe=False)
