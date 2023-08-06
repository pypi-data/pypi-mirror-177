import itertools
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple

import pypika
import sqlparse

from tecton_core.vendor.treelib import Tree

INDENT_BLOCK = "  "


class QueryNodeMap:
    def __init__(self):
        self.__counter = itertools.count(start=1)
        self.__map = {}

    def add(self, query_node: "QueryNode") -> int:
        node_id = next(self.__counter)
        self.__map[node_id] = query_node
        return node_id

    def __getitem__(self, node_id: int) -> "QueryNode":
        return self.__map[node_id]


query_node_map = QueryNodeMap()


@dataclass
class NodeRef:
    """
    Used so we can more easily modify the QueryTree by inserting and removing nodes, e.g.
    def subtree_rewrite(subtree_node_ref):
        subtree_node_ref.node = NewNode(subtree_node_ref.node)
    """

    node: "QueryNode"

    @property
    def columns(self) -> Tuple[str, ...]:
        return self.node.columns

    @property
    def inputs(self):
        return self.node.inputs

    @property
    def input_names(self):
        return self.node.input_names

    def as_str(self) -> str:
        return self.node.as_str()

    def pretty_str(
        self,
        verbose: bool = False,
        show_node_ids: bool = True,
    ) -> str:
        tree = self.create_tree(verbose=verbose, show_node_ids=show_node_ids)
        # key=False ensures that nodes on the same level are sorted by id and stdout=False ensures a string is returned
        return tree.show(key=False, stdout=False)

    def _to_query(self) -> pypika.Query:
        return self.node._to_query()

    def to_sql(self) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.
        """
        return self.node.to_sql()

    def create_tree(self, verbose: bool = False, show_node_ids: bool = True):
        tree = Tree()
        self._create_tree(tree, parent_id=None, verbose=verbose, show_node_ids=show_node_ids)
        return tree

    def _create_tree(
        self, tree, prefix: str = "", parent_id: Optional[int] = None, verbose: bool = False, show_node_ids: bool = True
    ):
        tag = self.as_str() if verbose else self.node.__class__.__name__
        tag = prefix + tag

        if self.input_names:
            tag += f"({', '.join(self.input_names)})"

        node_id = query_node_map.add(self.node)
        if show_node_ids:
            tag = f"<{node_id}> " + tag

        # The rendering is messed up if the tag has a newline.
        assert "\n" not in tag

        tree.create_node(tag=tag, identifier=node_id, parent=parent_id)

        # Recursively handle all children.
        if self.input_names:
            assert len(self.input_names) == len(
                self.inputs
            ), f"`input_names` has length {len(self.input_names)} but `inputs` has length {len(self.inputs)}"
            for name, i in zip(self.input_names, self.inputs):
                prefix = f"({name}) "
                i._create_tree(tree, prefix=prefix, parent_id=node_id, verbose=verbose, show_node_ids=show_node_ids)
        else:
            for i in self.inputs:
                i._create_tree(tree, parent_id=node_id, verbose=verbose, show_node_ids=show_node_ids)


class QueryNode(ABC):
    @property
    @abstractmethod
    def columns(self) -> Tuple[str, ...]:
        """
        The columns in the projectlist coming out of this node.
        """

    def as_ref(self) -> NodeRef:
        return NodeRef(self)

    # used for recursing through the tree for tree rewrites
    @property
    @abstractmethod
    def inputs(self) -> Tuple[NodeRef]:
        pass

    @property
    def input_names(self) -> Optional[List[str]]:
        """Returns a list of names for the inputs of this node, if all inputs have names. Otherwise returns None.

        If a list is returned, the order of the names should correspond to the order of nodes in the `inputs` property.
        """
        return None

    @abstractmethod
    def as_str(self) -> str:
        """
        Prints contents of this node and calls recursively on its inputs.
        Used by tecton.TectonDataFrame.explain
        """

    def to_sql(self) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.
        """
        sql_str = self._to_query().get_sql()
        return sqlparse.format(sql_str, reindent=True)

    @abstractmethod
    def _to_query(self) -> pypika.Query:
        """
        Attempts to recursively generate sql query for this and child nodes.

        TODO(11/30/2022): See if this ends up being generic enough for most usage of querytree, or
        if it should be moved into separate node.
        """
