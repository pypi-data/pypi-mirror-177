import setuptools

setuptools.setup(
    name="traffic_crashes",
    version="0.1.0",
    author="PSYC 40650",
    author_email="jadynpark@uchicago.edu",
    description="PSYC 40650 Collaborative Project - Traffic Crashes in Chicago",
    url="https://bitbucket.org/ytbai/traffic_crashes/src/master/",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'numpy',
        'scipy',
        'scikit-learn',
        'bokeh==2.2.2',
        'seaborn',
        'qgrid',
        'geoplot'
    ],
)
