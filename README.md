## mitmproxy-tools

List of generic mitmproxy scripts I use while working on various researches, pentests and bug bounties.

Previously

* I wrote a blog post about my [mitmproxy + openvpn](https://blog.flatt.tech/entry/mitmproxy) setup at my former workpace.
* then I wrote another [mitmproxy + openvpn](https://gist.github.com/stypr/abe9ef83556759847c063ae9389fa0ae) setup to show the current setup

What has been changed this time

* Directory structures have been changed for convenient addons
  - `views/*` can be used to auto decrypt some of request/response data for better visuals
  - `addons/*` can be used to work like plugins to do actions upon send/receive.

* Replacing openvpn setups to wireguard setups
  - When upstream SOCK5 proxy only supports TCP, UDP packets have to be passed through somehow.
    1. Unfortunately, transparent proxy will not pass UDP packets, while the wireguard mode does support DNS and UDP packet mitm.
  - Setups are much simpler than typical openvpn setup.
  - Reference: https://mitmproxy.org/posts/wireguard-mode/
  - There are still some limitations like lack of handling for HTTP2 and HTTP3, but we can still use the old HTTPS.

Feel free to contribute if you have any interesting addons/views to share.

### Installations

#### Summary

Most of them are same as [the gist version](https://gist.github.com/stypr/abe9ef83556759847c063ae9389fa0ae), except that you don't have to install OpenVPN anymore.

1. Install `wireguard` on your system (`apt install -y wireguard`)

2. `bind9` is not needed anymore. Also, [mitmproxy now has its own way to handle DNS manipulations now](https://github.com/Kriechi/mitmproxy/blob/dns-addon/docs/src/content/overview-features.md#dns-manipulation).

2. Install [Caddy](https://caddyserver.com/docs/install)

3. Add passwords on [caddy/Caddyfile](caddy/Caddyfile) using `caddy hash-password`, move files to `/etc/caddy`

4. Install mitmproxy to latest
```sh
apt install -y python3-pyasn1 python3-flask python3-dev python3-urwid python3-pip libxml2-dev libxslt-dev libffi-dev
pip3 install -U mitmproxy --break-system-packages
mitmproxy --version
```

5. The script proxies through upstream [WARP](https://one.one.one.one/) by default.
   You might want to install or make appropriate changes to the script.

6. Once everything is done, `screen ./run.sh`

#### Installing WARP on Linux

1. Install WARP CLI.

```sh
curl https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ bookworm main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt update && sudo apt install -y cloudflare-warp
```

2. Register WARP, set proxy with appropriate ports, start proxy.

```sh
warp-cli register
warp-cli proxy port 40000
warp-cli mode proxy
warp-cli connect
```
