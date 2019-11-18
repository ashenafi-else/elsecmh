from django.db import models
from elsepublic.models import (
    Base,
    DamAssetInfo,
)
from treebeard.mp_tree import MP_Node
from django.contrib.postgres.fields import JSONField


class Brand(Base):
    brand_external_id = models.CharField(unique=True, max_length=64)
    name = models.CharField(max_length=255)


class MaterialGroup(MP_Node, Base):
    name = models.CharField(max_length=64)
    node_order_by = ['name', ]

    def __str__(self):
        return self.name


class ColorGroup(MP_Node, Base):
    name = models.CharField(max_length=64)
    node_order_by = ['name']

    def __str__(self):
        return self.name


class Material(Base):
    name = models.CharField(max_length=64)
    material_group = models.ForeignKey(
        'MaterialGroup',
        on_delete=models.CASCADE,
        related_name='materials'
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    active_revision = models.ForeignKey(
        'MaterialRevision',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )

    class Meta:
        unique_together = (
            'name',
            'brand',
            'deleted',
        )

    def __str__(self):
        return self.name


class MaterialRevision(Base):

    STATUS_NEW = 'NEW'
    STATUS_VALIDATING = 'VALIDATING'
    STATUS_VALIDATED = 'VALIDATED'
    STATUS_PUBLISHING = 'PUBLISHING'
    STATUS_PUBLISHED = 'PUBLISHED'

    STATUSES = (
        (STATUS_NEW, 'New'),
        (STATUS_VALIDATING, 'Validating'),
        (STATUS_VALIDATED, 'Validated'),
        (STATUS_PUBLISHING, 'Publishing'),
        (STATUS_PUBLISHED, 'Published'),
    )

    material = models.ForeignKey(
        'Material',
        related_name='revisions',
        on_delete=models.CASCADE,
    )
    material_info = JSONField(null=True)
    status = models.CharField(
        max_length=256,
        choices=STATUSES,
        default=STATUS_NEW,
    )
    camera = models.CharField(max_length=255, null=True)
    colors = models.ManyToManyField(
        'Color',
        through='MaterialImplementation',
    )
    default_color = models.ForeignKey(
        'Color',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )

    @property
    def version(self):
        return self.material.revisions.count()

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return '%s(%s)' % (self.material.name, self.pk)


def generate_file_name(self, filename):
    """ Generates file name for assets """
    return "elsecmh/{}/{}".format(self.uuid, filename)


class MaterialAsset(Base, DamAssetInfo):
    MODEL_ASSET = 'MODEL_ASSET'
    ENVIRONMENT_ASSET = 'ENVIRONMENT_ASSET'
    SETTINGS_ASSET = 'SETTINGS_ASSET'
    AXF_ASSET = 'AXF_ASSET'
    U3M_ASSET = 'U3M_ASSET'
    PREVIEW_ASSET = 'PREVIEW_ASSET'
    TEXTURE_ASSET = 'TEXTURE_ASSET'

    ASSET_TYPES = (
        (MODEL_ASSET, 'Model asset'),
        (ENVIRONMENT_ASSET, 'Environment asset'),
        (SETTINGS_ASSET, 'Settings asset'),
        (AXF_ASSET, 'AxF asset'),
        (U3M_ASSET, 'U3M asset'),
        (PREVIEW_ASSET, 'Preview asset'),
        (TEXTURE_ASSET, 'Texture asset')
    )
    asset_type = models.CharField(
        max_length=255,
        choices=ASSET_TYPES,
        null=True,
    )

    material_revision = models.ForeignKey(
        'MaterialRevision',
        on_delete=models.SET_NULL,
        null=True,
        related_name='assets',
    )


class MaterialMetaData(MP_Node, Base):
    material_revision = models.ForeignKey(
        'MaterialRevision',
        on_delete=models.CASCADE,
        related_name='meta_data',
        null=True,
    )

    AXF_RAW_DATA = 'AXF_RAW_DATA'
    AXF_META_DATA = 'AXF_META_DATA'

    CATEGORIES = (
        (AXF_RAW_DATA, 'AxF raw data'),
        (AXF_META_DATA, 'AxF meta data'),
    )

    category = models.CharField(
        max_length=255,
        choices=CATEGORIES,
        null=True,
        default=AXF_META_DATA,
    )

    key = models.CharField(max_length=255, null=False)

    value = models.TextField(null=False, default='')


class MaterialImplementation(Base):
    name = models.CharField(max_length=255, null=False)
    material_revision = models.ForeignKey(
        'MaterialRevision',
        on_delete=models.SET_NULL,
        null=True,
        related_name='implementations',
    )

    color = models.ForeignKey(
        'Color',
        on_delete=models.SET_NULL,
        null=True,
        related_name='implementations',
    )

    class Meta:
        unique_together = ('name', 'material_revision', 'deleted')


class MaterialImplementationAsset(Base, DamAssetInfo):
    MODEL_ASSET = 'MODEL_ASSET'
    PREVIEW_ASSET = 'PREVIEW_ASSET'
    AXF_ASSET = 'AXF_ASSET'
    JSON_ASSET = 'JSON_ASSET'
    HTML_ASSET = 'HTML_ASSET'

    ASSET_TYPES = (
        (MODEL_ASSET, 'Model asset'),
        (PREVIEW_ASSET, 'Preview asset'),
        (AXF_ASSET, 'AxF asset'),
        (JSON_ASSET, 'JSON asset'),
        (HTML_ASSET, 'HTML asset'),
    )

    asset_type = models.CharField(
        max_length=255,
        choices=ASSET_TYPES,
        null=True,
    )

    material_implementation = models.ForeignKey(
        'MaterialImplementation',
        on_delete=models.SET_NULL,
        null=True,
        related_name='assets',
    )


class Color(Base):
    RGB = 'RGB'
    sRGB = 'sRGB'
    CMYK = 'CMYK'
    HSV = 'HSV'
    HSL = 'HSL'
    COLOR_SPACES = (
        (RGB, 'RGB'),
        (sRGB, 'sRGB'),
        (CMYK, 'CMYK'),
        (HSV, 'HSV'),
        (HSL, 'HSL'),
    )

    name = models.CharField(max_length=64)
    color_group = models.ForeignKey(
        ColorGroup,
        on_delete=models.CASCADE,
        related_name='colors',
    )
    color_space = models.CharField(
        max_length=64,
        choices=COLOR_SPACES,
    )
    value = models.CharField(max_length=225)
    description = models.TextField(
        null=True,
        blank=True,
    )
