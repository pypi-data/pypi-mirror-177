from cleo.io.io import IO
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry


class AutoVersionPlugin(Plugin):

    def activate(self, poetry: Poetry, io: IO):
        io.write_line("Setting version")
        poetry.package.version = "x.y.z.0"
