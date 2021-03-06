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

#---PIL


def init():
    global Image, ImageFilter, imtools
    from PIL import Image
    from PIL import ImageFilter
    from lib import imtools


def median(image, radius, amount=100):
    """Apply a filter
    - amount: 0-1"""
    image = imtools.convert_safe_mode(image)
    medianed = image.filter(ImageFilter.MedianFilter(radius))
    if amount < 100:
        return imtools.blend(image, medianed, amount / 100.0)
    return medianed

#---Phatch


class Action(models.Action):
    label = _t('Median')
    author = 'Stani'
    email = 'spe.stani.be@gmail.com'
    init = staticmethod(init)
    pil = staticmethod(median)
    version = '0.1'
    tags = [_t('filter')]
    __doc__ = _t("Copies the median pixel value")

    def interface(self, fields):
        fields[_t('Radius')] = self.RankSizeField(self.RANK_SIZES[0])
        fields[_t('Amount')] = self.SliderField(100, 1, 100)

    icon = \
'x\xda\x01 \x07\xdf\xf8\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\
\x00\x00+\x08\x06\x00\x00\x00>\x13\x0b\xdf\x00\x00\x00\x04sBIT\x08\x08\x08\
\x08|\x08d\x88\x00\x00\x06\xd7IDATh\x81\xcd\x99mL\x1c\xc7\x19\xc7\xff\xcf\
\xee\xde-\xc7qp\x1c\xe2\x8c!p$\x98\x82\xf0Q\x1b\xda\x80l\xe8\xcbEu,\x1bL%\
\x1a\xdb\xaa\xab(\x96]\xa9M>Dr"\xa7\x8d\x9a\xcaQ?\xb8\x15j\xac~H\x1b+J\xebDq\
\xd5\x88\xcaQ\x14\x9b\xb8\xa9i\xab\x04\xdb\t6\xc2\x8e\r\xd8\xf0\x81\x97\x03\
\x1c\x03\xe7\xdd{\x81\x03\xf6\xb8\x9d~\xe0\x0e\xdf\x0bR\xc32T\xf9I#\x96\x99\
\xdb\xf9\xcf\x7fv\x9e\xddgv\x891\x06\xde\x94\x94\x94\xbc2;;;\xaa(\xcaY\xee\
\x9d\xa7 lD\xa7\xc1`0S\xd3\xb4?\x10\x91s#\xfaO\x84\xab\x01"zd\xef\x9e=\xa3;w\
\xecxY\x92\xa4<\x00\xc3Dt\x90\xa7F*\x12\xaf\x8e\x88(\xff\xf8\x8b/\xf6\xd4\
\xd4\xd4l\x1a\x1b\x1b\xc3\xc8\xe8("\x91\x885\x1c\x0e\xbfCD\xf7\x18c]\xbc\xb4\
\x12\xe1v\x05\x0e\x1f>\xfc^ss\xf3\xa6\xbe\xfe~\x8c\x8f\x8f\xc3\xe3\xf1\xa0\
\xb0\xb0\x10\x82 \xc8\x00\xde$"\xe2\xa5\x95\x08\x17\x03\xb2,\xbb\x7fr\xe8\
\x90gxd\x046\x9b\r}\xfd\xfdxr\xd7.\xfc\xf1\xf5\xd7\xd1\xd6\xd6\x06A\x10*\x01\
\xec\xe5\xa1\x95\n\x17\x03\xad\xad\xad\xafTVV\x12\t\x02***\xd0\xd0\xd8\x08\
\x12\x04\xb4\xb7\xb7\xa3\xaa\xaa\n999\x00p\x80\x87V*\\b\xa0\xba\xbaz\x07\x00\
\xe4\xe5\xe6bb\xd2\x0b\x84o\xc1\xdb?\x81\x82\x82b\xb4\xb7\xb7CUU\x00\xa8\xe6\
\xa1\x95\n\x17\x03\xa2(\n\x00PY9\x81\x1f\xd4gB\xbf9\x081\xf8%\xe6K\x8b\xf1Q\
\xbf\x19o\xbf\r\x00\xd0yh\xa5\xc2e\t]\xbf~\xfd\xbc\xae\xeb\xf0\x07\x8a\x00\
\x06@\xb0\xac\xb4}\xfc\xaf\x07+\x87<\xb4R\xe1b\xe0\xdc\xb9s\xcf\x9f:u\xaa/\
\x14\xb2b>t\x13L\xd7\x00\x00\xba\x0e\\\xea\xf4\x01\xc0U\x00\xbf\xe1\xa1\x95\
\x06c\x8cK\x01 \xb8\\\xae\x9f^\xf8\xabgF\xbdX\xc3\x16\xda\xad\xec\xe3w\xcb\
\x15\x00?\x03 \xf1\xd2I-\xc4=\x17\x9a\xdam\xfd\xb2w|ZZP,\x99\xdbK7[\x1f\xfd|\
\x8a\xaf@\n\x1b1+\xf5\xf5\xf5\x7f\x7f\xb4\xb4\x94\x01\xd8\xb2Q3\x1f/\xdc\x93\
9"\x92\xb7UW7fX,\x00\xd0\xca\xbb\xffTx\'sDDg\xf7\xb5\xb4\x14\x88\xa2\x08\x00\
\xbf%\xa2\x97xj\xa4\xc1\xebR\xd6\xd6\xd6>c\xb5Z\xbb\xab\xddnV[S\xc3L&\x13\
\x03\xc0\x9e\xf0x\xd87\xca\xcb\xa3;\xea\xebo4555}\xad\x82\xf8\xe8\xd1\xa36\
\x9f\xcfw\xde\xef\xf77NOM\x89/\x1c;\x06M\xd3\xa0\xaa*n\xdc\xb8\x81\x0f/\\@mm\
-\x9ey\xfaitvv\xe2\x93\xae.\xe4\xe7\xe7\xab6\x9b\xedLss\xf3\xf1\x13\'N\xac\
\xfb\xe1f\xd8@\xc3\xce\x9doeZ,\x87g\x1e<\x10\xfd~?~w\xf2$t]\x87\xaa\xaaPU\
\x15c^/\xfer\xe6\x0ct]\xc7\xd6\xaa*TTT@\x92$|\xde\xdd\r\xaf\xd7\x0b\xa7\xd39\
g\xb7\xdb\x1b\x06\x07\x07\xbfX\x8f\x815\xa7\x12\xdb\xb6m\xfb\xbe\xa2(\x1f\
\x9aM&\xdb\xfd\xa9)dee\xe1\xcd\xd3\xa7!\xcbr<\xe7\x01\x00\xf4\xf4\xf4@\xd7\
\x97\'\xb8\x7f`\x00\xfd\x03\x03\x00\x80\xdc\xdc\xdc[\x00\xbe\xa9(J\xa6$I%\
\x00\xd6e`\xcdA\xec\xf7\xfb\x7f\x1d\x08\x04l\xb1\xd4y\xe4\x85c\xc7PPP\xb0\
\xd2ND\x08\x87\xc3\xb8u\xfb\xf6\xaa\xe7\x97\xba\\\xee\x8c\x8c\x0c\xd8\xed\
\xf6\x8f&\'\'\xcf\x1b\x1f\xfa2k6\xc0\x18{\xb9\xda\xed\x86(\x8a\xccn\xb7\xcf\
\xfc\xb0\xa5\x05\xa9{\x95\xc1\xa1\xa1\x95\xd9O\xa4\xa8\xa8\x08yyy\x82l6\xcf\
\xf8|\xbe}\xc6\x87\xfd\x905\x1b\xf0z\xbd\xd7\xa6gfz\xadV+=\xf7\xec\xb3u\xb1\
\xdbe\x92\x89`0\x98v\x9e\xcdf\xc3&\xa7\x13\xbd\xbd\xbd\x08\x04\x83\x11p\xca\
\x84\r=\x07\xa6\xa7\xa7w\xd9\xedv\xfd\xe0\xc1\xe4\xfdz\xdc\x843??\xed\x1c[V\
\x16\xc6\xbc^\x04C!\x00(\x04\xf0\xa4\x11\xedT\x0c\x19\x08\x04\x02JCC\x83&IR\
\xda\xf2!"8\x9d\xe9oS\x82\xc1 \x1e)*B\x86,\xc7\xab\xbeeD;\x15C\x06\x88\xc8U\
\xf7\xf8\xe3\x19\t\xff\'\xb5;\x1c\x0e\xc4\x97V\x9c\xd9\xb99h\x9a\x96X\xb5\
\xdd\x88v*FS\x89\xda\xba\xba\xba\xa4\x8aD\x13\xa2(\xc2n\xb7\xa7\x9dt\xe7\xee\
]\x90\xb0"\xb9\xd5\xa0v\x12F\r\xf8\x15UM\x9b\xf9D\xf2\x1c\x8eU\xebC\xcb1\x00\
\x00\xa3\x06\xb5\x930j\xe0J___\x04H\x9e\xf9\xc4\xe3\xd5\xae@\nW\rj\'a\xc8\
\x00cL\xeb\xe8\xe8\xb8\x12\x89D\xd2\xda\xe2&\xfeG\x8a\x12\x05\xd0aD;\x15\xc3\
\xe9\xf4\xe5\xcb\x97\x7f\xfc\xa77\xdeP\x81\xf4 &\xa2\xa4\x80u\xb9\\(..N\xfc\
\xc9/\x18c=F\xb5\x131\xfc0a\x8c\xdd\x97e\xf9;#\xc3\xc3\xddG\x8e\x1c\xb1\xa6\
\x9aP\x14\x05\x00PVV\x86\xf2\xc7\x9c\xb0\x88\xf701A`\x8c\xbd\xc5\x18{m}\xc3~\
\xc8\xba\xf7\xc4D\x94\xef*.~\xb5\xac\xac\xf4\xe7\xd99\x0e\xc1l6\xa3\xaf\xaf\
\x0f\x03w\xee\x00\x00\xb2\xb3\xb3q\xedt1\xc8\x14\xd0*\xf6O43\xc6.\xf1\x18\
\xf8\n\xbc6\x16\xa3\xef\xd7\x07\x9e;\xe4\xb8\x08\xe0\xb5\xadUUK\x00"\x00\xde\
\x01\xf0\xd2\xcc\xbfw\x0f\xcdvm\xe9\xf9Z\xef\x89\x0b71\xef\xef\x7fYt\t\xc0\
\xf1L\xabU\xc3r\xa0\x1ee\x8c\xb5\xe5f\xf9\xffI\xa2)\xcaK+\x11n\xdf\x07\x04av\
\x98Eac\x8c\xe9\xb2,\xb7\x0101\xc6\x96\x00@\x8f\xaa7\x11e\x1e^ZI\xba\xbc:b\
\xd10\xd8\xc2R\x13\x00,..\xbe\xca\x18\xfb\xd5J\x1b\x98\x8b\xcd\x05\xcbCC\xdf\
n\xe4\xa5\x17g\xfd/\xb6\x06\xdcf-\xa4\x9f\xa5I\xdfS\x0bY\x12\xe9E\x05\xef\
\xe7l\xddr\x00h\x8fb\xc0m\xd6\x82\xfa\xbb\xe2\xa4\xb2\x7fA\x8eR4\xdf\x11d\
\x9b\x1d?\xca)\xf9\xac\x93\xcf\xf0\xd7q\x05\x88H\xbaui\xbb;\x1c.\x98\x82\xdf\
\xb6_(>D\x90\xec0exZ\xbd\xb7\xef\xfd\xed\x83?\x97\xef\x9b\x9d+\xf4!\x94w\x80\
\n[H\x17\xed0\xe5\xee\xcbF\xd8\xf2\x8f/\xae5\xee%"\x0b\x11\x99\xd6k\xe0+\xc7\
@\xec\x13\x91\x1c+f\x00\xb2la\xcfO(\x93\x1d\x9bI\xdb=\xafv\xf9\xc8\xacY}\xe3\
W\x87\xbb\xef\x06\x86\xbeWe>y_\xb9w\xa7`)\xe0\xd6\xe7\xc1\xe6E\x160\xf9\xaf8\
Ff\xf1\xde\x83y\xad\n\xc0\x10\x80E"\xd2\x00,\x02\xd0\x00,2\xc6\xd6\x14\xec_y\
\t\xadb\xc0\x1c?6\x99 G"0\xc5\xeaL\x00DI\x82\xb4\xb4\x04\xd6\xec\xc9q\\\xf8O\
`\n@d\xcfws\xac\x17?\rL\xc7\x06\x9b4\xf0\xf8\xf1\x86\x19X\xc5\x90\x18\x1b\
\xac\x14+b\xac\x08x\xb84\t\xcb_\x0c\x18\x96o\xabz\xec\xefR\xacD\xe2w*\xa3\
\xf0\x7f;\xfd\x7f\xe6\xbf\x82\x1co\xb0\n\xf7\xb5u\x00\x00\x00\x00IEND\xaeB`\
\x82\xbea_\x9e'
