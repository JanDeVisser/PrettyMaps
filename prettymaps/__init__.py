#
# Copyright (c) 2018 Jan de Visser (jan@sweattrails.com)
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

import grumble
import grumble.image
import grit.handlers


class GPXLayer(grumble.Model):
    gpx = grumble.image.ImageProperty()

    def after_insert(self):
        project = self.parent()
        project.current_gpx = self
        project.put()


class Project(grumble.Model):
    project_name = grumble.TextProperty(verbose_name="Name")
    description = grumble.TextProperty()


class Map(grumble.Model):
    map_name = grumble.TextProperty(verbose_name="Name")
    description = grumble.TextProperty()
    gpx = grumble.image.ImageProperty()
    layers = grumble.JSONProperty();
    # current_gpx = grumble.ReferenceProperty(GPXLayer)