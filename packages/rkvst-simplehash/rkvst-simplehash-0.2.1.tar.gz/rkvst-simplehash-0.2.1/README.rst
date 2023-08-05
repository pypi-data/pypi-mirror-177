
.. _readme:

RKVST Simplehash in python
===========================

Prescribed python code that defines the hashing algorithm for DLT Anchoring.

Support
=======

This package currently is tested against Python versions 3.7,3.8,3.9, 3.10 and 3.11.

The current default version is 3.7 - this means that this package will not
use any features specific to versions 3.8 and later.

After End of Life of a particular Python version, support is offered on a best effort
basis. We may ask you to update your Python version to help solve the problem,
if it cannot be reasonably resolved in your current version.

Installation
=============

Use standard python pip utility:

.. code:: bash

    python3 -m pip install rkvst-simplehash

If your version of python3 is too old an error of this type or similar will be emitted:

.. note::

    ERROR: Could not find a version that satisfies the requirement rkvst-simplehash (from versions: none)
    ERROR: No matching distribution found for rkvst-simplehash

Examples
=============

You can then use the code to recreate the simple hash of a list of SIMPLE_HASH events from RKVST.

Importing in own code
.....................

.. code:: python

    """From a list of events.
    """

    from rkvst_simplehash.v1 import (
        anchor_events,
        SimpleHashError,
    )

    with open("credentials/token", mode="r", encoding="utf-8") as tokenfile:
        auth_token = tokenfile.read().strip()

    # SimpleHashClientAuthError is raised if the auth token is invalid or expired.
    # if any pending events a SimpleHashPendingEventFound error will be thrown
    # if any of the events do not contain the required field then a SimpleHashFieldMissing error will be thrown
    try:
        simplehash = anchor_events(
            "2022-10-07 07:01:34Z",
            "2022-10-16T13:14:56Z",
            "app.rkvst.io",
            auth_token,
        )
    except SimpleHashError as ex:
        print("Error", ex)

    else:
        print("simplehash=", simplehash)


Command Line
------------

This functionality is also available on the cmdline.

Using a virtual env and published wheel:
........................................

This can be executed anywhere using a virtualenv and published wheel.
Credentials are stored in files in credentials directory.

Using an auth token directly:

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    rkvst_simplehashv1 \
        --auth-token-file "credentials/token" \
        --start-time "2022-11-16T00:00:00Z" \
        --end-time "2022-11-17T00:00:00Z"
    
    deactivate
    rm -rf simplehash-venv

Using a client id and secret:

.. code:: bash

    #!/usr/bin/env bash
    #
    python3 -m venv simplehash-venv
    source simplehash-venv/bin/activate
    python3 -m pip install -q rkvst_simplehash
    
    CLIENT_ID=$(cat credentials/client_id)
    rkvst_simplehashv1 \
        --client-id "${CLIENT_ID}" \
        --client-secret-file "credentials/client_secret" \
        --start-time "2022-11-16T00:00:00Z" \
        --end-time "2022-11-17T00:00:00Z"
    
    deactivate
    rm -rf simplehash-venv
