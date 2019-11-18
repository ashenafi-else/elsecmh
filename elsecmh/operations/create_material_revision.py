from elsecommon import marshalling
from elsecmh.models import (
    Color,
    Material,
    MaterialAsset,
    MaterialRevision,
    MaterialImplementation,
)
from elsepublic.exceptions import (
    MissingColorException,
    MissingMaterialException,
)
from elsepublic.helpers.asset_dto_to_dict import asset_dto_to_dict
from elsecmh.operations.utils.material_types import get_asset_type_by_ext
from elsepublic.elsecmh.create_material_revision import (
    CreateMaterialRevParams,
    CreateMaterialRevResult,
    CreateMaterialRevParamsSerializer,
    CreateMaterialRevResultSerializer,
)


class CreateMaterialRevisionOp(marshalling.ElseOperation):
    """
    Operation to create material revision.
    After revision was created implementations are created
    according to the colors given and dam asset is put to the storage.
    Afterwords validation operation is called.

    Attributes
    ----------
    expect_serializer_class : CreateMaterialRevParamsSerializer
        Expect serializer.
    expose_serializer_class : CreateMaterialRevResultSerializer
        Expose serializer.

    Raises
    ------
    MissingMaterialException
        If the material passed as an argument does not exist.
    MissingColorException
        If any of the colors passed as an argument do not exist.
    """
    expect_serializer_class = CreateMaterialRevParamsSerializer
    expose_serializer_class = CreateMaterialRevResultSerializer

    def __call__(self, data: CreateMaterialRevParams,
                 **context) -> CreateMaterialRevResult:
        """
        Parameters
        ----------
        data:
            elsepublic.elsecmh.create_material_revision.CreateMaterialRevParams
            Operation input parameters
        context : dict
            context data
        Returns
        -------
        elsepublic.elsecmh.create_material_revision.CreateMaterialRevResult
            Operation result object
        """
        material = Material.objects.filter(uuid=data.uuid).first()
        if not material:
            raise MissingMaterialException

        colors = Color.objects.filter(uuid__in=data.color_uuids)
        if colors.count() != len(data.color_uuids):
            raise MissingColorException

        material_revision = MaterialRevision.objects.create(
            material=material,
            material_info=data.info,
        )
        material_revision.save()

        implementation_list = []
        for color in colors:
            implementation_list.append(
                MaterialImplementation(
                    name='{}_{}'.format(
                        material_revision.material.name,
                        color.name,
                    ),
                    material_revision=material_revision,
                    color=color,
                ))
        MaterialImplementation.objects.bulk_create(implementation_list)
        asset_types = set(get_asset_type_by_ext(asset.extension)
                          for asset in data.assets)
        if MaterialAsset.U3M_ASSET in asset_types:
            asset_type = MaterialAsset.U3M_ASSET
        elif MaterialAsset.AXF_ASSET in asset_types:
            asset_type = MaterialAsset.AXF_ASSET
        else:
            asset_type = MaterialAsset.MODEL_ASSET

        material_assets = [
            MaterialAsset(
                material_revision=material_revision,
                asset_type=asset_type,
                **asset_dto_to_dict(asset),
            ) for asset in data.assets
        ]
        MaterialAsset.objects.bulk_create(material_assets)

        return CreateMaterialRevResult(
            uuid=material_revision.uuid,
            material_info=material_revision.material_info,
            status=material_revision.status,
        )
