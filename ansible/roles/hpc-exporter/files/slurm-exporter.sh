#!/bin/bash

# Make prometheus user
sudo adduser --no-create-home --disabled-login --shell /bin/false --gecos "Slurm Exporter User" slurm-exporter

# Make directories and dummy files necessary for prometheus
sudo mkdir /usr/local/bin/slurm-exporter
sudo mkdir /var/lib/slurm-exporter

# Assign ownership of the files above to prometheus user
sudo chown -R slurm-exporter:slurm-exporter /etc/slurm-exporter
sudo chown slurm-exporter:slurm-exporter /var/lib/slurm-exporter

# Download prometheus and copy utilities to where they should be in the filesystem
git clone https://gitlab.com/surfprace/cathal.git

sudo cp cathal/main_exporter.py /usr/local/bin/slurm-exporter
sudo cp cathal/slurm_parser.py /usr/local/bin/slurm-exporter
sudo cp cathal/squeue.py /usr/local/bin/slurm-exporter
sudo chmod +x /use/local/bin/slurm-exporter/*.py

# Assign the ownership of the tools above to prometheus user
sudo chown slurm-exporter:slurm-exporter /usr/local/bin/slurm-exporter/

# Populate configuration files
cat roles/slurm-exporter/files/slurm-exporter/slurm-exporter.service| sudo tee /etc/systemd/system/slurm-exporter.service
# systemd
sudo systemctl daemon-reload
sudo systemctl enable slurm-exporter
sudo systemctl start slurm-exporter

# Installation cleanup
rm -rf cathal
