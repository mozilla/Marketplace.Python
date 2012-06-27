Examples of the Marketplace clients
===================================

Python
######
**Marketplace command line client**

Install requirements::

    cd python
    pip install -r requirements.txt

Test::

    nosetests

Usage
-----

* Set CONSUMER_KEY and CONSUMER_SECRET environment variables::

    export CONSUMER_KEY=yourconsumerkey
    export CONSUMER_SECRET=yourconsumersecret

* Validate manifest. Will return ``manifest_id`` which is needed for the next steps::

    python main.py validate_manifest http://mozilla.github.com/MarketplaceClientExample/manifest.webapp

* Check if the manifest is valid::

    python main.py is_manifest_valid your_manifest_id

* Add app to marketplace, app_id will be returned::

    python main.py create your_manifest_id

* Display status of the app::

    python main.py status your_app_id

* Add screenshot (currently only JPEG) to app, some data including id will be returned::

    python main.py add_screenshot your_app_id ~/data/some.jpg


