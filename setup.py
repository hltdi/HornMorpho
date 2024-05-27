from setuptools import setup, find_packages

setup(name='HornMorpho',
#      version='5.0',
#      description='Morphological analyzer/generator for Amharic',
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
                     'languages/fidel/t/*',
                     'languages/fidel/t/fst/*',
                     'languages/fidel/t/lex/*',
                     'languages/fidel/t/cas/*',
                     'languages/fidel/t/data/*',
                     'languages/fidel/t/stat/*',
                     'languages/fidel/t/pkl/*.pkl',
                     'morpho/geez/*']
                     },
      exclude_package_data={'hm':
                             ['__pycache__/*',
                              'morpho/amh_lang.py',
                              'morpho/am_lang.py',
                              'morpho/om_lang.py',
                              'morpho/ti_lang.py',
                              'morpho/stv_lang.py',
                              'morpho/__pycache__/*',
                              'languages/fidel/te/*',
                              'languages/fidel/k/*',
                              'languages/fidel/d/*',
                              'languages/fidel/ch/*',
                              'languages/fidel/m/*',
                              'languages/fidel/mh/*',
                              'languages/fidel/g/*',
                              'languages/old/*']
#                              'languages/som/fst/*',
#                              'languages/orm/pkl/*',
#                              'languages/eng/*']
                              }
                             )
