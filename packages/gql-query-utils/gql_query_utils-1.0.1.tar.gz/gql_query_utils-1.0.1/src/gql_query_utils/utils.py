"""
Python script that converts GraphQL query to dictionary using graphql-core python package
"""
from graphql import parse
from graphql.language import ast


def _node_to_dict(node: ast.Node) -> dict:
    """
    Convert GraphQL AST Node into dictionary

    :param node: GraphQL AST Node
    :return: result dictionary
    """
    if node.kind == "document":
        doc: ast.DocumentNode = node
        defs = {}
        for definition in doc.definitions:
            defs = {**defs, **_node_to_dict(definition)}
        return defs
    if node.kind == "operation_definition":
        op: ast.OperationDefinitionNode = node
        if op.operation == ast.OperationType.QUERY:
            return {op.operation.value: _node_to_dict(op.selection_set)}
    elif node.kind == "selection_set":
        ss: ast.SelectionSetNode = node
        selections = ss.selections
        sel_dict = {}
        for selection in selections:
            sel_dict = {**sel_dict, **_node_to_dict(selection)}
        return sel_dict
    elif node.kind == "field":
        field: ast.FieldNode = node
        args = {}
        for arg in field.arguments:
            args = {**args, **_node_to_dict(arg)}
        value = {'__args': args} if len(args) else {}
        if field.selection_set is not None:
            value = {**value, **_node_to_dict(field.selection_set)}
        else:
            value = True
        return {field.name.value: value}
    elif node.kind == "argument":
        arg: ast.ArgumentNode = node
        return {arg.name.value: _node_to_dict(arg.value)}
    elif node.kind == "string_value" \
            or node.kind == "int_value" \
            or node.kind == "float_value"\
            or node.kind == "boolean_value":
        s_val: ast.StringValueNode = node
        return s_val.value
    elif node.kind == "list_value":
        l_val: ast.ListValueNode = node
        value = []
        for val in l_val.values:
            value.append(_node_to_dict(val))
        return value
    elif node.kind == "object_value":
        o_val: ast.ObjectValueNode = node
        value = {}
        for field in o_val.fields:
            value = {**value, **_node_to_dict(field)}
        return value
    elif node.kind == "object_field":
        o_field: ast.ObjectFieldNode = node
        return {o_field.name.value: _node_to_dict(o_field.value)}
    else:
        print(node.to_dict())


def query_to_dict(query: str) -> dict:
    root_node = parse(query)
    result = _node_to_dict(root_node)
    return result
