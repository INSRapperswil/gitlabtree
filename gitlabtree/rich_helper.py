from rich.panel import Panel


def error(error: str, title: str = "ERROR") -> Panel:
    return Panel(error, style="red", title=title, title_align="left")
