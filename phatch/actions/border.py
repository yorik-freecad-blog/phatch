# Phatch - Photo Batch Processor
# Copyright (C) 2007-2008 www.stani.be
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
#
# Phatch recommends SPE (http://pythonide.stani.be) for editing python files.

# Embedded icon is taken from www.openclipart.org (public domain)

# Follows PEP8

from core import models
from lib.reverse_translation import _t
from lib.imtools import has_transparency, has_alpha, get_alpha, \
    convert_safe_mode, paste

#---PIL


def init():
    global Image, ImageDraw
    import Image
    import ImageDraw

OPTIONS = [_t('Equal for all sides'), _t('Different for each side')]


def border(image, method, border_width=0, left=0, right=0, top=0, bottom=0,
        color=0, opacity=100):
    """

    """
    #set up sizes, and make the target img
    if method == OPTIONS[0]:
        left, right, top, bottom = (border_width, ) * 4
    else:
        left, right, top, bottom = [x for x in (left, right, top, bottom)]

    #new image size attributes could get really messed up by negatives...
    new_width = sum([x for x in (image.size[0], left, right) if x >= 0])
    new_height = sum([x for x in (image.size[1], top, bottom) if x >= 0])

    # only need to do conversions when preserving transparency, or when
    # dealing with transparent overlays
    negative = [x for x in (left, right, top, bottom) if x < 0]
    if (negative and (opacity < 100)) or has_transparency(image):
        new_image = Image.new('RGBA', (new_width, new_height), color)
    else:
        new_image = Image.new('RGB', (new_width, new_height), color)

    # now for the masking component. The size of the mask needs to be the size
    # of the original image, and totally opaque. then we will have draw in
    # negative border values with an opacity scaled appropriately.
    # NOTE: the technique here is that rotating the image allows me to do
    # this with one simple draw operation, no need to add and subtract and
    # otherwise introduce geometry errors
    if negative:
        #draw transparent overlays
        mask = Image.new('L', image.size, 255)
        drawcolor = int(255 - (opacity / 100.0 * 255))
        for val in left, top, right, bottom:
            if val < 0:
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rectangle((0, 0, abs(val), max(mask.size)),
                    drawcolor)
                del mask_draw
            mask = mask.rotate(90)
    else:
        mask = None

    # negative paste position values mess with the result.
    left = max(left, 0)
    top = max(top, 0)
    paste(new_image, image, (left, top), mask)

    return new_image

#---Phatch
CHOICES = ['-25', '-10', '-5', '-1', '0', '1', '5', '10', '25']


class Action(models.Action):
    label = _t('Border')
    author = 'Erich'
    email = 'sophacles@gmail.com'
    init = staticmethod(init)
    pil = staticmethod(border)
    version = '0.2'
    tags = [_t('filter')]
    __doc__ = _t('Draw border inside or outside')

    def interface(self, fields):
        fields[_t('Method')] = self.ChoiceField(OPTIONS[0], choices=OPTIONS)
        fields[_t('Border Width')] = self.PixelField('1px', choices=CHOICES)
        fields[_t('Left')] = self.PixelField('0px', choices=CHOICES)
        fields[_t('Right')] = self.PixelField('0px', choices=CHOICES)
        fields[_t('Top')] = self.PixelField('0px', choices=CHOICES)
        fields[_t('Bottom')] = self.PixelField('0px', choices=CHOICES)
        fields[_t('Color')] = self.ColorField('#000000')
        fields[_t('Opacity')] = self.SliderField(100, 1, 100)

    def values(self, info):
        #pixel fields
        width, height = info['size']
        # pass absolute reference for relative pixel values such as %
        return super(Action, self).values(info, pixel_fields={
            'Border Width': (width + height) / 2,
            'Left': width,
            'Right': width,
            'Top': height,
            'Bottom': height,
        })

    def get_relevant_field_labels(self):
        """If this method is present, Phatch will only show relevant
        fields.
        :returns: list of the field labels which are relevant
        :rtype: list of strings
        .. note::
            It is very important that the list of labels has EXACTLY
            the same order as defined in the interface method.
        """
        relevant = ['Method', 'Color', 'Opacity']
        if self.get_field_string('Method') == OPTIONS[0]:
            relevant.append('Border Width')
        else:
            relevant.extend(['Left', 'Right', 'Top', 'Bottom'])
        return relevant

    icon = \
'x\xda\x01x\x0b\x87\xf4\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\
\x00\x000\x08\x06\x00\x00\x00W\x02\xf9\x87\x00\x00\x00\x04sBIT\x08\x08\x08\
\x08|\x08d\x88\x00\x00\x0b/IDATh\x81\xd5Z{P\\\xd5\x1d\xfe\xce9\xf7\xb1\xcb\
\x1bj\x08\x8f4\x04\xa3`\x001I\x8d\x9aJ\xb5Uk\xd5\x8c3\xa6\x13m,31jm\x93\xb1\
\x86\xc4\x88\x99j\x0c:&\x8e\xd5i\x8d\xd5\xa0I\xad\xedt\xaaf$\xea\xb4jLL5\xc4\
(I\xb4\n\x02\x01B\x80\x04X\x96\xc0\x02\xbb\xc0\xb2\xaf\xbb\xf7\x9c\xfe\xb1\
\x0f\x96}\x10\x12H;\xfef\xee\xb0\xb3\xf7\x9es\xbf\xef\xfc\xbe\xdf\xe3\x9c\
\x85\x08!\xf0]6\xfa\xff\x060]\xfb\xce\x13\x90.\xf4\x0b\x08!$\xf0\xd1\xffW\
\x00\x80\x98!\xed\x92\x0b\x11\x03a\xa0i\xc8\x05\xf8\x08\xe8\x00\xf4\x99 1\
\xa3\x04\xfc\xc0\x03\x17\x03 \x87\\\xd2\xaaU\xab2\n\n\n\xf2\x93\x93\x933\xd7\
\xae]\xfb\x12\xceB\xe2\xb3m\xa5\xd7\t\xce+N\xf5Z\x9e\\]\xf9\xef\xc3\xd1\x9e\
\x991\t\xf9\xc1S\xff\x9c\n\x00\x03\x00\xe3\xfd\xf7\xdf\xbf\xb8\xa8\xa8\xe8\
\xe7\xa9\xa9\xa9\xb70\xc6f\t!\xa0i\xda\xc7\x00v\xc0\xe7\x89H\xe0[W\xe5\nx\
\x9f\x1b\xb4\x8e\xac\xe8\xe8\xee\x81\xd1\xa0\xd6\x03\xb80\x04B\x803?p#\x80\
\x84\xf2\xf2\xf2\xdb\x8a\x8a\x8a\xca\x0c\x06\xc3\xa5B\x08\x84^6\x9b\xed(\xc6\
c"h\xd5O\xdd\x95@\x98\xf4\x98\xc3\xe1\xde\xd8\xdemR\xeccNp\x08\xa8\\\x8eJtZ\
\x04B\xe4\x12\x90\x8a\x11@Bii\xe9\xe2\x1bo\xfb\xd1\xd6\xd4\xb8\xd9\x05\x9cs\
\x84\x83\xe7\x9cc``\xa0&|\xb6C[\xef^\xads<{\xba\xdb\x94\xde;0\x04\x08\x81\
\x85\x0b\xf2\xd0z\xaa\x0b\x02\xd0f\x8c@\x08p\xea\x07\xae\x02H())\x99\xb7\xea\
\xbe\xd2M\x99\xe9s\x96A\xf8b\x8b\x10\x12A\x00\x80c\xe7\xce\x9d\xb5\x008\x00T\
o\xfbe\x89\x10+_\xec=cY\xdci\xee\x83\xae\x8f/6\xa3>\'q.f\xc6\x03Qt\x1e\x9f\
\x96\x96\x96VQQ\xf1\xeb\xf9y\xb9k$\xa2\xa8\xa1+M\x08\x81[\x17h\xb3\x0b\\\x96\
\xe8\xfb\xce\xedv\xb7\xf7\xf5\xf5\xb9w\x97\xdf173)\xfe\x99A\xab\xed\xae\x8en\
3\x9c.w\xcc\xf7r\xc1\xbd\xd3"\x10&\x97\x80\xce\x13\x1fy\xe4\x91\x1b\xae\xfbI\
\xc9S\xf1\x86\xc4\xecp\x99\xb8t\xa0vPG\x83\x95\xe3\xe2D\x8a\xc2\x14\nB\x08\
\xa0{N\xef\xdf\xf2\x8b\xc7\xb9\xe6YW\x7f\xa2M\xb5\x8d\x8cFy!\xfc\xd5\xc2g\
\x82\x8b\xf3#\x10\x92\xcf\x99\xffY\x03\x80\x84\xeb\xaf\xbf>\xf7\xc1\xdf\xae\
\xd9\x9c\x91\x91}\xb3\xe0\x13%\xe2\xd08\x8e\xf4ih\x18\xd2\xe0\xe5\x80\xcc(\
\xf2R$P*\xa0XO\xc1\xd8q\xf4\x86.s\xef\xed\xbd\x96A 2\x83\x1e-\xce\xbfD9\xdev\
jq\xa8\x94\xf4\xf3\x91PXvQ\x01\xc4\xa9\xaa\x9a\xb2}\xfb\xf6UE\xc5\x05\x1b$\
\xaa\x189\xe7\x10d\x1c\xfc\xb7\x16\x17\xaaMN8\xbd\x02\x12%\x88S\x18\x14\x89!\
\x97\x0cBn9\x86\xdeS-\xe8\xea9\x13\xef\xd5#\xf0\xf4\x12!6=\xfe~\xf3?>{z\xe1\
\xc1\xf0\x9b\x82\x9eC\x10\xc7\xc8.\x89eeeKn_\xbelkJBZ^\x00p H\xfb\xc74\xec\
\xed\x18E\xf7\xa8\x06F\t\x8c\x8a\x04UbH%.\xfc\xd0q\x14c5u\xe8\xe8\xee\x89\
\xd0\xb9\x00<\x10\xf8#7\x90m\x15o\x1f\xb7\x03\x00\xb6\x96\x86\x80\xf1\x15o\
\xa1O\xd1\x03!\xe0\x83rY\xb4hQ\xd6\x93On)\xcf\x99\x97\xbb\x02\x024T\xe7\x1a\
\x07\xaa\xbbFp\xa4\xc7\x0e\x80\xc0 KP%\x8a8I`\x91\xb3\x01\xb9\xfd\xff\xc1\
\xa9\xaeNt\x0cG\xd19\xf0/B\xe9\xc3\x9b\xdfkh\x8f\x05\x8e2\x02\x10\x02\xae\
\xebS\x8e\x81\x00\xf8x\x00)\x95\x95\x95+\xae^\xba\xe4q\x83\x12\x97\x1c\x9e\
\x0e[\x06\x9d\xf8\xa0\xd5\x8aa\xb7\x17\xaa\xe4\x93\x8a*1\xe4{N\xa3\xf8\xcc\
\x11\xf4uu\xa0\xd62\x10!s.\xd0\xaeib\xdd\xd6}\xcd\x1fEo#\xc6\x1bd\xe2\xf7\
\x00\x07\xceN D\xf3\xea\xca\x95+\xe7m\xd8\xb0\xbe2-\xed{\xd7\x84\x17\xa3!\
\x87\x07\xef5\xf5\xa3\xd9\xe2\x80*1$\xa8\nT\x89!K\x0c\xe2*\xebQ\xb8\xba\x9b\
\xd1`>\x03\xafw\xa2\xd7\x89\xa4@\x99\xb7\x18\xfb\xbfl\xbd\xed\x93\xcf?\xef\
\x88\x05\x882\x02\xe2/\xd2\x94\xfa%\xc4y\xcc~)\xdc\x03\x14\x80\xb2t\xe9\xd2\
\xe2\xf4\xf4\xd9\xd7\x04r\xb9\x10\x02^\x9d\xe3`\xc7 >>i\x01!\x04\t\x06\x19\
\xaa\xc4\x90B\\Xb\xff\x1aI=\xb5h3\xf5\xc0\xe9\x0c\xcf\xe7\x04Rf\x1e\x0c\xf3\
\xafBjz&\xe4&\xb3\'\x16\x18\x00\xa0\x84\x85\x0c\xa5 \xc4W\xf0\xa6B \xa8\x7f\
\x87\xc3!3\xc6\x82\xe0\xdb\x07\xecx\xa3\xd6\x84!\x87\x06U\x92\xa0H\x0c\x8a\
\xcc\x90\xc1\xad\xb8\xb6s\x0fNuv\xa23\x8a\xcem\x89\xf1\x18\x9a_\x88k\xe7\x96\
 ##\x03)))HKK\x9b\xb4\xfd%l\\B\x94R\x9c\xadW\x8e\x16\x03\x84s\x0eJi\x90\xc0\
\x17\x9dV\xd8=\x1c\t\x06\x05\xaaD}\x04$\x86\x14\xb7\x06\x8b\xa5\x1f\xd60\xf0\
#\x92\x86}\xb3\xfa\xd1\x10?\x82\x92\xd4\x8b\xf0@A\x01dY\x06!\x04\x06\x83\x81\
!J#\x17\x04@Bb\x80\x12@\x90){ 8\xce\xeb\xf5\n\xdfd\x04\x84\x10\xc4\xab2\x12T\
\x19\x8a\xec\x0bT\x85Q\xc8\x94\x809#\xd3\xf3\xb1\xe4!\xecO\xb6@S\x05\xa0\x12\
\xb8\x88\x03\xf1\xf1\xf1\xc1\xcc\x95\x9f\x9f\x7f\x11\x00S,@\x94\x85\x061\x8b\
\xf5\xd8\xf8\xf3!\x9fE\xe0\xd2u}\x02k\x83,!\xc1\xa0 A\x95\x11/3(\xd0\xe1\xb6\
\xf6\xc1>\xd0\x1b1\xe1q\xd5\x0e\xcd |3\r\x03\xd6\xde~0\xc6@)\x05c\x0c\xd9\
\xd9\xd9\xd9\x98\xc4\x03\x94\xb0\xe0]B\t@&WQ\xd4J\x1c\xf0@\xc0\x8c\x8a\x84\
\x04U\x02\x83\x80\xc7n\xc3\xd8`?\xb8\xe6F\x8f\xab\x1a9\x11\x08\x00\x8c\x02p\
\x01\x8aPp\xeb\xe2e\x08\x8d\xa7\xd4\xd4\xd4\xac\xc9\x00Q6\xbe\xea\x94R@\x9c\
\x07\x01`b\xe4\x1b$\x06\x85\xe8\xb0\x9a;\xa19\xec\xd0\x85\x13{Gw!K\x8c\x02\
\xc8\x9b8r6\x00\'p\xdd\x9c\x1bQq\xcbf\xccM\xc9\x9aP\xb5SRR2\x80\xd8\xa0\xc6k\
i \x1e&\xdf\xf3F%\x10.!\xa3D\xa1B\xc0\xe9\xb2\xe0\x1b\xf7>|\xeb<\x04\xaf\xd0\
\x90\x15\x17\xb9\x98\x92K\xc6\xc6\xab\x1f\xc5CK\xd6 \xbc\xb5\x1e\x19\x19\xf9\
\xb0\xa9\xa9\xe9\xcd\xf0\x05\x9a@ \xc4\x03\x84R\x08B\xce\x9d@x\x854(\x0c}\
\xb4\x19\xbbG\xb6a\xd4i\xf5\xbd>\x91\xf8\xeau\x98\xfd\xed\xe6\xd7\x91\xb3`\
\xc9\x84\xe2\xe7r\xb9\xdakkk7\x97\x96\x96\xee\x03\xe0\x00\xc0cm\xe6)\x99X\
\x89\xc9$\xde\x8aE "\x88\x0f\xdb?\xc2\xcb\xe6M\xd0\xed^\xc0\x03\x1f\x01\x05@\
\x94=\x88*\xa9\xfe\x97\x13p\xce\xedmmm\xdb\xef\xb9\xe7\x9eWM&\xd3\x88\x7f\
\x84\x171@5U=\xa5\x80\xd1\xe4 \x19J\xce/\x06\xbc^\xef\x04\x02-\xc3\xb5\xd0\
\xed:\xe0\x84\x8f\x80\x00 \x03\xaa\xa4\xc4\x9a\x97\xf7\xf7\xf7\xbf[YY\xf9\
\xf4k\xaf\xbd\xd6\xe5\x07\xae\xc1\x7f\n\x11m\xf5\xebv\x95/\x93\x08^0\x9b\xcd\
\x97\x06z7B\x19\xc4\xf9d!\x84iT\xf1\xca\x80\x1dA\x02D\xa7\xb8)\xf7fl\xffi\
\x19\xbe\xfa\xfb\xb3\x13\x06\x8e\x0e\xdb\xda\xbfz\xff\xfd\xf5k\xd7\xae=:>\
\x02\xba\x1fw\x04\x98\xfaW\xd6\xe7\x13&\xbd`\x1f\x19\xbd\xb5\xfex\x13\x86\
\x86\x86\x82\xf7\x08\xa1g=\xb8\x8aJ@\xd3\xb4\t\x83\x14M\x02\xec\x00qRd\xcbs\
\xb0\xf1\xc7\x1b\xf0\x83\xc2\xc5\xa0\xc4\x151\xb6\xea\xc5\x8aG+\x0f\x9e<\xe4\
\x07\xeeE\x0c\xbd\x1f{i]\x92QV\xb6xt\xb1\xae\xb9\xa9Q\xee\xec\xee\x0e\n\xcbh\
4\xa2\xb8\xf8r\xe8\x9c\xc3\xa3y&\xdd5N)\x06\x14]\xc6\x95i\xd7`E\xferd\xc4\
\xcd\x82$\xc5\x9e3\xc9\xc0\x02\xbe\xe2\x88\xba\xea\x84|\xfb\xea\xfa{\r\x8a\
\xf4L\xfb\xe9\xd3\xb3[O\x9e\x84\xa6\xf9$\xc3\x18C~\xde\xa5\xc8\xc9\x99\x87\
\xe3\xc7\x1b\x9d]\xdd&\x83 \xf8\x90K\xd2\x07S% \x80\xc8\x18\xf8\xcd\xa2\xfb\
\xa0\x16Ihll\x84\xa6i\xc1\x16c\xd46\xd4D\x08\nB\x9f5\xcaLC\x8c#\xc3\xda\x9d\
\x1b\x962l\xf8\x93e`\xf0\xca\xc6\xe6\x16\xd8\xed\xf6\xe0\xbd9s\xe6\xa0\xb0\
\xa8\x00\xdd]&\xbeo\xff\x01\x0e\xf0\x93B\xf0uO\xfc\xb3\xf9P\xcc\xd5\x8aB\xc0\
\xc7B\x88\t\x042\x12f\xc1j\xb5\xfa\x06H\x128\xe7\xfd555\xcf\xcd2\x1d23B\xdf\
\x0c}\x96R\x12\xb1\xea\xb5/?\x94E\x98\xfc{\xa7\xd3Yz\xbc\xf9\x04\xe9\xeb\xef\
\x0f\xdeKMI\xc1\x15\x0b\x8b\xe1t8Q}\xf0\x90\xdb\xa3y\xc68\xf8&\xbe\xa8\xf9\
\xf5\x8a\n1i#\x17\x8b\x80\xd0\xf5\xc8]7!\x04\x92$y\xccf\xf3\xee\x1d;v<\xd7\
\xd6\xd6f\xde\xbb\xe5\xee\x92\x01K\xec\xf3\x9c\xb6\x97\xd6\xa9v\x89<\xcc\x81\
\xcd\'[[\xe3:Nw\x82s\x1f&\x83\xc1\x80\xa2\xc2B$&%\xa2\xae\xaeN\xb3Y\x87\t\
\x07^\xe4\x9a{[\xc5\xde\x93#g\x03\x1e\x8b\x80\x00\xc0\x19c\x13P\x11B`\xb7\
\xdb\xf7WUU=\xbfg\xcf\x9eF\xf8\xba\x1d-)N\xf6\x0e\x90\xe8}Y\xdd\xcb\x0f\xdd\
\x01\xc6\xfe`\xea\xe9\xbd\xb8\xb9\xb5\x15n\xb7o\x1fC)E\xde%\x97 \'g.\x9aZZ\
\xc4W_\x7fM\x18c\x1f\x0bJ\xca\x9e\x98d\x7f|.\x04\xbcF\xa3q,\xf0\x85\xc3\xe18\
QSS\xb3e\xf5\xea\xd5\xd5\xf0U\xd1@v\x11\x94\xca\x82\x84\x11\xc8L\xbf(\xa7\
\xb6\xb2\xec\xc0\xf0\xa8\xfd\xa6\xc6\x96\x16\xd8l\xe3\x8b\x99\x9d\x95\x85\
\x82\x05\x97\xc1d6\xe3\xc0\'\x9frBH\x9b\x00Y\xf3\xd8\xbb\xf5\x11G)\xe7L@\x08\
!\x88\xaf\xef\xf0\xcc\x9e={\x84sn\xed\xea\xeaz~\xf9\xf2\xe5\x7f\xb5X,\x0e\
\x8cW\xd1`Z<\xf2\xc2\x1a\x84\x13\xc8HO\xffK]c\x13\xeb1\x9b\x83i199\tW\x14\
\x17\xc3\xe5t\xe2pM\r\xd7<\xda\x18\x17\xa4\\_\xd8\xf0\xe7\xa9\xe8|J\x04\xfc\
\xc6\x01h&\x93\xc9TUUu\xc5\xc6\x8d\x1b\x87\xe0+B^DI\x8b\x12\xfc={\x88\xd564\
\xb2\x00pUUQ\xb0 \x1f\xc9I\xc9\xa8oh\x106\xdb\x08\xa7\x12{\x85Jc\x9b\x7f\xf7\
v\xfb\xf0t\x80G%\xe0\xf7\x82\xbek\xd7\xaeQ\xf8j/\xe0\xdf\xe4Dm\xbe\x18\x03\
\xc2c@\xf8t>\xff\xe2\\\xe4\xcc\xfd>N\xb4\xb6\xa1\xb6\xae\x1e\xaa\xa2|\xa6\t\
\xf1\xab\x8a=um3\x01<*\x81\x00\t\x00"p.:\xd9O@LB\x84\x84233\xb0 ?\x1f\xe6\
\xde^\x1c\xac>,\xa8\xcc\xcc\x94\x89{\xcb\xabj\x0f\xcc$\xf0\x80\xc5,\xa9S\xfb\
\x01N\n\x9e\xe1$%&\xe2\xf2\xa2\x02\xb8\xdcn\x1c9z\x0c\x9a\xd7\xebb\x92\xb49\
\x17\xb5\xdb\xef|7\xf6\xd1\xe0tmZ?1I\xfe\xadbZj*\n\x0b.CcS3l\xd6a\x11\x17\
\x17\xf7\x96\x9b\xf3\x07+\xde\xf9\xc66S@cb\x98\xf6\x0c\x84\xc062\x82\xc3_\
\x1cABB\\\xbd\xacz\xef\xda\xf0\xd6\x97\'f\x00\xdb\x94lZ\x04\x18U\x04!D(\x8al\
\x93i\xe2\x03eo|\xf1\xceL\x01\x9b\xaaM\x8b@\xa1\xd9x\xa0\x89\x91\x9f\xe5\xf0\
o>\xbds\xf7\x85\xd3\xf9dvA~\xa9\xff_\xdaw\xfe\x9f=\xfe\x0b\xab\xec\x8a\xbc\
\x9biK\x93\x00\x00\x00\x00IEND\xaeB`\x82\xcd@\x83\xfb'
