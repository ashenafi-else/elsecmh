from elsecmh.settings import (
    RENDER_PREVIEW_QUALITY,
    RENDER_PREVIEW_IMAGE_EXTENSION,
    RENDER_PREVIEW_ENGINE,
    RENDER_PREVIEW_DEVICE,
    RENDER_PREVIEW_RESOLUTION_X,
    RENDER_PREVIEW_RESOLUTION_Y,
)


def get_preview_settings():
    """
    Get settings for render preview

    Returns
    -------
    dict
        dict with settings for render preview
    """
    return dict(
        quality=RENDER_PREVIEW_QUALITY,
        out_format=RENDER_PREVIEW_IMAGE_EXTENSION,
        engine=RENDER_PREVIEW_ENGINE,
        device=RENDER_PREVIEW_DEVICE,
        resolution_x=RENDER_PREVIEW_RESOLUTION_X,
        resolution_y=RENDER_PREVIEW_RESOLUTION_Y,
    )
