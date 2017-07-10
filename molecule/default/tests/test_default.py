import os
import pytest
import json
import ast

import testinfra.utils.ansible_runner
import testinfra.utils.openstack as openstack

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('keystone-hosts')

def openstack_wrapper(AnsibleVars, subcmd, **kwargs):
    auth_url = 'http://{}:35357/v3'.format(kwargs['auth_url'])
    return openstack.osclient(subcmd,
                              auth_url=auth_url,
                              username=AnsibleVars['tmp_auth_dict']['username'],
                              user_domain_name=AnsibleVars['tmp_auth_dict']['user_domain_name'],
                              password=AnsibleVars['tmp_auth_dict']['password'],
                              project=AnsibleVars['tmp_auth_dict']['project_name'],
                              project_domain_name=AnsibleVars['tmp_auth_dict']['project_domain_name'],
                             )


@pytest.fixture()
def AnsibleVars(Ansible):
    return Ansible("include_vars", os.path.join("../../defaults/main.yml"))["ansible_facts"]

def test_keystone_service(host):
    service = host.service("httpd")
    
    assert service.is_running
    assert service.is_enabled

def test_keystone_projects(host, AnsibleVars, capsys):
    projects = ['service','demo']
    project_results = []
    address = host.interface('eth0').addresses[0]
    for project in projects:
        subcmd = 'project show {} --format json'.format(project)
        cmd = host.check_output(openstack_wrapper(AnsibleVars, subcmd=subcmd, auth_url=address))
        project_results.append(cmd)

    for result in project_results:
        json_result =  json.loads(result)
        assert json_result['name'] in projects
        assert json_result['enabled'] == True


def test_keystone_users(host, AnsibleVars):
    users = ['demo']
    user_results = []
    address = host.interface('eth0').addresses[0]

    for user in users:
        subcmd = 'user show {} --format json'.format(user)
        cmd = host.check_output(openstack_wrapper(AnsibleVars, subcmd=subcmd, auth_url=address))
        user_results.append(cmd)

    for result in user_results:
        json_result = json.loads(result)
        assert json_result['name'] in users
        assert json_result['enabled'] == True
