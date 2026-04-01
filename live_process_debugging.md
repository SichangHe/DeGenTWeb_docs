# Live process debugging (Python 3.14 `sys.remote_exec`)

This document explains how to debug a running Python process in this repo,
how to grant access to another user (for example the agent user), and which
local scripts are useful for memory investigations.

## What `sys.remote_exec` does

`sys.remote_exec(pid, script_path)` asks the target Python process to run a
Python script file.

Important behavior from Python docs:

- `sys.remote_exec` may return before the script executes.
- Script execution happens later when the target reaches a safe evaluation point.

So always wait and poll for output files/logs after injection.

## Permission model on Linux

Python 3.14 remote debugging docs state:

- tracer needs ptrace permission (`CAP_SYS_PTRACE` or equivalent),
- target should be same UID and signal-able,
- Yama (`ptrace_scope`) can restrict attach.

## Human setup: grant debug access to another user

Assume:

- target process owner user: `TARGET_USER`
- debugging user (agent): `DEBUG_USER`
- Python binary used by debugger: `/path/to/python`

### 1) Check current state

```sh
id
cat /proc/sys/kernel/yama/ptrace_scope
ps -o pid,user,args -p <PID>
```

### 2) Preferred: run debugger as same user as target

If possible, run the debugger as the same user as the target process.

### 3) If different users: grant capability to debugger Python

Run as root:

```sh
sudo setcap cap_sys_ptrace+ep /path/to/python
getcap /path/to/python
```

### 4) If Yama blocks attach, relax ptrace policy

Temporary until reboot:

```sh
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```

Persistent:

```sh
echo "kernel.yama.ptrace_scope = 0" | sudo tee /etc/sysctl.d/99-dw-debug.conf
sudo sysctl --system
```

### 5) Verify the debugger user can signal target

```sh
kill -0 <PID> && echo OK
```

## Basic injection workflow

### Inject

```sh
"/path/to/python" - <<'PY'
import sys
print(sys.remote_exec(<PID>, "/abs/path/to/script.py"))
PY
```

### Wait and poll

```sh
sleep 90
ls -l /tmp/<expected_output_file>
```

If file not present, wait longer and poll again.

## Useful scripts in `scripts/`

### Stable/kept probes

- `scripts/muppy_heap_breakdown.py`
  - per-type heap size summary, includes `str >= 1MB` totals.
- `scripts/muppy_large_str_owners.py`
  - tags large strings by content and reports owner fields.
- `scripts/owner_awaited_by_probe.py`
  - finds task with largest `_asyncio_awaited_by` set and summarizes waiters.
- `scripts/clear_largest_awaited_by.py`
  - one-off cleanup of done waiters for the largest owner task.
  - diagnostic/rescue tool only; not a product fix.
- `scripts/remote_exec_write_probe.py`
  - minimal sanity check that remote script execution is happening.

### Typical sequence for memory leak triage

1. Run `muppy_heap_breakdown.py` to confirm dominant object type.
2. Run `muppy_large_str_owners.py` to identify payload type and owner fields.
3. Run `owner_awaited_by_probe.py` to detect task waiter retention patterns.
4. Patch root cause in normal code path.
5. Optionally run `clear_largest_awaited_by.py` once to validate hypothesis live.

## Practical caveats

- Always use absolute script paths for `sys.remote_exec`.
- Make scripts write outputs to predictable absolute paths (`/tmp/...` or repo data dir).
- For long-running probes, use larger waits (90-180s) before concluding failure.
- Avoid assuming immediate side effects after `sys.remote_exec` returns.

## Security notes

- Lowering `ptrace_scope` and granting `CAP_SYS_PTRACE` both reduce hardening.
- Only enable these in trusted environments and revert if not needed.
