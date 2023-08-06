from setuptools import setup
from os import path


root_dir = path.abspath(path.dirname(__file__))
with open(path.join(root_dir, 'README.md')) as f:
    long_description = f.read()

setup(
    name='mkdocs-drawio-exporter-fork',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.9.1',
    packages=['mkdocsdrawioexporter'],
    url='https://github.com/herberton/mkdocs-drawio-exporter',
    license='MIT',
    author='Herberton Candido Souza',
    author_email='herberton@gmail.com',
    description='Exports your Draw.io diagrams at build time for easier embedding into your documentation',
    install_requires=['mkdocs'],

    entry_points={
        'mkdocs.plugins': [
            'drawio-exporter = mkdocsdrawioexporter:DrawIoExporterPlugin',
        ],
    },
)
