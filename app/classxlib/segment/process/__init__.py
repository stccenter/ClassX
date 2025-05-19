# classxlib/segment/process/__init__.py

from ._segment_parameter import process_segment_parameters
from ._mark_boundary import mark_segment_boundaries
from ._merge_segment import merge_segments
from ._remove_segment import remove_small_segments

__all__ = ['process_segment_parameters','mark_segment_boundaries',
           'merge_segments','remove_small_segments']