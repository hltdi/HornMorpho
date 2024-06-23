from setuptools import setup, find_packages

setup(name='HornMorpho',
#      version='5.1',
#      description='Morphological analyzer/generator for languages of the Horn of Africa',
#      author='Michael Gasser',
#      author_email='gasser@indiana.edu',
#      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing'
      ],
#      install_requires=["conllu"],
#      python_requires='>=3.5',
      packages=find_packages(where="src"),
      package_dir={'': "src"},
      include_package_data=True,
#      package_data={'languages': ['eng/*']},
      exclude_package_data={'hm': ['__pycache__/*']
                             }
                             )
