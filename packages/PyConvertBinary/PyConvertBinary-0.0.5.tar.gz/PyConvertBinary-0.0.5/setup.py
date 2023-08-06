from setuptools import setup, find_packages

classifers = [
			  'Development Status :: 5 - Production/Stable',
			  'Intended Audience :: Education',
			  'Operating System :: Microsoft :: Windows :: Windows 10',
			  'License :: OSI Approved :: MIT License',
			  'Programming Language :: Python :: 3.9'
			  ]

setup (name='PyConvertBinary',
	   version='0.0.5',
	   description='Basic Binary Converter',
	   long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	   url='',
	   author='R3Pulse',
	   author_email='adrain911@gmail.com',
	   license='MIT',
	   classifiers=classifers,
	   keywords = ['converter', 'binary', 'decimal'],
	   packages=find_packages(),
	   install_requires=['']
)