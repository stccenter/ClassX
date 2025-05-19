# classxlib/segment/algorithm/__init__.py

from ._watershed import watershed_transformation
from ._slic import slic_transformation
from ._quickshift import quickshift_transformation
from ._felzenszwalb import felzenszwalb_transformation

__all__ = ['watershed_transformation','slic_transformation',
           'quickshift_transformation', 'felzenszwalb_transformation']