# `letsencrypt.sh` 阿里域名DNS hook
这是[letsencrypt.sh](https://github.com/lukas2511/letsencrypt.sh)脚本的 (一个[Let's Encrypt](https://letsencrypt.org/) ACME 客户端) 他允许你使用 [Alidns](http://netcn.console.aliyun.com/core/domain/tclist/) DNS 记录完成  `dns-01` 。运行需要提供Python运行环境和阿里云账户的AccessKey。

##安装步骤
```
$ git clone https://github.com/lukas2511/letsencrypt.sh
$ cd letsencrypt.sh
$ mkdir hooks
$ git clone https://github.com/Abriko/letsencrypt-alidns-hook.git hooks/alidns
$ pip install -r hooks/alidns/requirements.txt
```
如果你使用的Python2，请使用下列代码替代上面提到的最后一步。

```
$ pip install -r hooks/alidns/requirements-python-2.txt
```

##配置

仅需将阿里云账户的` Access Key ID` 和` Access Key Secret`配置到环境变量即可，如下：
```
$ export KEY_ID='QynxPDkzWbhAgr'
$ export KEY_SECRET='9fBnhxPTx5RbhA'
```

另外还可以通过`ALI_DNS_SERVERS`指定验证时使用的DNS：
```
$ export ALI_DNS_SERVERS='223.5.5.5 223.4.4.4'
```

当然也可以将下列代码放在 `letsencrypt.sh/config.sh`里。当执行 `letsencrypt.sh`会自动初始化配置 :

```
echo "export KEY_ID='QynxPDkzWbhAgr'" >> config.sh
echo "export KEY_SECRET='9fBnhxPTx5RbhA'" >> config.sh
```

## 使用

参照下列命令：
```
$ ./letsencrypt.sh -c -d example.com -t dns-01 -k 'hooks/alidns/hook.py'
#
# !! WARNING !! No main config file found, using default config!
#
Processing example.com
 + Signing domains...
 + Creating new directory /home/user/letsencrypt.sh/certs/example.com ...
 + Generating private key...
 + Generating signing request...
 + Requesting challenge for example.com...
 + Alidns hook executing: deploy_challenge
 + DNS not propagated, waiting 30s...
 + DNS not propagated, waiting 30s...
 + Responding to challenge for example.com...
 + Alidns hook executing: clean_challenge
 + Challenge is valid!
 + Requesting certificate...
 + Checking certificate...
 + Done!
 + Creating fullchain.pem...
 + Alidns hook executing: deploy_cert
 + ssl_certificate: /home/user/letsencrypt.sh/certs/example.com/fullchain.pem
 + ssl_certificate_key: /home/user/letsencrypt.sh/certs/example.com/privkey.pem
 + Done!
```

------
# Alidns  hook for `letsencrypt.sh`

This a hook for [letsencrypt.sh](https://github.com/lukas2511/letsencrypt.sh) (a [Let's Encrypt](https://letsencrypt.org/) ACME client) that allows you to use [Alidns](http://netcn.console.aliyun.com/core/domain/tclist/) DNS records to respond to `dns-01` challenges. Requires Python and your Aliyun account being in the environment.

## Installation

```
$ git clone https://github.com/lukas2511/letsencrypt.sh
$ cd letsencrypt.sh
$ mkdir hooks
$ git clone https://github.com/Abriko/letsencrypt-alidns-hook.git hooks/alidns
$ pip install -r hooks/alidns/requirements.txt
```
If using Python 2, replace the last step with the one below and check the [urllib3 documentation](http://urllib3.readthedocs.org/en/latest/security.html#installing-urllib3-with-sni-support-and-certificates) for other possible caveats.

```
$ pip install -r hooks/alidns/requirements-python-2.txt
```



## Configuration

Your account's Aliyun` Access Key ID` and `Access Key Secret` are expected to be in the environment, so make sure to:


```
$ export KEY_ID='QynxPDkzWbhAgr'
$ export KEY_SECRET='9fBnhxPTx5RbhA'
```

Optionally, you can specify the DNS servers to be used for propagation checking via the `ALI_DNS_SERVERS` environment variable:

```
$ export ALI_DNS_SERVERS='223.5.5.5 223.4.4.4'
```

Alternatively, these statements can be placed in `letsencrypt.sh/config.sh`, which is automatically sourced by `letsencrypt.sh` on startup:

```
echo "export KEY_ID='QynxPDkzWbhAgr'" >> config.sh
echo "export KEY_SECRET='9fBnhxPTx5RbhA'" >> config.sh
```




## Usage

```
$ ./letsencrypt.sh -c -d example.com -t dns-01 -k 'hooks/alidns/hook.py'
#
# !! WARNING !! No main config file found, using default config!
#
Processing example.com
 + Signing domains...
 + Creating new directory /home/user/letsencrypt.sh/certs/example.com ...
 + Generating private key...
 + Generating signing request...
 + Requesting challenge for example.com...
 + Alidns hook executing: deploy_challenge
 + DNS not propagated, waiting 30s...
 + DNS not propagated, waiting 30s...
 + Responding to challenge for example.com...
 + Alidns hook executing: clean_challenge
 + Challenge is valid!
 + Requesting certificate...
 + Checking certificate...
 + Done!
 + Creating fullchain.pem...
 + Alidns hook executing: deploy_cert
 + ssl_certificate: /home/user/letsencrypt.sh/certs/example.com/fullchain.pem
 + ssl_certificate_key: /home/user/letsencrypt.sh/certs/example.com/privkey.pem
 + Done!
```