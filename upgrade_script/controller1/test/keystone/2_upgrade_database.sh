#!/bin/bash

keystone-manage db_sync --expand
keystone-manage db_sync --migrate
service apache2 start
