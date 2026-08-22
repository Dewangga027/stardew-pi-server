# Troubleshooting

## Resolved: Ethernet had no internet or DNS

### Observed history

The Raspberry Pi originally used `192.168.50.2/24`. Windows Internet
Connection Sharing later placed the laptop Ethernet interface on
`192.168.137.1` and used the `192.168.137.0/24` subnet.

This left the Raspberry Pi with network settings that no longer matched the
Ethernet subnet. The Pi initially had no working route to the internet, and
hostname resolution also failed. Tailscale was managing `resolv.conf`, which
was relevant when tracing where DNS settings came from.

### Diagnostic sequence

The failure was separated into layers instead of changing configuration
immediately:

```bash
ip -4 -br addr
ip route
nmcli device status
nmcli connection show
ping -c 4 192.168.137.1
ping -c 4 1.1.1
getent hosts github.com
ls -l /etc/resolv.conf
cat /etc/resolv.conf
tailscale status
```

- The address and route commands reveal whether `eth0` is on the same subnet as
  the laptop and whether a default route exists.
- Pinging the gateway tests the local Ethernet path.
- Pinging a public IP tests routing without involving DNS.
- `getent hosts` tests the configured system resolver.
- Inspecting `/etc/resolv.conf` shows its current contents and whether it is a
  link managed by another service. These commands only read the file.
- `tailscale status` confirms Tailscale state without changing its DNS behavior.

### Root cause

The Windows ICS Ethernet network and the Raspberry Pi configuration did not
match. An address from `192.168.50.0/24` could not directly use the laptop at
`192.168.137.1` as its gateway. DNS could not work reliably until the basic
route was corrected, and the resolver state also needed to account for
Tailscale managing `resolv.conf`.

### Resolution already applied

The Raspberry Pi `eth0` configuration was aligned with the Windows ICS network:

| Setting | Working value |
|---|---|
| Address | `192.168.137.2/24` |
| Gateway | `192.168.137.1` |
| DNS | `1.1.1.1`, `8.8.8.8` |

With the correct gateway and DNS values, internet access and hostname
resolution were restored. The exact persistent configuration command used at
the time is not documented, so no replacement command is inferred here.

### Verification

```bash
ip -4 -br addr
ip route
ping -c 4 192.168.137.1
ping -c 4 1.1.1
getent hosts github.com
git ls-remote https://github.com/git/git.git HEAD
```

The verified end state is:

- `eth0` has `192.168.137.2/24`.
- The default route uses `192.168.137.1`.
- Public IP connectivity works.
- Hostname resolution works.
- GitHub is reachable through Git.
- SSH and VS Code Remote SSH work over the administration path.

## If the problem returns

Start with observation and repeat the layered checks above. Windows ICS may
change the laptop-side network, so confirm its current Ethernet address before
assuming `192.168.137.1` is still valid.

Do not blindly restore the former `192.168.50.2/24` address: it does not match
the currently verified ICS subnet. Do not hand-edit `/etc/resolv.conf` while it
is managed by Tailscale, because the edit may be overwritten and may hide the
real source of the resolver configuration. Inspect the active NetworkManager
profile and Tailscale state before selecting a persistent fix.
