#!/usr/bin/env python3
from socks5_proxy import Socks5Proxy

if __name__ == "__main__":
    proxy = Socks5Proxy()
    proxy.start()