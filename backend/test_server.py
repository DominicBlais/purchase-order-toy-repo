import os
import threading
import time
import unittest
import urllib3
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

    def test_upload_order_details_good1(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "good_1.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"100", "file":("good_1.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "success")

    def test_upload_order_details_good2(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "good_2.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("good_2.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "success")

    def test_upload_order_details_good3(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "good_3.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("good_3.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "success")

    def test_upload_order_details_good4(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "good_4.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("good_4.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "success")

    def test_upload_order_details_bad1(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "bad_1.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("bad_1.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "error")

    def test_upload_order_details_bad2(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "bad_2.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("bad_2.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "error")

    def test_upload_order_details_bad3(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "bad_3.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("bad_3.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "error")

    def test_upload_order_details_bad4(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "bad_4.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("bad_4.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "error")

    def test_upload_order_details_bad5(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "bad_5.csv") as csvfile:
            resp_json = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"0", "file":("bad_5.csv", csvfile.read())}).json()
            self.assertEqual(resp_json["status"], "error")

    def test_upload_order_details_bad6(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "good_1.csv") as csvfile:
            status = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"", "order_date":"0", "file":("good_1.csv", csvfile.read())}).status
            self.assertNotEqual(status, 200)

    def test_upload_order_details_bad7(self):
        with open(".." + os.sep + "test_csv_files" + os.sep + "good_2.csv") as csvfile:
            status = urllib3.request("POST", "http://127.0.0.1:8169/po/upload_order_details",
                                    fields={"vendor_name":"Testing", "order_date":"-100", "file":("good_2.csv", csvfile.read())}).status
            self.assertNotEqual(status, 200)
                                 
    def test_reset_database(self):
        resp_json = urllib3.request("GET", "http://127.0.0.1:8169/po/reset_database").json()
        self.assertEqual(resp_json["status"], "success")
        resp_json = urllib3.request("GET", "http://127.0.0.1:8169/po/get_order_details").json()
        self.assertEqual(resp_json["status"], "success")
        self.assertEqual(len(resp_json["details"]), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
    