from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='SuperSubCap',
  version='0.0.4',
  description='Superscripts and subscripts for latin and greek letters, numbers and operands',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Dryhb/SuperSubCap_library',  
  author='Dryhb',
  author_email='dryhb.pseudotooshort@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='latin greek subscripts superscripts caps letters', 
  packages=find_packages(),
  install_requires=[''] 
)
