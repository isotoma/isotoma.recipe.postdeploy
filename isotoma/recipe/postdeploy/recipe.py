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

from isotoma.recipe.postdeploy.history import get_history

class PostDeploy(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        options.setdefault("executable", sys.executable)
        options.setdefault("searchpath", "\n.")
        options.setdefault("history.yay", os.path.join(buildout['buildout']['directory'], 'var', '%s-history.yay' % self.name))
        options.setdefault("history.db", os.path.join(buildout['buildout']['directory'], 'var', '%s-history.db' % self.name))

        self.partsdir = os.path.join(buildout['buildout']['parts-directory'], name)
        self.buildoutyay = os.path.join(self.partsdir, "buildout.yay")

    def write_removed_yay(self):
        removed = {}
        if "history.track" in self.options:
            removed = get_history(
                self.options['history.db'],
                self.buildout,
                self.options.get_list("history.track"),
                )

        loader = PackageLoader("isotoma.recipe.postdeploy", "templates")
        template = Environment(loader=loader).get_template("history.yay.j2")

        open(self.options['history.yay'], "w").write(template.render(history=removed))
        self.options.created(self.options['history.yay'])

    def write_buildout_yay(self):
        """ Write out a buildout.yay based on the current buildout """
        loader = PackageLoader("isotoma.recipe.postdeploy", "templates")
        template = Environment(loader=loader).get_template("buildout.yay.j2")

        # Trigger any sections that aren't in _data and don't have recipes or ${}
        # This will get them in to _data as Option objects for next stage.
        for section in self.buildout:
            if not section in self.buildout._data:
                data = self.buildout._raw[section]
                for key, value in data.items():
                    if '$' in value:
                        break
                else:
                    self.buildout[section]

        open(self.buildoutyay, "w").write(template.render(buildout=self.buildout._data))
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
        config = [self.buildoutyay, self.options['history.yay'], self.options['config']]

        params = [
            "[%s]" % ",".join("'%s'" % c for c in config),
            "[%s]" % ",".join("'%s'" % s for s in searchpath),
            ]
        args = ",".join(params)

        ws = zc.buildout.easy_install.install(dependencies, dest, executable=self.options['executable'], path=egg_paths)
        zc.buildout.easy_install.scripts([(self.name, "isotoma.recipe.postdeploy.script", "main")], ws, self.options['executable'], path, arguments=args)
        self.options.created(os.path.join(path, self.name))

    def install(self):
        for opt in ('history.db', 'history.yay'):
            dirname = os.path.dirname(self.options[opt])
            if not os.path.exists(dirname):
                os.makedirs(dirname)

        if not os.path.exists(self.partsdir):
            os.makedirs(self.partsdir)
        self.options.created(self.partsdir)

        self.write_removed_yay()
        self.write_buildout_yay()
        self.create_bin()

        return self.options.created()

    update = install

