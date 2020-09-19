from setuptools import setup, find_packages
from kicad_tools import __version__

setup(
    name='kicad2jlcpcb',
    version=__version__,
    description='Plugin for KiCad 5 that allows generate files for jlcpcb pcb manufacturing and assembly service',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danidask/kicad2jlcpcb',
    author='Daniel Alvarez',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    entry_points={
        "console_scripts": [
            "kicad2jlcpcb = kicad_tools.kicad_tools:main",
        ]
    }
)
