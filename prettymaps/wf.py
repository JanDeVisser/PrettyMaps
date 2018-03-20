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

import gripe
import grumble
import grudge

import prettymaps


@grudge.OnStarted("add_gpx_to_project")
@grudge.OnAdd("done", grudge.Stop())
@grudge.Process()
class UploadGPX(grumble.Model):
    UploadedFile = grumble.ReferenceProperty(grit.upload.UploadedFile)
    project = grumble.ReferenceProperty(prettymaps.Project)
    done = grudge.Status()

    def add_gpx_to_project(self):
        gpx = prettymaps.GPXLayer(parent=self.project,
                                  gpx=self.uploadedFile.content,
                                  filename=self.uploadedFile.filename)
        gpx.put()
        return self.done
