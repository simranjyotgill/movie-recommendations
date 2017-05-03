from tornado.ioloop import IOLoop
from tornado import web, httpserver, process, netutil
from app.controllers.IndexController import IndexController
from app.controllers.SearchController import SearchController
from app.controllers.InfoController import InfoController
from app.controllers.RecommendationController import RecommendationController
from config import config

import logging
import os

log = logging.getLogger(__name__)


def main():
    print(config)
    SERVER_PORT = config["server_port"]

    SERVER_URL = config["server_url"]
    if "http://" in config["server_url"]:
        SERVER_URL = config["server_url"][7:]

    settings = {}

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(curr_dir, "app", "frontend", "build")
    if os.path.exists(build_dir):
        settings["static_path"] = build_dir
        settings["static_url_prefix"] = "/"

    socket = netutil.bind_sockets(SERVER_PORT, address=SERVER_URL)
    task_id = process.fork_processes(0)

    application = web.Application([
        (r"/", IndexController),
        (r"/movie/([^/]+)", IndexController),
        (r"/search", SearchController),
        (r"/info/([^/]+)", InfoController),
        (r"/recommend/([^/]+)", RecommendationController),
        (r"/(.*)", web.StaticFileHandler, {"path": build_dir})
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.add_sockets(socket)
    log.info("Worker listening on %d", SERVER_PORT)
    IOLoop.current().start()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s',
                        level=logging.DEBUG)
    main()
