---
name: openclaw-workshop-2
description: "OpenClaw Workshop 2: Power Features. Interactive checklist that guides users through setting up ack emojis, cron jobs, browser automations, 1Password, skills, and file sharing. Use when the user says 'workshop 2', 'openclaw power features', 'openclaw advanced setup', or has completed workshop 1 and wants to continue."
---

# OpenClaw Workshop 2: Power Features

You are running an interactive workshop checklist. Your job is to:

1. **List all tasks** below with their completion status
2. **Check each task** by inspecting the actual system state (files, configs, running processes)
3. **Offer to tackle incomplete tasks** one at a time, in order
4. **Mark the workshop complete** when all tasks pass verification

---

## Prerequisites

Before starting, verify Workshop 1 is complete:
- OpenClaw installed and running
- Telegram connected
- Email via IMAP working

If any are missing, direct user to run Workshop 1 first.

---

## Workshop Tasks

### Task 1: Ack Emojis Configured
**What:** Agent reacts to messages with emoji status indicators on Telegram.
- :eyes: = message received
- :saluting_face: = working/processing
- :white_check_mark: = task completed
- :x: = something went wrong

**How to verify:** Check openclaw config for ack emoji / reaction settings. Look in workspace files for emoji reaction configuration.
**Setup prompt to use:**
> Enable ack emoji reactions on Telegram so I can see when you receive and start processing my messages. Use :eyes: for received, :saluting_face: for working, :white_check_mark: for done.
**Verification:** Ask user to send a test message on Telegram and confirm they see the emoji reactions.
**Done when:** User confirms emoji reactions appear on their Telegram messages.

### Task 2: At Least One Cron Job Created
**What:** A scheduled task (cron job) is configured and running.
**How to verify:** Check openclaw cron configuration. List existing cron jobs in `~/.openclaw/cron/` or equivalent config location.
**Context to share:**
- **Heartbeat** (from Workshop 1): runs every N minutes, batch checks, periodic monitoring
- **Cron jobs** (new): exact timing ("9am Monday"), one-shot reminders, isolated from main session, can use different models
- Types: one-shot ("remind me in 20 min"), recurring ("every day at 6am"), cron expression (`0 9 * * 1-5`)

**Example prompts:**
> Every morning at 8am, check my Gmail for any urgent emails and send me a summary on Telegram.

Other ideas:
- 8am daily -- email digest of overnight messages
- Monday 9am -- weekly revenue report
- Every 4 hours -- check Twitter mentions
- 6pm daily -- Hacker News top stories summary

**Done when:** At least one cron job exists and has fired successfully (or is scheduled).

### Task 3: Browser Automation Tested
**What:** Agent can use the browser to navigate, interact with pages, and report back.
**How to verify:** Check if browser plugin is functional. Try a simple browse command.
**Context to share:**
- **openclaw profile:** Clean, isolated browser. Not logged in anywhere. Safe for research. Has audio.
- **user profile (via MCP):** Your real Chrome tabs. Already logged in everywhere. Requires remote debugging.

**Setup prompt to use:**
> Open a browser and search for the latest tech news. Summarize the top 3 stories you find.
**Verification:** Agent successfully navigates and returns meaningful results.
**Done when:** Browser automation produces correct results.

### Task 4: 1Password Integration (Optional but Recommended)
**What:** 1Password CLI (`op`) is installed and the agent can securely fetch credentials.
**How to verify:** Run `which op` or `op --version`. Check if desktop integration is enabled.
**Why it matters:** Agent needs credentials. Don't put them in text files. 1Password provides: on-demand credential fetching, TOTP 2FA codes, requires your approval via app.

**Setup steps:**
1. Install: `brew install 1password-cli`
2. Enable desktop integration in 1Password app settings
3. Agent runs `op signin` -- user approves on their device

**Setup prompt to use:**
> Set up 1Password CLI integration so you can securely fetch my credentials when needed. I have the 1Password desktop app installed.
**Verification:** Agent successfully fetches a test credential (e.g., list vaults).
**Done when:** `op` CLI works and agent can access 1Password, OR user explicitly skips this task.
**Note:** Mark as skipped if user doesn't use 1Password. Not a blocker.

### Task 5: Skills Explored
**What:** User understands the skills system and has reviewed installed skills.
**How to verify:** Check installed skills in openclaw config/workspace.
**Context to share:**

Built-in skills:
| Skill | What it does |
|---|---|
| **1password** | Secure credential management |
| **github** | Issues, PRs, CI/CD via gh CLI |
| **gog** | Gmail, Calendar, Drive, Contacts, Sheets, Docs |
| **xurl** | Twitter/X API -- post, reply, search, DM |
| **slack** | Slack control -- messages, reactions, pins |
| **weather** | Weather and forecasts |
| **whisper** | Local speech-to-text |

Two sources: Built-in (safe, ship with OpenClaw) and ClawHub (community marketplace -- **~20% are malicious, always review**).

**Setup prompt to use:**
> Show me what skills are already installed. Also, can you find a skill for managing Google Calendar?
**Done when:** User has reviewed their installed skills and understands how to find/install new ones.

### Task 6: File Sharing Method Configured
**What:** User has at least one way to share files with the agent.
**How to verify:** Check if gog skill is configured (Google Drive), or if a shared folder is set up.
**Three options:**
1. **Telegram/Chat:** Send files directly. Best for quick shares.
2. **Google Drive:** Use gog skill. Agent reads/writes Drive files. Best for shared data.
3. **macOS Shared Folder:** Drop files in shared directory. Agent picks them up. Best for local workflows.

**Setup prompt for Google Drive:**
> Set up Google Drive access using the gog skill so you can read and write files from my Google Drive.
**Done when:** At least one file sharing method is working and tested.

### Task 7: First Use Case Built
**What:** User has configured at least one real-world automation combining multiple features.
**How to verify:** Ask the user what they've built or want to build.
**Suggested use cases:**

**Meeting Summary:**
Record meeting -> share audio -> Whisper transcribes -> AI extracts key points -> summary + action items
Features: Whisper skill, file sharing, Google Drive

**Social Media Management:**
Cron: 6am daily -> browse trending topics -> draft 3 post ideas -> send for approval -> post to LinkedIn/X
Features: cron jobs, browser, 1Password, xurl skill

**Customer Support Automation:**
Email arrives -> classify intent -> check knowledge base -> route: auto or human? -> reply or escalate
Features: cron (every 15 min), IMAP, browser, files
Smart routing: simple question = auto-reply, needs context = draft + review, angry customer = escalate, sales inquiry = forward

**Done when:** User has at least one working automation that combines 2+ features.

---

## Execution Instructions

When this skill is invoked:

1. **Check prerequisites** -- verify Workshop 1 tasks are complete.

2. **Print the checklist** with status indicators:
   - `[ ]` = not yet verified
   - `[~]` = partially done / needs attention
   - `[x]` = verified complete
   - `[--]` = skipped (for optional tasks)

3. **Run automated checks** where possible (config files, installed tools, cron listings). Don't ask for things you can check yourself.

4. **Show results** and identify incomplete tasks.

5. **Offer to start** on the first incomplete task. Guide step-by-step using the setup prompts above.

6. **After each task**, verify it actually works (close the loop -- configure AND test).

7. **Move to the next task** until all required tasks are complete.

8. **When all tasks are done**, congratulate the user and display:
   ```
   ✅ Workshop 2 COMPLETE
   Your OpenClaw agent is fully configured with power features.
   
   Recap -- what you've set up:
   - Ack emojis for status feedback
   - Scheduled cron jobs for autonomous work
   - Browser automation for web tasks
   - 1Password for secure credentials
   - Skills system for extensibility
   - File sharing for data exchange
   - Your first real-world use case
   
   Your agent is now a proactive employee, not a reactive tool.
   ```

---

## Key Teaching Points (share during setup)

- **Close the loop:** Don't accept "I tried but it didn't work." Always verify: "...and confirm it works."
- **The setup tax is real:** OpenClaw was built for tinkerers. Many things don't work in one click. But once it's done, it's done forever.
- **Everything connects:** Cron triggers WHEN to act, browser is HOW to act, 1Password provides SAFE access, skills add NEW abilities, files move data IN & OUT, ack emojis keep YOU in the loop.

## Useful Chat Commands (share with user)

| Command | What it does |
|---|---|
| **/models** | Switch AI model (cheaper or smarter on demand) |
| **/restart** | Restart agent, clear stuck state |
| **/context** | Show context window usage |
| **/status** | Session status -- model, usage, cost, uptime |
| **/reasoning** | Toggle extended thinking |
| **/tasks** | View running background tasks |
