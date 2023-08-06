"""Pre-trained models for real-world problems."""
from .base import SparrowModel
from .detector import FCOS, detector_collate_fn
from .holdouts import Holdout, get_holdout
from .utils import get_slug
