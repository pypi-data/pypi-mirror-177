from noloco.constants import (
    BOOLEAN,
    COLLECTION,
    DATE,
    DECIMAL,
    DURATION,
    INTEGER,
    TEXT,
    MANY_TO_MANY,
    MANY_TO_ONE,
    MULTIPLE_OPTION,
    ONE_TO_MANY,
    ONE_TO_ONE,
    SINGLE_OPTION,
    TEXT)
from noloco.exceptions import (
    NolocoDataTypeNotFoundError,
    NolocoQueryNotSupportedError)
from pydash import (
    find,
    get,
    camel_case)


def pascal_case(str):
    camel = camel_case(str)
    return camel[:1].upper() + camel[1:]


def annotate_collection_args(data_type, data_types, args):
    annotated_args = {}

    # Process top-level supported parameters.
    if get(args, 'after') is not None:
        annotated_args['after'] = {'type': 'String', 'value': args['after']}
    if get(args, 'after') is None and get(args, 'before') is not None:
        annotated_args['before'] = {'type': 'String', 'value': args['before']}
    if get(args, 'first') is not None:
        annotated_args['first'] = {'type': 'Int', 'value': args['first']}
    if get(args, 'order_by') is not None:
        annotated_args['orderBy'] = {
            'type': 'OrderBy',
            'value': args['order_by']
        }
    if get(args, 'where') is not None:
        whereType = pascal_case(data_type['name']) + 'WhereInput'
        annotated_args['where'] = {'type': whereType, 'value': args['where']}

    # Recursively process nested supported parameters.
    if get(args, 'include') is not None:
        annotated_args['include'] = {}

        for nested_data_type_name, nested_args in args['include'].items():
            if nested_args is not True:
                relationship_data_type = find_relationship_data_type(
                    nested_data_type_name,
                    data_type['name'],
                    data_type['fields'],
                    data_types)['data_type']
                annotated_args['include'][nested_data_type_name] = \
                    annotate_collection_args(
                        relationship_data_type,
                        data_types,
                        nested_args)
            else:
                annotated_args['include'][nested_data_type_name] = True

    return annotated_args


def build_operation_arg(arg_name, arg_value):
    arg_type = arg_value['type']
    return f'${arg_name}: {arg_type}'


def build_operation_args(args):
    operation_arg_list = ', '.join([build_operation_arg(
        arg_name, arg_value) for arg_name, arg_value in args.items()])

    if operation_arg_list:
        return f'({operation_arg_list})'
    else:
        return ''


def build_data_type_arg(arg_full_name):
    arg_name = arg_full_name.split('_')[-1]
    return f'{arg_name}: ${arg_full_name}'


def build_data_type_args(args):
    data_type_arg_list = ', '.join(
        [build_data_type_arg(arg_name) for arg_name in args.keys()])
    if data_type_arg_list:
        return f'({data_type_arg_list})'
    else:
        return ''


def change_where_to_lookup(data_type, options):
    where = options.pop('where')['value']
    lookup_key = list(where.keys())[0]

    lookup_field = find_field_by_name(lookup_key, data_type['fields'])
    lookup_type = gql_type(data_type, lookup_field)
    lookup_value = where[lookup_key]['equals']

    if lookup_key == 'id':
        lookup_type = 'ID'

    options[lookup_key] = {'type': lookup_type, 'value': lookup_value}

    return options


def find_data_type_by_name(data_type_name, data_types):
    data_type = find(
        data_types,
        lambda project_data_type: project_data_type['name'] == data_type_name)

    if data_type is None:
        raise NolocoDataTypeNotFoundError(data_type_name)
    else:
        return data_type


def find_field_by_name(field_name, fields):
    field = find(
        fields,
        lambda data_type_field: data_type_field['name'] == field_name)

    return field


def find_relationship_data_type(
        relationship_name,
        data_type_name,
        data_type_fields,
        data_types):
    relationship_field = find_field_by_name(
        relationship_name,
        data_type_fields)

    if relationship_field is not None:
        # If the relationship field exists on the parent data type then
        # this is a forward relationship and we can simply look up the
        # relationship data type by the corresponding field type.
        return {
            'data_type': find_data_type_by_name(
                relationship_field['type'], data_types),
            'is_collection': is_multi_relationship(relationship_field['relationship'])
        }
    else:
        # If there isn't a corresponding relationship field on the
        # parent data type then this is a reverse relationship and we
        # have to search for the relationship data type.
        for candidate_data_type in data_types:
            for field in candidate_data_type['fields']:
                # We are looking for any fields whose type matches up with the
                # name of the parent data type that the reverse relationship is
                # from.
                if field['type'] == data_type_name:
                    # If the reverse name is populated and matches the parent
                    # type then we have found the data type the relationship
                    # goes to.
                    is_collection = field['relationship'] == MANY_TO_MANY or \
                        field['relationship'] == MANY_TO_ONE
                    if reverse_name_matches_relationship_name(
                            field, is_collection, relationship_name):
                        return {
                            'data_type': candidate_data_type,
                            'is_collection': is_collection
                        }
                    # If the reverse name is not populated but this field is a
                    # one-to-one relationship and the data type name matches
                    # the relationship name then we have found the data type
                    # the relationship goes to.
                    elif field['relationship'] == ONE_TO_ONE:
                        if candidate_data_type['name'] == relationship_name:
                            return {
                                'data_type': candidate_data_type,
                                'is_collection': False
                            }


def flatten_args(data_type_name, args):
    flattened_args = {}

    for arg_name, arg_value in args.items():
        if arg_name != 'include':
            flattened_args[data_type_name + '_' + arg_name] = arg_value
        else:
            for nested_data_type_name, nested_args in args['include'].items():
                if nested_args is not True:
                    flattened_nested_args = flatten_args(
                        data_type_name + '_' + nested_data_type_name,
                        nested_args)

                    for flattened_nested_arg in flattened_nested_args.keys():
                        flattened_args[flattened_nested_arg] = \
                            flattened_nested_args[flattened_nested_arg]

    return flattened_args


def gql_args(args):
    variables = {}

    for arg in args:
        variables[arg] = args[arg]['value']

    return variables


def gql_type(data_type, data_type_field, is_required=False):
    field_type = data_type_field['type']

    if field_type == TEXT:
        return with_required('String', is_required)
    elif field_type == DATE:
        return with_required('DateTime', is_required)
    elif field_type == INTEGER:
        return with_required('Int', is_required)
    elif field_type == DECIMAL:
        return with_required('Float', is_required)
    elif field_type == DURATION:
        return with_required('Duration', is_required)
    elif field_type == BOOLEAN:
        return with_required('Boolean', is_required)
    elif field_type == SINGLE_OPTION:
        enum_prefix = pascal_case(data_type['name'])
        enum_suffix = pascal_case(data_type_field['name'])
        return with_required(f'{enum_prefix}{enum_suffix}', is_required)
    elif field_type == MULTIPLE_OPTION:
        enum_prefix = pascal_case(data_type['name'])
        enum_suffix = pascal_case(data_type_field['name'])
        return with_required(f'[{enum_prefix}{enum_suffix}!]', is_required)


def has_files(args):
    for arg_value in args.values():
        if 'Upload' in arg_value['type']:
            return True

    return False


def options_without_data(options):
    new_options = {}

    for option in options.keys():
        if option != 'data':
            new_options[option] = options[option]

    return new_options


def result_name_suffix(query):
    if query == 'findMany':
        return 'Collection'
    elif query == 'findUnique':
        return ''
    else:
        raise NolocoQueryNotSupportedError(query)


def is_multi_relationship(relationship):
    return relationship == ONE_TO_MANY or relationship == MANY_TO_MANY


def is_reverse_multi_relationship(relationship):
    return relationship == MANY_TO_ONE or relationship == MANY_TO_MANY


def reverse_name_matches_relationship_name(
        field,
        is_collection,
        relationship_name):
    reverse_name = field['reverseName']

    if reverse_name is None or reverse_name == '':
        return False
    elif is_collection:
        reverse_collection_name = field['reverseName'] + COLLECTION
        return reverse_collection_name == relationship_name
    else:
        return reverse_name == relationship_name


def with_required(gql_type, is_required):
    if is_required:
        return f'{gql_type}!'
    else:
        return gql_type
