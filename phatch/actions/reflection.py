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
from lib.imtools import has_alpha, has_transparency, paste

#---Pil


def init():
    global Image, ImageColor, ImageFilter
    from PIL import Image
    from PIL import ImageColor
    from PIL import ImageFilter
    global HTMLColorToRGBA
    from lib.colors import HTMLColorToRGBA

REFLECT_ID = 'reflect_w%s_h%s_o%s'


def gradient_vector(size, opacity, cache):
    id = REFLECT_ID % (1, size, opacity)
    try:
        return cache[id]
    except KeyError:
        pass
    opacity = float(opacity)
    grad = Image.new('L', (1, size))
    data = [int(opacity * x / size) for x in range(size, 0, -1)]
    grad.putdata(data)
    cache[id] = grad
    return grad


def gradient_mask(size, opacity, cache):
    id = REFLECT_ID % (size[0], size[1], opacity)
    try:
        return cache[id]
    except KeyError:
        pass
    #gradient vector
    vector = gradient_vector(size[1], opacity, cache)
    #scale vector
    grad = cache[id] = vector.resize(size, Image.LINEAR)
    return grad


def reflect(image, depth, opacity, background_color, background_opacity,
        scale_method, gap=0, scale_reflection=False,
        blur_reflection=False, cache=None):
    if has_transparency(image):
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')
    if cache is None:
        cache = {}
    opacity = (255 * opacity) / 100
    background_opacity = (255 * background_opacity) / 100
    scale_method = getattr(Image, scale_method)
    if background_opacity == 255:
        mode = 'RGB'
        color = background_color
    else:
        mode = 'RGBA'
        color = HTMLColorToRGBA(background_color, background_opacity)
    width, height = image.size
    depth = min(height, depth)
    #make reflection
    if has_alpha(image) and background_opacity > 0:
        reflection = Image.new(mode, image.size, color)
        paste(reflection, image, (0, 0), image)
    else:
        reflection = image
    reflection = reflection.transpose(Image.FLIP_TOP_BOTTOM)
    if scale_reflection:
        reflection = reflection.resize((width, depth), scale_method)
    else:
        reflection = reflection.crop((0, 0, width, depth))
    if blur_reflection:
        reflection = reflection.filter(ImageFilter.BLUR)
    mask = gradient_mask((width, depth), opacity, cache)
    #composite
    total_size = (width, height + gap + depth)
    total = Image.new(mode, total_size, color)
    paste(total, image, (0, 0), image)
    paste(total, reflection, (0, height + gap), mask)
    return total

#---Phatch


class Action(models.Action):
    """Drops a reflection"""

    label = _t('Reflection')
    author = 'Stani'
    email = 'spe.stani.be@gmail.com'
    cache = True
    init = staticmethod(init)
    pil = staticmethod(reflect)
    version = '0.1'
    tags = [_t('filter')]
    __doc__ = _t('Drops a reflection')

    def interface(self, fields):
        fields[_t('Depth')] = self.PixelField('10%',
            choices=self.PIXELS[:-1])
        fields[_t('Gap')] = self.PixelField('0',
            choices=['0', '1', '2', '5'])
        fields[_t('Opacity')] = self.SliderField(60, 0, 100)
        fields[_t('Blur Reflection')] = self.BooleanField(False)
        fields[_t('Scale Reflection')] = self.BooleanField(False)
        fields[_t('Scale Method')] = self.ImageResampleField('antialias')
        fields[_t('Background Color')] = self.ColorField('#FFFFFF')
        fields[_t('Background Opacity')] = self.SliderField(90, 0, 100)

    def get_relevant_field_labels(self):
        """If this method is present, Phatch will only show relevant
        fields.

        :returns: list of the field labels which are relevant
        :rtype: list of strings

        .. note::

            It is very important that the list of labels has EXACTLY
            the same order as defined in the interface method.
        """
        relevant = ['Depth', 'Gap', 'Opacity', 'Blur Reflection',
            'Scale Reflection']
        if self.get_field_string('Scale Reflection') in ('yes', 'true'):
            relevant.append('Scale Method')
        relevant.extend(['Background Color', 'Background Opacity'])
        return relevant

    def values(self, info):
        #pixel fields
        y = info['height']
        return super(Action, self).values(info,
            pixel_fields={'Depth': y, 'Gap': y})

    icon = \
'x\xda\x01y\n\x86\xf5\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\
\x00\x000\x08\x06\x00\x00\x00W\x02\xf9\x87\x00\x00\x00\x04sBIT\x08\x08\x08\
\x08|\x08d\x88\x00\x00\n0IDATh\x81\xd5\x9aYl\\\xd5\x19\xc7\xff\xdf9\xe7\xde;\
\xf6,^\xc6\x1e\xc7qX\x9c\x18\x02\t1\x01+1\x9b l\x0f\xa5P\nR%\xaa*}\xeb&\xaa\
\xb6*\xa8Bj\xd5\xd0\x87\x8a.\x0f-m%*\x84TU\xa8E\x02\xb5\xaa\xaaJmi\x84\x02(\
\xc4q\x02v\xec\xe0I\x1d\x87\xd8q\xec$\x8e\x1d\xcf\x8cg\xee\x9d\xbb\x9c\xf3\
\xf5a\xc6\x03\xa9\xda\x12\xaf\xa8\x9ft5\x0f3:\xf7\xf7\xfb\xce\xf6\xdd{\x86\
\x98\x19\xff\xcf!>\xa9\x1b\x8f\x8d\x8d9\xab\xd1\xce\xba\x0b\xbc\xf6\xdak\xf2\
\xe8\xd1\xa3\xdf\x9a\x99\x99yy5\xda[W\x81\xa1\xa1\xa1\xde\xce\xce\xce\xa3a\
\x18\xfe,\x8a\xa2\x14\x00\xd1\xd7\xd7w\xedJ\xdaT\xab\x83\xf6\xbfcxx\xb8\t\
\xc0sa\x18~)\x08\x02122\x82D"\xd1z\xf8\xf0\xe1w\xa2(\xfa\x1b\x80g\x97\xdb\
\xf6\x9a\xf7\xc0\xf1\xe3\xc7\xf7\x028\x11\x86\xe1W\xa6\xa6\xa6\xc4\xeb\xaf\
\xbf\x0e\xdb\xb6\xb1y\xf3\xe6[\xc20\xec\xcd\xe7\xf3+J\xe2\x9a\xf5\xc0\xf0\
\xf0\xf0\rB\x88\x17\x00\xec\xc9\xe7\xf3\xe8\xef\xef\x07\x11\xe1\xc1\x07\x1f\
\x84m\xdb8{\xf6,\x1d9r\x04\xe9t:\x15\x8f\xc7\xd5\xc4\xc4D\xaf\x10"\xbfw\xef\
\xde\xe3K\xb9\xcf\xaa\x0b\x1c:t\xa8\xae\xa1\xa1\xe1{B\x88\xa7\xb5\xd6\xf6\
\xb1c\xc7p\xea\xd4)\xf4\xf4\xee\xc4\xd5\x1b;\x91\xcf\xe7\xf1\xe6\x9bobjj\nMM\
MH\xa7\xd3\x0fMMM}Q\x08\xd1\xa0\xb5\xbe}\xa9\xf7\xa3\xd5\xdc\x07\xb2\xd9\xec\
C\xcc\xfc+f\xee\x9c\x9e\x9eF__\x1f:\xae\xde\x88\x9e[z\xc0\x06\x18\x1c\x1c\
\xc4\x89\x13\'\xd0\xde\x91AG\xfb\xd5\x00\x00c\x0c\x8c1`\xe6b{{{\xd3\x9e={\
\xa2\xa5\xdcsUz`hhh\x93\x94\xf2y\x00\x8f{\x9e\x87\xfe\xfe~\xb8\xae\x8b{\xee\
\xbb\x0b\xe9\xc6\x0c&&&\xd0\xdf\xdf\x8fTc\x1c\xbbo\xdb\x05K\xda5p!\xc4\xa2\
\xc0\xc1\xa5\xc2\xafX\xe0\xc0\x81\x03*\x93\xc9|CJ\xf9\x03fNd\xb3Yd\xb3Y\xdc\
\xb4\xf3Fl\xdd\xb2\r\xc5b\x11\xfb\xf7\xefG\x10\xf8\xb8\xf9\xd6\x1d\xa8w\x12`\
f\x18c\x00\x12\x18+i$\x15\x90\xb1\r\x98yx9\x0c\xcb\x16\x18\x1e\x1e\xbe\xbd\
\xb5\xb5\xf5\xd7\xcc\xdc=;;\x8b\xbe\xbe>4\xa7\x1b\xf1\xd0\xc3\x9f\x82c\xc50<\
<\x8c\xb1\xb11\\w\xc3f\xb4\xb5l\xac\x81G\x86\x91\xcd\x058:\xabQ\x08\x18_\xd8\
\xac\xa0\x94\x801ft\xdd\x04FFF\xbe/\x84x\xd6\xf7}z\xef\xbd\xf7077\x87\x9e\
\xde\x9dho\xdd\x84\x0b\x17.\xe0\xf0\xe1\xfdh\xdb\xd0\x8a=\xf7\xde\x03Arq\x88\
`l\xde\xc7?&=\xe4}\x03\xc7\x92hK*\xa4\xeb\x08\xcc\x0cf^?\x01cL\xef\xf8\xf88\
\r\x0c\x0c\xe0\xba\x1b\xb7\xa0\xf7\xb6^\x04~\x80\xb7\xdf~\x1b\xae\xeb\xa2\
\xf7\x8e]hH4\xd5\xc0s\xe5\x10\x7f\xff\xa0\x88\x13\x97|\xd8J\xa2\xa1\xceF\xcc\
V\xe8L*(e\x16\xe7\xc3\xfa\t\x10\x91\x1e\x1c\x1c\xc4\x03\x0f\xdc\x8fd2\x85\
\x93\'Obdd\x04;n\xde\x8e\xcek\xb6\\6\xce\xdf\x99,\xe0\x8d\xf1<\x18\x84T\x9d\
\x8d\x98\xa5\x10\xb3\x14\xeal\x89MI\x01\xa54\x8c1H\xa5R\xb3\xeb&\x00\xc0\x10\
\x11l\xc7\xc1\xfe\xfd\xfb\xd1\xdc\xdc\x84\xcf<\xfa\x08l\xcb\xa9e}|\xde\xc5\
\x1fG.\xe2b)B\x9d]\x81\x8e\xd9\nu\x1f\x11h\xaa\x03\x94"\x18c\xe0y^\x02\xc0\
\xfc\x9a\x0b\x10\x11\r\x0f\x0f\x1b"\x02\x98\xe1y\x1e\xee\xbe\xfb\xb35\xf0\
\xa2\x1f\xe2/\xd9\x8b\xe8\x9f\xcc\xc1\xb1\x14\x1a\xe3N\x05\xd8\x92\x97\t\xc4\
l\x05\xdb\xd6\x90\x82!\x84\x80\xe7y\xa95\x17 "\x01@FQDD\x04S\xdd\x04\x95R0\
\xc6`:\xef\xe2\x17o\x7f\x80\xd00\x1a\xea\xab\xe0\x8b\xd9\xb7\x14\x8c\xbd\x80\
S\xf2(\xe6\xc4\x04.x\x1f\xe0\t\xeb\t\xecI\xec\x003C)\x95Z*\xfc\x15\x0b\x10\
\x11\xa1R\xf8\xd9\x00\xea=\xcf\xb3\xaa+\xc7\xe2\xf7\x90R\xa2\x142\xa4\x94\
\x88\xd7U3\xbe\x98i\x8b\xd1/_\xc5\xfe\xe8%x\xb9"\xb0\x00\xa0\x08\xdc\xb5y7T\
\xe3-0\xc6\xc0\xb2\xac\xe4\x9a\x08T\xe1-\x001\x00\x8d\x00\xd2\x85B\xa1\xde\
\x18\x03\xae\x0e\x9b\xc5p,\x89\x86z\xa7\x96\xf5:K\x82m\x0f/\x96\x9f\xc4\x99\
\xb9\x91\x1a8\x16*\xd7\\\xfc\x02\xd4\xf5\x95\xde+\x16\x8b\x8d\xab.P\x85W\x00\
\xe2\x002\x00\xda\x01dr\xb9\\\xbd\xd6\x1a\xcc\x95Zf1,)\xd0\xf8\x11\x01Xe<?\
\xf35L.\x9c\x00\xfc*\xf8\x0c\x809\xa0\xbb\xa3\x07\x8fo\x7f\xa46\xfc\x8c1M\
\xab.\x00`1\xfb\xa9*\xfc\xb5\x00ZJ\xa5R\x8c\x99\x11E!\xa2\xe8\xc3\xf2\xc5\
\x92\x12\x8d\xf5\x0e,\x9b\xf1\xae\xf93^\x9d\xfd)|\xe3UZ0\x00\x12\x80 \x81o\
\xde\xfe\x14\xbe\xbe\xeb\xcb\xb5\xe5Vk]\x9a\x9d\x9d\xbdHD\xc4K\xac.\xafd\x0e\
pU\xc4\xa9\x8a4\xbb\xaek\x1bc\x10\x84\xe1e=\xa0\xa4@96\x8d\x9f\xcf\x7f\x1bS\
\xc5S\x95\xac\x07\xa8|\xfa\xc0\x0ek\'~\xf3\xf8Kh\x8b\xb7\xd6\x8a\xb9l6\xfbN.\
\x97\xfb\xd3\xde\xbd{\x0f,\x15\xfeJ\x04\x18@\x04\xc0\x05P\xa8\xa2\xd8\xae\
\xebZZkDa\x08\xad5\x0c\x1b\x08\x128\xeb\x9f\xc6\x0f\xcf|\x1ee\xcf\xbd\x0c\
\xbe)l\xc6\xf3\xf7?\x8f\xfb\xb6\xdcSk\xf8\xfc\xf9\xf3fvv\xb6\x9c\xc9d\xb6\
\xb4\xb6\xb6\xf6\x02\x08\x97\n\xff\xb1\x02\xcc\xccD\xa4\x01\x94\x00\\\xac^W\
\xfb\xbe/\x8c1\x08\xc3\x08\xb5\xd5\x88\x80B\x90Cy\xeeCx\xe5)|u\xc7\x93xf\xcf\
S\xb56\x17\x16\x16066f\xd2\xe9\xb4\xced2u\x004\x11\x95\x96\x93\xfd\x8f\x15X\
\xf4@\x05\xe9\x12\x80)\x00\x9b\x98Y\x07A\x00\xdf\xf7\xa1\xb5\x06\x1b\x06\x04\
\xe0\xc0\x02r\x80\x0c\x14nO\xdf\x89\x97\xf6\xbe\x80\x84\x93\x00\x00h\xad\x91\
\xcdf\x8d\xe38\xdc\xd6\xd6&\x85\x10\x00\xa0QY\x97\xdc\xe5\xc0_\x91\xc0\xbf\
\xf5\xc29\x00\xe3\xc6\x98\xd2\xc2\xc2\x02\\\xd7\xad\xed\xc0\x00`\xc3\xc2C\
\x1b\x1e\xc5\xbe{\xbf\x8b\x8e\xd4\x86Z\x1b\xe3\xe3\xe3\\,\x16Mss\xb3\x10B\
\x10\x00\x1e\xcd\x9fc\xcdl\xb65u\x14\x85\x10\xder\x05\xae\xe8\xadD\xb5{CT\
\xb6\xfa\xd3\xb1X\xec\x92\xeb\xba\xe7]\xd7\x8d\xb4\xd6\xb5\x89\xbc3\xb3\x1d/\
>\xfa\xcb\x1a\xfc\xfc\xfc<\x0f\x0c\x0cDRJnii\x11RJ\xbe\x18\xe4\xf8\xb9\xa1\
\xdf\xd1w\xde{F\x8e\x15\xa6AD\x0b\x00\x96-\xb0\x94R\x82\x01\x94\x01\x9c;v\
\xec\xd8\xef\x01<\x1dEQ\xa6*x\xd9\x0f\x83 @6\x9b\x8dR\xa9\x14\xda\xdb\xdb%\
\x111\x83\xf9\'\xa7~KCt\x84J\x85\x05(G@)\xa9\x89(d\xe6\xf2\x9a\x0bT\x87R\x04\
\xa0\xf0\xd8c\x8f\xb5LNN&\xb5\xd6\xfe\xd4\xd4\x94\x88\xa2\xa8\xf6\x9estt\xd4\
h\xadu&\x93\x91D\x04"2\x7f\xbdp\x88^\xc9\xbd*\xb8.\x82\x84D\xb21\t!\x04b\x8e\
\x1d\x12\x91\x16B\xe85\x17\xf8\x88Dx\xd5UW\x95\x8c1\xb9B\xa1P_*\x95R\xcc\x8c\
\x99\x99\x19\x9e\x9e\x9e\x0e[ZZ\xa4eY\x12\x00Ox\x17\xf8\xc7g^P9k\x06*\xae\
\xa0l\x0b\x8eoA6\x088\x94@\xab\xd3\x1a\x10\x11\x03h[\x17\x81E\x89\x81\x81\
\x81\xc8\xb2\xacbKK\x8b\xe9\xea\xea\nGGGu:\x9d\xa6\r\x1b6(\x00\x1c\x91\xd1?:\
\xfd\x92\x1a\t\x06\x89l\x82e[\x90\x8eBR&\x10\xb3\xea\xb0!\xd8n:\xbd\xbb#\xdb\
\xa4B!\x043\xb3s\xf0\xe0\xc1\xe4\x9dw\xde\xb9\xb0\xe6\x02@\xe5\x89L\x08Qjnn.\
\xef\xde\xbd\xdb\xea\xe8\xe8\x88\x13\x11\x0b!\xf4\x81\x99\xe3\xf4\xf2\xcc+VQ\
\xcdB:\x12\xd2VP\xb6D\xbbu-_\xe5\xef4\x1d\xe5\x1d\x91\xc3\x89\x88$\x07\xc5\
\x80C\x00F\x08QJ&\x93\x1b\x01\xfcs\xdd\x04\x8c1\xaeR*\xac\xaf\xaf\x0f\x84\
\x10uDd^\x99|C\xfe!\xff{U\x81V\x90\xb6\x82\xe5\xd8\xd8\x1d<\x1enqo\x8d$\x91\
\x86@@D\xbe\x84\x88B\x8d\x88\x19\x93D(*\xa52\xeb*\x10\x86\xa1\x0b\xc0\'"\xa7\
:\xb9y\x9e\xf3R9\n\xca\xa9\xc0_+o\xd2\xbb\xfc\x87\xfd\x06\xd3\xac\x85%|\x00e\
\x01\x84\x82(\xaaw\xe8\xd25)yTJq\x16\x95%zM\xaa\xd1\xff&\x10\x19cJ\xcc\xec\
\x13QY\x08\x11\x01\xd0\xac\xb4\x8aQ\x1c\x9d\xd6\xf6h\x1b\xdd\x16\\c\xb6\x06$\
8\x84\x84\'\x88|"\n\x95\x80\xd7V/\xde\xefH\xaa\x13B\x08\x1f@\xc0\xcc\xe7\xb4\
\xd6}\xeb& \xa5\x0c\xb4\xd6.\x11y\xccl\x03\x08\x88(\xba#q7z\xdcO\x97\x1daG\
\x82\xaaE \x91\'\x05\x85\x82\x1048b\xbc#\xa1\x06\x1dK\x96P\xc9\xfa\x82\x10\
\xe2\xf0\xd6\xad[GQ\xd9g\xd6G\x80\x88\xc20\x0c]f\xf6\x008DT\x06\xa0\xdbUF\
\xcf;F0\xd8#\xa6\xa2\x14\x14\x10!\xa8\xb3\xc4\\[\\\r\xc6-\xbaHD!*u\xea\xfb\
\x96e\rtuu\xf9\xcbaX\x91\x00\x800\x08\x02\x97\x88\\\x006\x11yD\x14)\xc9l\x0b\
\x0e\xa4\x10.\x81CK\xc9RcLf\x1b\x1d:\x8dJ\xc6Cf>\x07\xe0\xf0\xb6m\xdb.\xad\
\x04|\xa5\x02\x811\xc6\xd5Z\x17\x99\xd9"\xa2\x05"\x9a\xb7$\x99\x84\xa3\x98\
\xc0~\xdc\xa6\x89\xa6\xb8=**\xbd\x14\x1ac\x8aR\xcaw\xb7n\xddzz5\xc0W$\xa0\
\x94\xf2}\xdfw\xa5\x94\x85(\x8a<"*\x11\x91_gI\xb2\x85\xce%c\xf6\xa8$\xce\xc3\
\x98\x80\x81@)u\xa2T*\xbd\xdf\xd3\xd3\xb3\xac\x87\x96U\x17\x00\xe0\x17\n\x85\
3\xae\xeb\xb2\xeb\xba\x9b*\xcf\xfe(\xc6\x15M\x92%/\x12q\x08 $\xa2sJ\xa9\x81\
\xae\xae\xae\xc2\xea!_\x1e\xcb\x12\x08\xc3\xf0\xfd}\xfb\xf6\x1dy\xeb\xad\xb7\
>\xa7\x94J\x00p\x99yJ)\xe9\xa3\x02\xbe\x00`\xe8\xfa\xeb\xaf\x9fZU\xda\xff\
\x10\xcb>b:p\xe0\x80\xda\xb4iSw\xa9T\xf2\x1d\xc7\xe9^\\]\xc20<9;;{r9\xa7-\
\xcb\x89\x15\x9f\x91e\xb3\xd9k\x88\xa8[\x08q\xbe\\.\x8ftww\x97V\x89\xed\x8ab\
\xc5gd\x96e\xb9\xae\xeb\x1e\xee\xee\xee\x9eY\r\xa0\xa5\xc6\xaa\x9eR~\x12\xf1\
\x89\xfd[e\xb5\xe2_\xcf\x113\xc7\xc5?\x80\xd7\x00\x00\x00\x00IEND\xaeB`\x82\
\x0b~\xf1$'
