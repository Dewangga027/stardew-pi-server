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

## Phase 2 — Operating System Preparation

Phase 2 prepares the verified Raspberry Pi host for long-running server
workloads. The goal is to ensure the operating system is updated, healthy, and
able to return to a working state after a reboot.

### Update the package index

```bash
sudo apt update
```

`apt update` downloads the latest package metadata from the configured Debian
repositories.

This command does not upgrade installed packages. It only refreshes the local
package index used by APT.

Expected result:

- Repository metadata is downloaded successfully.
- No repository errors are reported.
- APT reports whether package upgrades are available.

This operation updates local APT metadata and does not require a rollback.

### Upgrade installed packages

After the package index has been refreshed:

```bash
sudo apt upgrade -y
```

`apt upgrade` installs available updates for packages already installed on the
Raspberry Pi.

The `-y` option automatically confirms the package installation prompt.

This is a persistent system change because installed package versions may be
updated.

Before continuing to later infrastructure phases, verify that the upgrade
finishes without package-management errors.

### Check systemd health

Inspect failed systemd units:

```bash
systemctl --failed
```

This command is read-only and does not modify services.

Review any failed unit before continuing. A failed service should not be
ignored automatically because it may indicate an incomplete upgrade, hardware
issue, or service configuration problem.

### Reboot after system preparation

Reboot the Raspberry Pi when required after system updates:

```bash
sudo reboot
```

This intentionally terminates the current SSH and VS Code Remote SSH sessions.

Because the Raspberry Pi is administered remotely, confirm that the
administration laptop can reconnect after the system has finished booting.

### Post-reboot verification

After reconnecting through SSH, verify the host:

```bash
uptime
ip -4 -br addr
ip route
getent hosts github.com
systemctl --failed
```

These commands verify different parts of the recovered system:

- `uptime` confirms that the Raspberry Pi completed a new boot and reports the
  current system load.
- `ip -4 -br addr` confirms that the expected IPv4 interfaces returned.
- `ip route` confirms that the default route returned after reboot.
- `getent hosts github.com` verifies DNS resolution through the configured
  system resolver.
- `systemctl --failed` checks for systemd units that failed during boot.

For the current verified network configuration, `eth0` should return with:

```text
192.168.137.2/24
```

The routing table should contain a default route through:

```text
192.168.137.1
```

Detailed network architecture and configuration belong in
`docs/networking.md`.

### Phase 2 verification

Phase 2 is considered complete when:

- Debian package metadata can be refreshed successfully.
- Installed package upgrades complete without package-management errors.
- No relevant critical systemd service is left in a failed state.
- The Raspberry Pi successfully reboots.
- SSH access returns after reboot.
- The configured Ethernet address and default route persist.
- DNS and external connectivity return after reboot.

The verified host can then proceed to 24/7 reliability preparation.

## Phase 3 — 24/7 Reliability Preparation

Phase 3 verifies that the Raspberry Pi host is healthy enough for continuous
operation before Docker and the Stardew Valley runtime are introduced.

### Verify power and thermal state

```bash
vcgencmd get_throttled
vcgencmd measure_temp
uptime
```

Verified results:

```text
throttled=0x0
temp=45.5'C
```

`throttled=0x0` indicates that no throttling or undervoltage condition was
reported during the check.

The measured CPU temperature provides an idle baseline. Thermal behavior must
be checked again after Docker and the Stardew server are running under load.

### Verify remote services

```bash
systemctl is-enabled ssh
systemctl is-enabled tailscaled
```

Verified result:

```text
enabled
enabled
```

SSH and Tailscale are configured to start automatically during boot.

### Verify storage and logging

```bash
df -h /
journalctl --disk-usage
systemctl is-enabled systemd-journald
```

Verified state:

- Root filesystem: approximately 35% used with 18 GB available.
- System journal usage: approximately 8 MB.
- `systemd-journald`: `static`, which is valid for this service.

The current microSD capacity is sufficient for the initial setup. Storage and
log growth must be reviewed again after long-running services are deployed.

### Verify the boot target

```bash
systemctl get-default
```

Verified result:

```text
graphical.target
```

The default boot target is currently left unchanged.

Whether the server should later use `multi-user.target` will be reviewed after
the Stardew runtime requirements are known.

### Phase 3 verification

Phase 3 is considered complete because:

- no power or throttling warning was reported;
- idle CPU temperature is healthy;
- baseline system load is low;
- SSH and Tailscale start automatically;
- storage capacity is currently sufficient;
- journal usage is small and controlled;
- the current boot target is known and documented.

The host is ready to proceed to Docker setup.