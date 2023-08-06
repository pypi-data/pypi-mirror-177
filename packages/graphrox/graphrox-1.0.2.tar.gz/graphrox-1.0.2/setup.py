from setuptools import setup, find_packages, Distribution
 
 
class BinaryDistribution(Distribution):
    def has_ext_modules(_):
        return True


# from pathlib import Path
# cwd = Path(__file__).parent
# long_description = (cwd / "README.md").read_text()

setup(
    name='graphrox',
    version='1.0.2',
    author="Tanner Davies",
    description='A network graph library for efficiently compressing and generating approximations of graphs',
    license='MIT',
    packages=['graphrox'],
    keywords='machine learning, graph, graph approximation, compression',
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    package_data={
        'graphrox': [
            'graphrox-aarch64-apple-darwin.dylib',
            'graphrox-x86_64-apple-darwin.dylib',
            'graphrox-aarch64-unknown-linux-gnu.so',
            'graphrox-x86_64-unknown-linux-gnu.so',
            'graphrox-aarch64-w64.dll',
            'graphrox-x86_64-w64.dll',
        ],
    },
    distclass=BinaryDistribution,
    setup_requires=['wheel'],
)
