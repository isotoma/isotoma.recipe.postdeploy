Post-deploy
===========

This recipe is for people wanting to ease themselves into configuration
management. It provides the power of a full configuration management system
(Yaybu) but in a way that integrates with your buildout configuration.

You can:

 * Use it as a way to check a task is complete using its "simulate" mode. If
   someone forgets to symlink in a new config file, simulate will show you!

 * Monitor for files being manually modified outside of your buildout process.
   Wire the simulate command into Nagios and alert when the exit code isn't 254
   as that means your service needs attention!

 * And obviously, automate tasks that you normally run after buildout that
   require elevated priveleges such as setting up log rotation, enabling apache
   vhosts and setting up cron jobs.

Of course it can be called by another configuration management tool like
Puppet, Chef or even another Yaybu instance when you are ready to level up.
This is a great pattern to let your main server CM worry about the big picture
and the CM shipped with your buildout worry about the little details.


Basic use
---------

Consider a simple yaybu configuration::

    resources.append:
        - Execute:
            name: some-script
            command: ${buildout.buildout.directory}/bin/somescript
            user: root
            creates: ${buildout.buildout.directory}/stuff.cfg

You could wire this into buildout like so::

    [buildout]
    parts =
        postdeploy

    [postdeploy]
    recipe = isotoma.recipe.postdeploy
    config = config.yay

To look at the 'expanded' form of your configuration - with all the variables
filled in - you can now (after running buildout) do::

    $ ./bin/postdeploy show
    resources:
      - Execute:
          name: /var/somedir/bin/somescript
          user: root
          creates: /var/somedir/stuff.cfg

This command optionally takes ``-v`` which shows a more verbose dump of your
configuration.

You can simulate what would happen if the config was applied without harming
the system using the ``simulate`` command::

    $ ./bin/postdeploy simulate
    /---------------------------- Execute[some-script] -----------------------------
    | # /var/somedir/bin/somescript
    \-------------------------------------------------------------------------------

This command will have an exit code of 254 if it thinks no changes are
required, 0 if it successfully simulated applying some changes and anything
else indicates a problem with your configuration. It makes an ideal monitoring
tool as it can warn of manual hacks or incomplete deployments.

Finally you can apply the configuration with ``apply``::

    $ ./bin/postdeploy simulate
    /---------------------------- Execute[some-script] -----------------------------
    | # /var/somedir/bin/somescript
    | Here is the stdout from your command
    | ....
    | ....
    | Success!
    \-------------------------------------------------------------------------------


Mandatory Parameters
--------------------

config
    A Yay file to apply to this computer. It will have access to metadata in
    your buildout.


Optional Parameters
-------------------

searchpath
    A set of directories or URLs to search for assets needed to full configure
    this site.

history.track
    A list of values to monitor. This is useful when you have a list of parts
    that are buildout managed but need symlinking in postdeploy. Using history
    tracking you can make sure they are removed from the system if they are
    removed from buildout.

    For example::

        [buildout]
        parts =
            ${parts:apache}
            postdeploy

        [vhost1]
        <snip>

        [parts]
        apache = 
            vhost1
            vhost2

        [postdeploy]
        recipe = isotoma.recipe.postdeploy
        history.track =
            parts:apache

    And in your Yaybu configuration::

        resources.append:
          .foreach vhost in history.parts.apache:
            - Link:
                  name: /etc/apache2/sites-enabled/${buildout.sitename}-${vhost}
                  policy: remove

    The first time you run buildout a datafile with the current state is
    created, Now if you remove ``vhost2`` from your buildout and run postdeploy
    Yaybu will ensure your symlink is removed. This data persists across
    multiple buildouts so is safe even if you forget to run postdeploy.

    There are multiple history types. The default is ``removed``. Another
    example is ``max`` which will keep track of the largest value a field has
    ever held. This is useful if you have buildout with a scaleable number of
    services and want to make sure old services are stopped when you update
    buildout::

      [postdeploy]
      history.track =
          environment:zopes max

    I could then do something like this from my Yaybu configuration::

      .foreach i in range(buildout.environment.zopes, history.environment.zopes):
        - Execute:
            name: stop-forgotten-zope-${i}
            command: kill-command zope${i}
            unless: some-manual-pid-check

history.db
    You don't normally need to change this setting.

    Because this recipe has to support Python 2.4 it can't use Yay as its main
    datastore. This is the path to a Python shelf.

    The default is ``${buildout:directory}/var/${partname}-history.db``

history.yay
    You don't normally need to change this setting.

    The data from ``history.db`` is persisted as yay, it is loaded from here
    when you run ``bin/postdeploy``.

    The default is ``${buildout:directory}/var/${partname}-history.yay``

executable
    A python executable to use. Defaults to the same one used to invoke
    buildout. This is to support Python 2.4 buildouts as Yaybu requires 2.6 or
    2.7.


Repository
----------

This software is available from our `recipe repository`_ on github.

.. _`recipe repository`: http://github.com/isotoma/isotoma.recipe.deploy


License
-------

Copyright 2012 Isotoma Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


