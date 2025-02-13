# mitmproxy-setup

Here's the mitmproxy setup I use when working on various researches, pentests, and bug bounties.

Personally I have not been using Burp for many years unless I really had a reason to. Reasons include:

1. Free of cost.
2. Convenient to debug when performing security researches or playing CTFs.
3. Convenient to add plugins or features if you can write a code in python.
4. Viewing and editing via web interface. Simply install at your home, VPS, or work. extremely lightweight.
5. [Chaining proxies](https://docs.mitmproxy.org/stable/concepts-modes/#upstream-proxy) is very convenient.

Contributions are welcome! Feel free to share any interesting addons or views you have.

You may also want to look the official [Addons Examples](https://github.com/mitmproxy/mitmproxy/tree/main/examples/addons) for boilerplate codes.

## Background

### Previous Work

Long ago, I wrote a blog post of my [mitmproxy + OpenVPN setup](https://blog.flatt.tech/entry/mitmproxy) at my former workplace.
Later, I published another [mitmproxy + OpenVPN setup](https://gist.github.com/stypr/abe9ef83556759847c063ae9389fa0ae) to share my existing setup both in English and Korean.

### What's New?

This time introduces a few more changes:

#### Directory Structure Updates  

Directories are divided for convenient coding, hot-reloading on subdirectories are included

- **`views`**: Automates manipulation of specific request/response data to enhance data visualization.
- **`addons*`**: Acts as plugins to perform actions on send/receive HTTP data

#### Transition to WireGuard Setup  

- Completely Replaced OpenVPN with WireGuard for improved functionality. (Ref. [WireGuard Mode](https://mitmproxy.org/posts/wireguard-mode/))
  - WireGuard mode supports DNS and UDP packet inspection / manipulation unlike the transparent proxy. 
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

3. Install mitmproxy and check versions
    ```sh
    apt install -y python3-pyasn1 python3-flask python3-dev python3-urwid python3-pip libxml2-dev libxslt-dev libffi-dev  
    pip3 install -r requirements.txt --break-system-packages # or enable venv
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

1. Install WARP CLI

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
