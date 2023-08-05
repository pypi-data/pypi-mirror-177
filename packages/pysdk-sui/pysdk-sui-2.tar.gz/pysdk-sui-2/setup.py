from distutils.core import setup

setup(
    name='pysdk-sui',  # How you named your package folder (MyLib)
    packages=['pysdk-sui'],  # Chose the same as "name"
    version='2',  # Start with a small number and increase it with every change you make
    license='Open Software License 3.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Python SDK for SUI',  # Give a short description about your library
    author='Jammer',  # Type in your name
    readme="README.md",
    author_email='andlolkek@gmail.com',  # Type in your E-Mail
    url='https://github.com/Jaammerr/python_sui_sdk',  # Provide either the link to your github or to your website
    download_url='https://github.com/Jaammerr/python_sui_sdk/archive/refs/tags/v1.tar.gz',  # I explain this later on
    keywords=['SUI'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
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
