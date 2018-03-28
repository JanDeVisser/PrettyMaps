#
# Copyright (c) 2014 Jan de Visser (jan@sweattrails.com)
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

import webapp2
import grit.handlers
import prettymaps.model

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
        # project = prettymaps.model.Project.get(self.key())
        # if self.request.method == "GET":
        #     layer = project.current_gpx
        # else:
        #     layer = prettymaps.model.GPXLayer(parent=project)
        # self.key(layer.key(), True)
        # assert self.object(), "GPXHandler.object not set!"


class IconsHandler(webapp2.RequestHandler):
    def get(self, key, layer):
        map = prettymaps.model.Map.get(key)
        self.response.content_type = "text/json"
        self.response.json = map.layers.get(layer, {}) \
            if map.layers is not None \
            else {}
