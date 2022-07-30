import ast

from flake8_django.checkers.base_model_checker import BaseModelChecker
from flake8_django.checkers.issue import Issue


class DJ10(Issue):
    code = 'DJ10'
    description = 'Model should define verbose_name in its Meta inner class'


class DJ11(Issue):
    code = 'DJ11'
    description = 'Model should define verbose_name_plural in its Meta inner class'


class ModelMetaChecker(BaseModelChecker):
    model_name_lookup = 'Model'

    def checker_applies(self, node):
        return any(
            (
                self.is_model_name_lookup(base)
                or self.is_models_name_lookup_attribute(base)
            )
            and not self.is_abstract_model(node)
            for base in node.bases
        )

    @staticmethod
    def has_meta_class(element):
        # for node in element.body[0].body:  # type: ignore
        for node in element.body:  # type: ignore
            if isinstance(node, ast.ClassDef) and node.name == 'Meta':
                return node
        return

    def has_verbose_name(self, meta_class_node):
        return self._has_element(meta_class_node, 'verbose_name')

    def has_verbose_name_plural(self, meta_class_node):
        return self._has_element(meta_class_node, 'verbose_name_plural')

    @staticmethod
    def _has_element(element, target_name):
        for node in ast.iter_child_nodes(element):
            if not isinstance(node, ast.Assign):
                continue
            if not isinstance(node.targets[0], ast.Name):
                continue
            attr = node.targets[0].id
            if attr == target_name:
                return True
        return False

    def run(self, node):
        """
        Check a single model.
        """
        if not self.checker_applies(node):
            return

        meta_class_node = self.has_meta_class(node)

        issues = []
        if not meta_class_node or not self.has_verbose_name(meta_class_node):
            issues.append(
                DJ10(
                    lineno=node.lineno,
                    col=node.col_offset,
                )
            )

        if not meta_class_node or not self.has_verbose_name_plural(meta_class_node):
            issues.append(
                DJ11(
                    lineno=node.lineno,
                    col=node.col_offset,
                )
            )

        return issues
