"""Server."""
import os
import sys
from http.server import BaseHTTPRequestHandler
from vendor.mucca_logging.mucca_logging import logging
from src.routes.routes import router


class RequestHandler(BaseHTTPRequestHandler):
    """Extend base http servers."""

    def do_HEAD(self):
        """head."""
        logging.log_info(
            "head",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return

    def do_POST(self):
        """Post."""
        logging.log_info(
            "post",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return

    def do_GET(self):
        """Get."""
        rout = router(self.path, "request")
        rout.rout()
        self.respond()
        # self.send_response(200, 'OK')
        logging.log_info(
            "get",
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        return

    def handle_http(self, status, content_type):
        """Handler."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        logging.log_info(
            "status {} content {}".format(status, content_type),
            os.path.abspath(__file__),
            sys._getframe().f_lineno
        )
        print(self.path)
        # route_content = routes[self.path]
        return bytes("Suca", 'UTF-8')

    def respond(self):
        """Response."""
        content = self.handle_http(200, "text/html")
        self.wfile.write(content)
        return
