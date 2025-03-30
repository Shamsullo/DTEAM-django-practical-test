from django.test import TestCase, Client
from audit.models import RequestLog


class RequestLogTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_basic_get_request_logging(self):
        """Test that a basic GET request is logged correctly"""
        # Make a sample GET request
        response = self.client.get("/some-path/")

        # Get the last log entry
        log = RequestLog.objects.last()

        # Check if the request was logged
        self.assertIsNotNone(log)
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, "/some-path/")
        self.assertEqual(
            log.status_code, 404
        )  # Will be 404 since path doesn't exist

    def test_post_request_logging(self):
        """Test that a POST request is logged correctly"""
        # Make a sample POST request
        post_data = {"key": "value"}
        response = self.client.post("/another-path/", post_data)

        # Get the last log entry
        log = RequestLog.objects.last()

        # Check if the request was logged
        self.assertIsNotNone(log)
        self.assertEqual(log.method, "POST")
        self.assertEqual(log.path, "/another-path/")
        self.assertEqual(log.status_code, 404)

    def test_multiple_requests_logging(self):
        """Test that multiple requests are logged correctly"""
        # Make several requests
        initial_count = RequestLog.objects.count()

        self.client.get("/path1/")
        self.client.get("/path2/")
        self.client.post("/path3/", {"test": "data"})

        # Check if all requests were logged
        self.assertEqual(RequestLog.objects.count(), initial_count + 3)
