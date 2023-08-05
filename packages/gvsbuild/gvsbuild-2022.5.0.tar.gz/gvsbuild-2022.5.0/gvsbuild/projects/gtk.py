#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

import glob
import os

from gvsbuild.utils.base_builders import MakeGir, Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


class Project_gtk_base(Tarball, Project, MakeGir):
    def make_all_mo(self):
        if self.name == "gtk2":
            mo = "gtk20.mo"
        elif self.name == "gtk3":
            mo = "gtk30.mo"
        else:
            mo = "gtk40.mo"
        localedir = os.path.join(self.pkg_dir, "share", "locale")
        self.push_location(r".\po")
        for fp in glob.glob(os.path.join(self.build_dir, "po", "*.po")):
            f = os.path.basename(fp)
            lcmsgdir = os.path.join(localedir, f[:-3], "LC_MESSAGES")
            self.builder.make_dir(lcmsgdir)
            cmd = " ".join(["msgfmt", "-co", os.path.join(lcmsgdir, mo), f])
            self.builder.exec_cmd(cmd, working_dir=self._get_working_dir())
        self.pop_location()

        self.install(r".\COPYING share\doc\%s" % self.name)


@project_add
class Gtk2(Project_gtk_base):
    def __init__(self):
        Project.__init__(
            self,
            "gtk2",
            archive_url="https://download.gnome.org/sources/gtk+/2.24/gtk+-2.24.33.tar.xz",
            hash="ac2ac757f5942d318a311a54b0c80b5ef295f299c2a73c632f6bfb1ff49cc6da",
            dependencies=["atk", "gdk-pixbuf", "pango"],
            patches=[
                "gtk-revert-scrolldc-commit.patch",
                "gtk-bgimg.patch",
                "gtk-accel.patch",
                # https://github.com/hexchat/hexchat/issues/1007
                "gtk-multimonitor.patch",
                # https://github.com/hexchat/hexchat/issues/2077
                "0001-GDK-W32-Remove-WS_EX_LAYERED-from-an-opaque-window.patch",
            ],
        )
        if Project.opts.enable_gi:
            self.add_dependency("gobject-introspection")

    def build(self):
        self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz")
        self.exec_msbuild_gen(r"build\win32", "gtk+.sln", add_pars="/p:UseEnv=True")

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env("INCLUDE", f"{self.builder.gtk_dir}\\include\\cairo")
            self.builder.mod_env(
                "INCLUDE", f"{self.builder.gtk_dir}\\include\\harfbuzz"
            )
            self.make_single_gir("gtk2", prj_dir="gtk2")


@project_add
class Gtk3(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtk3",
            prj_dir="gtk3",
            archive_url="https://download.gnome.org/sources/gtk%2B/3.24/gtk%2B-3.24.34.tar.xz",
            hash="dbc69f90ddc821b8d1441f00374dc1da4323a2eafa9078e61edbe5eeefa852ec",
            dependencies=["atk", "gdk-pixbuf", "pango", "libepoxy"],
            patches=[
                "gtk_update_icon_cache.patch",
                "gdkwin32-fix-subclassing-for-gdkwin32selection.patch",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "true"
        else:
            enable_gi = "false"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(self, meson_params="-Dtests=false -Ddemos=false -Dexamples=false")

        self.install(r".\COPYING share\doc\gtk3")


@project_add
class Gtk4(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "gtk4",
            prj_dir="gtk4",
            archive_url="https://download.gnome.org/sources/gtk/4.8/gtk-4.8.1.tar.xz",
            hash="5ce8d8de98a23bd0c8eca1a61094e1c009b5f009dcbd60b45e990a8db1b742fd",
            dependencies=["gdk-pixbuf", "pango", "libepoxy", "graphene"],
            patches=[
                "gdkwin32-fix-subclassing-for-gdkwin32clipdrop.patch",
            ],
        )
        if self.opts.enable_gi:
            self.add_dependency("gobject-introspection")
            enable_gi = "enabled"
        else:
            enable_gi = "disabled"

        self.add_param(f"-Dintrospection={enable_gi}")

    def build(self):
        Meson.build(
            self,
            meson_params="-Dbuild-tests=false -Ddemos=false -Dbuild-examples=false -Dmedia-gstreamer=disabled",
        )

        self.install(r".\COPYING share\doc\gtk4")
