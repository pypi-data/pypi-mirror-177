from setuptools import setup, find_packages

########SAVE INFORMATION########
# python3 setup.py sdist bdist_wheel
# twine uplload dist/* --verbose
########SAVE INFORMATION########


VERSION = '0.0.3'
DESCRIPTION = 'A Simple Game Engine Libary'
LONG_DESCRIPTION = 'Check my github for a longer description. GITHUB: https://github.com/coding610/MySEAS/tree/master'

setup(
        name='My-SEAS',
        version=VERSION,
        author='Sixten Bohman',
        author_email='Sixten.bohman.08@gmail.com',
        description=DESCRIPTION,
        long_description_content_type='text/markdown',
        long_description=LONG_DESCRIPTION,

        packages=find_packages(),
        install_requires=['pygame', 'numpy'],
        keywords=['Python', 'Game Engine', 'Game', 'Engine', 'Beginner', 'Education', 'SEAS', 'MySEAS'],
        classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            ] 
        )
