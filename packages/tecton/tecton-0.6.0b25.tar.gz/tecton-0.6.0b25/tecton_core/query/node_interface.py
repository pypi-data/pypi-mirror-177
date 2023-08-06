from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

import pypika
import sqlparse

from tecton_core.vendor.treelib import Tree

INDENT_BLOCK = "  "


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
        show_columns: bool = False,
    ) -> str:
        """Returns a string that represents the query tree which has this NodeRef as the root node.

        Args:
            verbose: If True, nodes will be rendered by a lengthy description of their actions. Otherwise nodes will be
                rendered by their class name.
            show_node_ids: If True, the unique id associated with each node will be rendered.
            show_columns: If True, the columns of each node will be rendered as an appendix after tree itself.
        """
        tree = self.create_tree(verbose=verbose, show_node_ids=show_node_ids)

        # key=False ensures that nodes on the same level are sorted by id and stdout=False ensures a string is returned
        tree_str = tree.show(key=False, stdout=False)

        if not show_columns:
            return tree_str

        columns = []
        max_node_id = tree.size()
        for node_id in range(1, max_node_id + 1):
            node = tree.get_node(node_id).data
            columns.append((f"<{node_id}> " if show_node_ids else "") + f"{'|'.join(node.columns)}")

        return tree_str + "\n" + "\n".join(columns)

    def _to_query(self) -> pypika.Query:
        return self.node._to_query()

    def to_sql(self) -> str:
        """
        Attempts to recursively generate sql for this and child nodes.
        """
        return self.node.to_sql()

    def create_tree(self, verbose: bool = False, show_node_ids: bool = True) -> Tree:
        """Creates a Tree to represent the query tree which has this NodeRef as the root node.

        The Tree is built so that it can immediately generate a string representation.

        Args:
            verbose: If True, nodes will be rendered by a lengthy description of their actions. Otherwise nodes will be
                rendered by their class name.
            show_node_ids: If True, the unique id associated with each node will be rendered.
        """
        tree = Tree()
        self._create_tree(tree=tree, parent_id=None, verbose=verbose, show_node_ids=show_node_ids)
        return tree

    def _create_tree(
        self,
        tree: Tree,
        prefix: str = "",
        parent_id: Optional[int] = None,
        verbose: bool = False,
        show_node_ids: bool = True,
    ):
        tag = self.as_str() if verbose else self.node.__class__.__name__
        tag = prefix + tag

        # In the verbose case, adding the input names at the end is too clunky, so we omit them.
        if self.input_names and not verbose:
            tag += f"({', '.join(self.input_names)})"

        # Node ids are assigned sequentially, starting with 1.
        node_id = tree.size() + 1
        if show_node_ids:
            tag = f"<{node_id}> " + tag

        # The rendering is messed up if the tag has a newline.
        assert "\n" not in tag

        # We attach this NodeRef so that it can be retrieved later by its node id.
        tree.create_node(tag=tag, identifier=node_id, parent=parent_id, data=self.node)

        # Recursively handle all children.
        if self.input_names:
            assert len(self.input_names) == len(
                self.inputs
            ), f"`input_names` has length {len(self.input_names)} but `inputs` has length {len(self.inputs)}"
            for name, i in zip(self.input_names, self.inputs):
                prefix = f"({name}) "
                i._create_tree(
                    tree=tree,
                    prefix=prefix,
                    parent_id=node_id,
                    verbose=verbose,
                    show_node_ids=show_node_ids,
                )
        else:
            for i in self.inputs:
                i._create_tree(
                    tree=tree,
                    parent_id=node_id,
                    verbose=verbose,
                    show_node_ids=show_node_ids,
                )


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
        """


class DataframeWrapper(ABC):
    """
    A wrapper around pyspark, pandas, snowflake, etc dataframes provides a common interface through which we
    can register views.
    """

    @property
    def _dataframe(self) -> Any:
        """
        The underlying dataframe
        """
        raise NotImplementedError

    @property
    def _columns(self) -> List[str]:
        """
        The columns of the dataframe
        """
        raise NotImplementedError

    @abstractmethod
    def _register_temp_view(self):
        """
        Registers a temp view for the data
        """

    # @abstractmethod
    @property
    def _temp_view_name(self):
        """
        Gets the temp view name registered by register()
        """
        return f"TMP_VIEW_{id(self._dataframe)}"


def recurse_query_tree(node_ref: NodeRef, f: Callable):
    f(node_ref.node)
    for child in node_ref.inputs:
        recurse_query_tree(child, f)
