from setuptools import setup, find_packages

setup(name='hpc_job_scheduler_exporter',
    version='0.1',
    description='Prometheus Exporter for job information associated with HPC Scheduler',
    url='http://gitlab.com/surfprace/cathal',
    author='Cathal Corbett',
    author_email='cathalcorbett3@gmail.com',
    zip_safe=False,
    install_requires=[],
    packages=find_packages('hpc_job_scheduler_exporter', exclude=['tests']),
    entry_points={
        'console_scripts': [
            'main_exporter = hpc_job_scheduler_exporter.main_exporter:main',
            'slurm_parser = slurm_parser:parse_output',
            'squeue = squeue:main',
        ]
    }
)
