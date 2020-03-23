#from django.test import TestCase
from unittest import TestCase
from modules import trackers_gecko as tr


class TrackerTest(TestCase):

    def test_clean_url(self):
        self.assertEqual(tr.clean_url('test.com'), 'https://test.com')
        self.assertEqual(tr.clean_url('http://test.com'), 'http://test.com')

    
    def test_is_valid_url(self):
        self.assertIsNone(tr.is_valid_url('https://test'))
        self.assertIsNone(tr.is_valid_url('test'))
        self.assertIsNotNone(tr.is_valid_url('http://localhost'))
        self.assertIsNotNone(tr.is_valid_url('http://11.1.111.11'))
        self.assertIsNotNone(tr.is_valid_url('https://TesT.com'))


    def test_get_network_dat(self):
        url1 = 'https://google.com'
        url2 = 'https://nadsfn.dnh'
        self.assertIsNotNone(tr.get_network_dat(url1, 3))
        self.assertEqual(tr.get_network_dat(url2, 3), {"Connection Error"})

    
    def test_get_network_trackers(self):
        trackers = {"Google Analytics", "Google Static", "Google Tag Manager", "Facebook","DoubleClick","Amazon Advertising"}
        traff_urls1 = ["google-analytics.com", "gstatic.com", "googletagservices.com", "facebook.net", "invitemedia.com", "amazon-adsystem.com"]
        traff_urls2 = ['none']

        self.assertEqual(tr.get_network_trackers(traff_urls1), trackers)#sorted(trackers))
        self.assertEqual(tr.get_network_trackers(traff_urls2), set())


    def test_get_raw_trackers(self):
        """assumes three trackers are always in response from google"""
        url1 = 'https://google.com'
        url2 = 'https://nadsfn.dnh'

        track_reselt = tr.get_raw_trackers(url1)
        tracker = ['Google Static', 'YouTube', 'Google']

        self.assertEqual({'Connection Error'}, tr.get_raw_trackers(url2))

        for i in tracker:
            self.assertIn(i, track_reselt)


    def test_track_light(self):
        """tests check for all outcomes of track_light() using known sites 
            exhibiting behavior. May need to update in future"""
        self.assertEqual(tr.track_light('http://dsdfg.ckng', 2)[1], 0)
        self.assertEqual(tr.track_light('https://google.com', 2)[1], 1)
        self.assertEqual(tr.track_light('http://kevinbabcock.com', 2)[1], 2)
        self.assertEqual(tr.track_light('https://lowes.com', 2)[1], 4)
