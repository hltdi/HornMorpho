from setuptools import setup, find_packages

setup(name='HornMorphoA',
      version='5.0',
      description='Morphological analyzer/generator for Amharic',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing'
      ],
      install_requires=["conllu"],
      python_requires='>=3.5',
      packages=find_packages("src"),
      package_dir={'': "src"},
      package_data={'hm':
                    ['languages/fidel/a/*',
                     'languages/fidel/a/fst/*',
                     'languages/fidel/a/lex/*',
                     'languages/fidel/a/cas/*',
                     'languages/fidel/a/data/*',
                     'languages/fidel/a/stat/*',
                     'languages/fidel/a/pkl/*.pkl',
                     'morpho/geez/*']
                     },
      exclude_package_data={'hm':
                             ['languages/fidel/t/*',
                              'languages/fidel/te/*',
                              'languages/fidel/k/*',
                              'languages/fidel/d/*',
                              'languages/fidel/ch/*',
                              'languages/fidel/m/*',
                              'languages/fidel/mh/*',
                              'languages/fidel/g/*',
                              'languages/old/*',
                              'languages/eng/*',
                              'languages/orm/*',
                              'languages/som/*']
                              }
                             )
