#!/usr/bin/python
from novaclient import client
import os

auth_url = os.environ['OS_AUTH_URL']
auth_url = auth_url.split("/")
auth_url[-1] = "v2.0"
new_auth_url = "/".join(auth_url)
nova = client.Client('2',os.environ['OS_USERNAME'],
                     os.environ['OS_PASSWORD'],os.environ['OS_TENANT_NAME'],
                     new_auth_url)
conf = {}
with open("novacreate.conf") as f:
    for line in f:
        k, v = line.strip().split("=")
        conf[k] = v
n1=nova.networks.find(label=conf["net_label"])
i1=nova.images.find(name=conf["image_name"])
f1=nova.flavors.find(name=conf["flavor_name"])
myinst = nova.servers.create(conf["server_name"],image=i1, flavor=f1, nics=[{"net-id":n1.id}])
print myinst

