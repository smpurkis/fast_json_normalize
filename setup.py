from setuptools import find_packages, setup
from Cython.Build import cythonize


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name="fast_json_normalize",
    version="0.0.4",
    packages=find_packages(),
    author="Sam Purkis",
    description="A classification library using a novel audio-inspired algorithm.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/smpurkis/fast_json_normalize",
    ext_modules=cythonize(["fast_json_normalize/cythonized.pyx"]),
    install_requires=[
        'PyObjC;platform_system=="Darwin"',
        'PyGObject;platform_system=="Linux"',
    ]
)