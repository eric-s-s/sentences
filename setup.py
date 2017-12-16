from distutils.core import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='sentences',
      version='0.1.6',
      description='sentence generator',
      long_description=readme(),
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
      packages=['sentences', 'sentences.words'],
      entry_points={
          'console_scripts': ['gen_pdf=sentences.text_to_pdf:main'],
      },
      package_data={
          '': ['word_lists/*.csv']
      },
      # data_files=[('word_lists', ['word_lists/empty.csv',
      #                             'word_lists/empty_proper_nouns.csv',
      #                             'word_lists/nouns.csv',
      #                             'word_lists/uncountable.csv',
      #                             'word_lists/verbs.csv'])],
      install_requires=['reportlab'],
      include_package_data=True,
      zip_safe=False)
