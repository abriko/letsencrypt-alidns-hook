#!/usr/bin/env bash
#
echo "$@"
/app/dehydrated/dehydrated -c -t dns-01 -k 'hooks/alidns/hook.py' -d $1