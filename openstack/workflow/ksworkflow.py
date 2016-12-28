#!/usr/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from cinderclient import client as ciclient

#get input from user
prj=str(raw_input("Enter Project name :\n"))
grp=str(raw_input("Enter Group name: \n"))
usr=str(raw_input("Enter User name: \n"))
voltp=str(raw_input("Enter Type of the volume required : \n"))
volnm=str(raw_input("Enter Name of the volume required : \n"))
sz=int(raw_input("Enter size of the volume: \n"))

print prj,grp,usr,voltp,sz

#validate project,group and user info using keystone
auth = v3.Password(user_domain_name='default', username='admin',password='Nexii123',project_domain_name='default', project_name='admin', auth_url='http://localhost:5000/v3')
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)
#print keystone.projects.list()
d = keystone.domains.list()

#check if project exists
try:
 pf= keystone.projects.find(name=prj)
 if pf:
  projtouse = pf
  print "Project "+str(projtouse.to_dict()['name'])+" exists"
 else:
  projtouse = keystone.projects.create(prj, d[0])
  print "Project created"
except:
 projtouse = keystone.projects.create(prj, d[0])
 print "project created"

#check for group
try:
 gf = keystone.groups.find(name=grp)
 if gf:
  grouptouse=gf
  print "Group exists"
  grouptouse=gf
  print "Group exists"
 else:
  pass
except:
 grouptouse = keystone.groups.create(name=grp, domain=d[0])

#check for users
#uf = keystone.users.list()
ru = keystone.roles.find(name="user")
try:
 uf = keystone.users.find(name=usr, project=projtouse)
 if uf:
  usertouse = uf
  print "User "+str(usertouse.to_dict()['name'])+" exists"
except:
 try:
  uv = keystone.groups.list(user=uf)
  if uv:
   usertouse=uv
  else:
   pass
 except:
   pas=str(raw_input("Enter password for user: "+usr+"\n"))
   usertouse  = keystone.users.create(name=usr, password=pas, project=projtouse, domain=d[0])
   uag = keystone.users.add_to_group(usertouse, grouptouse)
   rg = keystone.roles.grant(ru, group=grouptouse, project=projtouse)
   print "User created"

#Use the values given by user after validation
projectname=projtouse.to_dict()['name']
username=usertouse.to_dict()['name']
password=str(raw_input("Enter password for user "+str(usertouse.to_dict()['name'])+": "))
print projectname,username,str(password)

#Logging in using the given values
auth1 = v3.Password(user_domain_name='default', username=username,password=password,project_domain_name='default', project_name=projectname, auth_url='http://controller:5000/v3')
sess1 = session.Session(auth=auth1)
cin = ciclient.Client('2.0',session=sess1)
#Creating volumes
myvol=cin.volumes.create(name=volnm,size=sz,volume_type=voltp)
print "Volume created successfully with volume id: "+myvol.id
                                                                        

