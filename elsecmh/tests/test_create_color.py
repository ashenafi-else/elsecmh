from elsecmh.tests.test_base_cmh import TestBaseCmh
from elsecmh.operations.create_color import CreateColorOp
from elsecmh.models import (
    ColorGroup,
    Color,
)
from elsepublic.elsecmh.create_color import (
    CreateColorParamsDTO,
    CreateColorResultDTO,
)


class TestCreateColor(TestBaseCmh):

    def setUp(self):
        super().setUp()

        color_group = ColorGroup.add_root(name='test_color_group')

        self.dto = CreateColorParamsDTO(
            name='test_color',
            color_group_uuid=color_group.uuid,
            color_space='RGB',
            value='255, 0, 0',
            description='test color',
        )

        self.op = CreateColorOp()

    def test_create_color(self):
        """
        Test create color
        """
        created_color_info = self.op(self.dto)

        self.assertIsInstance(created_color_info, CreateColorResultDTO)
        created_color = Color.objects.get(uuid=created_color_info.uuid)
        self.assertEqual(created_color.name, self.dto.name)
        self.assertEqual(created_color.color_group.uuid, self.dto.color_group_uuid)
        self.assertEqual(created_color.color_space, self.dto.color_space)
        self.assertEqual(created_color.value, self.dto.value)
        self.assertEqual(created_color.description, self.dto.description)
