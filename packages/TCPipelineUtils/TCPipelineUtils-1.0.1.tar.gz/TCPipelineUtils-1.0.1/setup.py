from setuptools import setup

setup(
    name='TCPipelineUtils',
    version='1.0.1',
    author='Matheus Tramontini',
    author_email='matheus.lopes@tc.com.br',
    packages=['TCPipelineUtils'],
    install_requires=[
        "TCGCSUtils==1.0.*",
        "numpy==1.23.*",
        "pandas==1.4.*"
    ],
    description='Lib to encapsulate TC pipelines functions'
)
