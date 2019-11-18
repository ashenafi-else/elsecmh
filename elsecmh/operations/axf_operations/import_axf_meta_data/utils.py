import numpy as np
from elsecmh.models import MaterialMetaData
from elsecmh.else_axf.py import axf_sdk


def dict_parse_tree(o, parent=None):
    json_tree = dict()
    name = o.name.replace(parent, '').replace('/', '') if parent else o.name
    path_list = [
        'com.xrite.HemisphereLUTs/ViewHemisphere',
        'com.xrite.HemisphereLUTs/LightHemisphere',
        'com.xrite.Resources/Chunks',
        'com.xrite.Resources/DPVF/Chunks',
        'com.xrite.Resources/DPVF/Chunks',
        'Views',
        'Lights',
    ]
    if any(path in o.name for path in path_list):
        return name, 'binaryData'
    if hasattr(o, 'keys'):
        for k in o.keys():
            child_name, child_value = dict_parse_tree(o[k], o.name)
            json_tree[child_name] = child_value
        value = json_tree
    else:
        value = o.value
        if isinstance(value, (np.int_, np.intc, np.intp, np.int8,
                              np.int16, np.int32, np.int64, np.uint8,
                              np.uint16, np.uint32, np.uint64)):
            value = int(value)
        elif isinstance(value, (np.float_, np.float16, np.float32,
                                np.float64)):
            value = float(value)
        elif isinstance(value, (np.ndarray,)):
            value = value.tolist()
            new_list = []
            for elem in value:
                if isinstance(elem, (np.bytes_, bytes)):
                    new_list.append(elem.decode('utf-8'))
                else:
                    new_list.append(elem)
            value = new_list
        elif isinstance(value, (np.bytes_, np.byte, np.nbytes)):
            value = value.decode('utf-8')
        elif isinstance(value, bytes):
            value = value.decode('utf-8')
    if not parent:
        return value
    return name, value


def get_property_value(document, property_index, storage_type):
    prop_value = axf_sdk.get_metadata_property_value(
        document, property_index, storage_type)
    return prop_value


def save_metadata_doc(document, parent, level=0):
    document_name = axf_sdk.get_metadata_document_name(document)
    child = parent.add_child(key=document_name)
    properties_count = axf_sdk.get_number_of_metadata_properties(document)
    for property_index in range(properties_count):
        property_name = axf_sdk.get_metadata_property_name(
            document, property_index)
        storage_type = axf_sdk.get_metadata_property_type(
            document, property_index)
        property_value = get_property_value(
            document, property_index, storage_type)
        child.add_child(key=property_name, value=property_value)
    num_sub_docs = axf_sdk.get_number_of_metadata_sub_documents(document)
    for document_index in range(num_sub_docs):
        subdocument = axf_sdk.get_metadata_data_sub_document(
            document, document_index)
        save_metadata_doc(subdocument, child, level + 1)


def save_meta_data(file_name, material_revision):
    axf_file = axf_sdk.open_file(file_name, True, False)
    material = axf_sdk.get_default_material(axf_file)
    material_display_name = axf_sdk.get_default_material_name(axf_file)
    material_meta_data = MaterialMetaData.add_root(
        material_revision=material_revision,
        category=MaterialMetaData.AXF_META_DATA,
        key=material_display_name,
    )
    metadata_documents_count = axf_sdk.get_number_of_metadata_documents(
        material)
    for document_index in range(metadata_documents_count):
        metadata_document = axf_sdk.get_metadata_document(
            material, document_index)
        save_metadata_doc(metadata_document, material_meta_data)

    representation_child = material_meta_data.add_child(key='representation')
    representation = axf_sdk.get_preferred_representation(material)
    representation_class = axf_sdk.get_representation_class(representation)
    major, minor, revision = axf_sdk.get_representation_version(representation)
    representation_child.add_child(
        key='representation_class',
        value=representation_class)
    representation_child.add_child(
        key='representation_version', value=(
            '{} {} {}'.format(
                major, minor, revision)))

    representation_carpaint_flakes = None
    representation_carpaint_tab_brdf = None
    representation_diffuse = None
    representation_specular = None

    CLASSES_CARPAINT = [
        axf_sdk.AXF_REPRESENTATION_CLASS_CARPAINT,
        axf_sdk.AXF_REPRESENTATION_CLASS_CARPAINT2
    ]

    if representation_class in CLASSES_CARPAINT:
        representation_carpaint_flakes = axf_sdk.get_car_paint_flakes_btf_representation(
            representation)
        representation_child.add_child(
            key='carpaint_flakes',
            value=representation_carpaint_flakes)

        if representation_carpaint_flakes:
            representation_type_key = axf_sdk.get_representation_type_key(
                representation_carpaint_flakes)
            representation_child.add_child(
                key='flakes_type_key', value=representation_type_key)

        representation_carpaint_tab_brdf = axf_sdk.get_car_paint_tabulated_brdf_representation(
            representation)

        if representation_carpaint_tab_brdf:
            representation_type_key = axf_sdk.get_representation_type_key(
                representation_carpaint_tab_brdf)
            representation_child.add_child(
                key='representation_type_key',
                value=representation_type_key)

    CLASSES_SVBRDF = [
        axf_sdk.AXF_REPRESENTATION_CLASS_SVBRDF,
        axf_sdk.AXF_REPRESENTATION_CLASS_CARPAINT,
        axf_sdk.AXF_REPRESENTATION_CLASS_CARPAINT2
    ]

    if representation_class in CLASSES_SVBRDF:
        representation_diffuse = axf_sdk.get_svbrdf_diffuse_model_representation(
            representation)
        representation_child.add_child(
            key='representation_diffuse',
            value=representation_diffuse)

        if representation_diffuse:
            representation_type_key = axf_sdk.get_representation_type_key(
                representation_diffuse)
            representation_child.add_child(
                key='representation_type_key',
                value=representation_type_key)

        representation_specular = axf_sdk.get_svbrdf_specular_model_representation(
            representation)
        representation_child.add_child(
            key='representation_specular',
            value=representation_specular)

        if representation_specular:
            representation_type_key = axf_sdk.get_representation_type_key(
                representation_specular)
            representation_child.add_child(
                key='representation_type_key',
                value=representation_type_key)

            specular_model_variant, is_anisotropic, has_fresnel = axf_sdk.get_svbrdf_specular_model_variant(
                representation_specular)

            representation_child.add_child(
                key='specular_model_variant',
                value=specular_model_variant)
            representation_child.add_child(
                key='is_anisotropic', value=is_anisotropic)
            representation_child.add_child(
                key='has_fresnel', value=has_fresnel)

            if has_fresnel:
                specular_fresnel_variant = axf_sdk.get_svbrdf_specular_fresnel_variant(
                    representation_specular)
                representation_child.add_child(
                    key='specular_fresnel_variant',
                    value=specular_fresnel_variant)

    representation_resources_count = axf_sdk.get_number_of_representation_resources(
        representation)

    resources = representation_child.add_child(key='resources')
    for resource_index in range(representation_resources_count):
        resource = resources.add_child(key=resource_index)

        representation_resource = axf_sdk.get_representation_resource_from_index(
            representation, resource_index)

        if representation_resource:
            representation_resource_node_path = axf_sdk.get_resource_node_path(
                representation_resource)
            resource.add_child(
                key='node_path',
                value=representation_resource_node_path)

            if representation_resource_node_path:
                dims_count = axf_sdk.get_resource_data_num_dims(
                    representation_resource)
                resource.add_child(key='dims_count', value=dims_count)

                for dim_index in range(dims_count):
                    dims_extent = axf_sdk.get_resource_data_dim_extent(
                        representation_resource, dim_index)
                    resource.add_child(key='dims_extent', value=dims_extent)

                representation_resource_lookup_path = axf_sdk.get_resource_lookup_path(
                    representation_carpaint_flakes, representation_resource)
                resource.add_child(
                    key='lookup_path',
                    value=representation_resource_lookup_path)

                if representation_carpaint_flakes:
                    carpaint_flakes_lookup_path = axf_sdk.get_resource_lookup_path(
                        representation_carpaint_flakes, representation_resource)
                    resource.add_child(
                        key='carpaint_flakes_lookup_path',
                        value=carpaint_flakes_lookup_path)

                if representation_carpaint_tab_brdf:
                    carpaint_tab_brdf_lookup_path = axf_sdk.get_resource_lookup_path(
                        representation_carpaint_tab_brdf, representation_resource)
                    resource.add_child(
                        key='carpaint_tab_brdf_lookup_path',
                        value=carpaint_tab_brdf_lookup_path)

                if representation_diffuse:
                    diffuse_lookup_path = axf_sdk.get_resource_lookup_path(
                        representation_diffuse, representation_resource)
                    resource.add_child(
                        key='diffuse_lookup_path',
                        value=diffuse_lookup_path)

                if representation_specular:
                    specular_lookup_path = axf_sdk.get_resource_lookup_path(
                        representation_specular, representation_resource)
                    resource.add_child(
                        key='specular_lookup_path',
                        value=specular_lookup_path)

                representation_lookup_path = axf_sdk.get_resource_lookup_path(
                    representation, representation_resource)
                resource.add_child(
                    key='representation_lookup_path',
                    value=representation_lookup_path)
