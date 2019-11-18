import tempfile

from cv2 import cv2
from elsecmh.else_axf.py import axf_sdk
from elsepublic.elsedam.asset_tags import AssetTags


class TextureExtractor:
    valid_names = (
        'SpecularLobe',
        'AnisoRotation',
        'SpecularColor',
        'DiffuseColor',
        'Normal')

    @staticmethod
    def _get_texture_tag_by_name(name):
        texture_tag = None

        if name == 'SpecularColor':
            texture_tag = AssetTags.TEXTURE_SPECULAR
        elif name == 'DiffuseColor':
            texture_tag = AssetTags.TEXTURE_DIFFUSE
        elif name == 'AnisoRotation':
            texture_tag = AssetTags.TEXTURE_AR
        elif name == 'Normal':
            texture_tag = AssetTags.TEXTURE_NORMAL
        elif name == 'SpecularLobe':
            texture_tag = AssetTags.TEXTURE_ROUGHNESS

        assert texture_tag is not None

        return texture_tag

    @property
    def _all_named_textures(self):
        num_textures = self.texture_decoder.getNumTextures()
        return map(self._named_texture_by_idx, range(num_textures))

    def __init__(self, file_name):
        axf_file = axf_sdk.open_file(file_name, True, False)
        material = axf_sdk.get_default_material(axf_file)
        representation = axf_sdk.get_preferred_representation(material)

        self.texture_decoder = axf_sdk.create_texture_decoder(representation)
        self.num_textures = self.texture_decoder.getNumTextures()

    def extract_tagged_textures(self):
        valid_named_textures = filter(
            self._is_texture_valid,
            self._all_named_textures)
        return list(map(self._tagged_texture, valid_named_textures))

    def _named_texture_by_idx(self, texture_idx):
        name = axf_sdk.get_texture_name(self.texture_decoder, texture_idx)
        data = axf_sdk.get_texture(self.texture_decoder, texture_idx)
        return name, data

    def _tagged_texture(self, named_texture):
        name, texture = named_texture
        return self._get_texture_tag_by_name(name), texture

    def _is_texture_valid(self, named_texture):
        name, texture = named_texture
        return name in self.valid_names


def texture2tagged_file(tagged_texture):
    tag, data = tagged_texture
    out_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    cv2.imwrite(out_file.name, data)
    return tag, out_file


def get_files_with_tagged_textures(textures):
    return list(map(texture2tagged_file, textures))
