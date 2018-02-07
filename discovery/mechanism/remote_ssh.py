"""
This module provides the utilities to execute probe in a remote machine
with SSH credential
"""

import ntpath
import paramiko
from discovery.probes.artifacts import PROBEREG


REMOTE_LOCATION = ".delphi/"


def __initiate_ssh_connection(hostname, username, password):
    sshclient = paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshclient.connect(hostname=hostname, username=username, password=password)
    return sshclient


def __send_probe(sshclient, probepath):
    sftp = sshclient.open_sftp()
    probename = ntpath.basename(probepath)
    remotepath = REMOTE_LOCATION + probename
    sftp.put(probepath, remotepath)
    sftp.close()
    return remotepath


def __execute_probe(sshclient, remotepath):
    command = "python " + remotepath
    _, ssh_stdout, ssh_stderr = sshclient.exec_command(command)
    return ssh_stdout, ssh_stderr


def execute_probe(probeid, hostname, options=None):
    """
    Execute a probe in a remote machine by ssh
    """
    username = None
    password = None
    if options:
        username = options.get("username")
        password = options.get("password")
    # Get the probe path
    probepath = PROBEREG.get(probeid, None)
    if not probepath:
        raise Exception("ProbeId is not registered: " + probeid)
    sshclient = __initiate_ssh_connection(hostname, username, password)
    remotepath = __send_probe(sshclient, probepath)
    out, err = __execute_probe(sshclient, remotepath)
    return out, err
