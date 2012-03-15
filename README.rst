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


