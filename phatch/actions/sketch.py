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

# Embedded icon is taken from
# http://www.tutorial9.net/resources/free-icon-pack-web-injection/
# by designer Jonatan Castro Fernandez.

# Follows PEP8

from core import models
from lib.reverse_translation import _t

#---Pil


def init():
    global Image, ImageMath, ImageOps, ImageFilter
    import Image
    import ImageMath
    import ImageOps
    import ImageFilter


def sketch(image, details_degree=1):
    im1 = image.convert('L')
    im2 = im1.copy()

    im2 = ImageOps.invert(im2)
    for i in range(details_degree):
        im2 = im2.filter(ImageFilter.BLUR)
    im1 = ImageMath.eval('convert(min(a * 255/ (256 - b), 255), "L")',
            a=im1,
            b=im2)
    return im1

#---Phatch


class Action(models.Action):

    label = _t('Sketch')
    author = 'Nadia Alramli'
    cache = False
    email = 'mail@nadiana.com'
    init = staticmethod(init)
    pil = staticmethod(sketch)
    version = '0.1'
    tags = [_t('filter')]
    __doc__ = _t('Transform to a grayscale pencil drawing')

    def interface(self, fields):
        fields[_t('Details Degree')] = self.IntegerField(
            '1', choices=['1', '5', '10', '20'])

    icon = \
'x\xda\x01\xd5\x08*\xf7\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\
\x00\x000\x08\x06\x00\x00\x00W\x02\xf9\x87\x00\x00\x00\x04sBIT\x08\x08\x08\
\x08|\x08d\x88\x00\x00\x08\x8cIDATh\x81\xed\x97}lU\xe5\x1d\xc7?\xcf\xb9\xf7\
\x9e\xfb\xde{o{o\xa1\xdcRJ[(\x14\xeap\xa55\xa2b6\xcc2%q\x9a0\xf7\xc7\x16^2\
\xb7\xfd\xb1\xb9\xa8\xc1i\x16\xdd\xe2\x92-f\xd9\xba\xa8\xc9\x82f\xb3L\x83Q\
\xfc\xc3mNQ\xbae*\x8a\x16I` \x94\x0e\x10J)H{\xe9}\xe9};\xe7\xdc\x97\xfdq\xce\
\xb1\x87\xf6\x16\x10\x90\xba\x84_\xf2\xe49\xf7\xdes\x9e\xf3\xf9\xfe\xce\xef|\
\x9f\xdf\x85kq-\xae\xc5\xb5\x98\xc9\x103\r0]l]\xbe\xbckvU\xd5ok\x83\xc1[\x03\
\xc1`\xda\xe6v\xbf\xa9\x14\x8b\xf7\xcf\xdd\xb4i\xd8z\xde\x97R\xc0\xd6\xce\
\xce\xf5\xf5\xc1`\xcf\x9cp\x98P}=\xde\xeaj(\x97\xc9\x8e\x8e\x8e\x0e\xc7\xe3\
\xab\x16o\xde\xbc\xdf<W\x9aI\xd0J\xf1\xec\xb2e\xebk\xfc\xfe\x9e\xdap\x98ps3\
\xfe\xc5\x8b\xb1uv"\xda\xda(\x17\n\x11\x87\xa6\xbd\xb4u\xc9\x12\xd9<\xffK%\
\xe0wk\xd6\xbc(\xbb\xdd=N\xbf\x1fO4\x8a\xa3\xa5\x05\x1a\x1a(\xaa*\xd9]\xbb\
\xc8&\x12\xe4S\xa96\x7f \xb0\xde\xbc\xe6K#\xa0\xbb\xbb\xfb\x81\xba\x9bo\xfeN\
\xd9\xeb%\xe7t\xa2\x86\xc3\x94\x9b\x9a\xd0\x12\t\xb2;w2~\xf2$\xc9d\x92T"\xc1\
\xf8\xf8x\xaby\x9d}&\xa1\xcd\xe8\xee\xee~\xa0\\.\xff~~W\x97p/]\xca\x91g\x9fe\
xh\x88\xe2;\xef\xe0\x88\xc5(\xc6b\xe4tp\xe2\xe94\xc9|\xfeS\xf3\xda\x19\x17\
\xd0\xfd\xf8Co766\xde2{\xf6l\xd1\xdf\xdf\xcf\x8a\x15+(\xac\\\xc9\'\xbd\xbd\
\xc4\x87\x87\xf1\x15\n8\x15\x85B6\xcbx6\xcb\xd9\\N=\x9b\xc9\xbcl^?\xa3\x02\
\xfe}\xdf\x92\xfb\x13K:o\x1d>u\x8a\x8e\x8e\x0eB\xa1\x10\xdb\xb6m\xa3T*\xe1\
\xeb\xea"\xdd\xdb\x8b;\x97\xc3]( T\x95\x8c\xaa\x12\xcb\xe77<r\xea\xd4\ts\r\
\xdbL\xc1\x1fX\'\x7f7\xe2\xcbo\xf2\xbb\x8a\xa2}\xf5\x8f\xf8\xc7\xebo\x90\xc9\
dH$\x12(\x8aB\xe7\xca\x95\xd4]\x7f=\x07{{\x19\x1f\x1f\'\xad\xaa\x8c\x15\n\
\x1b\x1e\x19\x1c|\xc1\xba\xce\x8c\x088p\xaf\xf7{\xde\xda\xe0\xf3\xbe\xe6v)\
\xd2\xdc\x8a\x92=K\xa2\x1c\xa6\xbf\xff\x10\xe1p\x98\x8e\x8e\x0e\x8e\x1d;Fc[\
\x1b\xe5\xd9\xb39\xfa\xfe\xfb\xa4\xdd\xee\x07\x7fu\xf8\xf0\xa6\xc9k]u\x01\
\xfd\x1b\\\xeb<\x91\xe0f_\xf32\xc9\xbd\xe0\x06\x1c\xb3\x9a\xf0q\x92\xfc\xe0\
\x1bd|\x1d\xa8Z\x81e\xcb\x96\x11\x89D\xe8\xeb\xeb\xc3U]]R\xeb\xea\x1e\xff\
\xc5\xd6\xadOTZ\xef\xaa\n8\xb8\xce\xb1\xd6\x1d\x90{|\xf3Z?\x83\x17\xf9\x13\
\x88\x91\xed\xd49\x8f\x13p\xe5iYq/;v\xbc\x87,\xcb\x94\xcb\xe5\xd2\xc0\xc0\
\xc0\xd6\x87\x1f{\xec\xbe\xe9\xd6\xbcj\x02\x0e\xaes\xacu\x87\\=\xae\x9a\x80\
\xe4jX\x84s~\x17\x926\x82\x18y\x13\xa1~\nv\t\x7f~\x88\xb1\xc1C\xd8\x1bVq\xe8\
\xd0@9\x99L>\xb2q\xe3\xc6\x07\xcf\xb7\xeeU\xe9\x85txw\x8f\xa7~\x9e\xe4n\xba\
\x1e\xc7\x9c\x05\xd8\x1d\x02\x11{\x1b\xf2\x83 4\x8a\xd9"\xf9\xb8\x8a\x96\xd4\
\x18\xd0\xae+\x1f)\xb5\xfc}\xdd/\xfft\xd7\x85\xd6\x16\x93\x8e\xad\x9f\xcb\
\xc6\xb8|\xf8\xa0\xb3\xc7S?O\xf2\xb4}\r9\xda\x86PO#\x86_A\x94s`\x17\xe7\xc0+\
)\xb5\xd4\x7f\\{\xe0\xb6\x17\x95\xa7.f}s\x1f\x10\xe8m\x85c\x92\x98\x92!\xa2\
\x04\x14?\xaf\xa8s\xe0\x17\xafD\x8e.F\xa4\xf6!\xe2\xef!\xcaY\xb0K\x97\x05o\
\x15`\x82\x15\xd1\xdf\x0b\x1b\xe0\x02\x9c\xc6\xef\x05@5~\xb7\x1eO+f\xa2l\x1a\
u\xf8\x86\xaf \x92\x1f#\x92\xbb\x10\xa5\xf4\x15\x81\x87\xa9%d\xce\x92!N\xb6\
\x08\x91\x01\xaf\xf19\x03\x8c\x01q@\x99,\xe4\xe0:\xc7Zw\x8d\xb7\xc7\xdb\xb0@\
r/\xbc\x11yN+"=\x80H\xf6!\xd4Q\xb0\x95\xae\x08<Tv!\xb3d\n\x80f\x00\xe6\xd1\
\xb3n\x07\xa2\xc0\x12\xa0\xd5\x10\xa3\x029S\x84\x15\xde\xb3\xe8\x16\xe49\x8b\
\xf4\xb2I|\x80\xd0\xce\x82\xad|\xc5\xe0\xa7\x130\x9d\x18\x95\x89\xccg\x800\
\xd0\t\xd4\x03) ~\xe0\xfb\xae\r\xde\x9a\xc0\x9f}\x8d\x8b$O\xeb\n\x1cu\x0b\
\x11\x89=\x88\xe4\x87\x88b\x02lL\x81\x1f\x18\xd26\xae\xda\xa2<y)\xf0pi6*\xd0\
\x9fD\x10X\x08\xdc\n(\xaf\xddi\x97\xda\x17\x86\x9e\xf06/\x95\xdc\xcd\xcbq\
\xd4\xceG$\xf7"\x12\x1f"\x8a\xc9\x8an30\xa4m\xfc\xfa\x0b\xca\x1f.\x15\x1e.\
\xad\x1b-\xa3\x97\xd6(0\x0e\x14~\xdee{\xb8\xbd\xb5\xfa[\xde\xf9m\x92\xbby9\
\xf6\xc8<\x18\xdb\x85\x18\xdfm\xbc\xb0_\x0c\xfc\xa5\n\xb0F\xfe\xad\xbb\x1d+\
\x16\xb6\xd4\xdc\xe5ki\x17\xae\xa6\x0e\xec\xe1zD|7R\xb2\x0fQ\xceTt\x9b\x0b\
\xc0W\xaa\x8ai\xdd\xee\xb2v\xe2}\xeb]?\xa8\x9a\x15\xdc\xe4kj\x97\\M_\xc5^\
\x13E\xc4?BJ\xed6|\xfe\xa22ou?\xeb0\xc1\'\x8fs\xe2s\xff\'~\xea\xa9\xfb\x9c\
\x80\xf3\xddo;~\xe2\xaf\xf1l\xf2\xce[$\xb9Z:\xf5\xcc\x9f\xfd\x00)\xf9\xa1\
\x91\xf9\xf3\xc2\x9b\x90\x12\xba\x918\xd0m\xda\x89\xeelV\xebv\xa0W\x8aT\x89\
\xf7B%$\x8c\x05\\\xc6b\xee\xb0\xbf\xee\xfe7\x1e\xba\xa9\xbd^\xd9\x7f\x9b\xa7\
.*\\\r\x8b\xb0\x07#\x88\xd8N\xa4\xf1\xdd\x08\x94)e\xa3\xa64\x0c\xf8\'- \xb6\
\nC2\xeei\xddX\xcd\xcdSX\xe6\xcf\x9e\xc4d\x01\xa6\xc3\xf8\x01\x9f1\x87\x81Z \
\x04\x04\x9c\xb2\xe3\x1eG\xed\xdc\xa8\xb7\x18\x13\x9e\xc5+qD\x1a\x10\xb1\x1d\
H\x99\xfd\xd3\xc2\xef\x1bT7~s\x8b\xf2\xb4\x91\x04\x9bq\x0f3\xb3fv+\x81c|\x96\
\xd0\xed|J\xc9[\x05\x08&\xac\xb1\x05\xa8C\xdfyK\xe8n\x93\xbc\xe9\xc6\xeb\xc6\
\x1a\xea\xe7\xd4\xefO)\x84"K\x8a\xed\xf5\xb56\x91\xdc\x8b\xc8\rL\x0b\xbf\xe7\
\xa8\xfa\xb3\xd5/+\xcf\x18\xc90K\xc2Z\x16&\xb8\xd9o\x15,\xe0%\xcb\xf7\xe6\
\xf1\x94\x8c\x9b\x11\x00\xbe\x014\x03\t`\x188\xcdD\xbb\x90{\xebo\x7f\xfca\
\xb8\xa6\xfa7\x0e\xd9M(\xdc@\xfe\xc4\xbb\xf9\xc6T\x8fK\x14SS\xda\x035\xa5\
\xb1\xf3\xb0\xf2\xe8\x9aW\xd4\xe7\xd0\xeb\xd9i\x017\xefkB\x15\x98\xd8\xf9Uc6\
G\xc1"`\xca\x8bl}\x02a\xf4\x16\xa1\x0f\xd8\x8b\xbe\xbb*\x96\x8c\x10\xa8\xf2\
\xde!\xd9\xec\x04\xab\xe7\xe0\xaf\nqDkp\xc9\x85h6jOx&\xc3o\xdf\xaf\xfcz\xfdk\
\xea_\x8d\'\xe9@/\x1dk\xb6\x0bL\x94\x8b\xd9\xb2\xa8\x16\x01\xa6\xa8\x8a\xe0\
\x95\x04\x14\xd07\xa71c(\xd6\x13\xdf\xeb}\xa6\xc1f\xb3\xdf\x1c\xaa\x89\x12\
\xaa\xa9\xa5\xa0\xe6\xa9\x9f\xe5\xe4\xb4\xd2\xe59q\xf4\x8cr\x9d<\xe44\xe1_\
\xdd\x93\x7f\xf2\xc7\xdb\xb4\xed\xc0,&\x9c\xc3\n[2@\xcd>\xcb\x9c/\x98\xf1\
\xf3\t\x88\x19\xd9\x97\x81\x08p\xc6\x92%\xa4\xb2\xb8;\x14\x8eR]3\x8b|6\xc9\
\xf0\xe0\xc7\x0c\x1f?@">\xc2\xa9\xd8\\\xe7\x88 }ca\xc0\xf7\xd2\x1e\xad\xe7\
\xc1m\xda?\xd1\xdf\'\x13\xda\xec\xa5L\xd0\x9ce(\x93\xc0\xa7\xf5\xfcJam\xe6\n\
\xe8eS\x04<\x9c\xfb\x98\xbd\xbe@\xcd_V\xdf~G\xa8TT\x189}\x84\xa3\x87v1\x9e\
\x8a!\x89"\xe1j7g\xf2\x0e\xf9P\xc6\xbd\xef\xa7\xcf\x0f>g$\xa6l\\\x9f\x07\xb2\
\xe8F\x90\xb2\x8c\xb4!\xc0,\x19k\xd6/:&w\xa3\x9aqC\xd0\x9f\x84\x0c\xc8\xa1P\
\xe8\xf6\xff\xec\xff\xef\xbd\x945\x96\xb6\xd6\x11\x1f=Fb\xec\x04\x12\x1a\xb2\
\xbdH2\x91\x18\xf8d\xe8\xcc[[\xde<\xf2\xea\xc8\xd9\\\x1a=\xab\x19\x034\x89n\
\x04\x89I\xe0f\xd6?7\xb45*\xb5\x12\xc2\x00\x0f\xa0{\x7f\x95\xdf_\xf5\xa8\xd7\
\xeb\xbdS\xd54\xee\xb9\xf3\x06V\xdf\x12)\x9d<52pt0\xf6\xd1\xeb\xff:\xdc\xd7\
\xffI|\x84\t\x07\xc9\x19\xf0ic\xceqn}_Tm_\xae\x00\xbb!`.\xd0\xe2ry\x9e\x96\
\x9drR\xc0`\xfb\xc2@\xfa\xf0\xf1\x91]gFsC\xe8Y5\xeb\xd8\xac\xef\xac1\xcc?A\
\xd6\xda\x9e\xe2\xe3_\x94\x00\t}\xe3\x89\x02\xf3\x8d\xd9g|\x9fF\x7f\xc1\xcd=\
\xc2\nj\xf5\xef\x8bv\x92+-\x00\x03T6\xa0\x83\xe8b\\\x06\x88\xc2\xc4\x0b\x99g\
\xc2\xafM\xd0/\x1c\xda\x1a\xe7k\xa7\xad\r\x97\x83\x89\x0e\xd2\xb4E\x13\xda,\
\x8b\xab\x02<9.\xf4\x7f@L\x9a\xadq\xc5\xeb\xf9Z\xfc?\xc6\xff\x00\xa1\xe7b\
\x91\xb3\x03\x82\xc8\x00\x00\x00\x00IEND\xaeB`\x82\xc1,r\xeb'
