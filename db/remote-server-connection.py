# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 17:15:07 2013

@author: dchen
"""

"""
DO NOT COMMIT THIS UNTIL YOU TAKE OUT THE PASSWORDS!
"""
"""
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('52916382e0b8cd6b2300001c@wordpresstest-gsumm.rhcloud.com',
            username='Maveri2k@yahoo.com', 
            password='gsummphds')
            
"""
# add_host 52916382e0b8cd6b2300001c@wordpresstest-gsumm.rhcloud.com, Maveri2k@yahoo.com, gsummphds

"""
#!/usr/bin/python

import paramiko
import cmd

class RunCommand(cmd.Cmd):
    """ Simple shell to run a command on the host """

    prompt = 'ssh > '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        """add_host 
        Add the host to the host list"""
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: host "

    def do_connect(self, args):
        """Connect to all hosts in the hosts list"""
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            client.connect(host[0], 
                username=host[1], 
                password=host[2])
            self.connections.append(client)

    def do_run(self, command):
        """run 
        Execute this command on all hosts in the list"""
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s' % (host[0], line)
        else:
            print "usage: run "

    def do_close(self, args):
        for conn in self.connections:
            conn.close()

if __name__ == '__main__':
    RunCommand().cmdloop()
#Example output:
#
#ssh > add_host 127.0.0.1,jesse,lol
#ssh > connect
#ssh > run uptime
#host: 127.0.0.1: 14:49  up 11 days,  4:27, 8 users,
#load averages: 0.36 0.25 0.19
#ssh > close
"""

import subprocess
import sys
 
HOST="www.example.org"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND="uname -a"
 
ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
result = ssh.stdout.readlines()
if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
else:
    print result
    
    