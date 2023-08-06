from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]



setup(
   name='board_to_fen_proba',
   version='0.0.1',
   author='Dominik Maćkiewicz',
   author_email='dominik.mackiewicz@icloud.com',
   packages=['board_to_fen'],
   scripts=[],
   url='http://pypi.python.org/pypi/board_to_fen/',
   license='MIT',
   description='An package that converts digial chessboard image into Forsyth-Edwards notation',
   long_description=open('README.md').read(),
   install_requires=[
       "tensorflow",
       "keras",
       "opencv-python",
       "pillow",
       "numpy"
   ],
   include_package_data=True
)
