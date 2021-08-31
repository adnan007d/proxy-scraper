#!/usr/bin/env python3
"""
For https://proxyscrape.com/free-proxy-list
"""

import requests
import os
from os import path
import re
from connection import check_connection

PROTOCOLS = ["http", "socks4", "socks5"]


def get_results(protocols: list[str] = []) -> None:

    urls = {}

    if protocols:
        for protocol in protocols:
            assert protocol.lower() in PROTOCOLS, \
                f"Invalid Protocol: {protocol}\n Valid protocols are: {PROTOCOLS}"
            urls.update(
                {
                    f"{protocol.lower()}": f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={protocol.lower()}&timeout=10000&country=all&ssl=all&anonymity=all"
                }
            )
    else:
        urls.update(
            {
                "all": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=all&timeout=10000&country=all&ssl=all&anonymity=all"
            }
        )

    for url in urls:
        r = requests.get(urls[url])
        if r.status_code != 200:
            print(
                f"Request failed while fetching {url} proxies with status code {r.status_code}"
            )
            r.close()
            return
        _path = path.join('log', f"proxyspace-{url}-proxies.txt")
        with open(_path, 'w') as f:
            f.write(r.text)
        print(f"Fetched {url} proxies")


def re_split(string: str, char: str) -> tuple:

    pattern = re.compile(char)
    ip, port = re.split(pattern, string)
    return (ip, int(port))


def filter_ips(log_file: str, result_file: str, timeout: int = 10) -> None:
    if not os.path.exists(log_file):
        raise IOError(f"{log_file} doesn't exits")

    if os.path.exists(result_file):
        n = input(
            f"{result_file} already exists, do you want to ovewrite ? [y/N]: "
        )
        if n.lower() != 'y':
            return

        with open(result_file, 'w') as f:
            f.write('')

    f = open(log_file, 'r')
    ips = [line.strip() for line in f.read().split('\n')]

    for ip in ips:
        host, port = re_split(ip, ':')
        if check_connection(host=host, port=port, timeout=timeout):
            with open(result_file, 'a') as f:
                f.write(f"{host}:{port}\n")


get_results(protocols=["http", "socks4", "socks5"])
filter_ips(
    log_file='log/proxyspace-socks5-proxies.txt',
    result_file="log/proxyspace-socks5-working-proxies.txt",
    timeout=10
)
