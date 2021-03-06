import os
from elsepublic.elserender.constants.defaults import (
    DEFAULT_QUALITY,
    DEFAULT_IMAGE_EXTENSION,
    DEFAULT_ENGINE,
    DEFAULT_DEVICE,
    DEFAULT_RESOLUTION_X,
    DEFAULT_RESOLUTION_Y,
)
RENDER_PREVIEW_QUALITY = DEFAULT_QUALITY
RENDER_PREVIEW_IMAGE_EXTENSION = DEFAULT_IMAGE_EXTENSION
RENDER_PREVIEW_ENGINE = os.getenv('ENGINE', DEFAULT_ENGINE)
RENDER_PREVIEW_DEVICE = DEFAULT_DEVICE
RENDER_PREVIEW_RESOLUTION_X = DEFAULT_RESOLUTION_X
RENDER_PREVIEW_RESOLUTION_Y = DEFAULT_RESOLUTION_Y

