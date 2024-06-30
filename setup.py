from setuptools import setup, find_packages

setup(name='HornMorpho',
      packages=find_packages(where="src"),
      package_dir={'': "src"},
      include_package_data=True,
      exclude_package_data={'hm': ['__pycache__/*']
                             }
                             )
