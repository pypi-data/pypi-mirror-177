import os
import unittest
import builtins
import json
from unittest import TestCase
from unittest.mock import patch


from blendedcli.blendedcli import *


class BackendTest(TestCase):
    """
    """
    def test_backend_setup(self):
        pass

    def test_backend_create_package(self):
        pass

    def test_backend_validate_package(self):
        pass

    def test_backend_save_draft(self):
        pass

    def test_backend_snapshot_draft(self):
        pass

    def test_backend_publish_package(self):
        pass

    def test_backend_get_packages(self):
        pass

    def test_backend_make_canonical(self):
        pass

    def test_backend_share_package(self):
        pass

    def test_backend_transfer_package(self):
        pass

    def test_backend_download_package(self):
        pass

    def test_backend_get_package(self):
        pass

    def test_backend_extend_package(self):
        pass

    def test_backend_clone_package(self):
        pass

    def test_backend_get_update(self):
        pass

    def test_backend_get_package_info(self):
        pass

    def test_backend_update_package_info(self):
        pass

'''
class ControllerTest(TestCase):
    """
    """
    #user
    def test_controller_setup(self):
        expected_output = {}
        output = controller.setup()
        self.assertEqual(output, expected_output)

    def test_controller_create_user(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password':'yash123',
                'email': 'ylodha@cognam.com', 'name': 'yash'
               }
        output = controller.create_user(body)
        self.assertEqual(output, expected_output)

    def test_controller_activate_user(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 
                'token':'vghdsgafv14cdfghggbc121'
               }
        output = controller.activate_user(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_get_organizations(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 
                'password':'yash123'
               }
        output = controller.get_organizations(body)
        self.assertEqual(output, expected_output)

    
    #organizations
    def test_controller_make_active_organization(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'organization_name':'Yash-Org'
               }
        output = controller.make_active_organization(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_accept_invite(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'token':'vghdsgafv14cdfghggbc121'
               }
        output = controller.accept_invite(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_create_organization(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'organization_name':'Yash-Org'
               }
        output = controller.create_organization(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_add_user_to_organization(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'organization_id': 1, 'email': 'ylodha@gmail.com'
               }
        output = controller.add_user_to_organization(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_delete_user_from_organization(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'organization_id': 1, 'email': 'ylodha@gmail.com'
               }
        output = controller.delete_user_from_organization(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_give_admin_permission(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'organization_id': 1, 'user_name_of_other_person': 'Prashant'
               }
        output = controller.give_admin_permissions(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_remove_admin_permission(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'organization_id': 1, 'user_name_of_other_person': 'Prashant'
               }
        output = controller.remove_admin_permissions(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_get_active_organization(self):
        pass

    def test_controller_get_admins(self):
        pass

    #plans
    def test_controller_get_plan(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'plan_id': 1, 'package_name': 'demo_theme'
               }
        output = controller.get_plan(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_make_validation_optional(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'validator_name': 'name', 'package_name': 'demo_theme'
               }
        output = controller.make_validation_optional(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_make_validation_mandatory(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'validator_name': 'name', 'package_name': 'demo_theme'
               }
        output = controller.make_validation_mandatory(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_delete_validation(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'validator_name': 'name', 'package_name': 'demo_theme'
               }
        output = controller.delete_validation(body)
        self.assertEqual(output, expected_output)
        pass

    #packages
    def test_controller_create_package(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'package_type': 'THEME', 'package_name': 'demo_theme'
               }
        output = controller.create_package(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_validate_package(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'draft_or_version_id': 1, 'package_name': 'demo_theme'
               }
        output = controller.validate_package(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_save_draft(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'package_name': 'demo_theme'
               }
        output = controller.save_draft(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_snapshot_draft(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'version_label': 2,'package_name': 'demo_theme'
               }
        output = controller.snapshot_draft(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_publish_package(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 'password': 'yash1234',
                'package_name': 'demo_theme'
               }
        output = controller.publish(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_get_packages(self):
        expected_output = {}
        body = {'user_name': 'yshlodha', 
                'password': 'yash1234'
               }
        output = controller.get_packages(body)
        self.assertEqual(output, expected_output)
        pass

    def test_controller_make_canonical(self):
        pass

    def test_controller_share_package(self):
        pass

    def test_controller_transfer_package(self):
        pass

    def test_controller_download_package(self):
        pass

    def test_controller_get_package(self):
        pass

    def test_controller_extend_package(self):
        pass

    def test_controller_clone_package(self):
        pass

    def test_controller_get_update(self):
        pass

    def test_controller_get_package_info(self):
        pass

    def test_controller_see_license(self):
        pass

    def test_controller_update_package_info(self):
        pass
'''

class TestCliAccountSuccess(TestCase):
    '''
    '''
    @patch('builtins.input')
    def test_account_create_without_prompt(self, m_input):
        app = Blended()
        m_input.side_effect = ['ylodha@cognam.com',]
        self.assertEqual(app.run(['account create', 'yash', 
                                   '--name', 'yash lodha', 
                                   '--password', 'yash123',
                                   '--email', 'ylodha@cognam.com']), 0)
        self.assertEqual(app.run(['account create', 'yash', 
                                   '--name', 'yash lodha', 
                                   '--password', 'yash123', 
                                    '--email', 'ylodha@cognam.com',
                                    '--no-login']), 0)

    @patch('builtins.input')
    def test_account_create_no_name_get_prompt(self, m_input):
        app = Blended()
        m_input.side_effect = ['yash',]
        self.assertEqual(app.run(['account create', 'yash', 
                                   '--password', 'yash12a', 
                                   '--email', 'yash@cognam.com']), 0)
        #self.assertEqual(app.run(['account create', 'yash', 
         #                          '--name', 'yash lodha', 
          #                         '--password', 'yash123', '--no-login']), 0)

    @patch('builtins.input')
    def test_account_create_no_password_get_prompt(self, m_input):
        app = Blended()
        m_input.side_effect = ['y123',]
        self.assertEqual(app.run(['account create', 'yash', 
                                   '--name', 'yash lodha', 
                                   '--email', 'yash@cognam.com']), 0)
        #self.assertEqual(app.run(['account create', 'yash', 
         #                          '--name', 'yash lodha', 
         #                          '--password', 'yash123', '--no-login']), 0)
    
    @patch('builtins.input')
    def test_account_create_no_options_get_prompt(self, m_input):
        app = Blended()
        m_input.side_effect = ['yash', 'ysh123', 'ylodha@cognam.com']
        self.assertEqual(app.run(['account create', 'yash', 
                                ]), 0)
                                   
    def test_account_activate(self):
        app = Blended()
        self.assertEqual(app.run(['account confirm', 'sdvbasxd101414dffgbd',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)

    @patch('builtins.input')
    def test_account_activate_no_option(self, m_input):
        app = Blended()
        m_input.side_effect = ['yash', 'ysh123']
        self.assertEqual(app.run(['account confirm', 'sdvbasxd101414dffgbd']), 0)

    def test_account_accept(self):
        app = Blended()
        self.assertEqual(app.run(['account accept', 'sdvbasxd101414dffgbd',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)
    
    @patch('builtins.input')
    def test_account_accept_no_option(self, m_input):
        app = Blended()
        m_input.side_effect = ['yash', 'ysh123']
        self.assertEqual(app.run(['account accept', 'sdvbasxd101414dffgbd']), 0)

    def test_account_list(self):
        app = Blended()
        self.assertEqual(app.run(['account list',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)
        self.assertEqual(app.run(['account list', '<account_name>yash',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)

    @patch('builtins.input')
    def test_account_list_no_option(self, m_input):
        app = Blended()
        m_input.side_effect = ['yash', 'ysh123']
        self.assertEqual(app.run(['account list']), 0)
        self.assertEqual(app.run(['account list', '<account_name>yash']), 0)

    def test_account_add(self):
        app = Blended()
        #<add_account_name> --> <account to be add>
        #<account_name> --> <account in which we have to new_account_name is added or current active account>
        self.assertEqual(app.run(['account add', '<add_account_name>',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--account', '<account_name>', '--admin']), 0)
        self.assertEqual(app.run(['account add', '<add_account_name>',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--account', '<account_name>', '--read']), 0)
        self.assertEqual(app.run(['account add', '<add_account_name>',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--account', '<account_name>', '--write']), 0)

    def test_account_add(self):
        app = Blended()
        #<remove_account_name> --> the account that need to be removed.
        #<account_name> --> name of account from which <remove_account_name> is removed.
        self.assertEqual(app.run(['account revoke', '<remove_account_name>',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--account', '<account_name>']), 0)

    def test_account_set_current(self):
        app = Blended()
        self.assertEqual(app.run(['account set-current', '<account_name>',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)

    def test_account_set(self):
        app = Blended()
        self.assertEqual(app.run(['account set', 'yash',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)

class TestCliPackagesSuccess(TestCase):
    '''
    '''
    def test_package_create(self):
        app = Blended()
        self.assertEqual(app.run(['package create', 'demo_theme',
                                   '--type', 'Theme',
                                   '--describtion', 'this is new theme named demo_theme.',
                                   '--login', 'yash',
                                   '--password', 'yash123']), 0)

    @patch('builtins.input')
    def test_package_create_no_option(self, m_input):
        app = Blended()
        m_input.side_effect = ['yash', 'ysh123', 'THEME', 'this is a new theme']
        self.assertEqual(app.run(['package create', 'demo_theme']), 0)

    def test_package_list(self):
        app = Blended()
        self.assertEqual(app.run(['package list',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--account', 'anyone']), 0)

    def test_package_license_list(self):
        app = Blended()
        self.assertEqual(app.run(['package list', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1']), 0)

    def test_package_get(self):
        app = Blended()
        self.assertEqual(app.run(['package get', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--license', 'MIT',
                                   '--new-name', 'demo_theme1']), 0)

    def test_package_get(self):
        app = Blended()
        self.assertEqual(app.run(['package get', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--license', 'MIT',
                                   '--new-name', 'demo_theme1']), 0)

    def test_package_clone(self):
        app = Blended()
        self.assertEqual(app.run(['package clone', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--license', 'MIT',
                                   '--new-name', 'demo_theme1',
                                   '--no-download']), 0)

    def test_package_download(self):
        app = Blended()
        self.assertEqual(app.run(['package pull', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--label', '<version_label>',
                                   '--draft', '<draft_name>']), 0)

    def test_package_update(self):
        app = Blended()
        self.assertEqual(app.run(['package update', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1']), 0)

    def test_package_save(self):
        app = Blended()
        self.assertEqual(app.run(['package push', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1']), 0)

    def test_package_validate(self):
        app = Blended()
        self.assertEqual(app.run(['package validate', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--label', 'version_label']), 0)

    def test_package_snapshot(self):
        app = Blended()
        self.assertEqual(app.run(['package snapshot', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--label', 'version_label']), 0)

    def test_package_canonize(self):
        app = Blended()
        self.assertEqual(app.run(['package canonize', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--label', 'version_label']), 0)

    def test_package_publish(self):
        app = Blended()
        self.assertEqual(app.run(['package publish', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--license', 'MIT',
                                   '--price', '100']), 0)

    def test_package_retract(self):
        app = Blended()
        self.assertEqual(app.run(['package retract', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--license', 'MIT']), 0)

    def test_package_share(self):
        app = Blended()
        self.assertEqual(app.run(['package share', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--account', 'Prashant']), 0)

    def test_package_transfer(self):
        app = Blended()
        self.assertEqual(app.run(['package transfer', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1',
                                   '--account', 'Prashant']), 0)

    def test_package_detail(self):
        app = Blended()
        self.assertEqual(app.run(['package detail', 'demo_theme',
                                   '--login', 'yash',
                                   '--password', 'yash123',
                                   '--package_id', '1']), 0)



if __name__ == '__main__':
    unittest.main()
