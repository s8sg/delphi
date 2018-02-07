"""
Module to provide methods to run discovery
"""
import discovery.mechanism.remote_ssh
from discovery.probes.artifacts import APP_PROBES
import discovery.model


def run_discovery(hostname, options=None, app=None):
    apps = []
    if app:
        apps.append(app)
    else:
        apps.extend(list(APP_PROBES.keys()))
      
