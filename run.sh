#!/bin/sh

warp-cli disconnect
warp-cli connect
mitmweb \
  --ignore-hosts dns.google.com \
  --web-port 8000 \
  --web-host localhost \
  --ssl-insecure \
  --set stream_large_bodies=1024000 \
  --set connection_strategy=lazy \
  --set http2=false \
  --set http3=false \
  --no-web-open-browser \
  --set confdir=$PWD/config \
  --mode wireguard:$PWD/config/wireguard_server1.conf@303 \
  --script main.py

# For mulitple clients, add more configs.
# Client configurations are available in the web frontend
#   --mode wireguard:$PWD/config/wireguard_server2.conf@304
