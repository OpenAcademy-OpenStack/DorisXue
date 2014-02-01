import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as nvclient
from novaclient import client as novaclient
import glanceclient
import os

def get_keystone_creds():
    d = {}
    d['username'] = 'admin'
    d['password'] = 'password'
    d['auth_url'] = 'http://10.0.2.15:5000/v2.0/'
    d['tenant_name'] = 'demo'
    return d

def get_nova_creds():
    d = {}
    d['username'] = 'admin'
    d['api_key'] = 'password'
    d['auth_url'] = 'http://10.0.2.15:5000/v2.0/'
    d['project_id'] = 'demo'
    return d

if __name__== "__main__":
    keystone_creds = get_keystone_creds()
    keystone = ksclient.Client(**keystone_creds)
    
    nova_creds = get_nova_creds()
    nova = nvclient.Client(**nova_creds)
    
    #if not nova.keypairs.findall(name="mykey"):
    #  with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
    #      nova.keypairs.create(name="mykey", public_key=fpubkey.read())
    
    glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                       endpoint_type='publicURL')
    glance = glanceclient.Client('1',glance_endpoint, token=keystone.auth_token)
    images = glance.images.list()
    for one_image in images:
        if one_image.name.find('ubuntu') > -1:
            print one_image.name
            image = nova.images.find(name=one_image.name)
            flavor = nova.flavors.find(name="m1.small")
            instance = nova.servers.create(name=one_image.name, image=image, flavor=flavor)
#instance = nova.servers.create(name=one_image.name, image=image, flavor=flavor, key_name="mykey")
