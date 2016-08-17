#!/usr/bin/env bash
#
echo "$@"
/app/letsencrypt.sh/letsencrypt.sh -c -t dns-01 -k 'hooks/alidns/hook.py' -d $1