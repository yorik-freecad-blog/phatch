# Phatch - Photo Batch Processor
# Copyright (C) 2007-2010 www.stani.be
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

# Copyright (C) 2010 by Pawel T. Jochym <jochym@gmail.com>, www.stani.be

# Embedded icon is created by Stani, but derived
# from Igor Kekeljevic (http://www.admiror-ns.co.yu).

# Make m x n grid with copies of input image

# Follows PEP8

# TODO: Add spacing between images for which the line color will need
# to be used.

from core import models
from core.translation import _t
from lib import imtools
from math import sqrt


CHOICES = ['0', '1', '2', '5', '10']
ZERO = ['', '0']


#---PIL
def init():
    global Image, ImageColor, HTMLColorToRGBA, imtools
    import Image
    import ImageColor
    from lib import imtools
    from lib.colors import HTMLColorToRGBA


def make_grid(image, grid, col_line_width=0, row_line_width=0,
        line_color='#FFFFFF', line_opacity=0, old_size=None, scale=True):

    # Check if there is any work to do.
    if grid == (1, 1):
        return image

    # Because of layer support photo size can be different
    # from image layer size
    if old_size is None:
        old_size = image.size

    # Unpack grid
    cols, rows = grid

    # Scaling down?
    if scale:
        # Keep the same number of pixels in the result
        s = sqrt(cols * rows)
        old_size = tuple([int(x / s) for x in old_size])
        # To scale down we need to make the image processing safe.
        image = imtools.convert_safe_mode(image)\
            .resize(old_size, getattr(Image, 'ANTIALIAS'))

    #displacement
    dx, dy = old_size
    dx += col_line_width
    dy += row_line_width
    new_size = cols * dx - col_line_width, rows * dy - row_line_width

    # The main priority is that the new_canvas has the same mode as the image.

    # Palette images
    if image.mode == 'P':

        if 0 < line_opacity < 255:
            # transparent lines require RGBA
            image = imtools.convert(image, 'RGBA')

        else:
            if 'transparency' in image.info and line_opacity == 0:
                # Make line color transparent for images
                # with transparency.
                line_color_index = image.info['transparency']
                palette = None
            else:
                line_color_index, palette = imtools.fit_color_in_palette(
                    image,
                    ImageColor.getrgb(line_color),
                )
            if line_color_index != -1:
                new_canvas = Image.new('P', new_size, line_color_index)
                imtools.put_palette(new_canvas, image, palette)
            else:
                # Convert to non palette image (RGB or RGBA)
                image = imtools.convert_safe_mode(image)

    # Non palette images
    if image.mode != 'P':

        line_color = ImageColor.getcolor(line_color, image.mode)
        if imtools.has_alpha(image):
            # Make line color transparent for images
            # with an alpha channel.
            line_color = tuple(list(line_color)[:-1] + [line_opacity])
            pass
        new_canvas = Image.new(image.mode, new_size, line_color)

    # Paste grid
    for x in range(cols):
        for y in range(rows):
            pos = (x * dx, y * dy)
            imtools.paste(new_canvas, image, pos, force=True)

    return new_canvas


#---Phatch
class Action(models.Action):
    label = _t('Grid')
    all_layers = True
    author = 'Pawel T. Jochym'
    email = 'jochym@gmail.com'
    init = staticmethod(init)
    pil = staticmethod(make_grid)
    version = '0.2'
    tags = [_t('size'), _t('filter')]
    update_size = True
    __doc__ = _t('Make n x m matrix of image')

    def interface(self, fields):
        fields[_t('Columns')] = self.SliderField(2, 1, 10)
        fields[_t('Rows')] = self.SliderField(2, 1, 10)
        fields[_t('Scale to Keep Size')] = self.BooleanField(False)
        fields[_t('Column Line Width')] = \
            self.PixelField('0 px', choices=CHOICES)
        fields[_t('Row Line Width')] = \
            self.PixelField('0 px', choices=CHOICES)
        fields[_t('Line Color')] = self.ColorField('#FFFFFF')
        fields[_t('Line Opacity')] = self.SliderField(0, 0, 100)

    def values(self, info):
        #size
        x0, y0 = info['size']
        dpi = info['dpi']
        x1 = self.get_field('Columns', info)
        y1 = self.get_field('Rows', info)
        #parameters
        return {
            'old_size': (x0, y0),
            'grid': (x1, y1),
            'scale': self.get_field('Scale to Keep Size', info),
            'col_line_width': self.get_field_size(
                'Column Line Width', info, y0, dpi),
            'row_line_width': self.get_field_size(
                'Row Line Width', info, x0, dpi),
            'line_color': self.get_field('Line Color', info),
            'line_opacity': \
                int(255 * self.get_field('Line Opacity', info) / 100.0),
        }

    def get_relevant_field_labels(self):
        relevant = ['Columns', 'Rows', 'Scale to Keep Size',
            'Column Line Width', 'Row Line Width']
        col_line_width = self.get_field_string('Column Line Width').strip()
        if col_line_width:
            col_line_width = col_line_width.split()[0]
        row_line_width = self.get_field_string('Row Line Width').strip()
        if row_line_width:
            row_line_width = row_line_width.split()[0]
        if not(col_line_width in ZERO and row_line_width in ZERO):
            relevant.extend(['Line Color', 'Line Opacity'])
        return relevant

    icon = \
'x\xda\x01\xcd\x0c2\xf3\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\
\x00\x000\x08\x06\x00\x00\x00W\x02\xf9\x87\x00\x00\x00\x04sBIT\x08\x08\x08\
\x08|\x08d\x88\x00\x00\x0c\x84IDATh\x81\xcd\x9a{\x90\x15\xd5\x9d\xc7?\xa7\
\xfbt\xf7\xed\xfb\x9cAT\x98\xe1%\xc6\'\x08\xc6\xac\x89FVB\xf0\x811\xd1d\xa8e\
\xdd\xda@-\xcc\xba\x1a\xd7\xa5BI\xb1\x82\xbaI\xcc\xc6`\x89\x0fP#\xbajVL\xa9\
\xb1\x12\xa3\xc9\xc6\xb0q\x8d\xd1U\x13\t\x88<bv\x84\x19\x06\x06\x98\xf7\xbd3\
w\xee\xf4}u\x9f\xb3\x7f\xdc\x073\n\x83<|\x9c\xaaSSsg\xfa\xf6\xf7\xfb\xeb\xef\
\xf9\x9e\xef\xf9\xdd\x8b\xd6\x9aO\xc3\x04\x04`\x02\x16\x10\x02\xa2@\xf4\xdak\
\xaf\xad\x01\xc4\xa1\xae\x13\xe5\x8b?\xb1!\x84\x10\x80A\t\xb8\x1b\x8dF\xa3\
\x0b\x17.\xfc\xc2\xc4\x89\x13g&\x12\x89\x0b\r\xc3H766^\xaa\xb5\x0e\x0ev\xbd\
\xfcX\xd1\x0e\x19C\x80K 2y\xf2\xe4\x93o\xb8\xf1\xbao\xd7\x8f\x9dp\x8di\x9aq\
\xa5\x14J)\xfa\xfb\xfbW\x95\xff\xef\xd3C@\x08Q\x01\xee\xda\xb6]{\xeb\xed\xff\
\xdax\xe6Yg\xdc\xe4\x10s\x95Rh\xad\xa9\xfc\xec\xe9\xe9y\x138\xa4L>V\x02\xe5\
\xaa\x9b\x80\x03$\x96.]:\xfb\xf3\x17\x9f\xbb2\xe1\x9cXW\xa9x1\xd0\xbc\xd7\
\x1fpZ\xd4@\xa0\xd9\xb8q\xe3;|\xd2\x04\xde\xa7\xf3\xe8\xacY\xb3&7\xde0\x7f\
\xe5\xb8\x13O\x99\xa5Ti1f\x8b\x01[R\x8a\xcd\xbd\x01\x11K0\xa5\xd6\xc4\xf7\
\xfd\xde\x17^x\xa1\xf7\x13%P\x96\x8b\t\xb8@\xcd\xfd\x0f\xae\xbe\xee\x9c\xe9S\
o\xb2\r\xd7\xa9T}{O\x9e\xdf\xb5\xe5\xc8\x05\x1a\xd7\x96\x9cZ+\x91RS(\x14v\
\x01\xfe\'B`H\xd5\x1d \xbex\xf1\xe2\x0b\xbe:\xf7\xf2\xbbO\x88\x8e\x99\\\xd1w\
\xd7`\x81_\xef\x1c`\xcf@\x11\xd7\x92\xd4\x86$\xaem1!f e@\x10\x04-@\xa0G\xb0\
\xca\xe3N\xa0\x0c\\\x006\x10\x99>}z\xfd\xbf}\x7f\xf9m\xa7O>{.Z\x88\x92\xce\
\x15\xbfkI\xf1z\xdb\x00\xb64\xa9\r\x87pmY\x9dc"\x1a\xcb00\x0cc\x90\x11\xaa\
\x7f\xdc\x08\x0c\x01]\xd9\x88\x1c ~\xf3\xcd7_}\xf1\x97f\xfcp\\\xdd\x84\xb0%m\
\xb4\xd6\xfc\xb9s\x80_\xbc\xdb\x85\xe7kb\xaeM\xd8\xb2pmI\xa8B\xc0\x92\xb8v\
\x11\x89\xc2q\x9c\xe8\xe1\xee}\xcc\x04\x86X\xa2\x03\xc4\x96-[vi]]\xdd\x15\
\xb1X\xec\xa2P(4.\xd5\xdb\xcf\xa4\t\x92\x81\xa2\xe6\xe7\xdb\xf6\xf3\x7f\xdd\
\x1e\xae-\xa9\x8dT\xc0\x0e\x99\x96\xa4`%1\xad\x04R\x07\xd8\xb6\x1d\xfb\xc8\
\x08\x0c\xb1\xc4\x10\x10kll\x9cq\xe1%\x9f\xbds\x94SwJeqj\xadq\x1c\x07\xcb\
\xb2X\xb7\xa1\x95n\xafHm$4\xa4\xd2\x12\xcbVl\x94\xcf\xf2\xae~\x8d\xf6\xbe\
\x9dx}\x03\xfc\xf6\xb3\xbf\xe7\x04\x19\xc1\xb6\xed(\xa5\'{\xfc\x08\x0cY\x9c6\
\x10\xbd\xea\xaa\xab\xce\xfa\xda5\x97\xfcplb\xf2\x17u\xd9\x12\x95R\x04J\x81\
\xd6D"\x11\xa4\x94\xc4\xc3!|a\x0e\x03\xdffm\xe2g\xc5;\xe8\xed\xd9\x07i \r"\r\
=g\xf4prm\xa2\xf2\x04\x84\x10B\x1cj!\x1f\x11\x81!r\t\xd7\xd7\xd7\x9f\xb4\xe2\
\xbb\xcb\x96}f\xd2\xe9\xff` \xcdJ\xc5\xdb2\x01\x9bz4\xe7\x8d\x92\x9c\xech\\\
\xd7E\x08A\xdc\xb5\xd1\x86Y\x05\xdf"\xde\xe2\xb1\xf6o\xe3\xa7\x8b\x882x\xd2\
\x10)\xc4pM\x0b)ee\r\x18#a\xfaP\x04\xde\'\x97\xf8\x8a\x15+\xe6\xcc\x98\xfd\
\x85;\xa3V\xed\xe8J\xc5\xf7\xa4\x8b\xbc\xb6\xbf@\xbb\x17\x10\xb6%c\xa3&\x86V\
D"\x11\x84\x10$\\\x1b\xc3T8\xb6`}\xfea~\x93|\x0cm(\x88\x826A\xf8\xf0\x951Wq\
\xcb\xec\x9b91r\x02J),\xcb\xb2)IHp\x087\x1a1\x8d\xbe\x7f\x07\x9d3g\xcei\xffx\
\xe3\x82\x95\xe3O:\xf5b\xadJ\xc0\xbdb\xc0\xff\xec\xce\xb0\xb5;\x8f#K\x12\xa9\
\x8bJ.\x1f\x03A\x10\xa8\xf1\xe3\xc7\x1b\xb1X\x8c\xd7\xdb2\xbc\x95}\x8du\xa9\
\xef\x91\xf2:!OuF\xbc\x08\xb7\x9f\x7f;\x7f3enu\xed\xb4\xb5\xb5m\xdd\xbcy\xf3\
v\xc7q\xfc\xeb\xaf\xbf~\xd1\x11\xa7\xd1!U\x0f\x87B\xa1Q?zx\xcd\xf5S\xa7\x9e\
\xb3\xc42Bv\xa5\xeao\xb7g\xf8\xed\xae4E\x05q\xd7\xa9\xba\xc9\x84\x84\x89\x94\
\x01\xbe\xefgL\xd3\x8c\x0b!X\xef\xfd\x98\'\xdb\xeeA\xe7u\x15\xb8\x995h\xa8\
\xff[V\xcd\xbb\x03\xd30\x01H\xa7\xd3\xb9m\xdb\xb6\x19\x9e\xe7M\xab\xad\xad\
\x9d\xe6y\xde#\x8c\xb0\x90G\x92\x90\x01Do\xb9\xe5\x96\x99s\xbe\xfe\xe5\xd5\
\xa3\xa3u\x13+\xee\xd21\x90\xe7\x17\x7f\xe9a\xef@\x01\xd7\x96D\xdfg\x87c" \
\xa5\xc0\xb2,\xa3T\x07\xd8\xd6\xf5\x06:\xa9\x11y \x07g\x87\xa6\xf2\xf8\xbc\
\xc7\xa8\x8f\x8f\x05\xa0P\xc8\xab\xa6\xa6\xf7\x8c\xae\xae\xae\x90\xe38D\xa3Q\
\xb4\xd6ttt\xbc5\x02\xc6\x83\x13(W_\xce\x9e=\xbbn\xd1\xa2E\xcfi\xad\r\xad5\
\xb9\xa2\xcf\x7f7\'y\xbd5\x85m\x99%K<\x88\x97\xbb\x8eF\x9a\x05\x94Rv\xe5\xe4\
\xe4\x0cZ\x88$\xc4\xfd\x04\xab.\xbf\x9b+\xce\xb8\xacz\xbf\xdd\xbb[\xf5\xde\
\xbd\xfb\x0c\xd34\x89\xc7\xe3\xf4\x15\x05q\xa9A+ZZZ6p\x94Y\xc8\xc8\xe5ra\xcb\
\xb2\x0c\xad5;\xbb\x07\xf8\xcf?\xed!\x17h\xe2ag\x98\x1d\xba\xb6$c\xefc\xb7\
\xb1\x9b\x1ev\xe1\xa8/2\xc69\x15!\x84UYc\x13\xe4x\xfen\xe6\x83\xcc\x9d\xf2\
\xb5\xea\r\x92\xa9^\xb5\xbbu\x8f\xa1\xb5\x16\xb1X\x8c\xee\x9cfcO@WV\xf3\xcdS\
L\x82 \xf0\xd6\xae]\xdbv\xb4\x04D:\x9d\xd6\x86Qr\xb1\xd6\xbe\x1c\x18f9p\x1d\
\x00\xdfo\xb7\xf2\x1c\xf7\xd2\x94\xd9P\xb5\xc2I\xa7\xd40c\xe2\x19\x18\x86Q5\
\x89{.[Y}\xe3\\.\x17\xb4\xb5\xb5\x99\x9e\xe7\x19\xae\xeb2P\x84\x97\xf6fiN\
\x07\xd8\xd2\xe4\xacZ\x1b)5\xbe\xef\xb7r,i4\x9b\xcdV/\x0c\xdb\x16\xb5\x91\
\xe1\x95\xdfl\xfe\x92gSw\xa0\xd2\xaa\xba\t1\x00\xfd\x91^\xe4\xa9\xb2\xea(\
\x15\x12J)\xdd\xde\xb1\x9f\xfe\xbe\xb4\xe98\x0e\xb1x\x827\xf7{\xbc\xb9?[\xdd\
+\\\xdbbR\xd9\x04\x82 h\xe6X\xd2h6\x9b\xadZW)\xbf\x1c\xd0\xfc\x1f\x8a\xcf\
\xf2\xd3}wB^#2@/\xd0\x0e\xe7\xd6\x9f\xcf7\xce\xbe\x12)\x87\x13\xe8M\xf6\xf8}\
\xa9~)\xa5\xa4\xa6\xa6\x86\xd6\xfe<\xbf\xda\xd1G\x7fA\xe1\xda\xd6\xb0u46\x02\
\xd2\x14h\xad\xbb\x015\x12\xc6\x91\x08h\xdf\xf7\xab\x17\xbb\xb6\xa4&\xec\xd0\
#\x9by4}\x07;\xbdwJ&[N\xfcF\xc2\xe4[\xd3od\xe9\x85\x8b\x19r \xef\xca\x17\xf2\
\xb5\xfd\xfd\xfd\x96\x94R&\x12\t<_\xf3BS\x0f[\xbb\xca\xa1.\xec\x0c\'`I\xe2!\
\x1fS\x0bl\xdb\x0e\x8f\x04\xfe\xb0O`pp\xb0\xfa\xe8lK\xf0\xaaz\x9c\x17\xf6?\
\x84\xce\xab\xaa\x97\x8b\x1cL\xb7\xcf\xe3\xf1\xb9\x8frRd4Zk<\xcf\xcbn\xdc\
\xb8qw:\x9d\x1e\xe7\xba\xae5m\xda4\xdcp\x98?\xee\xe9\xe3\xc5\xa6n\x10\xc6\
\xa1\x1d\xcc\x96\x98R`a\x10\n\x85\x8e-Ng2\x99\xaa\x84\xfe\xab\xe7)\x9e\xdf\
\xfd\xe0\x01\xe0y\xa8-\x9c\xc0\x9aK\xd7\xf0\xa5\xc9\x7f\r\x944\xde\xd2\xd2\
\xa2Z[[]\xc30\xceL$\x12\xd8\xb6M$\x12a\xdd\xdb\xfbh\xea\xf1\xca\xd5\xb6\x86\
\x81O\xd9-l3\xde\xa0K\xed\xa2\xbd\xb7\x99\'\x12?\xc6\x15\x16\x96e\xc58\xd64\
\xaa\xb5\xd6B\x08a\x145"\x05\xe4@\xe6$\xff4\xf5\x06\x96\xcfZZ\xfd\xbf\xae\
\xeeN\xb5sG\xb3\x11\x04\x81\x19\x8d\x1e(\\4\x1a\xc5\xb2,|Lj\x86D\xe9\xb0-)\
\xd8)~e<\xc8\xa6\xcco\xd0i\r\x03%#H\xd6\'\x19\x15\xad\xaf<\x81\xa3N\xa3\xba<\
\x15`\x86|\x1b\'\x1d\xe2\xc2\xd13xp\xfej\xe2\xa1\xd2Y\xc3\xcbzA\xf3\xcef3\
\x93\xc9\x18\x8e\xe3\x10\x08\x83\xed)E\x9d\x0b\xa3mM8\x1c\xc60\x0c\xe2a\x1b5\
$\x8df\xadn\x1e\xeao$\x95\xea(9\xd8\x00U\x1bN\x0f\xf6!k&bY\xd61\x9f\x07*$8\
\xff\xc4\xf3x\xe5\xef_a|M=\x00J\x05z\xcf\x9e6\x91L&M\xcb\xb2\x08E\xe3\xbc\
\xddS\xe4\x9d^\x1f_\x0b\x16~F"E)N\x03$\\\x1ba*\\K\xd2m\xec`M\xe7\xb7\xc8\xe4\
S\x07<\xc6\x83\xba`\x1c\xcb\x1bn\xe5\xa2I\x7fU9\x0cE8\xd63\xb1RJ\x9b\xa6\xc9\
yc\xcf\xa9\xbe\xd6\xd5\xdd\xa9\xba\xbbz\xaa[\xff_RE^\xde\xe3\x91\x0b\xc0\xb5\
-\xea"\x16Q\x07\x94RC\xce\x03\x0ei\xb3\x83g\xb2\xf7\xb2!\xbd\x1e]\xd4P\x04\n\
@\x003&\xced\xed\x9c\x07\x08\xcb0Zk\xf2\xf9|Oww\xf7\x0f\x00\xffh\xf7\x81\xca\
EU+\xcd\x0cf\xfc\xae\xce.\xa9\x942b\xb1\x18\xa9\\\xc0\xf3\xcd\x19v\xf5\xe7\
\xcbm\x91\x92\x1d\x966"E.\x97\x1b\x94RF\x84\x10\xb4\xeaM\xac\xea\xbc\x89\xb4\
\x97\x1cf\x04u\xfe8\x1e\x9e\xf30\xe7\x96\x0b\xa4\x94\xf2\xf7\xee\xdd\xfb\xc4\
\x9a5k\xfe\xfd\x99g\x9ei\xe7\x10=\xd1\x11\t\x94\x17.\x80\xd2Zk\xdf\xf7\x83\
\xce\xae\x0e\xa3\x90/J\xd7u\xc10\xf9}k\x1f\xff\xbbg\x00\xeb m\x91\xfa\xa8@\
\xca\x00)ePI\xa3\xcf\xed{\x84tw\xb2\n\xdc\xc9\x85X\xf1\xf9[Y\xf4\xb9\x05\xd5\
\xfb\xf6\xf5\xf5\xbd\xbe~\xfd\xfa\xe5K\x97.}\xa7Dq\xe4\xea\x1f\x92@\xa5Mr\
\xfa\xe9\xa7\x87</\xa3\x07\x07\xb3f\xc8q\x89Fb\xec\xe8\xf5x\xee\xddv2\x05E\
\xccu\x0e\xea\xe5aG!\xa5\xc0\xb6m\xbb\xf2\x9e\xb6g"\x92 r\x82\xaf\x8e\xbb\
\x9a\xd5W\xdf\x8deX\x00\xe4r\xb9\xb6\xad[\xb7~\xb7\xa1\xa1\xe19\xc0+\x03\x1f\
q\x07\x1e\x91@y\x18\xa3F\x8dr\x1c\xc7um;\xc4@\xde\xe7\x99\xed\x1dl\xef\x18 d\
Kj"\xf6\x07\xc0\x1b\xb2@\x9fl%#GS\'\xe3\x08!l\xa5J8\x9c\xacMC\xfd5,\xb9\xe0F\
&\x8d\x9a\x00@\x10\x04\xd9\xd6\xd6\xd6\x1f-^\xbc\xf8\xde-[\xb6\xf4RZ\x15\xea\
pU\xff\xb0\x04\xc8\xe5r\xd8\xb6\x8d\x10\x82\x97\x9b\xf7\xb3\xa3\xd7\x1b\xe6\
\xe5\x95\xb6\xc8\x9f\xcc\x9f\xf2\x07\xfd3\x92\xc9vtZ\xb3t\xdc\xf78\xbb\xeeJ\
\x8cJ\x94\x05\xee\xbf\xf4\x1eFGFU~\xd5\xdd\xdd\xdd/>\xf5\xd4S\xb7\xdeu\xd7];\
(\xc9e\xc4\xd0vT\x04\xf2\xf9\xbc\xaah8\x12\xb2?\xd0\xd3\xe9\xb1\x9aXWXN2\xb9\
\xbf\xba\t\x894\xa4\xc3\xbd\xc8\t\x92\xa1\xfd\xa1\n\xf8L&\xd3\xb4a\xc3\x86\
\x15\x0b\x16,x\x19\xc8r\x04r9b\x02\xb9\\nH\x9c\x1e\x9eF\x93f3\xff\xd1\xfe/\
\x0c\x0e\xa4K1:\x05\xf4C\xb8\x10\xe5\xcc\x0bN\xab\xa6\xd1\xca(\x16\x8b};w\
\xee\\5\x7f\xfe\xfcG:::\x068\n\xb9\x1c)\x01\x9d\xcb\xe5\xaa\x16\x16\xb2Lj\
\xc3\x0e\x96\xadx\xb5\xf8\x04\xbf\xec~\x88\xc0\xf0\xc1\x05]\xee[\\t\xd2L\xee\
\xbal%\'\x95\xdb"\xbe\xef\xfb\x86a\x88\xce\xce\xce\xa7\x1fx\xe0\x81\xef\xaf[\
\xb7n/e\xe7?V\xe0\x1f\x86\x00\xfd\xfd\xfd\xc3\xe2t\x97\xbd\x8dGS\xcb?\xd0\
\x16\t{an\xfb\xdcw\xf8\xe6\xb4k\x86~4\xf4\xf2\xd6\xad[\xd7\n!:\x16.\\\xb8\
\x05\xc8\x95\x81\x1f\xb5\\\x8e\x98\x80\xe7y\xd5\'\xb0a\xf0\x15\xee\xde\xfd\
\xcf\xa8|P\x05nd\r\xbe^7\x97{\xe6\xdd\x894JoU(\x14vm\xde\xbc\xf9\xb6y\xf3\
\xe6\xfd\x9a\x92\xc6\x03J\x9b\xa1>^U\xff\xd0\x04\xcaC\x03\xa23\xb3\x17\x95\
\x0cJm\x91<\x9c\x15\x9a\xc2\xe3\xf3\x1ec\\\xa2\x0e\x80 \x08\x06w\xed\xda\xb5\
\xfa\xba\xeb\xae\xbb\xbf\xa9\xa9\xa9\x8f\xe3\xa4\xf1\xc3\x8d\xc3\xa6\xd1J\
\x9c\x0e\xf9\x16"\x05\xa3\xf4\t\xac\x9c}\'W\x9cYm\x8b\xe8\xce\xce\xce\xe7\
\x9f|\xf2\xc9\xef\xdcw\xdf}-\x1c\x83%\x1e\xcd\xf8\xb0\xe7\x01&\x86\xc6\xb3f\
\xe6Z\xbe1\xe5+\xd5\xbfe2\x99\xedo\xbc\xf1\xc6\x8a\xc6\xc6\xc6W)\xcb\xe5xk\
\xfcp\xe3\xb0q\xba\x0c\xc8\xbc\xf2\xb4K\xaa/\x16\x8b\xc5\xd4{\xef\xbd\xb7\
\xb2\xa1\xa1\xe1\xf1\xc1\xc1\xc1\x01J\xad\x8f\x8f\\.\x07\x1b\x87\x93\x90bH\
\x1a\xd5Z\xfb\xfb\xf6\xed\xfb\xc9\xea\xd5\xab\x7f\xf0\xf4\xd3O\xef\xe78[\xe2\
\xd1\x8c\x91\x08(J\xd6\xa7\x00\xfa\xfa\xfa\xfe\xf8\xd2K/-_\xb2d\xc9&>"K<\xaa\
1\xc2\xb7GL \xd1\xd2\xd2\xf2\xe7\x17_|\xb1\x11\xa8\xa1\xf49\x98\xc1\x08\xdf\
\x1e\xf9\xb8\xe7\xe1\xbe\xfeb544\xc4\xcb\xc0\xcdO\x13\xf0\xca\xfc\x7f\x14M|\
\'\xf7n\xc13\x00\x00\x00\x00IEND\xaeB`\x82{Ik\xde'
