# coding=utf-8
# =========================================================================
# Copyright © 2018 T-Mobile USA, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================
 
import os, sys
import unittest
import tempfile
import logging
import json
from alarm import alarm

class AlarmTestCase(unittest.TestCase):

    def setUp(self):
        alarm.app.testing = True
        self.app = alarm.app.test_client()
        logging._handlers.clear()
        logging.shutdown(logging._handlerList[:])
        del logging._handlerList[:]
        alarm.LOGGING_CONF = os.path.dirname(os.path.realpath(__file__)) + "/logging.test.conf"
        logging.config.fileConfig(alarm.LOGGING_CONF)

    def tearDown(self):
        alarm.cleanup()

    def test_home(self):
        resp = self.app.get('/')
        self.assertEqual(resp.data, b'{"message": "Welcome to the Raspberry Pi Alarm!"}')
        self.assertEqual(resp.status_code, 200)

    def test_404(self):
        resp = self.app.get('/page_that_does_not_exist')
        self.assertEqual(resp.status_code, 404)
        resp = self.app.post('/page_that_does_not_exist')
        self.assertEqual(resp.status_code, 404)

    def test_no_keys(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.blank.txt"
        alarm.load_keys()
        self.assertFalse(alarm.keys_exist())

    def test_turn_on_with_no_keys(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.blank.txt"
        alarm.load_keys()
        resp = self.app.get('/alarm/on')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

    def test_invalid_key(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.1.txt"
        alarm.load_keys()
        self.assertTrue(alarm.keys_exist())
        self.assertTrue(alarm.check_key("abc123"))
        self.assertFalse(alarm.check_key("key_does_not_exist"))

    def test_unauthorized(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.1.txt"
        alarm.load_keys()
        resp = self.app.get('/alarm/on')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["status"], "error")
        self.assertEqual(resp.status_code, 403)

    def test_turn_on_off_with_access_key(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.1.txt"
        alarm.load_keys()
        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='abc123', timeout=180)),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='abc123', timeout=300)),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        alarm.cleanup()

    def test_turn_on_off_3_users(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.3.txt"
        alarm.load_keys()
        alarm.ENABLE_LAUNCH_BROWSER = False
        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='abc123')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='dfg456')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='rti652')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        self.assertTrue(len(alarm.timer_threads) == 1)

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='abc123')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        self.assertTrue(len(alarm.timer_threads) == 0)

        alarm.cleanup()

    def test_turn_on_off_5_users(self):
        alarm.KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.5.txt"
        alarm.load_keys()
        alarm.ENABLE_LAUNCH_BROWSER = False
        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='abc123')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='dfg456')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='rti652')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='xvl098')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='tyt484')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "on")

        resp = self.app.post('/alarm/on',
                       data=json.dumps(dict(access_key='doesnotexist')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["status"], "error")
        self.assertEqual(resp.status_code, 403)

        self.assertTrue(len(alarm.timer_threads) == 5)

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='abc123')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='dfg456')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='rti652')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='xvl098')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        resp = self.app.post('/alarm/off',
                       data=json.dumps(dict(access_key='tyt484')),
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["alarm"], "off")

        self.assertTrue(len(alarm.timer_threads) == 0)

        alarm.cleanup()

    def test_invalid_json_request(self):
        resp = self.app.post('/alarm/on',
                       data='{"bad json"}',
                       content_type='application/json')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(json_data["status"], "error")

    def test_info(self):
        resp = self.app.get('/info')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_data["status"], "OK")
        self.assertEqual(json_data["version"], alarm.VERSION)
        self.assertEqual(json_data["platform"], sys.platform)

    def test_logs(self):
        resp = self.app.get('/logs')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_data["status"], "OK")

    def test_ping(self):
        resp = self.app.get('/ping')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_data["status"], "OK")

    def test_reset(self):
        resp = self.app.get('/reset')
        json_data = json.loads(resp.data.decode("utf-8") )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json_data["status"], "OK")
        self.assertTrue(len(alarm.timer_threads) == 0)

    def test_process_arguments(self):
        alarm.process_arguments(['-d', '-p9999'])
        self.assertTrue(alarm.PORT == 9999)
        self.assertTrue(alarm.ENABLE_DEBUGGER)
        self.assertTrue(alarm.TIMEOUT == 60)

        alarm.ENABLE_DEBUGGER = False
        alarm.process_arguments(['-p3333', '-t360'])
        self.assertTrue(alarm.PORT == 3333)
        self.assertFalse(alarm.ENABLE_DEBUGGER)
        self.assertTrue(alarm.TIMEOUT == 360)

    def test_banner_info(self):
        alarm.banner_info()

if __name__ == '__main__':
    unittest.main()
