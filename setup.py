from setuptools import setup

setup(
    name='schemadocs',
    version='0.1.0',
    py_modules=['schemadocs'],
    install_requires=[
        "Click", "Jinja2"
    ],
    entry_points={
        'console_scripts': [
            'schemadocs = schemadocs:cli',
        ],
    },
)
