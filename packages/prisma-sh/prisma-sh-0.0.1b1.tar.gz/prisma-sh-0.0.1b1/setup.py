from setuptools import setup
import sys

with open('README.md') as f:
    long_description = f.read()

if sys.version_info[:3] < (3, 6, 1):
    raise Exception("websockets requires Python >= 3.6.1.")


setup(name='prisma-sh',
      version='0.0.1b1',
      description='`Command-line access to the controller-based Prisma SD-WAN ION Troubleshooting Toolkit.`',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ebob9/prisma-sh',
      author='Aaron Edwards',
      author_email='prisma-sh@ebob9.com',
      license='MIT',
      install_requires=[
            'cloudgenix >= 6.1.1b1',
            'fuzzywuzzy >= 0.17.0',
            'pyyaml >= 3.13'
      ],
      packages=['prisma_sh_lib'],
      classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.10"
      ],
      python_requires='>=3.10.1',
      entry_points={
            'console_scripts': [
                  'prisma-sh = prisma_sh_lib:toolkit_client',
            ]
      },
      )
