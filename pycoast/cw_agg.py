#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pycoast, Writing of coastlines, borders and rivers to images in Python
#
# Copyright (C) 2011-2015
#    Esben S. Nielsen
#    Hróbjartur Þorsteinsson
#    Stefano Cerino
#    Katja Hungershofer
#    Panu Lahtinen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from PIL import Image
import logging

import aggdraw

from cw_base import ContourWriterBase

logger = logging.getLogger(__name__)


class ContourWriterAGG(ContourWriterBase):

    """Adds countours from GSHHS and WDBII to images
       using the AGG engine for high quality images.

    :Parameters:
    db_root_path : str
        Path to root dir of GSHHS and WDBII shapefiles
    """
    _draw_module = "AGG"
    # This is a flag to make _add_grid aware of which text draw routine
    # from PIL or from aggdraw should be used
    # (unfortunately they are not fully compatible)

    def _get_canvas(self, image):
        """Returns AGG image object
        """
        return aggdraw.Draw(image)

    def _engine_text_draw(self, draw, x_pos, y_pos, txt, font, **kwargs):
        draw.text((x_pos, y_pos), txt, font)

    def _draw_polygon(self, draw, coordinates, **kwargs):
        """Draw polygon
        """
        pen = aggdraw.Pen(kwargs['outline'],
                          kwargs['width'],
                          kwargs['outline_opacity'])
        if kwargs['fill'] is None:
            fill_opacity = 0
        else:
            fill_opacity = kwargs['fill_opacity']
        brush = aggdraw.Brush(kwargs['fill'], fill_opacity)
        draw.polygon(coordinates, pen, brush)

    def _draw_rectangle(self, draw, coordinates, **kwargs):
        """Draw rectangle
        """
        pen = aggdraw.Pen(kwargs['outline'])

        fill_opacity = kwargs.get('fill_opacity', 255)
        brush = aggdraw.Brush(kwargs['fill'], fill_opacity)
        draw.rectangle(coordinates, pen, brush)

    def _draw_ellipse(self, draw, coordinates, **kwargs):
        """Draw ellipse
        """
        pen = aggdraw.Pen(kwargs['outline'])

        fill_opacity = kwargs.get('fill_opacity', 255)
        brush = aggdraw.Brush(kwargs['fill'], fill_opacity)
        draw.ellipse(coordinates, brush, pen)

    def _draw_text_box(self, draw, text_position, text, font, outline, box_outline, box_opacity):
        """Add text box in xy
        """

        if box_outline is not None:
            text_size = draw.textsize(text, font)
            margin = 2
            xUL = text_position[0] - margin
            yUL = text_position[1]
            xLR = xUL + text_size[0] + (2 * margin)
            yLR = yUL + text_size[1]
            box_size = (xUL, yUL, xLR, yLR)

            self._draw_rectangle(
                draw, box_size, fill=box_outline, fill_opacity=box_opacity,
                outline=box_outline)

        self._draw_text(draw, text_position, text, font, align="no")

    def _draw_line(self, draw, coordinates, **kwargs):
        """Draw line
        """
        pen = aggdraw.Pen(kwargs['outline'],
                          kwargs['width'],
                          kwargs['outline_opacity'])
        draw.line(coordinates, pen)

    def _finalize(self, draw):
        """Flush the AGG image object
        """

        draw.flush()

    def add_shapefile_shapes(self, image, area_def, filename, feature_type=None,
                             fill=None, fill_opacity=255, outline='white',
                             width=1, outline_opacity=255, x_offset=0,
                             y_offset=0):
        """Add shape file shapes from an ESRI shapefile.
        Note: Currently only supports lon-lat formatted coordinates.

        :Parameters:
        image : object
            PIL image object
        area_def : list [proj4_string, area_extent]
          | proj4_string : str
          |     Projection of area as Proj.4 string
          | area_extent : list
          |     Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        filename : str
            Path to ESRI shape file
        feature_type : 'polygon' or 'line', 
            only to override the shape type defined in shapefile, optional
        fill : str or (R, G, B), optional
            Polygon fill color
        fill_opacity : int, optional {0; 255}
            Opacity of polygon fill
        outline : str or (R, G, B), optional
            line color
        width : float, optional
            line width
        outline_opacity : int, optional {0; 255}
            Opacity of lines
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        self._add_shapefile_shapes(image=image, area_def=area_def,
                                   filename=filename, feature_type=feature_type,
                                   x_offset=x_offset, y_offset=y_offset,
                                   fill=fill, fill_opacity=fill_opacity,
                                   outline=outline, width=width,
                                   outline_opacity=outline_opacity)

    def add_shapefile_shape(self, image, area_def, filename, shape_id,
                            feature_type=None,
                            fill=None, fill_opacity=255, outline='white',
                            width=1, outline_opacity=255, x_offset=0,
                            y_offset=0):
        """Add a single shape file shape from an ESRI shapefile.
        Note: To add all shapes in file use the 'add_shape_file_shapes' routine.
        Note: Currently only supports lon-lat formatted coordinates.

        :Parameters:
        image : object
            PIL image object
        area_def : list [proj4_string, area_extent]
          | proj4_string : str
          |     Projection of area as Proj.4 string
          | area_extent : list
          |     Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        filename : str
            Path to ESRI shape file
        shape_id : int
            integer id of shape in shape file {0; ... }
        feature_type : 'polygon' or 'line', 
            only to override the shape type defined in shapefile, optional
        fill : str or (R, G, B), optional
            Polygon fill color
        fill_opacity : int, optional {0; 255}
            Opacity of polygon fill
        outline : str or (R, G, B), optional
            line color
        width : float, optional
            line width
        outline_opacity : int, optional {0; 255}
            Opacity of lines
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        self._add_shapefile_shape(image=image,
                                  area_def=area_def, filename=filename,
                                  shape_id=shape_id,
                                  feature_type=feature_type,
                                  x_offset=x_offset, y_offset=y_offset,
                                  fill=fill, fill_opacity=fill_opacity,
                                  outline=outline, width=width,
                                  outline_opacity=outline_opacity)

    def add_line(self, image, area_def, lonlats,
                 fill=None, fill_opacity=255, outline='white', width=1,
                 outline_opacity=255, x_offset=0, y_offset=0):
        """Add a user defined poly-line from a list of (lon,lat) coordinates.

        :Parameters:
        image : object
            PIL image object
        area_def : list [proj4_string, area_extent]
          | proj4_string : str
          |     Projection of area as Proj.4 string
          | area_extent : list
          |     Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        lonlats : list of lon lat pairs
            e.g. [(10,20),(20,30),...,(20,20)]
        outline : str or (R, G, B), optional
            line color
        width : float, optional
            line width
        outline_opacity : int, optional {0; 255}
            Opacity of lines
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        self._add_line(image, area_def, lonlats, x_offset=x_offset,
                       y_offset=y_offset, fill=fill, fill_opacity=fill_opacity,
                       outline=outline, width=width,
                       outline_opacity=outline_opacity)

    def add_polygon(self, image, area_def, lonlats,
                    fill=None, fill_opacity=255, outline='white', width=1,
                    outline_opacity=255, x_offset=0, y_offset=0):
        """Add a user defined polygon from a list of (lon,lat) coordinates.

        :Parameters:
        image : object
            PIL image object
        area_def : list [proj4_string, area_extent]
          | proj4_string : str
          |     Projection of area as Proj.4 string
          | area_extent : list
          |     Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        lonlats : list of lon lat pairs
            e.g. [(10,20),(20,30),...,(20,20)]
        fill : str or (R, G, B), optional
            Polygon fill color
        fill_opacity : int, optional {0; 255}
            Opacity of polygon fill
        outline : str or (R, G, B), optional
            line color
        width : float, optional
            line width
        outline_opacity : int, optional {0; 255}
            Opacity of lines
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        self._add_polygon(image, area_def, lonlats, x_offset=x_offset,
                          y_offset=y_offset, fill=fill,
                          fill_opacity=fill_opacity, outline=outline,
                          width=width, outline_opacity=outline_opacity)

    def add_grid(self, image, area_def, Dlon, Dlat, dlon, dlat,
                 font=None, write_text=True, fill=None, fill_opacity=255,
                 outline='white', width=1, outline_opacity=255,
                 minor_outline='white', minor_width=0.5,
                 minor_outline_opacity=255, minor_is_tick=True,
                 lon_placement='tb', lat_placement='lr'):
        """Add a lon-lat grid to a PIL image object

        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        (Dlon,Dlat): (float,float)
            Major grid line separation
        (dlon,dlat): (float,float)
            Minor grid line separation
        font: Aggdraw Font object, optional
            Font for major line markings
        write_text : boolean, optional
            Deterine if line markings are enabled
        fill_opacity : int, optional {0; 255}
            Opacity of text
        outline : str or (R, G, B), optional
            Major line color
        width : float, optional
            Major line width
        outline_opacity : int, optional {0; 255}
            Opacity of major lines
        minor_outline : str or (R, G, B), optional
            Minor line/tick color
        minor_width : float, optional
            Minor line width
        minor_outline_opacity : int, optional {0; 255}
            Opacity of minor lines/ticks
        minor_is_tick : boolean, optional
            Use tick minor line style (True) or full minor line style (False)
        """
        self._add_grid(image, area_def, Dlon, Dlat, dlon, dlat,
                       font=font, write_text=write_text,
                       fill=fill, fill_opacity=fill_opacity, outline=outline,
                       width=width, outline_opacity=outline_opacity,
                       minor_outline=minor_outline, minor_width=minor_width,
                       minor_outline_opacity=minor_outline_opacity,
                       minor_is_tick=minor_is_tick,
                       lon_placement=lon_placement, lat_placement=lat_placement)

    def add_grid_to_file(self, filename, area_def, Dlon, Dlat, dlon, dlat,
                         font=None, write_text=True,
                         fill=None, fill_opacity=255,
                         outline='white', width=1, outline_opacity=255,
                         minor_outline='white', minor_width=0.5,
                         minor_outline_opacity=255, minor_is_tick=True,
                         lon_placement='tb', lat_placement='lr'):
        """Add a lon-lat grid to an image

        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        (Dlon,Dlat): (float,float)
            Major grid line separation
        (dlon,dlat): (float,float)
            Minor grid line separation
        font: Aggdraw Font object, optional
            Font for major line markings
        write_text : boolean, optional
            Deterine if line markings are enabled
        fill_opacity : int, optional {0; 255}
            Opacity of text
        outline : str or (R, G, B), optional
            Major line color
        width : float, optional
            Major line width
        outline_opacity : int, optional {0; 255}
            Opacity of major lines
        minor_outline : str or (R, G, B), optional
            Minor line/tick color
        minor_width : float, optional
            Minor line width
        minor_outline_opacity : int, optional {0; 255}
            Opacity of minor lines/ticks
        minor_is_tick : boolean, optional
            Use tick minor line style (True) or full minor line style (False)
        """

        image = Image.open(filename)
        self.add_grid(image, area_def, (Dlon, Dlat), (dlon, dlat),
                      font=font, write_text=write_text,
                      fill=fill, fill_opacity=fill_opacity,
                      outline=outline, width=width,
                      outline_opacity=outline_opacity,
                      minor_outline=minor_outline,
                      minor_width=minor_width,
                      minor_outline_opacity=minor_outline_opacity,
                      minor_is_tick=minor_is_tick,
                      lon_placement=lon_placement, lat_placement=lat_placement)
        image.save(filename)

    def add_coastlines(self, image, area_def, resolution='c', level=1,
                       fill=None, fill_opacity=255, outline='white', width=1,
                       outline_opacity=255, x_offset=0, y_offset=0):
        """Add coastlines to a PIL image object

        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4}
            Detail level of dataset
        fill : str or (R, G, B), optional
            Land color
        fill_opacity : int, optional {0; 255}
            Opacity of land color
        outline : str or (R, G, B), optional
            Coastline color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """

        self._add_feature(image, area_def, 'polygon', 'GSHHS',
                          resolution=resolution, level=level,
                          fill=fill, fill_opacity=fill_opacity,
                          outline=outline, width=width,
                          outline_opacity=outline_opacity, x_offset=x_offset,
                          y_offset=y_offset)

    def add_coastlines_to_file(self, filename, area_def, resolution='c',
                               level=1, fill=None, fill_opacity=255,
                               outline='white', width=1, outline_opacity=255,
                               x_offset=0, y_offset=0):
        """Add coastlines to an image file

        :Parameters:
        filename : str
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4}
            Detail level of dataset
        fill : str or (R, G, B), optional
            Land color
        fill_opacity : int, optional {0; 255}
            Opacity of land color
        outline : str or (R, G, B), optional
            Coastline color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """

        image = Image.open(filename)
        self.add_coastlines(image, area_def, resolution=resolution,
                            level=level, fill=fill,
                            fill_opacity=fill_opacity, outline=outline,
                            width=width, outline_opacity=outline_opacity,
                            x_offset=x_offset, y_offset=y_offset)
        image.save(filename)

    def add_borders(self, image, area_def, resolution='c', level=1,
                    outline='white', width=1, outline_opacity=255,
                    x_offset=0, y_offset=0):
        """Add borders to a PIL image object

        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3}
            Detail level of dataset
        outline : str or (R, G, B), optional
            Border color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """

        self._add_feature(image, area_def, 'line', 'WDBII', tag='border',
                          resolution=resolution, level=level, outline=outline,
                          width=width, outline_opacity=outline_opacity,
                          x_offset=x_offset, y_offset=y_offset)

    def add_borders_to_file(self, filename, area_def, resolution='c',
                            level=1, outline='white', width=1,
                            outline_opacity=255, x_offset=0, y_offset=0):
        """Add borders to an image file

        :Parameters:
        image : object
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3}
            Detail level of dataset
        outline : str or (R, G, B), optional
            Border color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """
        image = Image.open(filename)
        self.add_borders(image, area_def, resolution=resolution, level=level,
                         outline=outline, width=width,
                         outline_opacity=outline_opacity, x_offset=x_offset,
                         y_offset=y_offset)
        image.save(filename)

    def add_rivers(self, image, area_def, resolution='c', level=1,
                   outline='white', width=1, outline_opacity=255,
                   x_offset=0, y_offset=0):
        """Add rivers to a PIL image object

        :Parameters:
        image : object
            PIL image object
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
            Detail level of dataset
        outline : str or (R, G, B), optional
            River color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """

        self._add_feature(image, area_def, 'line', 'WDBII', tag='river',
                          zero_pad=True, resolution=resolution, level=level,
                          outline=outline, width=width,
                          outline_opacity=outline_opacity, x_offset=x_offset,
                          y_offset=y_offset)

    def add_rivers_to_file(self, filename, area_def, resolution='c', level=1,
                           outline='white', width=1, outline_opacity=255,
                           x_offset=0, y_offset=0):
        """Add rivers to an image file

        :Parameters:
        image : object
            Image file
        proj4_string : str
            Projection of area as Proj.4 string
        area_extent : list
            Area extent as a list (LL_x, LL_y, UR_x, UR_y)
        resolution : str, optional {'c', 'l', 'i', 'h', 'f'}
            Dataset resolution to use
        level : int, optional {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
            Detail level of dataset
        outline : str or (R, G, B), optional
            River color
        width : float, optional
            Width of coastline
        outline_opacity : int, optional {0; 255}
            Opacity of coastline color
        x_offset : float, optional
            Pixel offset in x direction
        y_offset : float, optional
            Pixel offset in y direction
        """

        image = Image.open(filename)
        self.add_rivers(image, area_def, resolution=resolution, level=level,
                        outline=outline, width=width,
                        outline_opacity=outline_opacity, x_offset=x_offset,
                        y_offset=y_offset)
        image.save(filename)

    def _get_font(self, outline, font_file, font_size):
        """Return a font."""
        return aggdraw.Font(outline, font_file, size=font_size)


def _get_lon_lat_bounding_box(area_extent, x_size, y_size, prj):
    """Get extreme lon and lat values
    """

    x_ll, y_ll, x_ur, y_ur = area_extent
    x_range = np.linspace(x_ll, x_ur, num=x_size)
    y_range = np.linspace(y_ll, y_ur, num=y_size)

    lons_s1, lats_s1 = prj(np.ones(y_range.size) * x_ll, y_range, inverse=True)
    lons_s2, lats_s2 = prj(x_range, np.ones(x_range.size) * y_ur, inverse=True)
    lons_s3, lats_s3 = prj(np.ones(y_range.size) * x_ur, y_range, inverse=True)
    lons_s4, lats_s4 = prj(x_range, np.ones(x_range.size) * y_ll, inverse=True)

    angle_sum = 0
    prev = None
    for lon in np.concatenate((lons_s1, lons_s2, lons_s3[::-1], lons_s4[::-1])):
        if prev is not None:
            delta = lon - prev
            if abs(delta) > 180:
                delta = (abs(delta) - 360) * np.sign(delta)
            angle_sum += delta
        prev = lon

    if round(angle_sum) == -360:
        # Covers NP
        lat_min = min(lats_s1.min(), lats_s2.min(),
                      lats_s3.min(), lats_s4.min())
        lat_max = 90
        lon_min = -180
        lon_max = 180
    elif round(angle_sum) == 360:
        # Covers SP
        lat_min = -90
        lat_max = max(lats_s1.max(), lats_s2.max(),
                      lats_s3.max(), lats_s4.max())
        lon_min = -180
        lon_max = 180
    elif round(angle_sum) == 0:
        # Covers no poles
        if np.sign(lons_s1[0]) * np.sign(lons_s1[-1]) == -1:
            # End points of left side on different side of dateline
            lon_min = lons_s1[lons_s1 > 0].min()
        else:
            lon_min = lons_s1.min()

        if np.sign(lons_s3[0]) * np.sign(lons_s3[-1]) == -1:
            # End points of right side on different side of dateline
            lon_max = lons_s3[lons_s3 < 0].max()
        else:
            lon_max = lons_s3.max()

        lat_min = lats_s4.min()
        lat_max = lats_s2.max()
    else:
        # Pretty strange
        lat_min = -90
        lat_max = 90
        lon_min = -180
        lon_max = 180

    if not (-180 <= lon_min <= 180):
        lon_min = -180
    if not (-180 <= lon_max <= 180):
        lon_max = 180
    if not (-90 <= lat_min <= 90):
        lat_min = -90
    if not (-90 <= lat_max <= 90):
        lat_max = 90

    return lon_min, lon_max, lat_min, lat_max


def _get_pixel_index(shape, area_extent, x_size, y_size, prj,
                     x_offset=0, y_offset=0):
    """Map coordinates of shape to image coordinates
    """

    # Get shape data as array and reproject
    shape_data = np.array(shape.points)
    lons = shape_data[:, 0]
    lats = shape_data[:, 1]

    x_ll, y_ll, x_ur, y_ur = area_extent

    x, y = prj(lons, lats)

    # Handle out of bounds
    i = 0
    segments = []
    if 1e30 in x or 1e30 in y:
        # Split polygon in line segments within projection
        is_reduced = True
        if x[0] == 1e30 or y[0] == 1e30:
            in_segment = False
        else:
            in_segment = True

        for j in range(x.size):
            if (x[j] == 1e30 or y[j] == 1e30):
                if in_segment:
                    segments.append((x[i:j], y[i:j]))
                    in_segment = False
            elif not in_segment:
                in_segment = True
                i = j
        if in_segment:
            segments.append((x[i:], y[i:]))

    else:
        is_reduced = False
        segments = [(x, y)]

    # Convert to pixel index coordinates
    l_x = (x_ur - x_ll) / x_size
    l_y = (y_ur - y_ll) / y_size

    index_arrays = []
    for x, y in segments:
        n_x = ((-x_ll + x) / l_x) + 0.5 + x_offset
        n_y = ((y_ur - y) / l_y) + 0.5 + y_offset

        index_array = np.vstack((n_x, n_y)).T
        index_arrays.append(index_array)

    return index_arrays, is_reduced
