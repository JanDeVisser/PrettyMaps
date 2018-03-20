#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "jan"
__date__ = "$26-Jan-2013 9:47:24 PM$"

import webapp2
import gripe
gripe.add_app_dir("prettymaps", __file__)

import grit.handlers
import prettymaps


class MainPage(grit.handlers.PageHandler):
    template = "index"


class MapPage(grit.handlers.PageHandler):
    def get_context(self, ctx):
        ctx = super(MapPage, self).get_context(ctx)
        if self.object():
            gpx = self.object().gpx
            if gpx:
                ctx["gpx_map"] = self.key()
        return ctx


class GPXHandler(grit.handlers.ImageHandler):
    def initialize_bridge(self):
        pass
        # project = prettymaps.Project.get(self.key())
        # if self.request.method == "GET":
        #     layer = project.current_gpx
        # else:
        #     layer = prettymaps.GPXLayer(parent=project)
        # self.key(layer.key(), True)
        # assert self.object(), "GPXHandler.object not set!"

class IconsHandler(webapp2.RequestHandler):
    def get(self, key, layer):
        map = prettymaps.Map.get(key)
        self.response.content_type = "text/json"
        self.response.json = map.layers.get(layer) if map.layers is not None else {}


app = webapp2.WSGIApplication([('/', MainPage),
                               webapp2.Route(
                                    r'/project/<key>',
                                    handler="grit.handlers.PageHandler",
                                    name='manage-project',
                                    defaults={
                                        "kind": prettymaps.Project
                                    }
                               ),

                               webapp2.Route(
                                   r'/project',
                                   handler="grit.handlers.PageHandler", name='list-projects',
                                   defaults={
                                       "kind": prettymaps.Project
                                   }
                               ),

                               webapp2.Route(
                                    r'/map/<key>',
                                    handler="prettymaps.index.MapPage",
                                    name='manage-project',
                                    defaults={
                                        "kind": prettymaps.Map
                                    }
                               ),

                               webapp2.Route(
                                   r'/gpx/<key>',
                                   handler="prettymaps.index.GPXHandler", name='up-down-gpx',
                                   defaults={
                                        "kind": prettymaps.Map,
                                        "prop": "gpx",
                                        "content_type": "text/xml"
                                   }
                               ),

                               webapp2.Route(
                                   r'/layer/<layer>/<key>',
                                   handler="prettymaps.index.IconsHandler", name='up-down-icons'
                               )  # ,
                               ],
                              debug=True)

if __name__ == '__main__':
    import os.path

    import paste.httpserver
    import paste.translogger

    import autoreload
    import grit

    autoreload.start(interval=1.0)
    autoreload.track(os.path.join(os.path.dirname(__file__), '..', 'conf', 'app.json'))

    paste.httpserver.serve(paste.translogger.TransLogger(grit.app),
                           host = '127.0.0.1', port = '8080')
