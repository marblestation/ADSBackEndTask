from __future__ import division
import os
import urllib
from flask import json
from ReferenceResolver.Tests.BaseTestCase import BaseTestCase

class ResolveTestCase(BaseTestCase):
    """
    Unit test cases for the list of examples described in the ADS Back-End Task.

    Expected bibcode responses were obtained from ADS Resolver:
    http://adsres.cfa.harvard.edu/cgi-bin/refcgi.py
    """

    def _get_resolve(self, refstring):
        """
        Use the app resolve REST API to resolve a refstring.

        Parameters
        ----------
        refstring : string

        Returns
        -------
        json_response : dict
        """
        # Do not accept '/' in refstring or they will be interpret as part of the URL (even if properly encoded with quote)
        response = self.app.get(urllib.quote("/resolve/"+refstring.replace("/", ":")))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data())
        return json_response

    def _test_get_resolve(self, expected_response):
        """
        Resolve a refstring and assert its expected JSON response.

        Parameters
        ----------
        expected_response : dict
        """
        json_response = self._get_resolve(expected_response['refstring'])
        # TODO: Validate status field
        status = json_response.pop('status', None) # Do not validate status field (we need to collect scores)
        self.assertEquals(json_response, expected_response)

    def test_0001_task_example(self):
        """
        Test first example refstring.
        """
        ## Success:
        expected_response = {u'refstring': 'Abt, H. 1990, ApJ, 357, 1', \
                             u'bibcode': '1990ApJ...357....1A' }
        self._test_get_resolve(expected_response)

    def test_0002_modern_astronomical_journal(self):
        """
        Test modern astronomical journal refstring example.
        """
        ## Success:
        expected_response = {u'refstring': 'Accomazzi, A., Eichhorn, G., Kurtz, M. J., Grant, C. S., & Murray, S. S. 2000, A&AS, 143, 85', \
                             u'bibcode': '2000A&AS..143...85A' }
        self._test_get_resolve(expected_response)

    def test_0003_modern_physics_journal(self):
        """
        Test modern physics journal refstring example.
        """
        ## Success:
        expected_response = {u'refstring': 'J. B. Gupta, K. Kumar, and J. H. Hamilton, Phys. Rev. C 16, 427 (1977).', \
                             u'bibcode': '1977PhRvC..16..427G' }
        self._test_get_resolve(expected_response)

    def test_0004_annual_reviews(self):
        """
        Test annual reviews refstring example.
        """
        ## Fails because it seems that there is a typo in "Adainson M", which the ADS resolver managed to correct to "Adamson, A. J."
        ## while I do not find any result (ADS API Search is not using synonyms and I did not manage to activate that)
        expected_response = {u'refstring': 'Adainson M, Kerr Th, Whittet DCB, Duley WW. 1994. MNRAS 268:705-8', \
                             u'bibcode': '1994MNRAS.268..705A' }
        self._test_get_resolve(expected_response)

    def test_0005_books(self):
        """
        Test books refstring example.
        """
        ## Fails but the bibcode provided by the ADS resolver correspond to an author named "Wali, Rameshwar C." and not "Walli, K."
        ## it might be again a problem due to not being able to use synonyms with ADS API Search:
        expected_response = {u'refstring': 'Wali, K. 1991, Chandra: A Biography of S. Chandrasekhar (Chicago: Univ. Chicago Press)', \
                             u'bibcode': '1991cbsc.book.....W' }
        self._test_get_resolve(expected_response)

    def test_0006_conferences(self):
        """
        Test conferences refstring example.
        """
        ## Fails but provides an "equivalent" bibcode (same title, publication, etc):
        expected_response = {u'refstring': 'Rees, M. J. 1984, in Formation and Evolution of Galaxies and Large Scale Structure in the Universe, ed. J. Audouze and T. T. Van (Dordrecht: Reidel), 271', \
                             u'bibcode': '1984fegl.proc..271R' }
        self._test_get_resolve(expected_response)

    def test_0007_small_publications(self):
        """
        Test small publications refstring example.
        """
        ## Success:
        expected_response = {u'refstring': 'Hermsen, W., et. al. 1992, IAU Circ. No. 5541', \
                             u'bibcode': '1992IAUC.5541....1H' }
        self._test_get_resolve(expected_response)

    def test_0008_thesis(self):
        """
        Test thesis refstring example.
        """
        ## Fails because, again, not being able to use synonyms with ADS API Search:
        expected_response = {u'refstring': 'Pollock, J. T. 1982, Ph. D. Thesis, University of Florida.', \
                             u'bibcode': '1982PhDT.........1P' }
        self._test_get_resolve(expected_response)

