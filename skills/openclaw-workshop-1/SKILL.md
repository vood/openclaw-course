---
name: openclaw-workshop-1
description: "OpenClaw Workshop 1: Getting Started. Interactive checklist that guides users through installing OpenClaw, connecting Telegram, voice-to-text, email via IMAP, and browser setup. Use when the user says 'workshop 1', 'openclaw getting started', 'start openclaw setup', or wants to begin the OpenClaw course."
---

# OpenClaw Workshop 1: Getting Started

You are running an interactive workshop checklist. Your job is to:

1. **List all tasks** below with their completion status
2. **Check each task** by inspecting the actual system state (files, configs, running processes)
3. **Offer to tackle incomplete tasks** one at a time, in order
4. **Mark the workshop complete** when all tasks pass verification

---

## Workshop Tasks

### Task 1: Coding Agent Installed
**What:** User has a coding agent (Codex/ChatGPT or Claude desktop app) with a paid plan.
**How to verify:** Ask the user which coding agent they're using. If they're talking to you right now via one, it's done.
**Done when:** User confirms they have a working coding agent.

### Task 2: Project Folder Created
**What:** A dedicated folder exists at `~/openclaw` (or user's chosen location).
**How to verify:** Check if `~/openclaw` exists. Run `ls ~/openclaw`.
**Done when:** The directory exists.

### Task 3: OpenClaw Installed
**What:** OpenClaw is installed and can start.
**How to verify:** Check if the `openclaw` binary/command exists. Check `~/.openclaw/openclaw.json` exists.
**Setup prompt to use:**
> Help me install OpenClaw on my computer. As a non-technical person, please guide me through the process and explain security implications. In the non interactive mode. Don't ask me to do any actions in terminal. Do it yourself. I'm not technical.
**Done when:** `openclaw` command is available and config file exists.

### Task 4: Dedicated Gmail Created
**What:** User has a dedicated Gmail account (NOT their personal email) for the agent.
**Done when:** User provides the dedicated Gmail address.

### Task 5: Telegram Connected
**What:** OpenClaw is connected to Telegram via a bot.
**How to verify:** Check openclaw config for Telegram bot token. Check if the Telegram gateway is configured.
**Setup prompt to use:**
> Please connect OpenClaw to Telegram so I can message it from my phone. Walk me through creating a Telegram bot and configuring it.
**Verification:** Ask user to send a test message to their bot and confirm it responds.
**Done when:** User confirms they can chat with OpenClaw via Telegram.

### Task 6: Voice-to-Text Enabled
**What:** Whisper or equivalent speech-to-text is configured so voice messages on Telegram are transcribed.
**How to verify:** Check if whisper is installed (`which whisper` or check openclaw plugins/skills). Check voice-to-text config in openclaw.
**Setup prompt to use:**
> I want to send you voice messages on Telegram. Please add voice-to-text support.
**Verification:** Ask user to send a voice message on Telegram and confirm it gets transcribed.
**Done when:** Voice messages are transcribed automatically.

### Task 7: Email via IMAP Connected
**What:** The dedicated Gmail is connected to OpenClaw via IMAP so the agent can read and send email.
**How to verify:** Check openclaw config for IMAP/SMTP settings.
**Setup prompt to use:**
> Please connect my dedicated Gmail to OpenClaw via IMAP. Walk me through enabling IMAP access and configuring it.
**Verification:** Have the agent send a test email to the user's personal address.
**Done when:** Agent can send and receive email.

### Task 8: Browser Working
**What:** OpenClaw's headless browser is functional.
**How to verify:** Check if browser plugin/tool is configured in openclaw.
**Setup prompt to use:**
> Please open google.com and search for "OpenClaw GitHub". Tell me what you find.
**Done when:** Agent successfully navigates a webpage and reports back results.

---

## Execution Instructions

When this skill is invoked:

1. **Print the checklist** with status indicators:
   - `[ ]` = not yet verified
   - `[~]` = partially done / needs attention
   - `[x]` = verified complete

2. **Run automated checks** where possible (file existence, config checks, command availability). Don't ask the user for things you can check yourself.

3. **Show the results** and identify which tasks are incomplete.

4. **Offer to start working** on the first incomplete task. Guide the user through it step-by-step. Use the setup prompts provided above.

5. **After each task**, re-verify it's actually working (close the loop -- don't just configure, TEST it).

6. **Move to the next task** until all are complete.

7. **When all tasks are done**, congratulate the user and display:
   ```
   ✅ Workshop 1 COMPLETE
   OpenClaw is installed and connected.
   Next: Run Workshop 2 (/openclaw-workshop-2) to set up power features.
   ```

---

## Key Teaching Points (share during setup)

- **Treat OpenClaw like a new employee** -- its own workspace, email, calendar. Keep away from sensitive accounts.
- **Be specific** -- vague instructions = dangerous. "Set up email" is bad. "Set up email and send me a test email to confirm it works" is good.
- **Start safe, level up gradually:** No sensitive data -> small tasks -> expand access -> full autonomy.
- **Risks are real:** We've seen agents email 1,000 customers, delete files, refund Stripe charges. ~20% of ClawHub plugins are malicious. 390k+ instances exposed on the internet.
- **Costs:** OpenClaw is free, but AI API keys cost $3-10/day (light) to $150+/day (heavy Opus usage). $20/mo subscription won't work.
- **Recommended setup:** Dedicated OS user for isolation (not your personal account).

---

## Architecture Reference (for context during setup)

```
Telegram/WhatsApp/Slack/Discord -> Gateway (port 18789) -> AI Agent (Claude/GPT) <-> Nodes (iPhone, MacBook, Camera)
```

- **Gateway:** Switchboard between apps and AI. If misconfigured = open to the internet.
- **Nodes:** Devices (camera, mic, screen). Each must be approved.
- **Workspace:** Folder of text files the agent edits itself (personality, identity, memory, tools, heartbeat, startup).
- **Heartbeat:** Cron job that runs every N minutes. Defined in HEARTBEAT.md. Makes the agent proactive.
