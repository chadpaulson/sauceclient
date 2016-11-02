#!/usr/bin/env python
#
#   Copyright (c) 2013 Corey Goldberg
#
#   This file is part of: sauceclient
#   https://github.com/cgoldberg/sauceclient
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#

import os
import random
import unittest

import sauceclient


# set these to run tests
SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME', '')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY', '')
TEST_JOB_ID = os.environ.get('TEST_JOB_ID', '')  # any valid job


def assert_is_utf8(content, test_obj):
    if sauceclient.is_py2:
        test_obj.assertIsInstance(content, unicode)
    else:
        try:
            content.encode('utf-8')
        except UnicodeEncodeError:
            assert False


class TestSauceClient(unittest.TestCase):

    def setUp(self):
        self.sc = sauceclient.SauceClient(
            SAUCE_USERNAME,
            SAUCE_ACCESS_KEY,
        )

    def test_has_instances(self):
        self.assertIsInstance(self.sc.information, sauceclient.Information)
        self.assertIsInstance(self.sc.jobs, sauceclient.Jobs)
        self.assertIsInstance(self.sc.provisioning, sauceclient.Provisioning)
        self.assertIsInstance(self.sc.usage, sauceclient.Usage)

    def test_headers(self):
        headers = self.sc.headers
        self.assertIsInstance(headers, dict)
        self.assertIn('Authorization', headers)
        self.assertIn('Content-Type', headers)
        self.assertIn('Basic', headers['Authorization'])
        self.assertEqual('application/json', headers['Content-Type'])

    def test_request_get(self):
        url = '/rest/v1/info/status'
        json_data = self.sc.request('GET', url)
        self.assertIsInstance(json_data, dict)

class TestJobs(unittest.TestCase):

    def setUp(self):
        self.sc = sauceclient.SauceClient(
            SAUCE_USERNAME,
            SAUCE_ACCESS_KEY,
        )

    def test_get_job_ids(self):
        job_ids = self.sc.jobs.get_job_ids()
        self.assertIsInstance(job_ids, list)
        job_id = random.choice(job_ids)
        assert_is_utf8(job_id, self)
        self.assertTrue(job_id.isalnum())

    def test_get_jobs(self):
        jobs = self.sc.jobs.get_jobs()
        self.assertIsInstance(jobs, list)
        job = random.choice(jobs)
        self.assertIn('id', job)
        assert_is_utf8(job['id'], self)
        self.assertEqual(job['owner'], self.sc.sauce_username)

    def test_get_job_attributes(self):
        job_attributes = self.sc.jobs.get_job_attributes(TEST_JOB_ID)
        self.assertIsInstance(job_attributes, dict)
        self.assertIn('id', job_attributes)
        self.assertIn('status', job_attributes)
        self.assertIn('commands_not_successful', job_attributes)
        self.assertIn('name', job_attributes)
        self.assertIn('video_url', job_attributes)
        self.assertIn('tags', job_attributes)
        self.assertIn('start_time', job_attributes)
        self.assertIn('log_url', job_attributes)
        self.assertIn('creation_time', job_attributes)
        self.assertIn('custom-data', job_attributes)
        self.assertIn('browser_version', job_attributes)
        self.assertIn('end_time', job_attributes)
        self.assertIn('passed', job_attributes)
        self.assertIn('owner', job_attributes)
        self.assertIn('browser', job_attributes)
        self.assertIn('os', job_attributes)
        self.assertIn('public', job_attributes)
        self.assertIn('breakpointed', job_attributes)
        self.assertIn('build', job_attributes)
        self.assertEqual(job_attributes['id'], TEST_JOB_ID)
        self.assertIn(job_attributes['owner'], self.sc.sauce_username)

    def test_get_job_assets(self):
        job_assets = self.sc.jobs.get_job_assets(TEST_JOB_ID)
        self.assertIsInstance(job_assets, dict)
        self.assertIn('sauce-log', job_assets)
        self.assertIn('screenshots', job_assets)
        self.assertIn('selenium-log', job_assets)
        self.assertIn('video', job_assets)

    def test_update_job(self):
        job_attributes = self.sc.jobs.update_job(TEST_JOB_ID)
        self.assertIsInstance(job_attributes, dict)
        self.assertIn('id', job_attributes)
        self.assertEqual(job_attributes['id'], TEST_JOB_ID)


class TestProvisioning(unittest.TestCase):

    def setUp(self):
        self.sc = sauceclient.SauceClient(
            SAUCE_USERNAME,
            SAUCE_ACCESS_KEY,
        )

    def test_get_account_details(self):
        account_details = self.sc.provisioning.get_account_details()
        self.assertIsInstance(account_details, dict)
        self.assertIn('id', account_details)
        self.assertIn('minutes', account_details)
        self.assertIn('access_key', account_details)
        self.assertIn('subscribed', account_details)
        self.assertEqual(account_details['id'], self.sc.sauce_username)

    def test_get_account_limits(self):
        account_limits = self.sc.provisioning.get_account_limits()
        self.assertIsInstance(account_limits, dict)
        self.assertIn('concurrency', account_limits)
        self.assertTrue(account_limits['concurrency'] > 0)


class TestInformation(unittest.TestCase):

    def setUp(self):
        self.sc = sauceclient.SauceClient()

    def test_get_status(self):
        status = self.sc.information.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn('service_operational', status)
        self.assertIn('status_message', status)
        self.assertIn('wait_time', status)
        assert_is_utf8(status['status_message'], self)
        self.assertTrue(status['service_operational'])

    def test_get_status_with_auth(self):
        sc = sauceclient.SauceClient(
            SAUCE_USERNAME,
            SAUCE_ACCESS_KEY,
        )
        status = sc.information.get_status()
        self.assertIsInstance(status, dict)
        self.assertIn('service_operational', status)
        self.assertIn('status_message', status)
        self.assertIn('wait_time', status)
        self.assertTrue(status['service_operational'])

    def test_get_platforms(self):
        platforms = self.sc.information.get_platforms()
        self.assertIsInstance(platforms, list)
        self.assertTrue(len(platforms) > 0)
        platform = random.choice(platforms)
        self.assertIn('api_name', platform)
        self.assertIn('automation_backend', platform)
        self.assertIn('latest_stable_version', platform)
        self.assertIn('long_name', platform)
        self.assertIn('long_version', platform)
        self.assertIn('os', platform)
        self.assertIn('short_version', platform)
        assert_is_utf8(platform['api_name'], self)

    def test_get_platforms_webdriver(self):
        platforms = self.sc.information.get_platforms('webdriver')
        self.assertIsInstance(platforms, list)
        self.assertTrue(len(platforms) > 0)
        platform = random.choice(platforms)
        self.assertIn('api_name', platform)
        self.assertIn('automation_backend', platform)
        self.assertIn('latest_stable_version', platform)
        self.assertIn('long_name', platform)
        self.assertIn('long_version', platform)
        self.assertIn('os', platform)
        self.assertIn('short_version', platform)
        assert_is_utf8(platform['api_name'], self)

    def test_get_platforms_appium(self):
        platforms = self.sc.information.get_platforms('appium')
        self.assertIsInstance(platforms, list)
        self.assertTrue(len(platforms) > 0)
        platform = random.choice(platforms)
        self.assertIn('api_name', platform)
        self.assertIn('automation_backend', platform)
        self.assertIn('latest_stable_version', platform)
        self.assertIn('long_name', platform)
        self.assertIn('long_version', platform)
        self.assertIn('os', platform)
        self.assertIn('short_version', platform)
        assert_is_utf8(platform['api_name'], self)

    def test_get_appium_eol_dates(self):
        versions = self.sc.information.get_appium_eol_dates()
        self.assertIsInstance(versions, dict)
        self.assertTrue(len(versions) > 0)


class TestUsage(unittest.TestCase):

    def setUp(self):
        self.sc = sauceclient.SauceClient(
            SAUCE_USERNAME,
            SAUCE_ACCESS_KEY,
        )

    def test_get_current_activity(self):
        activity = self.sc.usage.get_current_activity()
        self.assertIsInstance(activity, dict)

        self.assertIn('subaccounts', activity)
        self.assertIn(SAUCE_USERNAME, activity['subaccounts'])

        subaccount_activity = activity['subaccounts'][self.sc.sauce_username]
        self.assertIn('all', subaccount_activity)
        self.assertIsInstance(subaccount_activity['all'], int)
        self.assertIn('in progress', subaccount_activity)
        self.assertIsInstance(subaccount_activity['in progress'], int)
        self.assertIn('queued', subaccount_activity)
        self.assertIsInstance(subaccount_activity['queued'], int)

        self.assertIn('totals', activity)
        self.assertIn('all', activity['totals'])
        self.assertIsInstance(activity['totals']['all'], int)
        self.assertIn('in progress', activity['totals'])
        self.assertIsInstance(activity['totals']['in progress'], int)
        self.assertIn('queued', activity['totals'])
        self.assertIsInstance(activity['totals']['queued'], int)

    def test_get_historical_usage(self):
        historical_usage = self.sc.usage.get_historical_usage()
        self.assertIn('usage', historical_usage)
        self.assertIn('username', historical_usage)
        self.assertEqual(historical_usage['username'], self.sc.sauce_username)
        self.assertIsInstance(historical_usage['usage'], list)


if __name__ == '__main__':
    if not all((SAUCE_USERNAME, SAUCE_ACCESS_KEY, TEST_JOB_ID)):
        raise SystemExit('Set your credentials (username/access-key)')
    unittest.main(verbosity=2)
