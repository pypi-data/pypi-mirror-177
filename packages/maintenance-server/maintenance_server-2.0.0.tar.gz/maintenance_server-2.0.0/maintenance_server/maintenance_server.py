import argparse
import dataclasses
import logging
import os
import subprocess
import sys
from os import path
from typing import Dict, List

from werkzeug.serving import BaseWSGIServer, make_server
from werkzeug.wrappers import Response

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


@dataclasses.dataclass()
class ServerConfig:
    host: str
    port: str
    page_path: str

    @staticmethod
    def get_config(args: List[str] = None, *, environ: Dict[str, str] = None):
        parser, default = get_arg_parser(environ)
        return parser.parse_args(args=args, namespace=default)

    def to_args(self) -> List[str]:
        return ["--host", self.host, "--port", self.port, "--page-path", self.page_path]


def get_default_from_env(environ: Dict[str, str] = None) -> ServerConfig:
    # Do not touch of os.environ and not import it like `from os import environ`
    # If you do that the new environ is not load and break the test
    environ = environ or dict(os.environ)
    host = environ.get("MAINTENANCE_HOST") or environ.get("HOST") or environ.get("HTTP_HOST") or "0.0.0.0"
    port = environ.get("MAINTENANCE_PORT") or environ.get("PORT") or environ.get("HTTP_PORT") or "8080"
    html_file_path = environ.get("MAINTENANCE_PAGE_PATH")
    if not html_file_path or not path.exists(html_file_path):
        html_file_path = path.join(path.dirname(__file__), "maintenance.html")
    return ServerConfig(host=host, port=port, page_path=html_file_path)


def get_arg_parser(environ: Dict[str, str] = None) -> (argparse.ArgumentParser, ServerConfig):
    parser = argparse.ArgumentParser()
    config = get_default_from_env(environ)
    parser.add_argument("--host", dest="host", default=config.host)
    parser.add_argument("--port", dest="port", default=config.port)
    parser.add_argument("--page-path", dest="page_path", default=config.page_path)
    return parser, config


def get_server(config: ServerConfig) -> BaseWSGIServer:
    _logger.info("###################################")
    _logger.info("Run maintenance Server")
    _logger.info("Conf %s", config)
    _logger.info("###################################")
    if not path.exists(config.page_path):
        config.page_path = path.join(path.dirname(__file__), "maintenance.html")
    with open(config.page_path) as f:
        text = f.read()
    reponse = Response(text, mimetype="text/html")
    return make_server(
        host=config.host,
        port=config.port,
        app=lambda environ, start_response: reponse(environ, start_response),
        threaded=True,
    )


class AutoTerminateProcess(subprocess.Popen):
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()
        super(AutoTerminateProcess, self).__exit__(exc_type, exc_val, exc_tb)


def start_as_process(config: ServerConfig = None) -> AutoTerminateProcess:
    _logger.info("Start a process on %s", config or "Default config")
    args = []
    if config:
        args = config.to_args()
    print()
    print(" ".join([sys.executable, "-m", "maintenance_server"] + args))
    return AutoTerminateProcess([sys.executable, "-m", "maintenance_server"] + args)
