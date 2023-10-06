import unittest
import urllib3
import threading
import time
import OrderUploadServer

class TestOrderUploadServer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        threading.Thread(target = OrderUploadServer.start).start()
        time.sleep(1.0)

    @classmethod
    def tearDownClass(self):
        urllib3.request("GET", "http://127.0.0.1:8169/shutdown")

    def test_get_order_details(self):
        resp_json = urllib3.request("GET", "http://127.0.0.1:8169/po/get_order_details").json()
        self.assertEqual(resp_json["status"], "success")

    def test_upload_order_details(self):
        resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details").json()
        # I need to do this a few different ways, with good requests as well as bad ones
        self.assertEqual(resp_json["status"], "success")

    def test_reset_database(self):
        resp_json = urllib3.request("GET", "http://127.0.0.1:8169/po/reset_database").json()
        self.assertEqual(resp_json["status"], "success")
        resp_json = urllib3.request("GET", "http://127.0.0.1:8169/po/get_order_details").json()
        self.assertEqual(resp_json["status"], "success")
        self.assertEqual(len(resp_json["details"]), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
    