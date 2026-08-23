# Command Reference

The commands below document the current Raspberry Pi validation workflow. They
are inspection or connectivity-test commands; none is intended to persistently
change system configuration.

## Host information

| Command | Purpose | System changes |
|---|---|---|
| `hostnamectl` | Show hostname, operating system, and architecture metadata. | None |
| `cat /etc/os-release` | Show the installed Linux distribution and release. | None |
| `uname -m` | Confirm the running architecture; expected: `aarch64`. | None |
| `free -h` | Show current memory totals and usage. | None |
| `findmnt /` | Show the device and filesystem mounted as root. | None |
| `whoami` | Show the current Linux user; expected: `ipp`. | None |

## Network state

| Command | Purpose | System changes |
|---|---|---|
| `ip -4 -br addr` | Show concise IPv4 interface state and addresses. | None |
| `ip route` | Show routes, including the default gateway. | None |
| `nmcli device status` | Show NetworkManager device state. | None |
| `nmcli connection show` | List saved and active NetworkManager connection profiles. | None |
| `ls -l /etc/resolv.conf` | Show whether the resolver file is a regular file or managed link. | None |
| `cat /etc/resolv.conf` | Show the resolver configuration currently presented to applications. | None |

For the verified configuration, `ip -4 -br addr` should show
`192.168.137.2/24` on `eth0`, and `ip route` should show a default route through
`192.168.137.1`.

## Connectivity tests

| Command | Purpose | System changes |
|---|---|---|
| `ping -c 4 192.168.137.1` | Test the local Ethernet path to the Windows ICS gateway. | Sends four ICMP echo requests only. |
| `ping -c 4 1.1.1.1` | Test public routing without relying on DNS. | Sends four ICMP echo requests only. |
| `getent hosts github.com` | Resolve GitHub through the system resolver. | None |
| `git ls-remote https://github.com/git/git.git HEAD` | Test DNS, HTTPS, and GitHub access through Git without cloning. | Reads remote metadata; does not change the local repository. |

A failed ping does not always prove the destination is unavailable because
some networks block ICMP. Compare the ping result with DNS and application-level
tests before deciding which layer failed.

## Remote-access services

| Command | Purpose | System changes |
|---|---|---|
| `systemctl status ssh --no-pager` | Show the SSH service state without opening a pager. | None |
| `tailscale status` | Show Tailscale state, addresses, and known peers. | None |

## Troubleshooting logs

```bash
journalctl -u NetworkManager -b --no-pager
journalctl -u tailscaled -b --no-pager
journalctl -u ssh -b --no-pager
```

`journalctl` reads service logs from the current boot (`-b`). The `-u` option
limits output to one service, and `--no-pager` prints directly to the terminal.
These commands do not alter services or logs. Log output may contain hostnames,
addresses, or other environment details, so review it before sharing publicly.

## Commands intentionally omitted

No persistent network-modification command is included because the exact active
connection profile and the command originally used to configure it have not
been recorded in this repository. Inspect the current state first and document
the actual change when a future configuration step is performed and verified.
