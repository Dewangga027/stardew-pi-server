# Raspberry Pi Setup

## Verified baseline

This document records only the setup that has already been completed and
verified.

| Area | Verified state |
|---|---|
| Hardware | Raspberry Pi 5 with 8 GB RAM |
| Operating system | Debian 13 (Trixie) |
| Architecture | ARM64 / `aarch64` |
| Storage | microSD |
| Hostname | `raspberrypi5` |
| Linux user | `ipp` |
| Primary interface | `eth0` |
| Remote access | SSH and VS Code Remote SSH working |
| Overlay network | Tailscale installed |
| External connectivity | DNS resolution and GitHub connectivity working |

The microSD card is acceptable for the current setup phase. Future services
should avoid unnecessary writes and unbounded logs.

## Verify the host

The following commands inspect the system without changing it:

```bash
hostnamectl
cat /etc/os-release
uname -m
free -h
findmnt /
whoami
```

- `hostnamectl` reports the hostname and operating-system metadata. Confirm the
  hostname is `raspberrypi5`.
- `cat /etc/os-release` reports the installed distribution and release. Confirm
  Debian 13 (Trixie).
- `uname -m` reports the running machine architecture. Confirm `aarch64` before
  selecting binaries or container images.
- `free -h` reports memory totals and current usage in human-readable units.
- `findmnt /` identifies the device and filesystem backing the root mount. It is
  useful when checking storage assumptions.
- `whoami` reports the current account. Administrative instructions in this
  repository assume the user is `ipp`.

These checks are temporary observations only; they make no persistent changes
and need no rollback.

## Verify remote and external access

From an active Raspberry Pi shell, use:

```bash
systemctl status ssh --no-pager
tailscale status
getent hosts github.com
git ls-remote https://github.com/git/git.git HEAD
```

- `systemctl status ssh --no-pager` shows whether the SSH service is running. It
  does not restart or modify the service.
- `tailscale status` reports the current Tailscale state and peers. It does not
  change Tailscale configuration.
- `getent hosts github.com` verifies resolution through the system resolver.
- `git ls-remote` verifies that Git can reach GitHub over HTTPS without cloning
  a repository or changing the working tree.

VS Code Remote SSH has also been verified from the administration laptop. That
client-side connection is the practical check that SSH transport and the remote
development workflow both work.

## Not configured in this phase

This baseline does not claim that any of the following are installed or
configured:

- Docker or a container stack
- Stardew Valley server components
- SMAPI
- Backups, monitoring, or automated recovery

Those areas must be documented only after their implementation has been tested
on this ARM64 host.
