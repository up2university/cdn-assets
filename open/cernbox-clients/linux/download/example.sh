#! /bin/sh
#
# This example demonstrates how to call repo-admin.py
# You will need to call repo-admin.py with your download url if the url shown below differs.
# Basic auth username and password is supported in the url.
#
# You can customitze the main html file and re-run repo-admin.py later.
#
cd "$(dirname "${0}")"
set -eux
python bin/repo-admin.py --url http://download.example.com/repo -d 'download' -p 'openup2u-client' -i 'index.html' -f ..
