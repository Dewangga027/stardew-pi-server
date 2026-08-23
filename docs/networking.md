# Networking

## Verified network

The Raspberry Pi currently uses its wired `eth0` interface as the primary
administration and internet path.

| Item | Verified value |
|---|---|
| Raspberry Pi interface | `eth0` |
| Raspberry Pi address | `192.168.137.2/24` (static) |
| Default gateway | `192.168.137.1` |
| DNS servers | `1.1.1.1`, `8.8.8.8` |
| Windows laptop Ethernet address | `192.168.137.1` |
| Remote administration | SSH and VS Code Remote SSH |
| Overlay networking | Tailscale installed |

The laptop shares its internet connection through Windows Internet Connection
Sharing (ICS):

```text
Internet
   |
Windows laptop Wi-Fi
   |
Windows Internet Connection Sharing
   |
Laptop Ethernet — 192.168.137.1
   |
Raspberry Pi eth0 — 192.168.137.2/24
```

ICS places the Ethernet link on `192.168.137.0/24`. The laptop is both the
next-hop router and the local peer used to administer the Raspberry Pi.

## Inspect the current state

Run these read-only commands before changing any network configuration:

```bash
ip -4 -br addr
ip route
nmcli device status
nmcli connection show
```

- `ip -4 -br addr` shows the IPv4 addresses assigned to each interface. Use it
  to confirm that `eth0` has `192.168.137.2/24`.
- `ip route` shows the kernel routing table. Use it to confirm that the default
  route points to `192.168.137.1` through `eth0`.
- `nmcli device status` shows which devices NetworkManager considers connected.
- `nmcli connection show` lists NetworkManager connection profiles. Inspect the
  active profile before attempting any persistent change.

These commands do not change the system and require no rollback.

## Verify connectivity by layer

Test the path from the nearest dependency outward:

```bash
ping -c 4 192.168.137.1
ping -c 4 1.1.1
getent hosts github.com
git ls-remote https://github.com/git/git.git HEAD
```

1. Pinging `192.168.137.1` checks the Ethernet link and local subnet.
2. Pinging `1.1.1.1` checks routing through the laptop without depending on
   DNS. A failed ping is useful evidence, although some networks may block
   ICMP.
3. `getent hosts github.com` checks hostname resolution through the system
   resolver.
4. `git ls-remote` checks DNS, HTTPS, and GitHub connectivity without cloning or
   changing the local repository.

## Change safety

The Ethernet link is the primary SSH administration path. A wrong address,
prefix, gateway, DNS value, or connection profile can disconnect the active
session. Inspect the active profile and keep local access available before
making persistent changes.

The exact file or command originally used to persist the current settings has
not been recorded here, so this document does not invent one. Do not edit
`netplan-eth0`, NetworkManager profiles, or Tailscale DNS settings until the
active configuration has been inspected and a rollback method is known.
