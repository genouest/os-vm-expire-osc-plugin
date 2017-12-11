===========================
OSC plugin for os-vm-expire
===========================

About
=====

This project is an Openstack client for os-vm-expire (https://github.com/genouest/os-vm-expire)

Usage
=====

.. code-block:: bash

  openstack osvmexpire -h
    Command "osvmexpire" matches:
      osvmexpire vmexpire delete
      osvmexpire vmexpire extend
      osvmexpire vmexpire list
      osvmexpire vmexpire show

  openstack osvmexpire vmexpire show 33787e68-a720-42b9-a041-4e6536abcc36

  # Specify os-vm-expire service type
  openstack --os-osvmexpire-service-type vmexpire  osvmexpire vmexpire show 33787e68-a720-42b9-a041-4e6536abcc36


License
=======

Apache 2.0, see LICENSE file.
