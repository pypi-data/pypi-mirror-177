"""

DocStringTransformer
"""
from typing import Any, Union, Dict, List
import libcst as cst
from jinja2 import Template

Statement = Union[cst.Module, cst.ClassDef, cst.FunctionDef]
Templates = Dict[Any, Template]


class DocstringTransformer(cst.CSTTransformer):
    """

    DocstringTransformer class

    Args:
        templates (Templates): templates instance
        indents_func (list): indents func list
        indents_class (list): indents class list
        module_name (str): module name

    """

    def __init__(
        self,
        templates: Templates,
        indents_func: list,
        indents_class: list,
        raises: Dict[str, List[cst.Raise]],
        module_name: str,
    ):
        """

        __init__ function

        Args:
            templates (Templates): templates instances
            indents_func (list): indents func list
            indents_class (list): indents class list
            raise (Dict[str, List[cst.Raise]]): raises with function name
                as key and Raise instance as value
            module_name (str): module name

        """
        cst.CSTTransformer.__init__(self)
        self._templates = templates
        self._module_name = module_name
        self._indents_func = indents_func
        self._indents_class = indents_class
        self._raises = raises

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:
        """

        leave_ClassDef function

        Args:
            original_node (cst.ClassDef): original node
            updated_node (cst.ClassDef): updated node after leaving

        Returns:
            cst.ClassDef: new class def

        """
        _indent = self._indents_class.pop(0)
        for item in original_node.body.body:
            if (
                isinstance(item, cst.SimpleStatementLine)
                and isinstance(item.body[0], cst.Expr)
                and isinstance(item.body[0].value, cst.SimpleString)
            ):
                break
        else:
            _init_args = next(
                filter(
                    lambda x: isinstance(x, cst.FunctionDef)
                    and x.name.value == "__init__",
                    original_node.body.body,
                ),
                None,
            )
            _attributes = []
            for item in original_node.body.body:
                if (
                    isinstance(item, cst.SimpleStatementLine)
                    and isinstance(item.body[0], cst.AnnAssign)
                    and isinstance(item.body[0].annotation.annotation, cst.Name)
                ):
                    _attributes.append(
                        {
                            "name": item.body[0].target.value,
                            "annotation": item.body[0].annotation.annotation.value,
                        }
                    )
                elif (
                    isinstance(item, cst.SimpleStatementLine)
                    and isinstance(item.body[0], cst.AnnAssign)
                    and isinstance(item.body[0].annotation, cst.Annotation)
                ):
                    _return_type = ".".join(
                        [
                            item.body[0].annotation.annotation.value.value,
                            item.body[0].annotation.annotation.attr.value,
                        ]
                    )
                    _attributes.append(
                        {"name": item.body[0].target.value, "annotation": _return_type}
                    )

            _args = []
            if _init_args:
                for item in _init_args.params.params:
                    if item.name.value == "self":
                        continue
                    if not item.annotation:
                        _args.append({"name": item.name.value, "annotation": "Any"})
                    else:
                        _args.append(
                            {
                                "name": item.name.value,
                                "annotation": generate_typing_str(item.annotation),
                            }
                        )

            _args = {
                "name": original_node.name.value,
                "attributes": _attributes,
                "_indent": _indent,
                "args": _args,
            }
            _res = self._templates[cst.ClassDef].render(_args)
            exist = updated_node.body.body
            _complete_indent = " " * (_indent + 4)
            _res = f'"""{_res}{_complete_indent}"""'
            return updated_node.with_changes(
                body=updated_node.body.with_changes(
                    body=(
                        cst.SimpleStatementLine(
                            body=[cst.Expr(value=cst.SimpleString(value=_res))]
                        ),
                    )
                    + tuple(exist)
                )
            )
        return updated_node

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.CSTNode:
        """

        leave_Module function

        Args:
            original_node (cst.Module): original node
            updated_node (cst.Module): node updated

        Returns:
            cst.Module: node updated

        """
        #       return original_node.with_changes(has_trailing_newline=False)
        for item in original_node.body:
            if (
                isinstance(item, cst.SimpleStatementLine)
                and isinstance(item.body[0], cst.Expr)
                and isinstance(item.body[0].value, cst.SimpleString)
            ):
                break
        else:
            _attributes = []
            for item in original_node.body:
                if isinstance(item, cst.SimpleStatementLine) and isinstance(
                    item.body[0], cst.Assign
                ):
                    _attributes.append(
                        {
                            "name": item.body[0].targets[0].target.value,
                            "annotation": "Any",
                        }
                    )
                elif isinstance(item, cst.SimpleStatementLine) and isinstance(
                    item.body[0], cst.AnnAssign
                ):
                    _attributes.append(
                        {
                            "name": item.body[0].target.value,
                            "annotation": generate_typing_str(item.body[0].annotation),
                        }
                    )

            _args = {"name": self._module_name, "attributes": _attributes}
            _res = self._templates[cst.Module].render(_args)
            _res = f'"""{_res}"""'
            exist = updated_node.body
            return updated_node.with_changes(
                body=(
                    cst.SimpleStatementLine(
                        body=[cst.Expr(value=cst.SimpleString(value=_res))]
                    ),
                )
                + exist
            )
        return updated_node

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.CSTNode:  # pylint: disable=too-many-branches
        """

        leave_FunctionDef function, callback on leave function

        Args:
            original_node (cst.FunctionDef): original function def
            updated_node (cst.FunctionDef): function def updated

        Returns:
            cst.FunctionDef: function def updated

        """
        found = False
        _indent = self._indents_func.pop(0)
        for item in original_node.body.body:
            if isinstance(item.body, list):
                for block in item.body:
                    if isinstance(block, cst.Expr) and isinstance(
                        block.value, cst.SimpleString
                    ):
                        found = True
                        break
            if found:
                break
        else:
            _raises = [
                item.exc.func.value for item in self._raises[original_node.name.value]
            ]
            # Not found expr
            _return_type = None
            if original_node.returns:
                _return_type = generate_typing_str(original_node.returns.annotation)

            _params = []
            for item in original_node.params.params:
                if item.name.value == "self":
                    continue
                if not item.annotation:
                    _params.append({"name": item.name.value, "annotation": "Any"})
                elif isinstance(item.annotation, cst.Annotation):
                    _params.append(
                        {
                            "name": item.name.value,
                            "annotation": generate_typing_str(item.annotation),
                        }
                    )

            _args = {
                "name": original_node.name.value,
                "params": _params,
                "return_type": _return_type,
                "_indent": _indent,
                "raises": _raises,
            }
            _res = self._templates[cst.FunctionDef].render(_args)
            _complete_indent = " " * (_indent + 4)
            _res = f'"""\n{_res}\n{_complete_indent}"""'
            #           updated_node.body.body = cst.Expr(value=_res) + (updated_node.body.body,)
            exist = updated_node.body.body
            _updated_node = updated_node.with_changes(
                body=updated_node.body.with_changes(
                    body=(
                        cst.SimpleStatementLine(
                            body=[cst.Expr(value=cst.SimpleString(value=_res))]
                        ),
                    )
                    + exist
                )
            )
            return _updated_node
        return updated_node


def generate_typing_str(annotation: Any) -> str:
    """

    generate_typing_str function

    Args:
        annotation (Any): annotation

    Raises:
      Exception: Unkown annotation type

    Returns:
        str: typing string

    """
    if isinstance(annotation, cst.Subscript):
        if isinstance(annotation.value, cst.Attribute):
            _namespace = [
                annotation.value.value.value,
                annotation.value.attr.value,
            ]
        else:
            _namespace = [
                annotation.value.value,
            ]
        _return_type = ".".join(_namespace)
        _arr = []
        for _slice in annotation.slice:
            _arr.append(
                generate_typing_str(_slice.slice)
                if isinstance(_slice, cst.SubscriptElement)
                else _slice.slice.value.value
            )
        _return_type += f"[{', '.join(_arr)}]"
        return _return_type
    if isinstance(annotation, cst.Annotation):
        return generate_typing_str(annotation.annotation)
    if isinstance(annotation, cst.Index):
        return generate_typing_str(annotation.value)
    if isinstance(annotation, cst.Ellipsis):
        return "..."
    if isinstance(annotation, cst.SubscriptElement):
        return generate_typing_str(annotation.slice)
    if isinstance(annotation, cst.Name):
        return annotation.value
    if isinstance(annotation, cst.Attribute):
        _namespace = [
            generate_typing_str(annotation.value.value),
            generate_typing_str(annotation.attr.value),
        ]
        return ".".join(_namespace)
    if isinstance(annotation, cst.SimpleString):
        return annotation.value
    if isinstance(annotation, str):
        return annotation
    raise Exception(f"Unkown type object {type(annotation)}")
