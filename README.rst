Post-deploy
===========

This recipe is for people who want to automate checking (or actual application)
of post-buildout deployment steps and havent adopted a configuration management
system like Yaybu, Puppet or Chef.

It takes a template Yaybu configuration and allows you to inject settings from
your buildout - so the configuration is configured for that one particualar
deployment. It creates a ``bin/postdeploy`` wrapper and installs Yaybu like any
other package in your buildout.

When you graduate to server-wide configuration management you can opt to keep
your post-deployment configuration with your buildout.


Mandatory Parameters
--------------------

template
    A jinja2 template containing your post deployment steps in the Yaybu
    configuration format.


Optional Parameters
-------------------


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


