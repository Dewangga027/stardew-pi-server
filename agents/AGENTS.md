# Project Context

Project: Raspberry Pi 5 Stardew Valley 24/7 Server

## Goals
- Run a Stardew Valley server continuously on Raspberry Pi 5.
- Use Docker where appropriate.
- Keep all configuration reproducible.
- Maintain backup, monitoring, and recovery scripts.
- Store documentation in this repository.

## Target Environment
- Raspberry Pi 5
- Raspberry Pi OS 64-bit
- ARM64 / aarch64
- Managed primarily through SSH and VS Code Remote SSH

## Repository Rules
- Never commit `.env`
- Never commit passwords, tokens, or SSH private keys
- Never commit Stardew save backups
- Never commit Docker runtime volumes
- Check ARM64 compatibility before adding binaries or Docker images
- Document important commands and architecture decisions