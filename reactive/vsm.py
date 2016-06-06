import os

from charmhelpers.core.host import mkdir
from charms.reactive import when, when_not, set_state
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_install

# PACKAGES = ['', '', '', '', '']

__author__ = 'Chris Holcombe <chris.holcombe@canonical.com>'


@when('keystone.available')
def setup_django_template():
    vsm_context = {

    }
    vsm_conf_path = "/var/lib/charm/{}/ceph.conf"
    mkdir(os.path.dirname(vsm_conf_path), owner="vsm",
          group="vsm")
    render('vsm.conf',
           vsm_conf_path,
           vsm_context, perms=0o644)


@when('keystone.available')
def setup_vsm_dashboard_conf():
    vsm_dashboard_context = {

    }
    vsm_conf_path = "/var/lib/charm/{}/ceph.conf"
    mkdir(os.path.dirname(vsm_conf_path), owner="vsm",
          group="vsm")
    render('vsm-dashboard-settings',
           vsm_conf_path,
           vsm_dashboard_context,
           perms=0o644)


# @when_not('vsm.installed')
# def install_vsm_base():
#     apt_install(PACKAGES)
#     set_state('vsm.installed')


@when('apache.available')
def apache_installed():
    pass
