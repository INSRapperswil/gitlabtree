from rich.panel import Panel
from rich.tree import Tree
from rich.console import Group as RichGroup

from .models import Group


def error(error: str, title: str = "ERROR") -> Panel:
    return Panel(error, style="red", title=title, title_align="left")


def render_tree(root: Group, guide_style: str = "uu green") -> Tree:
    def build_tree(tree: Tree, top: Group) -> None:
        for group in top.groups:
            node = tree.add(group)
            if info_list := [info for info in group.info]:
                node.add(RichGroup(*info_list))
            build_tree(node, group)
        for repo in top.repositories:
            rg = RichGroup(repo, *[info for info in repo.info])
            tree.add(rg)

    # Using super_group Group so the build_tree logic works for the top level as well.
    git_tree = Tree("GitLabTree", hide_root=True, guide_style=guide_style)
    super_group = Group(name="git_tree", groups=[root])
    build_tree(git_tree, super_group)

    return git_tree.children[0]
