# Copyright 2010 Isotoma Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys, os
from jinja2 import Environment, PackageLoader, ChoiceLoader, FunctionLoader, FileSystemLoader
import zc.buildout
import missingbits


class PostDeploy(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        options.setdefault("executable", sys.executable)
        options.setdefault("searchpath", "\n.")

        self.partsdir = os.path.join(buildout['buildout']['parts-directory'], name)
        self.buildoutyay = os.path.join(self.partsdir, "buildout.yay")

    def write_buildout_yay(self):
        """ Write out a buildout.yay based on the current buildout """
        loader = PackageLoader("isotoma.recipe.postdeploy", "templates")
        template = Environment(loader=loader).get_template("buildout.yay.j2")

        open(self.buildoutyay, "w").write(template.render(buildout=self.buildout))
        self.options.created(self.buildoutyay)

    def create_bin(self):
        path = self.buildout["buildout"]["bin-directory"]
        egg_paths = [
            self.buildout["buildout"]["develop-eggs-directory"],
            self.buildout["buildout"]["eggs-directory"],
            ]
        dest = self.buildout["buildout"]["eggs-directory"]
        dependencies = ["Yaybu", "isotoma.recipe.postdeploy"]

        searchpath = self.options.get_list("searchpath") + [self.partsdir]
        config = [self.buildoutyay, self.options['config']]

        params = [
            "[%s]" % ",".join("'%s'" % c for c in config),
            "[%s]" % ",".join("'%s'" % s for s in searchpath),
            ]
        args = ",".join(params)

        ws = zc.buildout.easy_install.install(dependencies, dest, executable=self.options['executable'], path=egg_paths)
        zc.buildout.easy_install.scripts([(self.name, "isotoma.recipe.postdeploy.script", "main")], ws, self.options['executable'], path, arguments=args)
        self.options.created(os.path.join(path, self.name))

    def install(self):
        if not os.path.exists(self.partsdir):
            os.makedirs(self.partsdir)
        self.options.created(self.partsdir)

        self.write_buildout_yay()
        self.create_bin()

        return self.options.created()

    def update(self):
        pass

