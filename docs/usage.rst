.. _Search Query Reference: https://www.jetbrains.com/help/youtrack/standalone/Search-and-Command-Attributes.html
.. _Command Reference: https://www.jetbrains.com/help/youtrack/standalone/Command-Reference.html

==================
Command line usage
==================
The cli is invoked using the `pyu` executable.

Configuration
-------------
Before getting started you should configure `pyu`. This can be done manually by
creating a `~/.pyutrack` file with the following contents::

   [pyutrack]
   base_url = https://my.myjetbrains.com/youtrack/
   username = myusername
   password = mypassword


`password` is optional and if not provided will be prompted for and subsequently
persisted to the system keychain.

You can optionally store the config file in a custom location and on subsequent
invocations of the executable provide the `--config=${CONFIG_LOCATION}` option.

Lastly, you can interactively generate the configuration by calling `pyu new config`

Quick start
-----------
All interaction with YouTrack resources is performed around five main sub-commands:
`new`, `update`, `list`, `show` & `delete`.

Listing...
~~~~~~~~~~

Users::

   pyu list users

Projects::

   pyu list projects

All Issues (useless)::

   pyu list issues

Issues filtered with a query [`Search Query Reference`_]::

   pyu list issues --filter='crash' # issues containing the word "crash"
   pyu list issues --filter='for: me' # issues for current user
   pyu list issues --filter='reporter: me' # issues reported by current user
   pyu list issues --filter='priority: Critical' # critical issues

Creating...
~~~~~~~~~~~

New regular user::

   pyu new user new_user01 'New User' newuser@moo.com password

New user with specific group(s)::

   pyu new user new_admin01 'New Admin' newadmin@moo.com password --group=Admin

Command documentation
---------------------

.. click:: pyutrack.cli:cli
   :prog: pyu
   :show-nested:
