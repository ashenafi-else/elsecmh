from elsecmh.tests.test_base_cmh import TestBaseCmh

from elsepublic.elsecmh.dto.get_material_implementation import GetMaterialImplementationResultDTO
from elsepublic.elsecmh.dto.validate_material_revision import ValidateMaterialRevParamsDTO

from elsecmh.operations.publish_material_revision.publish_material_revision_success import \
    PublishMaterialRevisionSuccessHandler

from elsecmh.models import (
    MaterialImplementation,
    MaterialRevision,
    Material,
)


class TestPublishMaterialRevisionSuccessHandler(TestBaseCmh):

    def setUp(self):
        super().setUp()
        material = Material.objects.create(name='material', material_group=self.root)
        self.material_revision = MaterialRevision.objects.create(material=material, material_info='')
        self.material_implementation = MaterialImplementation.objects.create(material_revision=self.material_revision)
        self.dto = GetMaterialImplementationResultDTO(uuid=self.material_implementation.uuid)
        self.op = PublishMaterialRevisionSuccessHandler()

    def test_publish_material_revision_success_handler(self):
        """
        Test publish material revision success handler
        """
        handler_result = self.op(self.dto)
        self.assertIsInstance(handler_result, ValidateMaterialRevParamsDTO)
        result_revision = MaterialRevision.objects.filter(uuid=handler_result.uuid).first()
        self.assertEqual(self.material_revision.uuid, result_revision.uuid)
        self.assertEqual(result_revision.status, MaterialRevision.STATUS_PUBLISHED)
        self.assertEqual(result_revision, result_revision.material.active_revision)
