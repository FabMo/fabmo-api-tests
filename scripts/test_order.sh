#!/bin/sh
cd /api-tests
/usr/bin/pytest -s test_dev_check_one.py
/usr/bin/pytest -s test_dev_check_five.py
/usr/bin/pytest -s test_dev_check_seven.py
/usr/bin/pytest -s test_runMacro_five.py
/usr/bin/pytest -s test_runMacro_two_hundred_one.py
/usr/bin/pytest -s test_runMacro_two_hundred_eleven.py
/usr/bin/pytest -s test_clearJobQueue.py
/usr/bin/pytest -s test_submitJob.py
/usr/bin/pytest -s test_runNextJob.py
