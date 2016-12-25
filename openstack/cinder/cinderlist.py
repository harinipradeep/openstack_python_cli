#!/usr/bin/python
from cinderclient import client
import os
auth_url = os.environ['OS_AUTH_URL']
auth_url = auth_url.split("/")
auth_url[-1] = "v2.0"
new_auth_url = "/".join(auth_url)
cinder=client.Client('2',os.environ['OS_USERNAME'],
                     os.environ['OS_PASSWORD'],os.environ['OS_TENANT_NAME'],
                     new_auth_url)
for i in cinder.volumes.list():
 print "size : ",i.to_dict()['size']
 print "name : ",i.to_dict()['name']
 print "status : ",i.to_dict()['status']
 print "volume_type : ", i.to_dict()['volume_type']
 print "\n"
