from setuptools import setup

setup(name='time_series_monitoring',
    version='0.1',
    description='Time Series Monitoring System',
    url='http://gitlab.com/surfprace/cathal',
    author='Cathal Corbett',
    author_email='cathalcorbett3@gmail.com',
    packages=['time_series_monitoring'],
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'main_exporter = time_series_monitoring.main_exporter:main',
            'slurm_parser = slurm_parser:main',
            'squeue = squeue:main',
        ]
    }
)
