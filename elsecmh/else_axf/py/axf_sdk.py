import struct

import cv2
import numpy as np
from colormath.color_objects import (
    XYZColor,
    sRGBColor,
)
from colormath.color_conversions import convert_color

from ..py import axf

AXF_COMPAT_PROF_SVBRDF = axf.AXF_COMPAT_PROF_SVBRDF
AXF_COMPAT_PROF_SVBRDF_REFRACT = axf.AXF_COMPAT_PROF_SVBRDF_REFRACT
AXF_COMPAT_PROF_CARPAINT = axf.AXF_COMPAT_PROF_CARPAINT
AXF_COMPAT_PROF_CARPAINT_REFRACT = axf.AXF_COMPAT_PROF_CARPAINT_REFRACT
AXF_COMPAT_PROF_BTF = axf.AXF_COMPAT_PROF_BTF
AXF_COMPAT_PROF_BASELINE_SVBRDF = axf.AXF_COMPAT_PROF_BASELINE_SVBRDF
AXF_COMPAT_PROF_BASELINE_BTF = axf.AXF_COMPAT_PROF_BASELINE_BTF
AXF_REPRESENTATION_CLASS_SVBRDF = axf.AXF_REPRESENTATION_CLASS_SVBRDF
AXF_REPRESENTATION_CLASS_CARPAINT = axf.AXF_REPRESENTATION_CLASS_CARPAINT
AXF_REPRESENTATION_CLASS_CARPAINT2 = axf.AXF_REPRESENTATION_CLASS_CARPAINT2
AXF_REPRESENTATION_CLASS_FACTORIZED_BTF = axf.AXF_REPRESENTATION_CLASS_FACTORIZED_BTF
AXF_REPRESENTATION_CLASS_LAYERED = axf.AXF_REPRESENTATION_CLASS_LAYERED
AXF_TYPEKEY_SVBRDF_DIFFUSE_LAMBERT = axf.AXF_TYPEKEY_SVBRDF_DIFFUSE_LAMBERT
AXF_TYPEKEY_SVBRDF_DIFFUSE_ORENNAYAR = axf.AXF_TYPEKEY_SVBRDF_DIFFUSE_ORENNAYAR
AXF_TYPEKEY_SVBRDF_SPECULAR_WARD = axf.AXF_TYPEKEY_SVBRDF_SPECULAR_WARD
AXF_TYPEKEY_SVBRDF_SPECULAR_BLINNPHONG = axf.AXF_TYPEKEY_SVBRDF_SPECULAR_BLINNPHONG
AXF_TYPEKEY_SVBRDF_SPECULAR_COOKTORRANCE = axf.AXF_TYPEKEY_SVBRDF_SPECULAR_COOKTORRANCE
AXF_TYPEKEY_SVBRDF_SPECULAR_PHONG = axf.AXF_TYPEKEY_SVBRDF_SPECULAR_PHONG
AXF_TYPEKEY_SVBRDF_SPECULAR_GGX = axf.AXF_TYPEKEY_SVBRDF_SPECULAR_GGX
AXF_SVBRDF_SPECULAR_WARD_VARIANT_GEISLERMORODER = axf.AXF_SVBRDF_SPECULAR_WARD_VARIANT_GEISLERMORODER
AXF_SVBRDF_SPECULAR_WARD_VARIANT_DUER = axf.AXF_SVBRDF_SPECULAR_WARD_VARIANT_DUER
AXF_SVBRDF_SPECULAR_WARD_VARIANT_WARD = axf.AXF_SVBRDF_SPECULAR_WARD_VARIANT_WARD
AXF_SVBRDF_SPECULAR_BLINN_VARIANT_ASHIKHMIN_SHIRLEY = axf.AXF_SVBRDF_SPECULAR_BLINN_VARIANT_ASHIKHMIN_SHIRLEY
AXF_SVBRDF_SPECULAR_BLINN_VARIANT_BLINN = axf.AXF_SVBRDF_SPECULAR_BLINN_VARIANT_BLINN
AXF_SVBRDF_SPECULAR_BLINN_VARIANT_VRAY = axf.AXF_SVBRDF_SPECULAR_BLINN_VARIANT_VRAY
AXF_SVBRDF_SPECULAR_BLINN_VARIANT_LEWIS = axf.AXF_SVBRDF_SPECULAR_BLINN_VARIANT_LEWIS
AXF_SVBRDF_FRESNEL_VARIANT_SCHLICK = axf.AXF_SVBRDF_FRESNEL_VARIANT_SCHLICK
AXF_SVBRDF_FRESNEL_VARIANT_FRESNEL = axf.AXF_SVBRDF_FRESNEL_VARIANT_FRESNEL
AXF_TYPEKEY_FACTORIZED_BTF_DFMF = axf.AXF_TYPEKEY_FACTORIZED_BTF_DFMF
AXF_TYPEKEY_FACTORIZED_BTF_DPVF = axf.AXF_TYPEKEY_FACTORIZED_BTF_DPVF
AXF_FACTORIZED_BTF_REPRESENTATION_VARIANT_DEFAULT = axf.AXF_FACTORIZED_BTF_REPRESENTATION_VARIANT_DEFAULT
AXF_FACTORIZED_BTF_REPRESENTATION_VARIANT_SQRTY = axf.AXF_FACTORIZED_BTF_REPRESENTATION_VARIANT_SQRTY
AXF_PREVIEW_IMAGE_NAME_DEFAULT = axf.AXF_PREVIEW_IMAGE_NAME_DEFAULT
AXF_SVBRDF_TEXTURE_NAME_DIFFUSE_COLOR = axf.AXF_SVBRDF_TEXTURE_NAME_DIFFUSE_COLOR
AXF_SVBRDF_TEXTURE_NAME_NORMAL = axf.AXF_SVBRDF_TEXTURE_NAME_NORMAL
AXF_SVBRDF_TEXTURE_NAME_SPECULAR_COLOR = axf.AXF_SVBRDF_TEXTURE_NAME_SPECULAR_COLOR
AXF_SVBRDF_TEXTURE_NAME_SPECULAR_LOBE = axf.AXF_SVBRDF_TEXTURE_NAME_SPECULAR_LOBE
AXF_SVBRDF_TEXTURE_NAME_ANISO_ROTATION = axf.AXF_SVBRDF_TEXTURE_NAME_ANISO_ROTATION
AXF_SVBRDF_TEXTURE_NAME_ALPHA = axf.AXF_SVBRDF_TEXTURE_NAME_ALPHA
AXF_SVBRDF_TEXTURE_NAME_HEIGHT = axf.AXF_SVBRDF_TEXTURE_NAME_HEIGHT
AXF_SVBRDF_TEXTURE_NAME_FRESNEL = axf.AXF_SVBRDF_TEXTURE_NAME_FRESNEL
AXF_SVBRDF_TEXTURE_NAME_CLEARCOAT_NORMAL = axf.AXF_SVBRDF_TEXTURE_NAME_CLEARCOAT_NORMAL
AXF_SVBRDF_TEXTURE_NAME_CLEARCOAT_IOR = axf.AXF_SVBRDF_TEXTURE_NAME_CLEARCOAT_IOR
AXF_SVBRDF_TEXTURE_NAME_CLEARCOAT_COLOR = axf.AXF_SVBRDF_TEXTURE_NAME_CLEARCOAT_COLOR
AXF_SVBRDF_TEXTURE_NAME_SUBSURFACESCATTERING_TRANSMISSIONCOLOR = axf.AXF_SVBRDF_TEXTURE_NAME_SUBSURFACESCATTERING_TRANSMISSIONCOLOR
AXF_SVBRDF_TEXTURE_NAME_SUBSURFACESCATTERING_EXTINCTIONLENGTH = axf.AXF_SVBRDF_TEXTURE_NAME_SUBSURFACESCATTERING_EXTINCTIONLENGTH
AXF_CARPAINT2_TEXTURE_NAME_BRDF_COLORS = axf.AXF_CARPAINT2_TEXTURE_NAME_BRDF_COLORS
AXF_CARPAINT2_TEXTURE_NAME_BTF_FLAKES = axf.AXF_CARPAINT2_TEXTURE_NAME_BTF_FLAKES
AXF_CARPAINT2_TEXTURE_NAME_CLEARCOAT_NORMAL = axf.AXF_CARPAINT2_TEXTURE_NAME_CLEARCOAT_NORMAL
AXF_CARPAINT2_PROPERTY_BRDF_CT_DIFFUSE = axf.AXF_CARPAINT2_PROPERTY_BRDF_CT_DIFFUSE
AXF_CARPAINT2_PROPERTY_BRDF_CT_COEFFS = axf.AXF_CARPAINT2_PROPERTY_BRDF_CT_COEFFS
AXF_CARPAINT2_PROPERTY_BRDF_CT_F0S = axf.AXF_CARPAINT2_PROPERTY_BRDF_CT_F0S
AXF_CARPAINT2_PROPERTY_BRDF_CT_SPREADS = axf.AXF_CARPAINT2_PROPERTY_BRDF_CT_SPREADS
AXF_CARPAINT2_PROPERTY_FLAKES_NUM_THETAF = axf.AXF_CARPAINT2_PROPERTY_FLAKES_NUM_THETAF
AXF_CARPAINT2_PROPERTY_FLAKES_NUM_THETAI = axf.AXF_CARPAINT2_PROPERTY_FLAKES_NUM_THETAI
AXF_CARPAINT2_PROPERTY_FLAKES_MAX_THETAI = axf.AXF_CARPAINT2_PROPERTY_FLAKES_MAX_THETAI
AXF_CARPAINT2_PROPERTY_FLAKES_THETAFI_SLICE_LUT = axf.AXF_CARPAINT2_PROPERTY_FLAKES_THETAFI_SLICE_LUT
AXF_CARPAINT2_PROPERTY_CC_IOR = axf.AXF_CARPAINT2_PROPERTY_CC_IOR
AXF_CLEARCOAT_PROPERTY_NAME_NO_REFRACTION = axf.AXF_CLEARCOAT_PROPERTY_NAME_NO_REFRACTION
AXF_COLORSPACE_CIE_1931_XYZ = axf.AXF_COLORSPACE_CIE_1931_XYZ
AXF_COLORSPACE_LINEAR_SRGB_E = axf.AXF_COLORSPACE_LINEAR_SRGB_E
AXF_COLORSPACE_LINEAR_ADOBE_RGB_E = axf.AXF_COLORSPACE_LINEAR_ADOBE_RGB_E
AXF_COLORSPACE_LINEAR_ADOBE_WIDEGAMUT_RGB_E = axf.AXF_COLORSPACE_LINEAR_ADOBE_WIDEGAMUT_RGB_E
AXF_COLORSPACE_LINEAR_PROPHOTO_RGB_E = axf.AXF_COLORSPACE_LINEAR_PROPHOTO_RGB_E
AXF_MAX_KEY_SIZE = axf.AXF_MAX_KEY_SIZE
TYPE_HALF = axf.TYPE_HALF
TYPE_HALF_ARRAY = axf.TYPE_HALF_ARRAY
TYPE_INT = axf.TYPE_INT
TYPE_INT_ARRAY = axf.TYPE_INT_ARRAY
TYPE_FLOAT = axf.TYPE_FLOAT
TYPE_FLOAT_ARRAY = axf.TYPE_FLOAT_ARRAY
TYPE_STRING = axf.TYPE_STRING
TYPE_UTF_STRING = axf.TYPE_UTF_STRING
TYPE_BOOLEAN = axf.TYPE_BOOLEAN
TYPE_ERROR = axf.TYPE_ERROR
TEXTURE_TYPE_HALF = axf.TEXTURE_TYPE_HALF
TEXTURE_TYPE_FLOAT = axf.TEXTURE_TYPE_FLOAT
TEXTURE_TYPE_BYTE = axf.TEXTURE_TYPE_BYTE
ORIGIN_TOPLEFT = axf.ORIGIN_TOPLEFT
ORIGIN_BOTTOMLEFT = axf.ORIGIN_BOTTOMLEFT
LOGLEVEL_INFO = axf.LOGLEVEL_INFO
LOGLEVEL_WARNING = axf.LOGLEVEL_WARNING
LOGLEVEL_ERROR = axf.LOGLEVEL_ERROR
LOGCONTEXT_AXF_IO = axf.LOGCONTEXT_AXF_IO
LOGCONTEXT_DECODERS = axf.LOGCONTEXT_DECODERS
LOGCONTEXT_GENERIC = axf.LOGCONTEXT_GENERIC
TextureDecoder = axf.TextureDecoder

DATA_TYPES = {
    TYPE_BOOLEAN: 'BOOLEAN',
    TYPE_INT: 'INT',
    TYPE_INT_ARRAY: 'INT_ARRAY',
    TYPE_HALF: 'HALF',
    TYPE_FLOAT: 'FLOAT',
    TYPE_HALF_ARRAY: 'HALF_ARRAY',
    TYPE_FLOAT_ARRAY: 'FLOAT_ARRAY',
    TYPE_STRING: 'STRING',
    TYPE_UTF_STRING: 'UTF_STRING',
    TYPE_ERROR: 'ERROR'
}

TEXTURE_TYPES = {
    TEXTURE_TYPE_HALF: "TEXTURE_TYPE_HALF",
    TEXTURE_TYPE_FLOAT: "TEXTURE_TYPE_FLOAT",
    TEXTURE_TYPE_BYTE: "TEXTURE_TYPE_BYTE"
}


def __buffer_decode(buf):
    return buf.decode("utf-8", 'ignore').strip("\x00")


__SIZEOF_WCHAR = 4

__EMPTY_BUFFER = bytearray()


class AxfException(Exception):
    pass


class AxfUnexpectedDataTypeException(AxfException):
    pass


class AxfDataTypeException(AxfException):
    pass


class AxfRepresentationVersionException(AxfException):
    pass


class AxfSpecularModelVariant(AxfException):
    pass


class AxfPreviewImageInfoException(AxfException):
    pass


class AxfTextureInfoException(AxfException):
    pass


def buffer(size):
    return bytearray(size)


def get_material_display_name(axf_material):
    buf = buffer(
        axf.axfGetMaterialDisplayName(
            axf_material,
            __EMPTY_BUFFER) *
        __SIZEOF_WCHAR)
    axf.axfGetMaterialDisplayName(axf_material, buf)
    return __buffer_decode(buf)


def get_material_id_string(axf_material):
    buf = buffer(axf.axfGetMaterialIDString(axf_material, __EMPTY_BUFFER))
    axf.axfGetMaterialIDString(axf_material, buf)
    return __buffer_decode(buf)


def get_material_name(axf_file, i_material):
    buf = buffer(axf.axfGetMaterialName(axf_file, i_material, __EMPTY_BUFFER))
    axf.axfGetMaterialName(axf_file, i_material, buf)
    return __buffer_decode(buf)


def get_default_material_name(axf_file):
    buf = buffer(axf.axfGetDefaultMaterialName(axf_file, __EMPTY_BUFFER))
    axf.axfGetDefaultMaterialName(axf_file, buf)
    return __buffer_decode(buf)


def get_metadata_document_name(axf_metadata_document):
    buf = buffer(
        axf.axfGetMetadataDocumentName(
            axf_metadata_document,
            __EMPTY_BUFFER))
    axf.axfGetMetadataDocumentName(axf_metadata_document, buf)
    return __buffer_decode(buf)


def get_metadata_property_name(axf_metadata_document, i_property):
    buf = buffer(
        axf.axfGetMetadataPropertyName(
            axf_metadata_document,
            i_property,
            __EMPTY_BUFFER))
    axf.axfGetMetadataPropertyName(axf_metadata_document, i_property, buf)
    return __buffer_decode(buf)


def get_representation_class(axf_representation):
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    axf.axfGetRepresentationClass(axf_representation, buf)
    return __buffer_decode(buf)


def get_representation_type_key(axf_representation):
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    axf.axfGetRepresentationTypeKey(axf_representation, buf)
    return __buffer_decode(buf)


def get_resource_lookup_path(axf_representation, axf_resource):
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    axf.axfGetResourceLookupPath(axf_representation, axf_resource, buf)
    return __buffer_decode(buf)


def get_resource_node_path(axf_resource):
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    axf.axfGetResourceNodePath(axf_resource, buf)
    return __buffer_decode(buf)


def get_preview_image_name(axf_representation, i_image_idx):
    # TODO: need to check
    buf = buffer(
        axf.axfGetPreviewImageName(
            axf_representation,
            i_image_idx,
            __EMPTY_BUFFER))
    axf.axfGetPreviewImageName(axf_representation, i_image_idx, buf)
    return __buffer_decode(buf)


def __decode_buffer(buf, i_type):
    if i_type == TYPE_BOOLEAN:
        return buf.pop() == 1
    elif i_type == TYPE_INT:
        # TODO: Need to test this type
        return struct.unpack('i', buf)
    elif i_type == TYPE_INT_ARRAY:
        # TODO: Need to test this type
        [struct.unpack('i', buf) for i in buf.split()]
    elif i_type == TYPE_HALF or i_type == TYPE_FLOAT:
        # TODO: Need to test this type
        return struct.unpack('f', buf)
    elif i_type == TYPE_HALF_ARRAY or i_type == TYPE_FLOAT_ARRAY:
        # TODO: Need to test this type
        [struct.unpack('f', buf) for i in buf.split()]
    elif i_type == TYPE_STRING or i_type == TYPE_UTF_STRING:
        return __buffer_decode(buf)
    elif i_type == TYPE_ERROR:
        raise AxfDataTypeException()
    else:
        raise AxfUnexpectedDataTypeException()


def get_metadata_property_value(axf_metadata_document, i_property, i_type):
    buf = buffer(
        axf.axfGetMetadataPropertyValueLen(
            axf_metadata_document,
            i_property))
    axf.axfGetMetadataPropertyValue(
        axf_metadata_document, i_property, i_type, buf)
    return __decode_buffer(buf, i_type)


def get_representation_variant(axf_representation):
    # TODO: need to check
    buf = buffer(
        axf.axfGetRepresentationVariant(
            axf_representation,
            __EMPTY_BUFFER))
    axf.axfGetRepresentationVariant(axf_representation, buf)
    return __buffer_decode(buf)


def get_svbrdf_specular_fresnel_variant(axf_specular_model_representation):
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    axf.axfGetSvbrdfSpecularFresnelVariant(
        axf_specular_model_representation, buf)
    return __buffer_decode(buf)


def get_resource_data(axf_resource):
    # TODO: need to check
    buf = buffer(axf.axfGetResourceData(axf_resource, __EMPTY_BUFFER))
    axf.axfGetResourceData(axf_resource, buf)
    return __buffer_decode(buf)


def get_svbrdf_specular_model_variant(axf_specular_model_representation):
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    success, is_anisotropic, has_fresnel = axf.axfGetSvbrdfSpecularModelVariant(
        axf_specular_model_representation, buf)
    if not success:
        raise AxfSpecularModelVariant()
    return (__buffer_decode(buf), is_anisotropic, has_fresnel)


def get_representation_version(representation):
    success, major, minor, revision = axf.axfGetRepresentationVersion(
        representation)
    if not success:
        raise AxfRepresentationVersionException()
    return major, minor, revision


def get_preview_image_info(repr, idx):
    """Get the information about the preview image.
        This method is a wrapper of axfGetPreviewImageInfo from C++ library.

        Args:
            repr: valid handle to a representation.
            idx: Index of the preview image.
        Returns:
            width: width of the stored preview image in pixels.
            height: height of the stored preview image in pixels.
            channels: will be set to 4 if the stored preview image contains an alpha/opacity channel, 3 otherwise.
            width_mm: spatial width of the stored preview image in millimeters.
            height_mm: spatial height of the stored preview image in millimeters.
    """
    success, width, height, channels, width_mm, height_mm = axf.axfGetPreviewImageInfo(
        repr, idx)
    if not success:
        raise AxfPreviewImageInfoException()
    return int(width), int(height), int(channels), width_mm, height_mm


def get_preview_image(repr, idx, width, height, channels):
    """Returns preview image.
    Get the preview image. Return preview image as 3D array of numbers. Thus channels must be either 3 or 4: For
    channels = 3, a 3-channel color image (without alpha) is returned. If the source preview image from the AxF file
    actually has an alpha/opacity channel, the SDK tries to convert it to a non-transparent preview image by
    rendering it in front of a checkerboard background, which becomes "baked" into the resulting 3-channel image.
    Note that the latter is only guarantueed to work correctly for the default planar preview image (named
    AXF_PREVIEW_IMAGE_NAME_DEFAULT). For channels = 4, a 4-channel color/alpha image is returned (e.g. RGBA). No
    background is integrated into the resulting image. If the source preview image from the AxF file does not have an
    alpha/opacity channel, a trivial alpha channel (1.0f) is added to the result image.

        Args:
            repr: valid handle to a representation.
            idx: Index of the preview image.
            width: width of the stored preview image in pixels.
            height: height of the stored preview image in pixels.
            channels: number of channels of the image buffer (3 or 4).
        Returns:
            image_array: 3D array of the preview image in RGB or RGBA color space
    """
    buffer_size = int(width * height * channels)
    image_buffer = axf.float_buffer(buffer_size)
    axf.axfGetPreviewImage(
        repr,
        idx,
        AXF_COLORSPACE_CIE_1931_XYZ,
        image_buffer,
        width,
        height,
        channels)
    image_array = _convert_image_buffer_to_array(
        image_buffer, width, height, channels)
    return np.apply_along_axis(_XYZ2BGR, 2, image_array)


def _convert_image_buffer_to_array(image_buffer, width, height, channels):
    """Convert image buffer to 3D array

        Args:
            image_buffer: 1D buffer of size (width*height*channels)s
            width: width of the stored preview image in pixels.
            height: height of the stored preview image in pixels.
            channels: number of channels of the image buffer (3 or 4).
        Returns:
            image_array: 3D array [width][height][channels]
    """
    arr = []
    for x in range(int(width * height * channels)):
        arr.append(image_buffer[x])
    image_array = np.array(arr, dtype=float).reshape(height, width, channels)
    return image_array


def create_texture_decoder(repr):
    """Create a texture decoder for a given AxF representation,

         Args:
            repr: valid handle to AxF representation (get_representation())
         Returns:
            texture_decoder:
            Interface for simple extraction of texture resources (and associated rendering semantic) from AxF
            representations
    """
    return TextureDecoder.create(repr, AXF_COLORSPACE_LINEAR_SRGB_E)


def get_texture_name(texture_decoder, idx):
    """Get name of the texture by index

          Args:
              texture_decoder: texture decoder
              idx: index of the texture
          Returns:
              texture_name: name of the texture
    """
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    texture_decoder.getTextureName(idx, buf)
    return __buffer_decode(buf)


def get_texture_info(texture_decoder, idx):
    """Get the information about the texture.

        Args:
            texture_decoder: texture decoder.
            idx: Index of the texture.
        Returns:
            width: width of the stored preview image in pixels.
            height: height of the stored preview image in pixels.
            depth: depth of the texture.
            channels: will be set to 4 if the stored preview image contains an alpha/opacity channel, 3 otherwise.
            data_type: the texture type in which the data is stored in the AxF file.
    """
    success, width, height, depth, channels, data_type = texture_decoder.getTextureSize(
        idx, 0)
    if not success:
        raise AxfTextureInfoException()
    return width, height, depth, channels, data_type


def get_texture(texture_decoder, idx):
    """Return texture as 3D array of numbers. Color space depends on the texture channels.
    If the texture has 3 channels, RGB will be chosen. For 1-channel texture greyscale image is returned.

        Args:
            texture_decoder: texture decoder.
            idx: Index of the texture.
        Returns:
            texture: the texture in greyscale or RGB color space.
    """
    width, height, depth, channels, datatype = get_texture_info(
        texture_decoder, idx)
    size_of_texture_type = 4 if datatype == TEXTURE_TYPE_FLOAT else 2
    buffer_size = int(width * height * channels * depth * size_of_texture_type)
    texture_data = axf.float_buffer(buffer_size)
    texture_decoder.getTextureData(idx, 0, datatype, texture_data)
    texture_array = _convert_image_buffer_to_array(
        texture_data, width, height, channels)
    # see documentation to find out how to specific texture represented
    texture_name = get_texture_name(texture_decoder, idx)
    if texture_name == AXF_SVBRDF_TEXTURE_NAME_NORMAL:
        texture = np.apply_along_axis(_XYZ2BGR, 2, texture_array)
    else:
        texture = None

    # handle texture according to the number of its channels
    if texture is None:
        if channels == 3:
            texture = np.apply_along_axis(_RGB2BGR, 2, texture_array)
        elif channels == 1:
            texture = texture_array * 255
        elif channels == 2:
            texture = _optical_flow2BGR(texture_array)
        else:
            texture = texture_array * 255
    return texture


def get_texture_params(texture_decoder, idx):
    _, i_min_filter, i_mag_filter, i_wrap_s, i_wrap_t, i_wrap_r, b_texture_array = texture_decoder.getTextureParams(
        idx)
    return i_min_filter, i_mag_filter, i_wrap_s, i_wrap_t, i_wrap_r, b_texture_array


def get_num_texture_properties(texture_decoder):
    """Return texture properties

        Args:
            texture_decoder: texture decoder.
        Returns:
            num_texture_properties:number of the texture properties.
    """
    return texture_decoder.getNumProperties()


def get_texture_property_name(texture_decoder, prop_idx):
    """Return property name by index.

        Args:
            texture_decoder: texture decoder.
            prop_idx: property index.
        Returns:
            property_name: name of the texture property.
    """
    buf = buffer(axf.AXF_MAX_KEY_SIZE)
    texture_decoder.getPropertyName(prop_idx, buf)
    return __buffer_decode(buf)


def get_texture_property_type(texture_decoder, prop_idx):
    return texture_decoder.getPropertyType(prop_idx)


def get_texture_property(texture_decoder, prop_idx):
    size = texture_decoder.getPropertySize(prop_idx)
    type = get_texture_property_type(texture_decoder, prop_idx)
    buf = axf.float_buffer(
        size) if type == TYPE_FLOAT else axf.int_buffer(size)
    b = texture_decoder.getProperty(prop_idx, buf, type, size)
    print(b, prop_idx, size, type, texture_decoder.getPropertyLen(prop_idx))
    arr = []
    for x in range(int(size)):
        arr.append(buf[x])

    print(arr)
    return 0


def _XYZ2BGR(xyz_color):
    """Convert XYZ color to BGR color

        Args:
            xyz_color: XYZ color
        Returns:
            bgr_color: BGR color
    """
    xyz = XYZColor(*xyz_color)
    return _RGB2BGR(convert_color(xyz, sRGBColor).get_value_tuple())


def _RGB2BGR(rgb_color):
    """Convert RGB color to BGR color

        Args:
            rgb_color: RGB color
        Returns:
            bgr_color: BGR color
    """
    r, g, b = rgb_color
    return np.array((b, g, r)) * 255


def _optical_flow2BGR(optical_flow):
    xy = np.transpose(optical_flow)
    # print(len(xy[0][0]), len(xy[1]), len(xy))
    magnitude, angle = cv2.cartToPolar(xy[0], xy[1], angleInDegrees=True)
    # print(magnitude)
    # print(angle)
    _, max_val, _, _ = cv2.minMaxLoc(magnitude)
    k = 1 / max_val
    magnitude *= k
    # print("min-max loc", max_val)
    hsv = np.zeros([3, len(angle[0]), len(angle)], dtype="float32")
    hsv[0] = np.transpose(angle)
    hsv[1] = np.ones(len(angle))
    hsv[2] = np.transpose(magnitude)
    hsv_img = cv2.merge(hsv)
    bgr_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR) * 255
    return bgr_img


enable_logging = axf.axfEnableLogging
disable_logging = axf.axfDisableLogging
open_file = axf.axfOpenFile
open_file_w = axf.axfOpenFileW
close_file = axf.axfCloseFile
get_number_of_materials = axf.axfGetNumberOfMaterials
get_material = axf.axfGetMaterial
get_default_material = axf.axfGetDefaultMaterial
find_material_by_id_string = axf.axfFindMaterialByIDString
get_number_of_metadata_documents = axf.axfGetNumberOfMetadataDocuments
get_metadata_document = axf.axfGetMetadataDocument
get_number_of_metadata_sub_documents = axf.axfGetNumberOfMetadataSubDocuments
get_metadata_data_sub_document = axf.axfGetMetadataDataSubDocument
get_number_of_metadata_properties = axf.axfGetNumberOfMetadataProperties
get_metadata_property_type = axf.axfGetMetadataPropertyType
get_metadata_property_value_len = axf.axfGetMetadataPropertyValueLen
get_number_of_representations = axf.axfGetNumberOfRepresentations
get_representation = axf.axfGetRepresentation
get_preferred_representation = axf.axfGetPreferredRepresentation
get_highest_supported_representation_version = axf.axfGetHighestSupportedRepresentationVersion
is_representation_supported = axf.axfIsRepresentationSupported
check_representation_compatibility_profile = axf.axfCheckRepresentationCompatibilityProfile
get_car_paint_flakes_btf_representation = axf.axfGetCarPaintFlakesBtfRepresentation
get_car_paint_tabulated_brdf_representation = axf.axfGetCarPaintTabulatedBrdfRepresentation
get_svbrdf_diffuse_model_representation = axf.axfGetSvbrdfDiffuseModelRepresentation
get_svbrdf_specular_model_representation = axf.axfGetSvbrdfSpecularModelRepresentation
get_number_of_representation_resources = axf.axfGetNumberOfRepresentationResources
get_representation_resource_from_index = axf.axfGetRepresentationResourceFromIndex
get_representation_resource_from_lookup_path = axf.axfGetRepresentationResourceFromLookupPath
get_representation_resource_from_lookup_name = axf.axfGetRepresentationResourceFromLookupName
get_resource_data_num_dims = axf.axfGetResourceDataNumDims
get_resource_data_dim_extent = axf.axfGetResourceDataDimExtent
get_resource_data_num_elems = axf.axfGetResourceDataNumElems
get_num_preview_images = axf.axfGetNumPreviewImages
store_preview_image = axf.axfStorePreviewImage
get_spectralization_trafo = axf.axfGetSpectralizationTrafo
