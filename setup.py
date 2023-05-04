from setuptools import setup, find_packages

# with open('README.md', 'r') as file:
#    long_description = file.read()

# with open("requirements.txt", "r") as f:
#    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name="nornir_snmp",
    version="0.5.0",
    description="SNMP transport plugin for Nornir",
    url="https://github.com/jschilders/nornir_snmp",
    packages=find_packages(),
    author="Jos Schilders",
    author_email="jschilders@groomlake.nl",
    license="BSD 2-clause",
    keywords=["snmp", "nornir"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
    ],
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    # install_requires=INSTALL_REQUIRES,
    install_requires=[
        "pysnmplib",
        "nornir",
    ],
    entry_points={
        "nornir.plugins.connections": "SNMP = nornir_snmp.plugins.connections:SNMP"
    },
)
