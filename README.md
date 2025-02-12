# mitmproxy-setup

Here's the mitmproxy setup I use when working on various researches, pentests, and bug bounties.

Contributions are welcome! Feel free to share any interesting addons or views you have.

## Background

### Previous Work

Long ago, I wrote a blog post of my [mitmproxy + OpenVPN setup](https://blog.flatt.tech/entry/mitmproxy) at my former workplace.
Then I later published another [mitmproxy + OpenVPN setup](https://gist.github.com/stypr/abe9ef83556759847c063ae9389fa0ae) to show the current setup both in English and Korean.

### What's New?

This time introduces a few more changes:

### Directory Structure Updates  

- **`views/*`**: Automates decryption of specific request/response data to enhance data visualization.
- **`addons/*`**: Acts as plugins to perform actions on send/receive HTTP data

#### Transition to WireGuard Setup  

- Completely Replaced OpenVPN with WireGuard for improved functionality. (Ref. [WireGuard Mode](https://mitmproxy.org/posts/wireguard-mode/))
  - WireGuard mode supports DNS and UDP packet manipulation, unlike the transparent proxy, which cannot pass UDP packets when the upstream SOCKS5 proxy only supports TCP.
  - WireGuard setups are significantly simpler compared to traditional OpenVPN configurations.
  - Some limitations remain, such as partial handling of HTTP2/HTTP3 traffics, but there seems not much problem of just using old HTTPS.


## Installations

### Overview

The installation process is similar to the [old gist](https://gist.github.com/stypr/abe9ef83556759847c063ae9389fa0ae), with a few key differences:
- OpenVPN is no longer required.
- The `bind9` dependency is removed, as [mitmproxy now handles DNS manipulations](https://github.com/Kriechi/mitmproxy/blob/dns-addon/docs/src/content/overview-features.md#dns-manipulation).

1. Install WireGuard
    ```sh
    apt install -y wireguard
    ```

2. Install Caddy
    Follow instructions [here](https://caddyserver.com/docs/install).
    - Add passwords to the [Caddyfile](caddy/Caddyfile) using `caddy hash-password`.
    - Move [Caddyfile](caddy/Caddyfile) to `/etc/caddy`.

3. Install mitmproxy
    ```sh
    apt install -y python3-pyasn1 python3-flask python3-dev python3-urwid python3-pip libxml2-dev libxslt-dev libffi-dev  
    pip3 install -U mitmproxy pycryptodome requests --break-system-packages  
    mitmproxy --version  
    ```

4. Set up WARP proxy (default)
   The script proxies through [WARP](https://one.one.one.one/) by default. You may need to customize the script for your needs.

5. Run the Setup:
   Once everything is ready, use:
   ```sh
   screen ./run.sh
   ```

#### Installing WARP on Linux

1. Install WARP CLI.

```sh
curl https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ bookworm main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list
sudo apt update && sudo apt install -y cloudflare-warp
```

2. Register WARP, set proxy with appropriate ports, start proxy.

```sh
warp-cli registration new
warp-cli proxy port 40000
warp-cli mode proxy
warp-cli connect
```
