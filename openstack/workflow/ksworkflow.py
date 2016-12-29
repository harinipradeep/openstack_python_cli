#!/usr/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from cinderclient import client as ciclient

#get input from user
prj=str(raw_input("Enter Project name :\n"))
#rp=str(raw_input("Enter Group name: \n"))
usr=str(raw_input("Enter User name: \n"))

#Depending upon the access assign role to user and add to the group
def access_role(user,project,access):
 ru = keystone.roles.find(name="user")
 rd = keystone.roles.find(name="vol_del")
 gru = keystone.groups.find(name="cinder_delete")
 if access == 1:
  keystone.roles.grant(ru,user=user,project=project)
  keystone.roles.grant(rd,user=user,project=project)
  keystone.users.add_to_group(user, gru)
 elif access == 2:
  keystone.roles.grant(ru,user=user,project=project)
 else:
  keystone.roles.grant(rd,user=user,project=project)
  keystone.users.add_to_group(user, gru)
   #rg = keystone.roles.grant(ru, group=grouptouse, project=projtouse)
   #print "User created"

#validate project and user info using keystone
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
  #print "Project "+str(projtouse.to_dict()['name'])+" already exists.Using the same"
 else:
  projtouse = keystone.projects.create(prj, d[0])
  print "New Project created"
except:
 projtouse = keystone.projects.create(prj, d[0])
 print "New project created"


#check for users
#uf = keystone.users.list()
try:
 uf = keystone.users.find(name=usr, project=projtouse)
 if uf:
  usertouse = uf
  #print "User "+str(usertouse.to_dict()['name'])+" exists"
except:
 #try:
 #uv = keystone.groups.list(user=uf)
 #if uv:
  #usertouse=uv
  #else:
  # pass
 #except:
 #pas=str(raw_input("Enter password for user: "+usr+"\n"))
 pas=usr
 usertouse  = keystone.users.create(name=usr, password=pas, project=projtouse, domain=d[0])
 access=int(raw_input("User has been newly created. Please select kind of access required\n 1.All volume operations\n 2.All volume operations except volume delete \n 3.Only volume delete\n"))
 access_role(usertouse,projtouse,access)


#Use the values given by user after validation
projectname=projtouse.to_dict()['name']
username=usertouse.to_dict()['name']
password=str(raw_input("Enter password for user "+str(usertouse.to_dict()['name'])+": "))
#print projectname,username,str(password)

#Logging in using the given values
auth1 = v3.Password(user_domain_name='default', username=username,password=password,project_domain_name='default', project_name=projectname, auth_url='http://controller:5000/v3')
sess1 = session.Session(auth=auth1)
cin = ciclient.Client('2.0',session=sess1)

val = int(raw_input("Select any cinder operation to perform\n 1.Create \n2.List \n3.Delete \n"))
if val==1:
 voltp=str(raw_input("Enter Type of the volume required(gold or silver) : \n"))
 volnm=username+projectname+voltp
 sz=int(raw_input("Enter size of the volume: \n"))
 #Creating volumes
 myvol=cin.volumes.create(name=volnm,size=sz,volume_type=voltp)
 print "Volume created successfully with volume id: \n"+myvol.id
elif val==2:
 #print cin.volumes.list()
 if not cin.volumes.list():
  print "No volumes are present in this project"
 else:
  for i in cin.volumes.list():
   print i
   print "size : ",i.to_dict()['size']
   print "name : ",i.to_dict()['name']
   print "status : ",i.to_dict()['status']
   print "volume_type : ", i.to_dict()['volume_type']
   print "\n"
else:
 vol_name = str(raw_input("Enter the volume name to be deleted: \n"))
 vn = cin.volumes.find(name=vol_name)
 vid = vn.to_dict()['id']
 cin.volumes.delete(vid)

