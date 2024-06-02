from setuptools import setup, find_packages

setup(name="HornMorpho",
#      classifiers=[
#          'Development Status :: 5 - Production/Stable',
#          'Intended Audience :: Information Technology',
#          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
#          'Programming Language :: Python :: 3',
#          'Topic :: Text Processing'
#      ],
      packages=find_packages("src"),
      package_dir={"": "src"},
      include_package_data=True,
#      package_data={"languages": ["eng/*"]},
      exclude_package_data={"hm": ["__pycache__/*"]
                             }
                             )
