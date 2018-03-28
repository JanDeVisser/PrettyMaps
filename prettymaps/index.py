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
import gripe
import grit
import grit.handlers

import prettymaps
import prettymaps.model


app = webapp2.WSGIApplication([webapp2.Route(
                                    r'/project/<key>',
                                    handler="grit.handlers.PageHandler",
                                    name='manage-project',
                                    defaults={
                                        "kind": prettymaps.model.Project
                                    }
                               ),

                               webapp2.Route(
                                   r'/project',
                                   handler="grit.handlers.PageHandler", name='list-projects',
                                   defaults={
                                       "kind": prettymaps.model.Project
                                   }
                               ),

                               webapp2.Route(
                                    r'/map/<key>',
                                    handler="prettymaps.handlers.MapPage",
                                    name='manage-project',
                                    defaults={
                                        "kind": prettymaps.model.Map
                                    }
                               ),

                               webapp2.Route(
                                   r'/gpx/<key>',
                                   handler="prettymaps.handlers.GPXHandler", name='up-down-gpx',
                                   defaults={
                                        "kind": prettymaps.model.Map,
                                        "prop": "gpx",
                                        "content_type": "text/xml"
                                   }
                               ),

                               webapp2.Route(
                                   r'/layer/<layer>/<key>',
                                   handler="prettymaps.handlers.IconsHandler", name='up-down-icons'
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
