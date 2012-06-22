Examples of the Marketplace clients
===================================

Python
######

Install requirements
--------------------

    cd python
    pip install requirements.txt

Test
----

    nosetests

Usage
-----

* Set CONSUMER_KEY and CONSUMER_SECRET environment

  export CONSUMER_KEY=yourconsumerkey
  export CONSUMER_SECRET=yourconsumersecret

* Validate manifest will return ``manifest_id`` which is needed in next steps:

    python main.py validate_manifest http://example.com/manifest.webapp

* Check if the manifest is valid:

    python main.py is_manifest_valid your_manifest_id

* Add app to marketplace, app_id will be returned:

    python main.py create your_manifest_id

* Display status of the app:

    python main.py status your_app_id
