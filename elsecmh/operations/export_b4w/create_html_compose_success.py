from elsecommon.transports.router import Router
from elsecommon import marshalling
from elsepublic.dto.dam_asset_info import DamAssetsInfoDTO
from elsepublic.elserender.dto.export_b4w import ExportB4WParamsDTO
from elsepublic.elserender.interfaces.export_b4w import ExportB4WOpInterface
from elsepublic.elserender.serializers.export_b4w import ExportB4WParamsSerializer
from elsepublic.elsedam.asset_extensions import AssetExtensions
from elsepublic.serializers.dam_asset_info import DamAssetsInfoSerializer


class CreateHTMLComposeSuccessHandler(marshalling.ElseOperation):
    """
    Handler which responds to put assets operation called by compose
    operation after create html for b4w operation

    Attributes
    ----------
    expect_serializer_class : elsepublic.serializers.dam_asset_info.DamAssetsInfoSerializer
        Expect serializer.
    expose_serializer_class : elsepublic.elserender.serializers.export_b4w.ExportB4WParamsSerializer
        Expose serializer.
    """
    expect_serializer_class = DamAssetsInfoSerializer
    expose_serializer_class = ExportB4WParamsSerializer

    def __call__(self, data: DamAssetsInfoDTO, **context) -> ExportB4WParamsDTO:
        """
        Parameters
        ----------
        data : elsepublic.dto.dam_asset_info.DamAssetsInfoDTO
            Operation input parameters
        context : dict
            context data {export_camera}

        Returns
        -------
        elsepublic.elsedam.dto.export_b4w.ExportB4WParamsDTO
            Operation output result
        """
        export_dam_asset_info = data.dam_assets_info[0]

        export_b4w_op = Router[ExportB4WOpInterface]
        export_b4w_dto = ExportB4WParamsDTO(
            dam_asset_info=export_dam_asset_info,
            export_type=AssetExtensions.HTML,
            camera=context.pop('export_camera'),
        )
        export_b4w_op(export_b4w_dto, **context)
        return export_b4w_dto
