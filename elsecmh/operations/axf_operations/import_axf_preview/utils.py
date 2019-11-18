import tempfile

from cv2 import cv2
from elsecmh.else_axf.py import axf_sdk


def extract_preview(file_name):
    axf_file = axf_sdk.open_file(file_name, True, False)
    material = axf_sdk.get_default_material(axf_file)
    representation = axf_sdk.get_preferred_representation(material)
    width, height, channels, w_mm, h_mm = axf_sdk.get_preview_image_info(
        representation, 0)
    preview_image = axf_sdk.get_preview_image(
        representation, 0, width, height, channels)
    return preview_image


def get_file_with_preview(preview):
    out_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    preview_bgr = preview

    cv2.imwrite(out_file.name, preview_bgr)
    out_file.close()
    return out_file
