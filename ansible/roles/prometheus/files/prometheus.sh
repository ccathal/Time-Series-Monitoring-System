#!/bin/bash

# Download prometheus and copy utilities to where they should be in the filesystem
# VERSION=2.2.1
VERSION=$(curl https://raw.githubusercontent.com/prometheus/prometheus/master/VERSION)
wget https://github.com/prometheus/prometheus/releases/download/v${VERSION}/prometheus-${VERSION}.linux-amd64.tar.gz
tar xvzf prometheus-${VERSION}.linux-amd64.tar.gz

sudo cp prometheus-${VERSION}.linux-amd64/prometheus /usr/local/bin/
sudo cp prometheus-${VERSION}.linux-amd64/promtool /usr/local/bin/
sudo cp -r prometheus-${VERSION}.linux-amd64/consoles /etc/prometheus
sudo cp -r prometheus-${VERSION}.linux-amd64/console_libraries /etc/prometheus

# Download alertmanager and copy utilities to where they should be in the filesystem
# VERSION=0.21.0
ALERT_VERSION=$(curl https://raw.githubusercontent.com/prometheus/alertmanager/master/VERSION)
wget https://github.com/prometheus/alertmanager/releases/download/v${ALERT_VERSION}/alertmanager-${ALERT_VERSION}.linux-amd64.tar.gz
tar xvzf alertmanager-${ALERT_VERSION}.linux-amd64.tar.gz

sudo cp alertmanager-${ALERT_VERSION}.linux-amd64/alertmanager /usr/local/bin/
