from setuptools import setup, find_packages

setup(
    name='superbuddy',
    version='0.0.5',
    author='Rahul Shome',
    author_email='rahulshome8@gmail.com',
    packages=find_packages(),
    install_requires=['click'],
    keywords='example',
    entry_points="""
    [console_scripts]
    buddy=cli.superbuddy:main
    """
)