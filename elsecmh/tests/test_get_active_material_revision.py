import os
from elsecmh.models import (
    Material,
    MaterialRevision,
    Color,
    MaterialImplementation,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsepublic.elsecmh.dto.get_active_material_revision import (
    GetActiveMaterialRevisionParamsDTO,
    GetActiveMaterialRevisionResultDTO,
)
from elsecmh.operations.get_active_material_revision import GetActiveMaterialRevisionOp
from elsepublic.exceptions import (
    MissingMaterialException,
    MissingActiveMaterialRevisionException,
)


class TestGetActiveMaterialRevision(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, 'fixtures')
    fixtures_models_path = os.path.join(test_path, 'fixtures', 'common_test_data.json')
    fixtures_implementation_models_path = os.path.join(test_path, 'fixtures', 'color_test_data.json')
    fixtures = (fixtures_models_path, fixtures_implementation_models_path)

    def setUp(self):
        super().setUp()
        self.test_material = Material.objects.create(name='test_material1', material_group=self.root)
        self.color = Color.objects.get(uuid='e29dcd47-6965-4d01-a208-7a0418716c90')
        self.test_revision = MaterialRevision.objects.create(
            material=self.test_material,
            status=MaterialRevision.STATUS_PUBLISHED,
            default_color=self.color,
        )
        MaterialImplementation.objects.create(
            name='test_implementation',
            material_revision=self.test_revision,
            color=self.color,
        )

        self.test_material.active_revision = self.test_revision
        self.test_material.save()

        self.test_material_without_active_revision = Material.objects.create(
            name='test_material2',
            material_group=self.root,
        )

        self.get_active_material_revision_dto = GetActiveMaterialRevisionParamsDTO(
            material_name=self.test_material.name,
        )

        self.get_active_revision_of_missing_material_dto = GetActiveMaterialRevisionParamsDTO(
            material_name='Missing material',
        )

        self.get_missing_active_material_revision_dto = GetActiveMaterialRevisionParamsDTO(
            material_name=self.test_material_without_active_revision.name,
        )

        self.op = GetActiveMaterialRevisionOp()

    def test_get_active_material_revision(self):
        """
        Test get active material revision
        """
        result = self.op(self.get_active_material_revision_dto)
        self.assertIsInstance(result, GetActiveMaterialRevisionResultDTO)
        self.assertEqual(result.revision_uuid, self.test_revision.uuid)
        self.assertEqual(result.material_name, self.test_material.name)
        self.assertEqual(result.material_info, self.test_revision.material_info)
        self.assertEqual(result.colors[0].name, result.default_color.name, self.color.name)
        self.assertEqual(result.colors[0].color_space, result.default_color.color_space, self.color.color_space)
        self.assertEqual(result.colors[0].value, result.default_color.value, self.color.value)
        self.assertEqual(result.colors[0].description, result.default_color.description, self.color.description)

    def test_get_active_revision_of_missing_material(self):
        """
        Test get active revision of missing material
        """
        with self.assertRaises(MissingMaterialException):
            self.op(self.get_active_revision_of_missing_material_dto)

    def test_get_missing_active_material_revision(self):
        """
        Test get missing active material revision
        """
        with self.assertRaises(MissingActiveMaterialRevisionException):
            self.op(self.get_missing_active_material_revision_dto)
