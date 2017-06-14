from setuptools import setup

setup(name='TextPreViz',
      version='0.1',
      description='text analysis and visualization aider',
      url='https://github.com/yang0339/TextPreViz',
      author='Fred Yang',
      author_email='fredyang0507@gmail.com',
      license='MIT',
      packages=['TextPreViz'],
      package_data={'': ['self_constructed_dict.csv']},
      zip_safe=False,
      include_package_data=True,
      install_requires = [
              'nltk',
              'matplotlib',
              'pandas',
              'numpy',
              ],
)