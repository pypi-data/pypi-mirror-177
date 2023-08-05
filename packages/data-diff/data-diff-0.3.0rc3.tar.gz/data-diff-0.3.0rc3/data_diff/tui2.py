import asyncio
from concurrent.futures import thread
import sys
from threading import Thread
from time import monotonic
import traceback

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import var
from textual.widgets import Footer, Header, Static

from dataclasses import dataclass
from functools import lru_cache
from os import scandir
import os.path

from rich.console import RenderableType
import rich.repr

from rich.text import Text

from textual.message import Message
from textual._types import MessageTarget
from textual.widgets._tree_control import TreeControl, TreeNode

from data_diff.diff_tables import SegmentInfo, InfoTree

g_dt = None
g_app = None
g_refresh_css = False


class SegmentInfo(SegmentInfo):
    def get_label(self):
        label = ""

        if self.rowcounts and self.diff_count:
            if self.rowcounts[0]:
                label += f" | {100 * self.diff_count / self.rowcounts[0]:.2f}% diff"
        else:
            label += "no diff"

        return label

    def get_icon(self):
        if self.is_diff is None:
            return "❓"

        return "❌" if self.is_diff else "✔️"

    def set_diff(self, diff):
        # global g_refresh_css
        # g_refresh_css = True
        return super().set_diff(diff)

    def __id__(self):
        return self.is_diff, self.diff_count, self.rowcounts, tuple(id(t) for t in self.tables)

    def __hash__(self):
        return hash(self.__id__())

    def __eq__(self, other: SegmentInfo):
        return self.__id__() == other.__id__()


class InfoTreeWrapper(InfoTree):
    def __init__(self, ui_node, *args, **kw) -> None:
        self.ui_node: TreeControl[SegmentInfo] = ui_node
        super().__init__(*args, **kw)

    def add_node(self, t1, t2, **kw):
        si = SegmentInfo([t1, t2], **kw)
        self.ui_node.add("-", si)
        self.ui_node.expand()
        ctl = self.ui_node.children[-1]
        n = InfoTreeWrapper(ctl, si)
        self.children.append(n)
        global g_refresh_css
        g_refresh_css = True
        return n


def run_diff_thread(differ, tables, tree_control, log):
    try:
        start = monotonic()
        log.append("Starting!")

        info_tree = InfoTreeWrapper(tree_control.root, SegmentInfo(tables))
        info_tree.log = log
        res = differ.diff_tables(*tables, info_tree=info_tree)
        for i in res:
            log.append(str(i))

        end = monotonic() - start
        log.append(f"Done in {end:.2f} seconds.")
    except Exception as e:
        log.append(f"{type(e)} - {traceback.format_exc()}")


class DirectoryTree(TreeControl[SegmentInfo]):
    @rich.repr.auto
    class FileClick(Message, bubble=True):
        def __init__(self, sender: MessageTarget, path: str) -> None:
            self.path = path
            super().__init__(sender)

    def __init__(
        self,
        path: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self.path = os.path.expanduser(path.rstrip("/"))
        label = os.path.basename(self.path)
        data = SegmentInfo([])
        super().__init__(label, data, name=name, id=id, classes=classes)
        self.root.tree.guide_style = "black"

    def render_node(self, node: TreeNode[SegmentInfo]) -> RenderableType:
        return self.render_tree_label(
            node,
            node.data,
            node.expanded,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
        )

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[SegmentInfo],
        data,
        expanded: bool,
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
    ) -> RenderableType:
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }
        label = data.get_label()  # node.label
        # if node.children:
        #     p = 100 * len([1 for c in node.children if c.data.is_diff is not None]) // len(node.children)
        #     label += f" [{p}%]"

        label = Text(label) if isinstance(label, str) else label
        if is_hover:
            label.stylize("underline")

        # if len(node.children) > 0:
        #     icon = "📂" if expanded else "📁"

        label.stylize("white")

        label.highlight_regex(r"\d*", "cyan")

        if label.plain.startswith("."):
            label.stylize("dim")

        if is_cursor and has_focus:
            label.stylize("reverse")

        icon_label = Text(f"{data.get_icon()} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)
        return icon_label

    # @lru_cache(maxsize=1024 * 32)
    # def render_tree_label(
    #     self,
    #     node: TreeNode[DirEntry],
    #     is_dir: bool,
    #     expanded: bool,
    #     is_cursor: bool,
    #     is_hover: bool,
    #     has_focus: bool,
    # ) -> RenderableType:
    #     meta = {
    #         "@click": f"click_label({node.id})",
    #         "tree_node": node.id,
    #         "cursor": node.is_cursor,
    #     }
    #     label = Text(node.label) if isinstance(node.label, str) else node.label
    #     if is_hover:
    #         label.stylize("underline")
    #     if is_dir:
    #         label.stylize("bold")
    #         icon = "📂" if expanded else "📁"
    #     else:
    #         icon = "📄"
    #         label.highlight_regex(r"\..*$", "italic")

    #     if label.plain.startswith("."):
    #         label.stylize("dim")

    #     if is_cursor and has_focus:
    #         cursor_style = self.get_component_styles("tree--cursor").rich_style
    #         label.stylize(cursor_style)

    #     icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
    #     icon_label.apply_meta(meta)
    #     return icon_label

    def on_styles_updated(self) -> None:
        self.render_tree_label.cache_clear()

    def on_mount(self) -> None:
        # self.call_later(self.load_directory, self.root)
        pass

    async def on_tree_control_node_selected(self, message: TreeControl.NodeSelected[SegmentInfo]) -> None:
        dir_entry = message.node.data
        # if not dir_entry.is_dir:
        #     await self.emit(self.FileClick(self, dir_entry.path))
        # else:
        #     if not message.node.loaded:
        #         await self.load_directory(message.node)
        #         message.node.expand()
        #     else:
        #         message.node.toggle()


class FeedViewer(Static):
    def __init__(self, **kw) -> None:
        self.lines = []

        super().__init__(**kw)

    def append(self, line):
        self.lines.append(line)

    async def append_async(self, line):
        self.lines.append(line)

    def update_view(self):
        self.update(Text("\n".join(str(x) for x in self.lines)))
        global g_refresh_css
        if g_refresh_css:
            g_app.refresh_css()
            g_app.refresh(layout=True)
            g_refresh_css = False

    def on_mount(self):
        self.set_interval(0.1, self.update_view)


class DataDiffApp(App):
    """Textual code browser app."""

    CSS_PATH = "tui.css"
    BINDINGS = [("f", "toggle_files", "Toggle Files"), ("q", "quit", "Quit"), ("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self, differ, tables, **kw) -> None:
        self.differ = differ
        self.tables = tables
        global g_app
        g_app = self
        super().__init__(**kw)

    show_tree = var(True)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        global g_dt
        g_dt = DirectoryTree(path, id="tree")
        yield Header()
        yield Container(
            Vertical(g_dt, id="tree-view"),
            Vertical(FeedViewer(id="code", expand=True), id="code-view"),
        )
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        tree_view = self.query_one("#tree-view")
        tree_view.focus()

        log = self.query_one("#code", FeedViewer)
        log.append("hello!")

        tree = self.query_one("#tree")
        t = Thread(target=run_diff_thread, args=[self.differ, self.tables, tree, log])
        t.daemon = True
        t.start()

    def on_directory_tree_file_click(self, event: DirectoryTree.FileClick) -> None:
        """Called when the user click a file in the directory tree."""
        code_view = self.query_one("#code", FeedViewer)
        try:
            syntax = Syntax.from_path(
                event.path,
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = event.path

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree


def start_app(differ, *tables):
    # DataDiffApp(differ=differ, tables=tables).run()
    DataDiffApp(differ=differ, tables=tables).run()


# import logging
# logging.basicConfig(level=logging.INFO)

from data_diff import connect_to_table, HashDiffer
from tests.local_settings import TEST_MYSQL_CONN_STRING


def test():
    kw = dict(
        # update_column = "timestamp",
        thread_count=8,
        # where = 'id < 100000',
    )
    table1 = connect_to_table(TEST_MYSQL_CONN_STRING, "Rating", **kw)
    table2 = connect_to_table(TEST_MYSQL_CONN_STRING, "Rating_del1", **kw)

    differ = HashDiffer(
        bisection_factor=32,
        max_threadpool_size=16,
    )

    start_app(differ, table1, table2)
    # log = []
    # run_diff_thread(differ, [table1, table2], None, log)
    # print(log)


if __name__ == "__main__":
    test()
