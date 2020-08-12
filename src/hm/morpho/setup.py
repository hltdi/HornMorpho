from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("letter_tree", ["letter_tree.pyx"]),
               Extension("fs", ["fs.pyx"]),
               Extension("fst", ["fst.pyx"])]

setup(
  name = 'HornMorpho',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
