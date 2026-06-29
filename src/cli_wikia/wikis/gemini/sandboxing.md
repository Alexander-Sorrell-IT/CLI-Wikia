# Sandboxing

Sandboxing isolates potentially dangerous operations — shell commands and file modifications — from your host system, putting a security barrier between the model's tool calls and your environment. It limits filesystem access to the project directory and provides reproducible, consistent execution environments.

Sandboxing is **off by default**. You opt in per-session (flag), per-environment (env var), or persistently (settings).

---

## Enabling sandboxing

There are three ways to turn sandboxing on, listed in order of precedence (the flag wins over the env var, which wins over settings):

| Method | How |
|---|---|
| Command flag | `gemini -s …` or `gemini --sandbox …` |
| Environment variable | `GEMINI_SANDBOX=true\|docker\|podman\|sandbox-exec\|runsc\|lxc` |
| Settings file | `"sandbox"` key inside the `tools` object of `settings.json` |

```bash
# Flag
gemini -s -p "analyze the code structure"

# Env var (macOS/Linux)
export GEMINI_SANDBOX=true
gemini -p "run the test suite"
```

```powershell
# Env var (Windows PowerShell)
$env:GEMINI_SANDBOX="true"
gemini -p "run the test suite"
```

```json
{
  "tools": {
    "sandbox": "docker"
  }
}
```

`"sandbox": true` picks a default method for your platform; a string (`"docker"`, `"podman"`, `"sandbox-exec"`, `"runsc"`, `"lxc"`) selects a specific one.

---

## Sandboxing methods

The right method depends on your OS and preferred container runtime.

| Method | Platform | Notes |
|---|---|---|
| macOS Seatbelt (`sandbox-exec`) | macOS only | Lightweight, built-in; no container needed |
| Docker / Podman | Cross-platform | Full process isolation; default image `ghcr.io/google/gemini-cli:latest` |
| gVisor (`runsc`) | Linux only | Strongest isolation; user-space kernel; must be set explicitly |
| LXC / LXD | Linux only (experimental) | Full-system container with `systemd`/`snapd`; for tools like Snapcraft |
| Windows Native | Windows only | Uses `icacls` integrity levels |

### macOS Seatbelt

Built-in sandboxing via `sandbox-exec`. The default profile is `permissive-open`: it restricts writes outside the project directory but allows most other operations.

Profiles are selected with the `SEATBELT_PROFILE` environment variable:

| Profile | Writes | Reads | Network |
|---|---|---|---|
| `permissive-open` (default) | Restricted | Open | Allowed |
| `permissive-proxied` | Restricted | Open | Via proxy |
| `restrictive-open` | Strict | Open | Allowed |
| `restrictive-proxied` | Strict | Open | Via proxy |
| `strict-open` | Strict | Restricted | Allowed |
| `strict-proxied` | Strict | Restricted | Via proxy |

Custom Seatbelt profiles can be supplied as `.gemini/sandbox-macos-<name>.sb` files in your project and referenced via `SEATBELT_PROFILE=<name>`. (Profile file naming — `sandbox-macos-*.sb` — should be verified in official docs.)

### Docker / Podman

Cross-platform isolation. Docker or Podman must be installed and running.

**Workspace mounting:** inside the container your current working directory is mounted at the **exact same absolute path** as on the host. Running from `/Users/you/project` means the sandbox operates within `/Users/you/project` inside the container, so the model can read and modify project files while staying isolated from the rest of your system.

```bash
# Recommended: env var
export GEMINI_SANDBOX=docker
gemini -p "build the project"
```

```json
// Or persistently in settings.json
{ "tools": { "sandbox": "docker" } }
```

### gVisor (runsc)

The strongest available isolation on Linux. Containers run inside a user-space kernel via [gVisor](https://github.com/google/gvisor), which intercepts all container syscalls and handles them in a sandboxed kernel written in Go.

When `sandbox` is `runsc`, Gemini CLI runs `docker run --runtime=runsc …`. runsc is **not auto-detected** — you must request it explicitly (`GEMINI_SANDBOX=runsc` or `"sandbox": "runsc"`). Setup requires installing the runsc binary, configuring the Docker daemon to use the runsc runtime, and verifying the installation.

### LXC / LXD (experimental)

Full-system containers running a complete Linux system (`systemd`, `snapd`, etc.) — ideal for tools that don't work in standard Docker containers, such as Snapcraft and Rockcraft.

```bash
lxd init --auto                          # first time only
lxc launch ubuntu:24.04 gemini-sandbox   # create + start the container
export GEMINI_SANDBOX=lxc
gemini -p "build the project"
```

Use `GEMINI_SANDBOX_IMAGE` to target a custom container name. Limitations: Linux only; the container **must already exist and be running** (Gemini does not create it); the workspace is bind-mounted at the same absolute path and must be writable inside the container.

### Windows Native

Uses `icacls` to set a "Low Mandatory Level" on files and directories it writes to. These integrity-level changes **persist** on the filesystem after the session ends. Reset manually with:

```powershell
icacls "C:\path\to\dir" /setintegritylevel Medium
```

System folders such as `C:\Windows` are automatically skipped.

---

## Custom sandbox images

For container-based methods you can supply your own image when a project needs specific dependencies. Any Docker/Podman image works as long as it has standard shell utilities (such as `bash`).

### Use an existing image

Point at a registry image via settings or the `GEMINI_SANDBOX_IMAGE` env var:

```json
{
  "tools": {
    "sandbox": {
      "command": "docker",
      "image": "us-central1-docker.pkg.dev/my-project/my-repo/my-custom-sandbox:latest"
    }
  }
}
```

```bash
export GEMINI_SANDBOX_IMAGE="us-central1-docker.pkg.dev/my-project/my-repo/my-custom-sandbox:latest"
```

### Build an image from a Dockerfile

Define the environment as code and let Gemini CLI build it:

1. Create `.gemini/sandbox.Dockerfile` in your project root.
2. Ensure the `gh` CLI is installed and authenticated (if you base the image on the default `ghcr.io/google/gemini-cli` image).
3. Run with `BUILD_SANDBOX` set:

```bash
BUILD_SANDBOX=1 GEMINI_SANDBOX=docker gemini -p "run my custom build"
```

> Automatic `BUILD_SANDBOX` builds are only available when running Gemini CLI **from source**. npm installs need a prebuilt image instead.

---

## Tool sandboxing

Tool-level sandboxing isolates individual tool executions (such as `shell_exec` and `write_file`) instead of sandboxing the whole CLI process. This gives better integration with your local environment for non-tool tasks (UI rendering, config loading) while still isolating tool-driven operations.

Disable it with:

```json
{
  "security": {
    "toolSandboxing": false
  }
}
```

> Changing `security.toolSandboxing` requires restarting Gemini CLI to take effect.

---

## Sandbox expansion

Sandbox expansion is a dynamic permission system: when a sandboxed command fails due to restrictions (blocked paths or network), or is proactively identified as needing extra permissions (e.g. `npm install`), Gemini CLI shows a **Sandbox Expansion Request** modal explaining the additional permissions required. Approving grants the extended permissions for that single run, so you don't have to re-run commands with looser settings.

### Mounting files outside the workspace

By default the sandbox only sees the current project workspace. To expose other paths, use `SANDBOX_MOUNTS` — a comma-separated list of `from:to:opts` definitions. `to` defaults to the same path as `from`; `opts` defaults to `ro` (read-only). The `from` path must be absolute.

```bash
export SANDBOX_MOUNTS="/path/on/host:/path/in/container:rw,/another/path:ro"
```

---

## Proxying

The `*-proxied` Seatbelt profiles (and the proxy-enabled container modes) route network traffic through a proxy rather than allowing direct outbound access. Use these when you need to filter, inspect, or centrally log the model's network activity. Pair a proxied profile with your organization's proxy configuration and verify the proxy is reachable if you hit network errors.

---

## Running Gemini CLI inside a Docker container

If the CLI itself runs inside a container and you want sandboxing, you must let it spawn **sibling** sandbox containers via the host's Docker daemon:

1. **Mount the Docker socket** — map `/var/run/docker.sock` so the CLI can talk to the host daemon.
2. **Align workspace paths** — the workspace path inside the container must exactly match its absolute path on the host, because the host daemon resolves volume mounts against the host filesystem.

```bash
docker run -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /absolute/path/on/host/project:/absolute/path/on/host/project \
  -w /absolute/path/on/host/project \
  -e GEMINI_SANDBOX=docker \
  ghcr.io/google/gemini-cli:latest
```

---

## Advanced settings

### Custom container flags

Inject extra flags into the `docker`/`podman` command with `SANDBOX_FLAGS` (space-separated for multiple):

```bash
export SANDBOX_FLAGS="--security-opt label=disable"   # e.g. disable SELinux labeling (Podman)
export SANDBOX_FLAGS="--flag1 --flag2=value"
```

### Linux UID/GID handling

The sandbox handles user permissions automatically on Linux. Override with:

```bash
export SANDBOX_SET_UID_GID=true    # force host UID/GID
export SANDBOX_SET_UID_GID=false   # disable UID/GID mapping
```

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `Operation not permitted` | Command needs access outside the sandbox — use a more permissive profile or add a mount point |
| Missing commands | Add them to a custom Dockerfile (npm installs need a prebuilt image), or install via `sandbox.bashrc` |
| Network errors | Confirm the profile allows network; verify proxy configuration |

```bash
# Debug output
DEBUG=1 gemini -s -p "debug command"

# Inspect the sandbox environment
gemini -s -p "run shell command: env | grep SANDBOX"
gemini -s -p "run shell command: mount | grep workspace"
```

> `DEBUG=true` in a project's `.env` file does **not** affect gemini-cli (it's excluded automatically). Use a `.gemini/.env` file for gemini-cli-specific debug settings.

---

## Limitations & security notes

- Sandboxing reduces but does not eliminate all risk — use the most restrictive profile that still allows your work.
- GUI applications may not work inside sandboxes.
- Container overhead is minimal after the first build.
- Mounting `/var/run/docker.sock` grants effective host access; treat it carefully.

---

## See also

- [permissions.md](./permissions.md) — approval modes, the policy engine, and trusted folders
- [settings.md](./settings.md) — full `tools.sandbox` and `security.*` keys
- [configuration.md](./configuration.md) — environment variables and precedence
- [cli-reference.md](./cli-reference.md) — the `-s`/`--sandbox` flag
