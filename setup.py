from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='minesweeper',
    version='1.0.0',
    description='A Minesweeper implementation with Python and Pyxel',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/btravers/minesweeper',
    author='Benoit TRAVERS',
    author_email='benoit.travers.fr@gmail.com',
    license='MIT',
    packages=[
        'minesweeper'
    ],
    install_requires=[
        'pyxel'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'minesweeper=minesweeper:run'
        ]
    }
)