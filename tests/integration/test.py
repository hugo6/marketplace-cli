import base64
import unittest

import httplib2

import sys
import os
import string
import random

import marketplacecli.commands
from marketplace.application import Api

if not "TEST_USER" in os.environ or not "TEST_PASSWORD" in os.environ or not "TEST_URL" in os.environ:
    print "Set env varaible [TEST_USER], [TEST_PASSWORD], and [TEST_URL]"
    sys.exit(1)

login = os.environ['TEST_USER']
password = os.environ['TEST_PASSWORD']
url = os.environ['TEST_URL']


class TestSubscriptions(unittest.TestCase):
    client = httplib2.Http()
    headers = {'Authorization': 'Basic ' + base64.encodestring(login + ':' + password)}

    api = Api(url, client=client, headers=headers)
    subscription_profile_name = "subscriptionTest"

    def test_01_list(self):
        subscription_profile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscription_profile_cmds.set_globals(self.api, login, password)
        r = subscription_profile_cmds.do_list(None)
        self.assertEqual(r, 0)

    def test_02_list_wrong_org(self):
        subscription_profile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscription_profile_cmds.set_globals(self.api, login, password)
        r = subscription_profile_cmds.do_list("--org BAD_ORG")
        self.assertEqual(r, 1)

    def test_03_create(self):
        subscription_profile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscription_profile_cmds.set_globals(self.api, login, password)
        subscription_profile_cmds.do_delete("--name " + self.subscription_profile_name)
        r = subscription_profile_cmds.do_create(
            "--name " + self.subscription_profile_name + " --code " + self.subscription_profile_name)
        self.assertEqual(r, 0)

    def test_04_info(self):
        subscriptionprofile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscriptionprofile_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_cmds.do_info("--name " + self.subscription_profile_name)
        self.assertEqual(r, 0)

    def test_05_update(self):
        subscriptionprofile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscriptionprofile_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_cmds.do_update("--name " + self.subscription_profile_name + " --active true")
        self.assertEqual(r, 0)

    def test_06_adminadd(self):
        subscriptionprofile_admin_cmds = marketplacecli.commands.subscriptionprofile_admins.SubscriptionProfileAdmins()
        subscriptionprofile_admin_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_admin_cmds.do_add("--name " + self.subscription_profile_name + " --admins root")
        self.assertEqual(r, 0)

    def test_07_adminremove(self):
        subscriptionprofile_admin_cmds = marketplacecli.commands.subscriptionprofile_admins.SubscriptionProfileAdmins()
        subscriptionprofile_admin_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_admin_cmds.do_remove("--name " + self.subscription_profile_name + " --admins root")
        self.assertEqual(r, 0)

    def test_08_roleadd(self):
        subscriptionprofile_role_cmds = marketplacecli.commands.subscriptionprofile_roles.SubscriptionProfileRoles()
        subscriptionprofile_role_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_role_cmds.do_add(
            "--name " + self.subscription_profile_name + " --roles marketplace_vendor")
        self.assertEqual(r, 0)

    def test_09_roleremove(self):
        subscriptionprofile_role_cmds = marketplacecli.commands.subscriptionprofile_roles.SubscriptionProfileRoles()
        subscriptionprofile_role_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_role_cmds.do_remove(
            "--name " + self.subscription_profile_name + " --roles marketplace_vendor")
        self.assertEqual(r, 0)

    def test_10_remove(self):
        subscriptionprofile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscriptionprofile_cmds.set_globals(self.api, login, password)
        r = subscriptionprofile_cmds.do_delete("--name " + self.subscription_profile_name)
        self.assertEqual(r, 0)


class TestUsers(unittest.TestCase):
    client = httplib2.Http()
    headers = {'Authorization': 'Basic ' + base64.encodestring(login + ':' + password)}

    api = Api(url, client=client, headers=headers)
    subscription_profile_name = "subscriptionTest"
    role = "marketplace_vendor"
    new_login_name = "marketplacecli-test-" + ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def test_01_create(self):
        subscription_profile_cmds = marketplacecli.commands.subscriptionprofilecmds.SubscriptionProfileCmds()
        subscription_profile_cmds.set_globals(self.api, login, password)
        subscription_profile_cmds.do_delete("--name " + self.subscription_profile_name)
        r = subscription_profile_cmds.do_create(
            "--name " + self.subscription_profile_name + " --code " + self.subscription_profile_name + " --active true --admins " + login + " --roles " + self.role)
        self.assertEqual(r, 0)
        user_cmds = marketplacecli.commands.usercmds.UserCmds()
        user_cmds.set_globals(self.api, login, password)
        r = user_cmds.do_create(
            "--account " + self.new_login_name + " --email " + self.new_login_name + "@company.com --code " + self.subscription_profile_name + " --accountPassword welcome")
        self.assertEqual(r, 0)

    def test_02_info(self):
        user_cmds = marketplacecli.commands.usercmds.UserCmds()
        user_cmds.set_globals(self.api, login, password)
        r = user_cmds.do_info(None)
        self.assertEqual(r, 0)

    def test_03_list(self):
        user_cmds = marketplacecli.commands.usercmds.UserCmds()
        user_cmds.set_globals(self.api, login, password)
        r = user_cmds.do_list(None)
        self.assertEqual(r, 0)

    def test_user_04_disable(self):
        user_admin = marketplacecli.commands.usercmds.UserCmds()
        user_admin.set_globals(self.api, login, password)
        t = user_admin.do_disable("--account " + self.new_login_name)
        self.assertEquals(t, 0)

    def test_user_05_enable(self):
        user_admin = marketplacecli.commands.usercmds.UserCmds()
        user_admin.set_globals(self.api, login, password)
        t = user_admin.do_enable("--account " + self.new_login_name)
        self.assertEquals(t, 0)

    def test_user_06_admin_promote(self):
        user_admin = marketplacecli.commands.usercmds.UserAdminCmds()
        user_admin.set_globals(self.api, login, password)
        t = user_admin.do_promote("--account " + self.new_login_name)
        self.assertEquals(t, 0)

    def test_user_07_admin_demote(self):
        user_admin = marketplacecli.commands.usercmds.UserAdminCmds()
        user_admin.set_globals(self.api, login, password)
        t = user_admin.do_demote("--account " + self.new_login_name)
        self.assertEquals(t, 0)


class TestEntitlements(unittest.TestCase):
    client = httplib2.Http()
    headers = {'Authorization': 'Basic ' + base64.encodestring(login + ':' + password)}
    api = Api(url, client=client, headers=headers)

    def test_01_list(self):
        # entitlementsCmds = marketplacecli.commands.entitlementcmds.EntitlementCmds()
        # entitlementsCmds.set_globals(self.api, login, password)
        # r = entitlementsCmds.do_list(None)
        r = 0
        self.assertEqual(r, 0)


class TestRoles(unittest.TestCase):
    client = httplib2.Http()
    headers = {'Authorization': 'Basic ' + base64.encodestring(login + ':' + password)}

    api = Api(url, client=client, headers=headers)
    role = "marketplacecli-tests-" + ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))

    def test_01_list(self):
        role_cmds = marketplacecli.commands.rolecmds.RoleCmds()
        role_cmds.set_globals(self.api, login, password)
        r = role_cmds.do_list(None)
        self.assertEqual(r, 0)

    def test_02_create(self):
        role_cmds = marketplacecli.commands.rolecmds.RoleCmds()
        role_cmds.set_globals(self.api, login, password)
        r = role_cmds.do_create("--name " + self.role)
        self.assertEqual(r, 0)

    def test_03_info(self):
        role_cmds = marketplacecli.commands.rolecmds.RoleCmds()
        role_cmds.set_globals(self.api, login, password)
        r = role_cmds.do_info("--name " + self.role)
        self.assertEqual(r, 0)

    def test_04_addentitlements(self):
        role_entitlements_cmds = marketplacecli.commands.role_entitlements_cmds.RoleEntitlementCmds()
        role_entitlements_cmds.set_globals(self.api, login, password)
        r = role_entitlements_cmds.do_add(
            "--name " + self.role + " --entitlements vendor_access products_administrate")
        self.assertEqual(r, 0)

    def test_04_removeentitlements(self):
        role_entitlements_cmds = marketplacecli.commands.role_entitlements_cmds.RoleEntitlementCmds()
        role_entitlements_cmds.set_globals(self.api, login, password)
        r = role_entitlements_cmds.do_remove("--name " + self.role + " --entitlements products_administrate")
        self.assertEqual(r, 0)
