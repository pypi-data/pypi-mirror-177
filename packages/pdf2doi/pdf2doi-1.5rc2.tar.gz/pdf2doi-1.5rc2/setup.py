import setuptools
from setuptools.command.install import install
from os import path
import sys

class InstallCommand(install):
    user_options = install.user_options + [
        ('no-textract', None, None)
    ]
    def initialize_options(self):
        install.initialize_options(self)
        self.notextract = None

    def finalize_options(self):
        install.finalize_options(self)

    def run(self):
        install.run(self)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'),encoding ='unicode_escape') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

print(sys.argv)

if "--no-textract" in sys.argv:
    # Remove the requirement for textract
    print('textract will NOT be installed.')
    required_packages = [x for x in required_packages if not x.startswith('textract')]
    sys.argv.remove("--no-textract")

print(required_packages)

setuptools.setup(name='pdf2doi',
      version='1.5rc2',
      description='A  python library/command-line tool to extract the DOI or other identifiers of a scientific paper from a pdf file.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/MicheleCotrufo/pdf2doi',
      author='Michele Cotrufo',
      author_email='michele.cotrufo@gmail.com',
      license='MIT',
      entry_points = {
        'console_scripts': ["pdf2doi = pdf2doi.main:main"],
      },
      packages=['pdf2doi'],
      install_requires= required_packages,
      zip_safe=False,
      cmdclass={
        'install': InstallCommand,
        }
      )