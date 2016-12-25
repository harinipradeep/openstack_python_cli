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
f=open('cindercreate.conf')
vname = f.readline().split('=')[1].strip()
vsize = int(f.readline().split('=')[1].strip())
myvol=cinder.volumes.create(name=vname,size=vsize)
print myvol.id
