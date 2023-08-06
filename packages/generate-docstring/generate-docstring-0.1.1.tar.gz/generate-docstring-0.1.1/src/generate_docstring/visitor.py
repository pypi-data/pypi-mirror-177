"""

Visitor class
"""
import libcst as cst


class Visitor(cst.CSTVisitor):
    """

    Visitor class

    """

    def __init__(self):
        """

        __init__ function

        """
        self.indent = 0
        self.indents_func = []
        self.indents_class = []
        self.raises = {}
        self.current_function_name = None
        self.in_func = False

    def on_visit(self, node: cst.CSTNode) -> bool:
        """

        on_visit function

        Args:
            node (cst.FunctionDef): node to visit

        Returns:
            bool: return always True

        """
        if isinstance(node, cst.IndentedBlock):
            self.indent += 4
        elif isinstance(node, cst.FunctionDef):
            self.in_func = True
            self.current_function_name = node.name.value
            self.raises[self.current_function_name] = []
        return True

    def on_leave(self, original_node: cst.CSTNode):
        """

        on_leave function

        Args:
            original_node (cst.FunctionDef): node on leave

        """
        if isinstance(original_node, cst.IndentedBlock):
            self.indent -= 4
        elif isinstance(original_node, cst.FunctionDef):
            self.indents_func.append(self.indent)
            self.in_func = False
        elif isinstance(original_node, cst.ClassDef):
            self.indents_class.append(self.indent)
#       elif isinstance(original_node, cst.Module):
#           _docstring = original_node.get_docstring()

    def visit_Raise_exc(self, node: cst.CSTNode):
        """

        visit_Raise_exc add raises to current function

        Args:
            node (cst.CSTNode): raise node
        """
        if self.in_func:
            self.raises[self.current_function_name].append(node)
