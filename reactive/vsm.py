import os

from charmhelpers.core.hookenv import charm_name
from charmhelpers.core.host import mkdir
from charms.reactive import when, when_not, set_state
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_install

# PACKAGES = ['', '', '', '', '']

__author__ = 'Chris Holcombe <chris.holcombe@canonical.com>'


@when('keystone.available')
def request_keystone_auth(keystone):
    keystone.request_credentials(username=charm_name())

@when('keystone.available.auth')
def configure_keystone(keystone):
    data = {
        'vsm.keystone.configured': True,
        # Keystone connection info
        'vsm.keystone.private-address': keystone.private_address(),
        'vsm.keystone.credentials_host': keystone.credentials_host(),
        'vsm.keystone.credentials_protocol': keystone.credentials_protocol(),
        'vsm.keystone.credentials_port': keystone.credentials_port(),
        'vsm.keystone.api_version': keystone.api_version(),
        'vsm.keystone.auth_host': keystone.auth_host(),
        'vsm.keystone.auth_protocol': keystone.auth_protocol(),
        'vsm.keystone.auth_port': keystone.auth_port(),
        # Keystone AUTH
        'vsm.keystone.project': keystone.credentials_project(),
        'vsm.keystone.username': keystone.credentials_username(),
        'vsm.keystone.password': keystone.credentials_password(),
        'vsm.keystone.project_id': keystone.credentials_project_id(),
    }

    for state, data in data.items():
        set_state(state, data)

@when('queue.available')
def configure_rabbit(rabbit):
    data = {
        'vsm.rabbit.configured': True,
        # RabbitMQ Configuration
        'vsm.rabbit.hostname': rabbit.private_address(),
        'vsm.rabbit.vhost': rabbit.vhost(),
        'vsm.rabbit.username': rabbit.username(),
        'vsm.rabbit.password': rabbit.password(),
        'vsm.rabbit.port': 5672, # This is not currently configured by the charm
    }

    for state, data in data.items():
        set_state(state, data)



@when('vsm.keystone.configured', 'vsm.rabbit.configured')
@when_not('vsm.configured')
def configure_vsm_conf():
    vsm_dashboard_context = {
        'keystone_private': get_state('vsm.keystone.private-address'), 
        'keystone_credentials_host': get_state('vsm.keystone.credentials_host'), 
        'keystone_credentials_protocol': get_state('vsm.keystone.credentials_protocol'), 
        'keystone_credentials_port': get_state('vsm.keystone.credentials_port'), 
        'keystone_api_version': get_state('vsm.keystone.api_version'), 
        'keystone_auth_host': get_state('vsm.keystone.auth_host'), 
        'keystone_auth_protocol': get_state('vsm.keystone.auth_protocol'), 
        'keystone_auth_port': get_state('vsm.keystone.auth_port'), 
        # Auth Data
        'keystone_project': get_state('vsm.keystone.project'),
        'keystone_username': get_state('vsm.keystone.username'),
        'keystone_password': get_state('vsm.keystone.password'),
        'keystone_project_id': get_state('vsm.keystone.project_id'),
        'rabbit_hostname': get_state('vsm.rabbit.hostname'),
        'rabbit_vhost': get_state('vsm.rabbit.vhost'),
        'rabbit_username': get_state('vsm.rabbit.username'),
        'rabbit_password': get_state('vsm.rabbit.password'),
        'rabbit_port': get_state('vsm.rabbit.port'),
    }
    # TODO: Where do we put this file?
    vsm_conf_path = "/tmp"
    mkdir(os.path.dirname(vsm_conf_path), owner="vsm",
          group="vsm")
    render('vsm.conf',
           vsm_conf_path,
           vsm_dashboard_context,
           perms=0o644)
    set_state('vsm.configured')


@when('apache.available')
def apache_installed():
    pass
