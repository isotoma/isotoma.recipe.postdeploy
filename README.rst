Post-deploy
===========

This recipe is for people who want to automate checking (or actual application)
of post-buildout deployment steps and havent adopted a configuration management
system like Yaybu, Puppet or Chef.

It takes a template Yaybu configuration and allows you to inject settings from
your buildout - so the configuration is configured for that one particualar
deployment. It creates a ``bin/postdeploy`` that you can run with sudo after
running buildout.

When you graduate to server-wide configuration management you can opt to keep
your post-deployment configuration with your buildout and just call
``postdeploy`` from your main configuration management tool.


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


