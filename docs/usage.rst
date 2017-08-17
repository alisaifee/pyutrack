.. _Search Query Reference: https://www.jetbrains.com/help/youtrack/standalone/Search-and-Command-Attributes.html
.. _Command Reference: https://www.jetbrains.com/help/youtrack/standalone/Command-Reference.html

==================
Command line usage
==================
The cli is invoked using the ``pyu`` executable.

Configuration
-------------
Before getting started you should configure ``pyu``. This can be done manually by
creating an ini file at ``~/.pyutrack`` with the following contents:

.. code-block:: ini

   [pyutrack]
   base_url = https://my.myjetbrains.com/youtrack/
   username = myusername
   password = mypassword


``password`` is optional and if not provided will be prompted for and subsequently
persisted to the system keychain.

You can optionally store the config file in a custom location and on subsequent
invocations of the executable provide the ``--config=${CONFIG_LOCATION}`` option.

Lastly, you can interactively generate the configuration by calling ``pyu new config``

Quick start
-----------
All interaction with YouTrack resources is performed around five main sub-commands:
``new``, ``update``, ``list``, ``show`` & ``delete``.

Here's a few examples to get started. For more details on each sub-command refer to `command documentation`_.

Listing...
~~~~~~~~~~

Users
^^^^^
.. code-block:: bash

   pyu list users

Projects
^^^^^^^^
.. code-block:: bash

   pyu list projects

All Issues in a project
^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu list issues --project=MYPROJECT

Issues filtered with a query (`Search Query Reference`_)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu list issues --filter='crash' # issues containing the word "crash"
   pyu list issues --filter='for: me' # issues for current user
   pyu list issues --filter='reporter: me' # issues reported by current user
   pyu list issues --filter='priority: Critical' # critical issues

Creating...
~~~~~~~~~~~

New regular user
^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu new user new_user01 'New User' newuser@moo.com password

New user with specific group(s)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu new user new_admin01 'New Admin' newadmin@moo.com password --group=Admin


New issue
^^^^^^^^^
.. code-block:: bash

   pyu new issue MYPROJECT 'this is an important issue'

New issue tagged with kitties and marked as critical and assigned to me (`Command Reference`_)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu new issue MYPROJECT 'this is an important issue' --command='tag kitties priority critical assignee me'


Updating...
~~~~~~~~~~~

Change a user's password
^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu update user some-user --password=new-password

Update an issue using a command (`Command Reference`_)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

   pyu update issue PRO-1 --command='assignee: me' # assign issue to yourself
   pyu update issue PRO-1 --command='tag: kitties' # tag the issue with kitties
   pyu update issue PRO-1 --command='priority: critical' # increase priority to critical
   pyu update issue PRO-1 --command='fixed' # mark issue as fixed

Command documentation
---------------------

.. click:: pyutrack.cli:cli
   :prog: pyu
   :show-nested:
