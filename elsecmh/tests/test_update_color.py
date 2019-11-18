from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.operations.update_color import UpdateColorOp
from elsecmh.models import (
    ColorGroup,
    Color,
)

from elsepublic.elsecmh.update_color import (
    UpdateColorParamsDTO,
    UpdateColorResultDTO,
)


class TestUpdateColor(TestBaseCmh):

    def setUp(self):
        super().setUp()

        color_group = ColorGroup.add_root(name='test_color_group')
        new_color_group = color_group.add_child()

        self.color = Color.objects.create(
            name='test_color',
            color_group=color_group,
            color_space='RGB',
            value='255, 0, 0',
            description='test color',
        )

        self.dto = UpdateColorParamsDTO(
            color_uuid=self.color.uuid,
            name='new_test',
            color_group_uuid=new_color_group.uuid,
            color_space='CMYK',
            value='255, 0, 0, 0',
            description='',
        )

        self.just_name_dto = UpdateColorParamsDTO(
            color_uuid=self.color.uuid,
            name='new_test',
        )

        self.op = UpdateColorOp()

    def test_update_color(self):
        """
        Test update color
        """
        updated_color_info = self.op(self.dto)

        self.assertIsInstance(updated_color_info, UpdateColorResultDTO)
        updated_color = Color.objects.get(uuid=updated_color_info.uuid)
        self.assertEqual(updated_color.name, self.dto.name)
        self.assertEqual(updated_color.color_group.uuid, self.dto.color_group_uuid)
        self.assertEqual(updated_color.color_space, self.dto.color_space)
        self.assertEqual(updated_color.value, self.dto.value)
        self.assertEqual(updated_color.description, self.dto.description)

    def test_update_color_name(self):
        """
        Test update color name
        """
        updated_color_info = self.op(self.just_name_dto)

        self.assertIsInstance(updated_color_info, UpdateColorResultDTO)
        updated_color = Color.objects.get(uuid=updated_color_info.uuid)
        self.assertEqual(updated_color_info.name, self.just_name_dto.name)
        self.assertEqual(self.color.color_group.uuid, updated_color.color_group.uuid)
        self.assertEqual(self.color.color_space, updated_color.color_space)
        self.assertEqual(self.color.value, updated_color.value)
        self.assertEqual(self.color.description, updated_color.description)
