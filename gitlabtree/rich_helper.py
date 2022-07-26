from rich.panel import Panel
from rich.tree import Tree

from .models import Group


def error(error: str, title: str = "ERROR") -> Panel:
    return Panel(error, style="red", title=title, title_align="left")


def render_tree(root: Group, guide_style: str = "uu green") -> Tree:
    def build_tree(tree: Tree, top: Group) -> None:
        for group in top.groups:
            new = tree.add(group)
            build_tree(new, group)
        for repo in top.repositories:
            tree.add(repo)

    git_tree = Tree(root, guide_style=guide_style)
    build_tree(git_tree, root)

    return git_tree
