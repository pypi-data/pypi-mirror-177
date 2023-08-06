# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dask4dvc', 'dask4dvc.cli', 'dask4dvc.utils']

package_data = \
{'': ['*']}

install_requires = \
['dask-jobqueue>=0.8.1,<0.9.0',
 'dask>=2022.7.1,<2023.0.0',
 'distributed>=2022.7.1,<2023.0.0',
 'dvc>=2.15.0,<3.0.0',
 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['dask4dvc = dask4dvc.cli.main:app']}

setup_kwargs = {
    'name': 'dask4dvc',
    'version': '0.1.0',
    'description': 'Use dask to run the DVC graph',
    'long_description': '[![Coverage Status](https://coveralls.io/repos/github/zincware/dask4dvc/badge.svg?branch=main)](https://coveralls.io/github/zincware/dask4dvc?branch=main)\n![PyTest](https://github.com/zincware/dask4dvc/actions/workflows/pytest.yaml/badge.svg)\n\n# Dask4DVC - Distributed Node Exectuion\n[DVC](dvc.org) provides tools for building and executing the computational graph locally through various methods. \nThe `dask4dvc` package combines [Dask Distributed](https://distributed.dask.org/) with DVC to make it easier to use with HPC managers like [Slurm](https://github.com/SchedMD/slurm).\n\n## Usage\nDask4DVC provides a CLI similar to DVC.\n\n- `dvc repro` becomes `dask4dvc repro`\n\n### SLURM Cluster\n\nYou can use `dask4dvc` easily with a slurm cluster.\nThis requires a running dask scheduler:\n```python\nfrom dask_jobqueue import SLURMCluster\n\ncluster = SLURMCluster(\n    cores=1, memory=\'128GB\',\n    queue="gpu",\n    processes=1,\n    walltime=\'8:00:00\',\n    job_cpu=1,\n    job_extra=[\'-N 1\', \'--cpus-per-task=1\', \'--tasks-per-node=64\', "--gres=gpu:1"],\n    scheduler_options={"port": 31415}\n)\ncluster.adapt()\n```\n\nwith this setup you can then run `dask4dvc repro --address 127.0.0.1:31415` on the example port `31415`.',
    'author': 'zincwarecode',
    'author_email': 'zincwarecode@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
