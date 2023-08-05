from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pysdk_sui',
    packages=['pysdk_sui'],
    version='0.2',
    license='Open Software License 3.0',
    description='Python SDK for Sui Blockchain',
    author='Jammer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email='andlolkek@gmail.com',
    url='https://github.com/Jaammerr/python_sui_sdk',
    download_url='https://github.com/Jaammerr/python_sui_sdk/archive/refs/tags/v1.tar.gz',
    keywords=['SUI'],
    install_requires=[
        'bip_utils',
        'requests',
        'pyuseragents',
        'mnemonic'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
