Contributing
============

In order to contribute to CIFY, you will need to

    1. Create a GitHub account.

    2. Clone the repository.

    3. Install an appropriate version of Python.

    4. Create a virtual environment within the project directory and install the necessary dependencies.

1. Getting the repository on your local machine.
------------------------------------------------

First, `create a GitHub account <https://github.com/join>`_. Once your account has been created, go to the
`project homepage <https://github.com/davidmccleave/cify>`_ and find the green "Code" button towards the top of
the page. Clicking on this button will open up a few options for cloning the repository. You can choose between HTTPS,
SSH and GitHub CLI. If you are using SSH, you may need to link an SSH key to your GitHub account first. Instructions
for this are given `here <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account>`_.

Find a folder on your local machine to clone the repository to and execute the command to clone it. If you are using SSH,
the command would look as follows::

    git clone git@github.com:davidmccleave/cify.git

The repository will be cloned into its own folder within the directory you ran the command.

2. Setting up a Python virtual environment.
-------------------------------------------

Head over to the `Python Downloads <https://www.python.org/downloads/>`_ page and select the appropriate version
for your operating system. It is recommended to install Python 3.8 or later. Once Python has been installed,
you will need to create a virtual environment to install all the dependencies required to work on CIFY. These dependencies
are kept in the ``dev-requirements.txt`` file. For a primer on Python virtual environments follow `this link <https://docs.python.org/3/library/venv.html>`_.

You'll want to create the virtual environment in the same directory as the cloned repository. Execute::

    python3 -m venv <name>

from a terminal in the directory, where ``<name>`` is the name of the virtual environment and should be either `.venv` or `venv`.
This is so that the created virtual environment will not be staged by git. (The virtual environment folder is typically quite large
and there is no need to track changes to it. Each contributor will have their own local virtual environment.).

Once the virtual environment has been created, you will need to activate the environment using::

    source <name>/bin/activate

Now we can install the necessary dependencies to this virtual environment using::

    pip install -r dev-requirements.txt

This same process must be executed if you wish to tamper with the documentation. For this, `cd` into the `docs/` directory, and run
the command, ``pip install -r docs-requirements.txt``.

You should now have the appropriate environment set up to start working on contributions.

3. Contributing
---------------

All contributions should take place on a new branch. For more on branching in git, check out `this link <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches>`_.

Open up your preferred editor to make changes to the code making sure to use the previously created virtual environment
when linting source code or running examples. Once the appropriate changes have been made you will need to push this new
branch and, optionally, create a pull request. If you only wished to make changes to a certain collaborative branch then there is no
need to create a pull request until the branch is ready to be merged.

A pull request is a request from a contributor to a maintainer of the repository to merge the changes from one branch
into another. The request has a title and description so that maintainers can understand the changes you have made before
examining them directly.

For more on creating pull requests, follow `this link <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`_.
