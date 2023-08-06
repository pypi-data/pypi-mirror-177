from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='algorsort',
  version='2',
  description='A few sorting algorithms!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://jased.xyz/',  
  author='Jase Williams',
  author_email='jased@jased.xyz',
  license='MIT', 
  classifiers=classifiers,
  keywords='sorting', 
  packages=find_packages(),
  install_requires=[''] 
)
