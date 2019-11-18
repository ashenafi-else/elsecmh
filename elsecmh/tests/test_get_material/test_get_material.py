import os
from unittest.mock import (
    Mock,
    patch,
)
from elsecmh.operations.get_material.get_material import GetMaterialOp
from elsecommon import marshalling

from elsecmh.models import (
    Material,
    MaterialRevision,
    MaterialImplementation,
)
from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecommon.tests.helpers import RouterMock
from elsepublic.elsecmh.dto.get_material import GetMaterialParamsDTO
from elsepublic.elsecmh.interfaces.get_material_implementation import GetMaterialImplementationOpInterface
from elsepublic.elsecmh.interfaces.publish_existed_material import PublishExistedMaterialOpInterface
from elsepublic.exceptions import MissingMaterialException


class TestGetMaterial(TestBaseCmh):
    test_path = os.path.dirname(os.path.realpath(__file__))
    fixtures_path = os.path.join(test_path, '..', 'fixtures')

    def setUp(self):
        super().setUp()

        material = Material.objects.create(name='mat_nappa', material_group=self.root)
        self.material_revision1 = MaterialRevision.objects.create(
            material=material,
            material_info={
                'name': material.name,
                'type': 'sometype',
                'available_colors': ['191A1B', '1B2028']
            },
            status=MaterialRevision.STATUS_PUBLISHED
        )
        material.active_revision = self.material_revision1
        material.save()
        self.material_implementation1 = MaterialImplementation.objects.create(
            material_revision=self.material_revision1,
            name='mat_nappa_191A1B'
        )
        self.existed_material_dto = GetMaterialParamsDTO(color_name='mat_nappa_191A1B')
        self.publish_existed_material_dto = GetMaterialParamsDTO(color_name='mat_nappa_1B2028')
        self.not_available_color_name_dto = GetMaterialParamsDTO(color_name='mat_nappa_E62900')
        self.wrong_color_name_dto = GetMaterialParamsDTO(color_name='mat_cotton_C1BFC2')

        self.op = GetMaterialOp()

        self.router_mock = RouterMock()
        self.router_mock[GetMaterialImplementationOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.router_mock[PublishExistedMaterialOpInterface] = Mock(spec=marshalling.ElseOperation)
        self.patch = patch(
            'elsecmh.operations.get_material.get_material.Router',
            new=self.router_mock
        )

    def test_get_material_implementation(self):
        """
        Test get material implementation
        """
        with self.patch:
            get_material_result = self.op(self.existed_material_dto)
            self.assertIsNone(get_material_result)
            publish_existed_mat_mock = self.router_mock[PublishExistedMaterialOpInterface.uri]
            self.assertFalse(publish_existed_mat_mock.called)
            get_mat_impl_mock = self.router_mock[GetMaterialImplementationOpInterface.uri]
            self.assertEqual(get_mat_impl_mock.call_count, 1)
            get_mat_impl_dto, context = get_mat_impl_mock.call_args
            self.assertEqual(get_mat_impl_dto[0].uuid, self.material_implementation1.uuid)

    def test_publish_existed_material(self):
        """
        Test publish existed material 
        """
        with self.patch:
            get_material_result = self.op(self.publish_existed_material_dto)
            self.assertIsNone(get_material_result)
            get_mat_impl_mock = self.router_mock[GetMaterialImplementationOpInterface.uri]
            self.assertFalse(get_mat_impl_mock.called)
            publish_existed_mat_mock = self.router_mock[PublishExistedMaterialOpInterface.uri]
            self.assertEqual(publish_existed_mat_mock.call_count, 1)
            publish_existed_mat_dto, context = publish_existed_mat_mock.call_args
            self.assertEqual(publish_existed_mat_dto[0].uuid, self.material_revision1.uuid)

    def test_missing_material(self):
        """
        Test missing material
        """
        with self.assertRaises(MissingMaterialException):
            self.op(self.wrong_color_name_dto)
