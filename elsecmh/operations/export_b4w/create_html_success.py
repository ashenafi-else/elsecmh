from typing import Optional

from elsecmh.services.create_material_implementation_asset import create_material_implementation_asset
from elsecommon import marshalling
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO
from elsepublic.elsecmh.serializers.get_material_implementation import GetMaterialImplementationResultSerializer
from elsepublic.serializers.dam_asset_info import DamAssetsInfoSerializer


class CreateHTMLSuccessHandler(marshalling.ElseOperation):
    """
    Handler which responds to put assets operation called by export b4w operation
    after create html for b4w operation

    Attributes
    ----------
    expect_serializer_class : elsepublic.serializers.dam_asset_info.DamAssetsInfoSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elsecmh.serializers.get_material_implementation.GetMaterialImplementationResultSerializer
        Expose serializer.
    """
    expect_serializer_class = DamAssetsInfoSerializer
    expose_serializer_class = GetMaterialImplementationResultSerializer

    def __call__(self, data: DamAssetsInfoDTO, **context) -> Optional[GetMaterialImplementationResultDTO]:
        """
        Parameters
        ----------
        data : elsepublic.dto.dam_asset_info.DamAssetsInfoDTO
            Operation input parameters
        context : dict
            context data {material_implementation_uuid, asset_type}

        Returns
        -------
        elsepublic.elsecmh.dto.get_material_implementation.GetMaterialImplementationResultDTO or None
            Operation output result. Returns in case it is the last handler call
        """
        return create_material_implementation_asset(
            data,
            context['material_implementation_uuid'],
            context['asset_type'],
        )
