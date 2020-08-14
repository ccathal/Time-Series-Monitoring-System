# Time Series Monitoring (TSM) of Slurm Scheduler
This repository consists of -
1. Python3 exporter which collects job queue status information associated with the Slurm scheduler contained in the `src/job_queue_exporter` directory.
2. Python3 tests & associated mock test data for the exporter contained in the `tests` directory.
3. Ansible deplyoment of the exporter, prometheus, grafana and the reverse proxy contained in the `ansible` directory.

## Main Instructions to Deploy TSM System
The deployment of the Time Series Monitoring System occurs under the `localhost` domain.
1. Install Ansible & ansible-galaxy collection for Grafana:
```
sudo apt install ansible && ansible-galaxy collection install community.grafana
```
2. Clone Git Repository:
```
git clone https://gitlab.com/surfprace/cathal.git
```
4. Change the `--command` flag in the exporter service file at `ansible/roles/hpc-exporter/files/hpc-exporter.service` for the python script to execute the official Slurm `squeue` commnd. The following command is recommended to insert:
```
squeue --all -h --format=%A,%j,%a,%g,%u,%P,%v,%D,%C,%T,%V,%M
```
4. From the `ansible` directory, run the ansible playbook & enter root user password when prompted:
```
ansible-playbook -K playbook.yml
```
5. It can happen that if any of the services (`nginx.service`,`hpc-exporter.service`,`prometheus.service`,`grafana-server.service`) being configured by Ansible happen to be already running on the the machine prior to running Ansible will not get restarted. If a service (particularly `nginx.service`) has been running prior to the ansible installation, restart the service manually:
```
systemctl restart <service-name.service>
```
6. Result:
* If you open your web browser and visit the following sites, metrics of each sub-system can be observed:
    * http://localhost:80/grafana/metrics
    * http://localhost:19090/prometheus/metrics
    * http://localhost:8000/metrics (exporter)
* To view the main Prometheus page search `http://localhost:19090/prometheus/`.
* To view Grafana search `http://localhost:80/grafana/` where the Prometheus datasource and JSON dashboard have been preconfigured and graphs should be immediatly available.

## Slurm Exporter
The exporter is avalable as a `pip` package. To install the exporter package execute: 
```
pip3 install job-queue-exporter
```

The package creates `entry_points` as found in the `setup.py` file. These `entry_points` are usually found under `/usr/local/bin/` when the above command is executed.

1. `main_exporter` is the associated entry point to  `main_exporter.py` which contians the exporter main method.
2. `squeue_dummy` is the associated entry point to `squeue.py` which generated mock slurm squeue output for testing purposes.

Note the `slurm_parser.py` does **not** have an associated entry point. The `main_exporter.py` calls the parser with the following:
```
from job_queue_exporter.slurm_parser import parse_output
```
The `parse_ouput` function can then be accessed directly within the main exporter.

## Testing
The `tox` package is used to automate the 3 `pytest` files within the `tests` directory which is run in the CICD pipeline.

## Ansible Deployment
The Ansible `playbook.yml` contains 5 roles:
1. `reverse-proxy` deploys `nginx` reverse proxy for Promteheus and Grafana.
2. `hpc-exporter` deploys the above exporter.
3. `prometheus` deploys Prometheus.
4. `grafana` deploys Grafana.
5. `grafana-config` deploys the associated Grafana datasource (Prometheus) and dashboard.

## Running the Playbook
Prior to running the playbook ensure ansible is installed:
```
sudo apt install ansible
```
Within the `ansible` directory execute:
```
ansible-playbook -K playbook.yml
```
You will be then prompted for your root user password. When entered the ansible playbook will run the above 5 roles.

To execute an individual role, use the --tags flag along with one of the above 5 roles. For example:
```
ansible-playbook -K playbook.yml --tags grafana-config
```
### NGINX Reverse Proxy
Prometheus by default runs at `http://localhost:9090/`. The reverse proxy makes the service available at `http://localhost:19090/prometheus/`. Prometheus metrics are avalaible at `http://localhost:19090/prometheus/metrics`

Grafana by default runs at `http://localhost:3000/`. The reverse proxy makes the service available at `http://localhost:80/grafana/`. Grafana metrics are avalaible at `http://localhost:80/grafana/metrics`.

If the NGINX reverse proxy is already running on the local machine before running the Ansible script the Ansible script may fail to reload the new NGINX configurations. Thhis will have to be maunually done via:
```
systemctl restart nginx.service
```

### HPC-Exporter
The Ansible role for the `hpc-exporter` runs the `main_exporter` entry point as a background service. The associated systemd service file is located under `/etc/systemd/system/hpc-exporter.service` once the Ansible script has finished executing.

The status of the exporter service can be viewed:
```
systemctl status hpc-exporter.service
```

By default the `main_exporter` runs the `squeue_dummy` entry point to generate mock Slurm `squeue` data.
To get the `main_exporter` to execute the proper Slurm squeue command & generate real data, the `--commmand` flag in the service file located under `ansible/roles/hpc-exporter/files/hpc-exporter.service` in the Ansible script will need to be changed. The following is the recommended format which is compatible with `slurm_parser.py`
```
[Unit]
Description=HPC Scheduler Exporter Service

[Service]
ExecStart=main_exporter --command 'squeue --all -h --format=%A,%j,%a,%g,%u,%P,%v,%D,%C,%T,%V,%M'

[Install]
WantedBy=multi-user.target
```

### Prometheus Server
The number one file in configuring Prometheus is `prometheus.yml` which specifies all the Prometheus Targets, their associated http endpoint where metrics are exposed and scraping time interval. Other information can be configured here associated with Prometheus Rules and the built-in Prometheus AlertManager System (not yet implemented). The `prometheus.yml` file is found under `ansible/roles/prometheus/files/prometheus/prometheus.yml` which runs at `http://localhost:9090/` locally or `http://localhost:19090/prometheus/` to the outside world due to the reverse proxy.

### Grafana
Grafana runs at `http://localhost:3000/` locally or `http://localhost:80/grafana/` to the outside world due to the reverse proxy. The default Grafana username and password is `admin` to login.

Two tasks need to be completed before getting nice dynamic graphs of job queue information.
1. Configure our Prometheus data source to http://localhost:19090/prometheus/
2. Configure the dashboard which is stored as JSON data. Our Grafana dashboard stored under `ansible/roles/grafana/files/grafana.json`

Our graphs are created through Prometheus PromQL queries in the following format: `squeue_jobs{job_type=<job_type.name>}` which creates graphs for individual job queue types. The graphs can be further inspected by clicking on an individual `{{slurm_group}}` in the graph legend.

Additionally, our Grafana JSON graph uses the Grafana builtin *variable* tool. This dashboard panels (graphs) to be created dynamically based the available `job_type`. Therefore, all job queue information displayed on graphs is relevant and no graphs are statically written with no available data. If no dashboard data shows when logging in often the user will need to enter `dashboad settings > variables` and double click one of the toggles until the variables show at the bottom of the page.