# 🌱 Stardew Pi Server — Agent Guide

> Rules for agents working on the Raspberry Pi 5 Stardew Valley 24/7 server.

## 🎯 Project at a Glance

| Area | Details |
|---|---|
| Platform | Raspberry Pi 5 · Debian 13 (Trixie) |
| Architecture | ARM64 / `aarch64` |
| RAM | 8 GB |
| Storage | microSD |
| Hostname | `raspberrypi5` |
| Linux user | `ipp` |
| Operations | SSH · VS Code Remote SSH · Docker |
| Remote Access | LAN · Tailscale |
| Priorities | Reproducible setup · backups · monitoring · recovery |

## 🛡️ Golden Rules

- Never commit secrets, credentials, private keys, `.env` files, saves, backups, logs, or runtime volumes.
- Check ARM64 compatibility before adding binaries or Docker images.
- Prefer native ARM64 solutions over emulation when practical.
- Keep configuration reproducible and document important commands or decisions.
- Verify changes before treating them as complete.
- Preserve unrelated user changes; only stage files required by the approved task.
- Do not make unnecessary changes to networking, SSH, or other administration paths.
- Prefer simple and maintainable solutions over unnecessary infrastructure complexity.

## 🗂️ Repository Role

GitHub is the source of truth for:

- Documentation
- Docker configuration
- Shell scripts
- Configuration templates
- Monitoring configuration
- Architecture decisions
- Troubleshooting notes

Runtime data stays outside Git.

Expected structure:

```text
stardew-pi-server/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── config/
├── docs/
│   ├── setup.md
│   ├── networking.md
│   ├── troubleshooting.md
│   └── commands.md
└── scripts/
```

The structure may evolve as the server architecture becomes clearer.

## 🌐 Networking

Current primary network:

| Item | Value |
|---|---|
| Raspberry Pi interface | `eth0` |
| Raspberry Pi IPv4 | `192.168.137.2/24` |
| Default gateway | `192.168.137.1` |
| DNS | `1.1.1.1` · `8.8.8.8` |
| Tailscale IPv4 | `100.122.179.123` |

Current topology:

```text
Internet
   ↓
Laptop Wi-Fi
   ↓
Windows Internet Connection Sharing
   ↓
Laptop Ethernet — 192.168.137.1
   ↓
Raspberry Pi eth0 — 192.168.137.2
```

The Ethernet connection is currently the primary SSH and administration path.

Before changing networking, inspect:

```bash
ip -4 -br addr
ip route
nmcli device status
nmcli connection show
```

Do not casually modify `netplan-eth0`, because a bad change may disconnect the active SSH session.

## 🐳 Docker Rules

- Verify `linux/arm64` support before introducing an image.
- Prefer maintained upstream images.
- Avoid privileged containers unless clearly required.
- Keep persistent runtime data outside Git.
- Document ports, volumes, environment variables, and dependencies.
- Use restart policies for services intended to run 24/7.
- Add health checks where they provide meaningful monitoring.
- Do not commit Docker volumes or generated container data.

Do not finalize the Stardew Docker stack until the selected server solution is confirmed to work on Raspberry Pi ARM64.

## 🧩 ARM64 Compatibility

Raspberry Pi 5 uses:

```text
aarch64
```

Do not assume normal desktop Linux binaries will work.

Before installing software, check:

- ARM64 binary availability
- Docker multi-architecture support
- Required dependencies
- Emulation requirements
- Performance impact of emulation
- Stardew Valley compatibility
- SMAPI compatibility

## 🌾 Stardew Server

Stardew Valley does not provide a traditional official dedicated server.

The final solution may involve:

- Stardew Valley Linux files
- SMAPI
- Headless display/runtime
- Unattended host or server bot
- Docker
- Persistent save storage

Research and validate the exact implementation before committing to an architecture.

Important server data must survive container recreation and Raspberry Pi reboot.

## 💾 Saves & Backups

- Stardew saves are critical runtime data.
- Keep saves outside container layers.
- Never commit saves or backups to Git.
- Create automatic backups.
- Use a retention policy.
- Monitor backup failures.
- Document restore procedures.
- Test restore procedures before considering the backup system complete.
- Keep at least one backup copy outside the Raspberry Pi when the server becomes production-like.

## 🖥️ 24/7 Reliability

The final server should recover from:

- Raspberry Pi reboot
- Docker restart
- Stardew process crash
- Temporary network interruption

Monitor at minimum:

- CPU usage
- RAM usage
- Disk usage
- CPU temperature
- Docker container state
- Stardew server state
- Backup status

Current storage is microSD. It is acceptable for initial development, but unnecessary writes and unbounded logs should be avoided.

## 🤖 Discord Integration

Discord integration is planned after the core Stardew server is stable.

Potential responsibilities:

- Server status
- Downtime alerts
- Backup notifications
- Maintenance notifications
- Player coordination
- Server changelogs
- Read-only status commands
- Restricted admin operations

Never expose arbitrary shell execution through Discord.

Administrative commands must use strict authorization.

## 📝 Documentation Rules

Document significant setup and architecture changes while implementing them.

For important commands, explain:

- What the command does
- Why it is needed
- What it changes
- Whether the change is temporary or persistent
- How to verify the result
- How to revert it when appropriate

Do not postpone all documentation until the end of the project.

## 🔎 Troubleshooting Approach

Do not immediately change configuration when something fails.

Use:

```text
Observe
→ Gather evidence
→ Identify the failing layer
→ Form a hypothesis
→ Run the smallest useful test
→ Confirm root cause
→ Apply the minimal fix
→ Verify
→ Document
```

For networking:

```text
Physical link
→ Interface
→ IP address
→ Local subnet
→ Default route
→ Internet by IP
→ DNS
→ Application
```

## 🌿 Branch Guide

Branches should describe the work, not the device performing it.

Good:

```text
feat/pi-base-setup
feat/docker-setup
feat/stardew-server
feat/backup-system
feat/monitoring
feat/discord-integration
fix/networking
```

Avoid:

```text
raspberryPi5
```

## 📝 Commit Guide

Use: `type(scope): description`

| Type | Use for |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fixes |
| `docs` | Documentation |
| `refactor` | Code changes without new behavior |
| `test` | Tests |
| `chore` | Maintenance |
| `ci` / `build` | CI or build changes |
| `perf` | Performance improvements |
| `revert` | Reverting a commit |

Write descriptions in English, lowercase, imperative mood, and without a trailing period.

Keep each commit focused on one logical change.

```text
feat(server): add automated save backup
fix(docker): correct arm64 image selection
docs(setup): document remote ssh deployment
docs(network): document windows ics configuration
```

For breaking changes, add `!` after the type or scope and include a `BREAKING CHANGE:` footer.

## ✅ Before Committing

- [ ] Review `git status`.
- [ ] Review the complete diff.
- [ ] Run relevant tests or validation checks.
- [ ] Stage only files related to the task.
- [ ] Confirm no secrets or runtime data are included.
- [ ] Confirm documentation is updated when required.
- [ ] **Ask the user for explicit commit approval.**

## 🚀 Before Pushing

- [ ] Verify the current local branch.
- [ ] Verify the destination remote and branch.
- [ ] Verify the working tree.
- [ ] Review outgoing commits.
- [ ] Tell the user the source and destination branches.
- [ ] **Ask for separate, explicit push approval.**
- [ ] Do not treat commit approval as push approval.
- [ ] Do not push directly to `main` unless that exact destination is approved.
- [ ] Never force-push or rewrite shared history without explicit approval.

## 🗺️ Project Roadmap

| Phase | Task | Status |
|---|---|---|
| 1 | Raspberry Pi validation | ✅ Complete |
| 2 | Operating system preparation | 🔄 Current |
| 3 | 24/7 reliability preparation | ⏳ |
| 4 | Docker | ⏳ |
| 5 | Stardew ARM64 compatibility | ⏳ |
| 6 | Stardew server installation | ⏳ |
| 7 | LAN multiplayer testing | ⏳ |
| 8 | Backup system | ⏳ |
| 9 | Reliability testing | ⏳ |
| 10 | Remote multiplayer | ⏳ |
| 11 | Monitoring | ⏳ |
| 12 | Discord integration | ⏳ |
| 13 | Final documentation | ⏳ |

GitHub documentation runs in parallel with every phase.

The roadmap may be adjusted when compatibility constraints, implementation issues, or better architecture decisions are discovered.

## ⚙️ Working Principle

Prefer:

```text
Understand
→ Implement
→ Test
→ Verify
→ Document
→ Commit
```

Reliability and recoverability are more important than unnecessary complexity.
