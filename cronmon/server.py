'''
Look at your logs in the brower
'''
import os
from flask import Flask
from jinja2 import FileSystemLoader


class WebApp(object):
    def __init__(self, port, location):
        self.template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.app = Flask(__name__)
        self.app.jinja_loader = FileSystemLoader(self.template_path)

    def serve(self):
        self._map_urls()
        self.app.debug = True
        self.app.run(host="0.0.0.0")

    def project_log(self, project, log):
        pass

    def project(self, project):
        pass

    def about(self):
        pass

    def index(self):
        return "welcome"

    def _map_urls(self):
        self.app.add_url_rule('/<project>/<log>', "project_log", self.project_log)
        self.app.add_url_rule('/<project>', "project", self.project)
        self.app.add_url_rule('/about', "about", self.about)
        self.app.add_url_rule('/', "index", self.index)


def start(port, location):
    WebApp(port, location).serve()


if __name__ == '__main__':
    print(__doc__)
