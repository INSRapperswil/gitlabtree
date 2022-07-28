"""
Helper functions using rich
"""
from rich.panel import Panel
from rich.tree import Tree
from rich.console import Group as RichGroup

from .models import Group


def error(error_msg: str, title: str = "ERROR") -> Panel:
    """Nice looking error message

    Args:
        error (str): Error message
        title (str, optional): Panel title. Defaults to "ERROR".

    Returns:
        Panel: Rich Panel with error message for printing
    """
    return Panel(error_msg, style="red", title=title, title_align="left")


def render_tree(root: Group, guide_style: str = "uu green") -> Tree:
    """Rendering a Rich tree for printing in the console

    Args:
        root (Group): Root group to start the tree
        guide_style (str, optional): Tree style can be changed. Defaults to "uu green".

    Returns:
        Tree: Rich tree starting at the provided root group. Ready to print
    """

    def build_tree(tree: Tree, top: Group) -> None:
        for group in top.groups:
            node = tree.add(group)
            if info_list := list(group.info):
                node.add(RichGroup(*info_list))
            build_tree(node, group)
        for repo in top.repositories:
            rich_group = RichGroup(repo, *list(repo.info))
            tree.add(rich_group)

    # Using super_group Group so the build_tree logic works for the top level as well.
    git_tree = Tree("GitLabTree", hide_root=True, guide_style=guide_style)
    super_group = Group(name="git_tree", groups=[root])
    build_tree(git_tree, super_group)

    return git_tree.children[0]
