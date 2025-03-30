import logging
from CVProject import settings
from .models import RequestLog
import time
import json

logger = logging.getLogger(__name__)


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("RequestLogMiddleware initialized")

    def __call__(self, request):
        if not self.should_log_request(request):
            return self.get_response(request)

        # Start timer for response time
        start_time = time.time()

        # Get response from the view
        response = self.get_response(request)

        # Calculate response time
        response_time = time.time() - start_time

        try:
            # Prepare headers (excluding sensitive information)
            headers = {}
            sensitive_headers = {
                "cookie",
                "authorization",
                "proxy-authorization",
            }
            for header_name, header_value in request.META.items():
                if (
                    header_name.startswith("HTTP_")
                    and header_name[5:].lower() not in sensitive_headers
                ):
                    headers[header_name[5:].lower()] = header_value

            # Get request body while respecting privacy
            try:
                request_body = request.body.decode("utf-8")
                # Try to parse as JSON to clean sensitive data
                try:
                    body_data = json.loads(request_body)
                    if isinstance(body_data, dict):
                        # Remove sensitive fields
                        for key in ["password", "token", "key", "secret"]:
                            if key in body_data:
                                body_data[key] = "[FILTERED]"
                    request_body = json.dumps(body_data)
                except json.JSONDecodeError:
                    # If not JSON, store as is but limit size
                    request_body = (
                        request_body[:1000]
                        if len(request_body) > 1000
                        else request_body
                    )
            except:
                request_body = None

            # Create and save the log entry
            log_entry = RequestLog.objects.create(
                # Request details
                method=request.method,
                path=request.path,
                query_string=request.META.get("QUERY_STRING", ""),
                remote_addr=self.get_client_ip(request),
                user=request.user if request.user.is_authenticated else None,
                # Response details
                status_code=response.status_code,
                response_time=response_time,
                # Request metadata
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
                referer=request.META.get("HTTP_REFERER", ""),
                request_body=request_body,
                content_type=request.content_type,
                session_key=request.session.session_key,
                headers=headers,
                host=request.get_host(),
                is_secure=request.is_secure(),
                is_ajax=request.headers.get("X-Requested-With")
                == "XMLHttpRequest",
                encoding=request.encoding,
            )

            logger.debug(f"Request logged successfully: ID={log_entry.id}")

        except Exception as e:
            logger.error(f"Failed to log request: {e}", exc_info=True)

        return response

    def get_client_ip(self, request):
        """Get the real IP address of the client, considering proxy headers"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def should_log_request(self, request):
        """Determine if the request should be logged based on settings"""
        if not getattr(settings, "REQUEST_LOG_ENABLED", True):
            return False

        # Don't log static/media files
        if request.path.startswith(("/static/", "/media/")):
            return False

        # Check excluded paths from settings
        for path in getattr(settings, "REQUEST_LOG_EXCLUDE_PATHS", []):
            if request.path.startswith(path):
                return False

        # Check excluded extensions from settings
        for ext in getattr(settings, "REQUEST_LOG_EXCLUDE_EXTENSIONS", []):
            if request.path.endswith(ext):
                return False

        return True
