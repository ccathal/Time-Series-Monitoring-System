from setuptools import setup, find_packages

setup(
    name='job_queue_exporter',
    version='0.7',
    description='Prometheus Exporter for job information associated with HPC Scheduler',
    url='http://gitlab.com/surfprace/cathal',
    author='Cathal Corbett',
    author_email='cathalcorbett3@gmail.com',
    zip_safe=False,
    install_requires=['argparse', 'prometheus_client'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'main_exporter = job_queue_exporter.main_exporter:main',
            'squeue_dummy = job_queue_exporter.squeue:main',
        ]
    }
)
