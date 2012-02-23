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

"""
This is an alternative "runner" that strips out options from core Yaybu
that don't make sense.
"""

import sys
import os
import optparse
import yay
from yaybu.core import runner, runcontext


def version(argv, config, searchpath):
    import pkg_resources

    for pkg in ("Yaybu", "yay", "isotoma.recipe.postdeploy"):
        version = pkg_resources.get_distribution(pkg).version
        print "%s = %s" % (pkg, version)

    return 0


def expand(argv, config, searchpath):
    p = optparse.OptionParser()
    p.add_option("-v", "--verbose", default=2, action="count",  help="Write additional informational messages to the console log. repeat for even more verbosity.")
    opts, args = p.parse_args()

    opts.resume = False
    opts.no_resume = False
    opts.user = "root"
    opts.host = ""
    opts.ypath = searchpath
    opts.simulate = False
    opts.env_passthrough = []

    ctx = runcontext.RunContext(config, opts)
    cfg = ctx.get_config().get()

    if opts.verbose <= 2:
        cfg = dict(resources=cfg.get("resources", []))

    print yay.dump(cfg)
    return 0


def _do(argv, config, searchpath, simulate=True):
    p = optparse.OptionParser()
    p.add_option("-v", "--verbose", default=2, action="count", help="Write additional informational messages to the console log. repeat for even more verbosity.")
    p.add_option("--resume", default=False, action="store_true", help="Resume from saved events if terminated abnormally")
    p.add_option("--no-resume", default=False, action="store_true", help="Clobber saved event files if present and do not resume")
    opts, args = p.parse_args()

    opts.simulate = simulate
    opts.ypath = searchpath

    r = runner.Runner()
    ctx = runcontext.RunContext(config, opts)
    return r.run(ctx)


def simulate(argv, config, searchpath):
    return _do(argv, config, searchpath, simulate=True)


def apply(argv, config, searchpath):
    return _do(argv, config, searchpath, simulate=False)


def main(config, searchpath, argv=None):
    if not argv:
        argv = sys.argv[1:]

    if len(argv) < 1:
        print "expand, simulate or apply?"
        sys.exit(1)

    subcommand = argv[0]
    argv = argv[1:]

    funcs = dict(
        expand = expand,
        simulate = simulate,
        apply = apply,
        version = version,
        )

    if not subcommand in funcs:
        print "%s is not a valid subcommand" % subcommand
        sys.exit(1)

    return funcs[subcommand](argv, config, searchpath)

