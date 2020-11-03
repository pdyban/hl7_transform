from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.1.6'
account_name = 'pdyban'
setup(
  name = 'hl7_transform',
  packages = find_packages(),
  version = version,
  license='MIT',
  description = 'Library that transforms HL7 messages using mapping schemes',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Pavlo Dyban (Doctolib GmbH)',
  author_email = 'pavlo.dyban@doctolib.com',
  url = f'https://github.com/{account_name}/hl7_transform',
  download_url = f'https://github.com/{account_name}/hl7_transform/archive/v.{version}.tar.gz',
  keywords = ['HL7', 'hospital IT', 'infrastructure', 'message', 'transform'],
  python_requires='>=3',
  install_requires=['hl7apy',],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Developers',
    'Intended Audience :: Healthcare Industry',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Telecommunications Industry',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Communications',
    'Topic :: Software Development :: Libraries',
  ],
  test_suite="hl7_transform.test",
  entry_points={
        "console_scripts": [
            "hl7_transform = hl7_transform.__main__:main",
            ]
        },
)
