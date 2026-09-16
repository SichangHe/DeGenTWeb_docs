# Personal browser authentication

Status: draft for human review. Do not treat this document as agent
instructions until the human approves this exact text.

This workflow governs DW agents that need a website available only through the
human's authenticated personal-browser session. It remains applicable while DW
uses that shared browser profile.

## Human-established session

1. From the personal-browser setup, an agent runs
   `scripts/browser-use/opencode-share`. This supported entry point starts or
   reuses the display, Chrome, noVNC, and resize workers and prints the human's
   noVNC URL and SSH-forwarding command. `opencode-ensure` alone does not start
   noVNC.
2. The agent confirms that both the noVNC URL and Chrome's browser-control
   health endpoint respond. It then relinquishes browser control and stops any
   agent or automation that can observe the display or browser-control endpoint.
3. The human enters the password, multifactor code, recovery response, or other
   login secret directly in noVNC. The agent does not ask the human to send a
   secret through chat, email, a file, or a command.
4. The human tells the agent only that login is complete. An agent that the
   human has explicitly authorized for the named site and task may then verify
   the resulting login state from a non-sensitive page marker.
5. Only an agent with that human authorization reuses the authenticated browser
   profile in place through its loopback-only browser-control endpoint. It does
   not extract cookies,
   authorization headers, browser storage, saved passwords, or other reusable
   authentication material.

## Agent use

- repair or reuse the existing browser stack through its supported wrappers;
  preserve its profile and human-owned tabs
- open a task-owned tab, record its exact browser target identifier, and close
  only that tab when finished
- read only the pages needed for the assigned task; do not inspect account,
  profile, or private page content unrelated to that task
- keep browser-control, VNC, and noVNC endpoints loopback-only; expose the
  viewer only through the human's SSH tunnel
- keep credentials, session artifacts, private page content, screenshots, and
  operational logs out of the DW repository

## When authentication is missing

1. Stop at the login, multifactor, consent, or challenge boundary without
   entering, revealing, or bypassing it.
2. Preserve the browser profile and relevant page state.
3. Ask the human for one action: use noVNC to complete the named site's login,
   then confirm completion. Do not solicit a credential.
4. After confirmation, verify only that the required authenticated page is
   available and resume in a task-owned tab.

Agents cannot safely perform a fresh human login by learning the human's USC
credentials. Localhost is a network boundary, not a same-account secrecy
boundary: any process running as the browser's host user can reach the
passwordless noVNC viewer and browser-control endpoint. Therefore, the human
must enter secrets only while agents and automation with that access are not
running. Later reuse grants an agent the human session's effective account
access even though the agent does not know the credential. The human, not the
agent, must authorize the named site and task before each use. If USC later
provides a scoped delegated login or service credential intended for
automation, the human must authorize a separate workflow for it.
