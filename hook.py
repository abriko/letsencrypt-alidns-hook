#!/usr/bin/env python
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str

from future import standard_library

import dns.exception
import dns.resolver
import logging
import os
import requests
import base64
import sys
import time
import hmac
import uuid
from hashlib import sha1
from tld import get_tld

standard_library.install_aliases()

# Enable verified HTTPS requests on older Pythons
# http://urllib3.readthedocs.org/en/latest/security.html
if sys.version_info[0] == 2:
    requests.packages.urllib3.contrib.pyopenssl.inject_into_urllib3()
    from urllib import quote
    from urllib import urlencode
else:
    from urllib.parse import quote
    from urllib.parse import urlencode

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

try:
    ACCESS_KEY_ID = os.environ['KEY_ID']
    ACCESS_KEY_SECRET = os.environ['KEY_SECRET']
except KeyError:
    logger.error(" + Unable to locate Aliyun api credentials in environment!")
    sys.exit(1)

try:
    dns_servers = os.environ['ALI_DNS_SERVERS']
    dns_servers = dns_servers.split()
except KeyError:
    dns_servers = False


def _has_dns_propagated(name, token):
    txt_records = []
    try:
        if dns_servers:
            custom_resolver = dns.resolver.Resolver()
            custom_resolver.nameservers = dns_servers
            dns_response = custom_resolver.query(name, 'TXT')
        else:
            dns_response = dns.resolver.query(name, 'TXT')
        for rdata in dns_response:
            for txt_record in rdata.strings:
                txt_records.append(txt_record)
    except dns.exception.DNSException:
        return False

    for txt_record in txt_records:
        if txt_record == token:
            return True

    return False

# for ali api signature


def _percent_encode(txt):
    res = quote(str(txt))
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def _compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(
        parameters.items(), key=lambda parameters: parameters[0])

    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + \
            _percent_encode(k) + '=' + _percent_encode(v)

    stringToSign = 'GET&%2F&' + _percent_encode(canonicalizedQueryString[1:])
    bs = access_key_secret + "&"

    h = hmac.new(
        key=bytearray(bs, 'utf-8'),
        msg=bytearray(stringToSign, 'utf-8'),
        digestmod=sha1
    )
    signature = base64.encodestring(h.digest()).strip()
    return signature


def _compose_url(params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    parameters = {
        'Format': 'JSON',
        'Version': '2015-01-09',
        'AccessKeyId': ACCESS_KEY_ID,
        'SignatureVersion': '1.0',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'Timestamp': timestamp,
    }

    for key in params.keys():
        parameters[key] = params[key]

    signature = _compute_signature(parameters, ACCESS_KEY_SECRET)
    parameters['Signature'] = signature

    url = "https://alidns.aliyuncs.com/?" + urlencode(parameters)

    return url


def _make_request(params):
    url = _compose_url(params)

    r = requests.get(url)
    r.raise_for_status()

    try:
        obj = r.json()
        return obj
    except ValueError as e:
        raise SystemExit(e)


# https://help.aliyun.com/document_detail/29772.html AddDomainRecord
def create_txt_record(args):
    domain, token = args[0], args[2]

    res = get_tld("http://" + domain, as_object=True)
    if res.subdomain:
        name = "{0}.{1}".format('_acme-challenge', res.subdomain)
    else:
        name = '_acme-challenge'

    payload = {
        'Action': 'AddDomainRecord',
        'DomainName': res.tld,
        'RR': name,
        'Type': 'TXT',
        'Value': token,
    }

    r = _make_request(payload)
    record_id = r['RecordId']
    logger.debug(" + TXT record created, ID: {0}".format(record_id))

    # give it 10 seconds to settle down and avoid nxdomain caching
    logger.info(" + Settling down for 10s...")
    time.sleep(10)

    look_up_args = "{0}.{1}".format(name, res.tld)
    while(_has_dns_propagated(look_up_args, token) is False):
        logger.info(" + DNS not propagated, waiting 30s...")
        time.sleep(30)


# https://help.aliyun.com/document_detail/29776.html DescribeDomainRecords
# https://help.aliyun.com/document_detail/29773.html DeleteDomainRecord
def delete_txt_record(args):
    domain, token = args[0], args[2]
    if not domain:
        logger.info(" + http_request() error in letsencrypt.sh?")
        return

    res = get_tld("http://" + domain, as_object=True)
    if res.subdomain:
        name = "{0}.{1}".format('_acme-challenge', res.subdomain)
    else:
        name = '_acme-challenge'

    payload = {
        'Action': 'DescribeDomainRecords',
        'DomainName': res.tld,
        'RRKeyWord': name,
        'TypeKeyWord': 'TXT',
        'ValueKeyWord': token,
    }

    r = _make_request(payload)
    logger.debug(" + Found {0} record".format(r['TotalCount']))
    if r['TotalCount'] > 0:
        for record in r['DomainRecords']['Record']:
            logger.debug(
                " + Deleting TXT record name: {0}.{1}, RecordId: {2}".format(
                    record['RR'], record['DomainName'], record['RecordId']))
            payload = {
                'Action': 'DeleteDomainRecord',
                'RecordId': record['RecordId'],
            }
            r_d = _make_request(payload)
            if r_d['RecordId'] == record['RecordId']:
                logger.debug(
                    " + RecordId {0} has been deleted".format(r['TotalCount']))


def deploy_cert(args):
    domain, privkey_pem, cert_pem, fullchain_pem, chain_pem, timestamp = args
    logger.info(' + ssl_certificate: {0}'.format(fullchain_pem))
    logger.info(' + ssl_certificate_key: {0}'.format(privkey_pem))
    return


def unchanged_cert(args):
    return

def exit_hook(args):
    return

def main(argv):
    ops = {
        'deploy_challenge': create_txt_record,
        'clean_challenge': delete_txt_record,
        'deploy_cert': deploy_cert,
        'unchanged_cert': unchanged_cert,
        'exit_hook': exit_hook,
    }
    logger.info(" + AliDNS hook executing: {0}".format(argv[0]))
    ops[argv[0]](argv[1:])


if __name__ == '__main__':
    main(sys.argv[1:])
