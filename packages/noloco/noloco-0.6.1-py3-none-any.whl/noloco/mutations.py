from noloco.exceptions import (
    NolocoFieldNotFoundError,
    NolocoInvalidMultiFieldConnectionError,
    NolocoInvalidSingleFieldConnectionError,
    NolocoUnknownError)
from noloco.fields import DataTypeFieldsBuilder
from noloco.utils import (
    build_operation_args,
    gql_type,
    with_required,
    is_multi_relationship,
    is_reverse_multi_relationship, pascal_case,
    with_required)
from pydash import (
    find,
    get
)


DATA_TYPE_MUTATION = '''mutation{mutation_args} {{
  {mutation_fragment}
}}'''


class MutationBuilder:
    def __init__(self):
        self.fields_builder = DataTypeFieldsBuilder()

    def build_data_type_mutation_args(self, data_type, data_types, args):
        mutation_args = {}

        for arg_name, arg_value in args.items():
            data_type_fields = [
                field
                for field
                in data_type['fields']
                if field['name'] == arg_name]
            data_type_field = find(data_type_fields)

            if data_type_field is not None:
                is_required = data_type_field['required']

                # The field is either a top-level or relationship field on the
                # data type.
                if data_type_field['relationship'] is None and \
                        data_type_field['type'] != 'file':
                    # This is a top-level field, so map the arg onto a
                    # primitive.
                    mutation_args[arg_name] = {
                        'type': gql_type(
                            data_type,
                            data_type_field,
                            is_required),
                        'value': arg_value}
                elif get(arg_value, 'connect') is not None:
                    # This is a relationship field, so map the arg onto an Id
                    # arg.
                    # TODO - stronger validation and error handling.
                    # TODO - consider supporting connecting on other fields.

                    connection_value = arg_value['connect']
                    if is_multi_relationship(data_type_field['relationship']):

                        if not isinstance(connection_value, list):
                            raise NolocoInvalidMultiFieldConnectionError(
                                arg_name)

                        mutation_args[arg_name + 'Id'] = {
                            'type': with_required('[ID!]', is_required),
                            'value': [connection['id'] for connection in connection_value]
                        }
                    else:
                        if not isinstance(connection_value, dict):
                            raise NolocoInvalidSingleFieldConnectionError(
                                arg_name)

                        mutation_args[arg_name + 'Id'] = {
                            'type': with_required('ID', is_required),
                            'value': connection_value['id']
                        }
                elif data_type_field['type'] == 'file':
                    # This is a file upload field, so map the arg onto an
                    # Upload arg, although do not open the file yet.
                    # TODO - stronger validation and error handling.
                    if is_multi_relationship(data_type_field['relationship']):
                        mutation_args[arg_name] = {
                            'type': with_required('[Upload!]', is_required),
                            'value': arg_value
                        }
                    else:
                        mutation_args[arg_name] = {
                            'type': with_required('Upload', is_required),
                            'value': arg_value
                        }
                else:
                    raise NolocoUnknownError()
            else:
                # The field is a reverse relationship field to the data type or
                # doesn't exist.
                for related_data_type in data_types:
                    for field in related_data_type['fields']:
                        if field['type'] == data_type['type'] and \
                                field['reverseName'] == arg_name:
                            related_field = field

                if related_field is not None:
                    # This is a reverse relationship field and can be
                    # connected.
                    if is_reverse_multi_relationship(related_field['relationship']):
                        connection_value = arg_value['connect']

                        if not isinstance(connection_value, list):
                            raise NolocoInvalidMultiFieldConnectionError(
                                arg_name)

                        mutation_args[arg_name + 'Id'] = {
                            'type': with_required('[ID!]', related_field['required']),
                            'value': [connection['id'] for connection in connection_value]
                        }
                    else:
                        connection_value = arg_value['connect']

                        if not isinstance(connection_value, dict):
                            raise NolocoInvalidSingleFieldConnectionError(
                                arg_name)

                        mutation_args[arg_name + 'Id'] = {
                            'type': with_required('ID', related_field['required']),
                            'value': connection_value['id']
                        }
                else:
                    # This field doesn't exist on the type.
                    raise NolocoFieldNotFoundError(arg_name)

        return mutation_args

    def build_data_type_mutation(
            self,
            mutation,
            data_type,
            data_types,
            options,
            flattened_options):
        mutation_args = build_operation_args(flattened_options)

        mutation_fragment = self.fields_builder.build_fields(
            mutation + pascal_case(data_type['name']),
            data_type,
            data_types,
            options)

        return DATA_TYPE_MUTATION.format(
            mutation_args=mutation_args,
            mutation_fragment=mutation_fragment)
