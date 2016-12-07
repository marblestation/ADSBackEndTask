import os
import urllib
from flask import json
from ReferenceResolver.Tests.BaseTestCase import BaseTestCase

class ResolveTestCase(BaseTestCase):

    def test_0001_get_resolve(self):
        expected_response = {u'refstring': 'Abt, H. 1990, ApJ, 357, 1', \
                             u'bibcode': '1990ApJ...357....1A' }
        response = self.app.get(urllib.quote("/resolve/Abt, H. 1990, ApJ, 357, 1"))
        json_response = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEquals(json_response, expected_response)

