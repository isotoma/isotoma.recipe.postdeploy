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
import missingbits


class PostDeploy(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        options.setdefault("template", sibpath(self.default_template))
        options.setdefault("executable", sys.executable)

        self.partsdir = os.path.join(buildout['buildout']['parts-directory'], name)
        self.config = os.path.join(self.partsdir, "postdeploy.yay")

    def write_config(self):
        """ Write the config out, using the jinja2 templating method """
        dirname, basename = os.path.split(self.options['template'])

        loader = FileSystemLoader(dirname)
        template = Environment(loader=loader).get_template(basename)

        open(self.config, "w").write(template.render(self.options))
        self.options.created(self.config)

    def create_bin(self):
        path = self.buildout["buildout"]["bin-directory"]
        egg_paths = [
            self.buildout["buildout"]["develop-eggs-directory"],
            self.buildout["buildout"]["eggs-directory"],
            ]
        dependencies = ["Yaybu", "isotoma.recipe.postdeploy"]

        params = [
            "'%s'" % self.config,
            "['%s']" % self.partsdir,
            ]
        args = ",".join(params)

        ws = zc.buildout.easy_install.install(dependencies, options['executable'], egg_paths)
        zc.buildout.easy_install.scripts([(self.name, "isotoma.recipe.postdeploy.script", "main")], ws, options['executable'], path, arguments=args)
        self.options.created(os.path.join(path, self.name))

    def install(self):
        if not os.path.exists(self.partsdir):
            os.makedirs(self.partsdir)
        self.options.created(self.partsdir)

        self.write_config()
        self.create_bin()

        return self.options.created()

    def update(self):
        pass

