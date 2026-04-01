---
name: openclaw-workshop-2
description: "OpenClaw Workshop 2: Power Features. Interactive checklist that guides users through setup (ack emojis, cron, 1Password, skills) then hands-on use cases (YouTube Music, calendar booking, Twitter, meeting summary to Apple Notes, morning briefing cron, custom automation). Use when the user says 'workshop 2', 'openclaw power features', or has completed workshop 1."
---

# OpenClaw Workshop 2: Power Features

## Your Role

You're continuing the journey with someone who already has a working OpenClaw agent. Last time they built the foundation. Today they transform their agent from a chatbot into an autonomous employee -- and they'll do it by building real things.

The workshop has two parts:
1. **Setup** -- configure the remaining power features (quick, building on Workshop 1)
2. **Use Cases** -- hands-on exercises where they actually USE what they've built

When you run this workshop:

1. **Welcome them back** -- acknowledge how far they've come
2. **Check that Workshop 1 is solid**
3. **Breeze through the setup** -- it's lighter than Workshop 1
4. **Spend most of the time on use cases** -- this is where the magic happens
5. **End with their own idea** -- they leave with something personal

---

## The Welcome

Welcome back! Last time you set up your agent from scratch -- installed OpenClaw, connected Telegram, got voice, email, and browser working. That was the hard part.

Today's different. We'll do a bit more setup, and then the fun begins: you're going to make your agent play music, book events, post tweets, summarize meetings, and deliver you a personalized morning briefing. By the end, you'll have built something you'll actually use every day.

Let's see where we're at.

---

## Prerequisites Check

Before we dive in, let's make sure Workshop 1 is solid:
- OpenClaw installed and running
- Telegram connected
- Voice-to-text working
- Email via IMAP working
- Browser functional

If anything is missing, let's fix it first. Everything today builds on this.

---

## Part 1: Setup

> Quick configuration to unlock today's use cases. This should go fast.

### Chapter 1: Quality of Life

**Step 1: Ack Emojis**
Your agent reacts to every message so you always know what's happening:
- :eyes: = "I see your message"
- :saluting_face: = "I'm working on it"
- :white_check_mark: = "All done!"
- :x: = "Something went wrong"

*How to check:* Look in openclaw config for ack emoji / reaction settings.
*Setup prompt:*
> Enable ack emoji reactions on Telegram so I can see when you receive and start processing my messages. Use :eyes: for received, :saluting_face: for working, :white_check_mark: for done.

*Verification:* Send a test message and watch for the reactions.

---

### Chapter 2: Google Workspace (gog skill)

**Step 2: Connect Google Workspace**
This is a big one. The gog skill gives your agent access to Gmail, Google Calendar, Google Drive, Contacts, Sheets, and Docs. Many of today's use cases depend on this -- calendar booking, meeting summaries, file sharing.

To use gog, you need a Google OAuth client. You have two options:

**Option A: Use our pre-configured client (Recommended)**
We've included a ready-to-go OAuth client in this project. Quick and painless:
- File: `secrets/gog-credentials.zip`
- Passphrase: *(shared during the workshop)*

*Setup prompt:*
> Unzip secrets/gog-credentials.zip (the passphrase is [passphrase]) and use the client_secret.json inside to configure the gog skill for Google Workspace access. Set up Gmail, Calendar, and Drive.

**Option B: Register your own Google OAuth client**
If you prefer full control over your own Google Cloud project:

*Setup prompt:*
> Help me create my own Google OAuth client for the gog skill. Walk me through setting up a project in Google Cloud Console, enabling the Gmail, Calendar, and Drive APIs, and creating OAuth credentials. I'm not technical -- guide me through every step.

**For both options -- verification:**
> List my 3 most recent emails, show tomorrow's calendar events, and list 5 recent files in my Google Drive.

*Close the loop:* All three should work -- email, calendar, and Drive. If any fail, troubleshoot the OAuth scopes. This is the foundation for several use cases today, so take the time to get it right.

---

### Chapter 3: Execution Approvals (Optional)

**Step 3: Check Exec Approval Mode**
OpenClaw has a safety feature called "exec approvals" -- it asks you to approve every command before the agent runs it. This is great for learning, but once you trust your agent, it slows everything down.

*How to check:* Look at `~/.openclaw/exec-approvals.json` or check the openclaw settings for execution approval mode.

**If exec approvals are enabled:**
Explain what they do -- every time the agent wants to run a terminal command, it asks you first. This is safe but tedious, especially for today's exercises where we'll be running lots of commands.

Offer the choice:
- **Keep them on** -- safer, but you'll be approving a LOT of things today. Good if you want to see exactly what your agent does.
- **Turn them off** -- the agent runs freely. This is how it works in "employee mode." You trust it to act, and you review the results.

*Prompt to disable:*
> Disable execution approvals so you can run commands without asking me each time. I trust you.

*Prompt to keep but allow-list:*
> Keep execution approvals on, but auto-approve safe commands like ls, cat, find, and brew.

**Why this matters:** This is a trust decision. In Workshop 1 we talked about leveling up like an employee. Turning off approvals is like saying "I trust you to do your job without checking in on every little thing." Most people disable them once they're comfortable -- it makes the agent dramatically more useful.

---

### Chapter 4: Secure Access

**Step 4: 1Password Integration** *(Optional -- skip if you don't use 1Password)*

Your agent needs to log into things. The right way: 1Password. Agent fetches credentials on demand, gets 2FA codes automatically, and you approve from your phone. No passwords in text files. Ever.

*How to check:* Run `which op` or `op --version`.
*Setup:*
1. `brew install 1password-cli`
2. Enable desktop integration in 1Password app settings
3. Agent runs `op signin` -- you approve on your phone

*Setup prompt:*
> Set up 1Password CLI integration so you can securely fetch my credentials when needed. I have the 1Password desktop app installed.

*If they don't use 1Password:* Skip it. Not a blocker.

---

### Chapter 5: Skills Check

**Step 5: Review Installed Skills**
Skills are pre-built instruction manuals that teach your agent new abilities instantly.

*Setup prompt:*
> Show me what skills are already installed.

Key skills we'll use today:
- **gog** -- Gmail, Calendar, Drive (just configured in Chapter 2)
- **whisper** -- speech-to-text (set up in Workshop 1)
- **xurl** -- Twitter/X (we'll set this up in Use Case 4)

**Now let's install a skill from the marketplace.**

Skills live on [skills.sh](https://skills.sh) (also known as [clawhub.ai](https://clawhub.ai)). This is the community marketplace -- thousands of skills you can add with one command. Let the student browse and pick one that interests them, or suggest one that's relevant to their use case.

*Setup prompt:*
> Browse skills.sh and find a skill that looks useful to me. Show me what it does before installing. Then install it.

Or if they want something specific:
> Install the [skill name] skill from skills.sh.

**What to watch for:**
- Does the agent find and explain the skill before installing?
- Does the installation work?
- Can the agent actually use the new skill?

**A word of caution:** The marketplace has 2,800+ skills, but ~20% are malicious. Always review what a skill does before installing. Built-in skills are safe. Marketplace skills need vetting -- read the description, check the author, and don't install anything that asks for permissions it shouldn't need.

---

### Setup Complete Checkpoint

```
Part 1 done! Quick recap:
✅ Ack emojis -- visual feedback on every message
✅ Google Workspace -- Gmail, Calendar, Drive connected via gog
✅ Exec approvals -- configured to your comfort level
✅ 1Password -- secure credential access (or skipped)
✅ Skills -- reviewed, marketplace skill installed

Now the fun part. Let's build real things.
```

---

## Part 2: Use Cases

> This is why you're here. Each use case builds on the last, and by the end you'll have a genuinely useful agent.

---

### Use Case 1: Play Music on YouTube Music 🎵

> Let's start with something fun. Your agent controls your browser and plays music for you.

**What we're doing:** Tell your agent to open YouTube Music and play something you like. It navigates, searches, and hits play -- all on its own.

**What this teaches:** Browser automation basics -- navigating, clicking, interacting with real websites. If it can play music, it can fill forms, post content, and do research.

**Prompt to try:**
> Open YouTube Music in the browser and play some feel-good music for me.

Or get specific:
> Open YouTube Music and play "Daft Punk - Get Lucky"

**What to watch for:**
- Does it navigate to the right site?
- Does it find the search bar and type?
- Does it actually play the track?
- Can you hear it? (The openclaw browser profile has audio!)

**If using 1Password:** The agent can log into your YouTube account automatically via 1Password. Otherwise it works in guest/free mode.

**Celebrate:** You just told your agent to play music and it did. That's browser automation in action. Everything else today uses the same muscle.

---

### Use Case 2: Disk Cleanup -- Your Agent Sees Everything 🗂️

> Your agent scans your entire home folder, finds the biggest space wasters, and helps you safely clean up.

**What we're doing:** Ask your agent to scan your user folder for large files and present the absolute safest ones to delete -- old downloads, cache files, duplicate media, forgotten .dmg installers. Nothing risky. The agent shows you exactly what it found, how much space each takes, and only suggests things that are genuinely safe to remove.

**What this really teaches:** This isn't about disk space. This is the "oh wow" moment where they realize: *my agent can see my entire filesystem.* It can read files, navigate folders, and understand what's on their computer. That's the power -- and the responsibility -- of having an AI agent with real system access.

**Prompt to try:**
> Scan my home folder and find the largest files and folders that are safe to delete. I'm talking about things like old .dmg installers in Downloads, Xcode caches, old Zoom recordings, duplicate files, and anything clearly temporary. Be very conservative -- only suggest things that are absolutely safe to remove. Show me what you find with file sizes before deleting anything.

**What to watch for:**
- Does it scan real directories? (~/Downloads, ~/Library/Caches, ~/Movies, etc.)
- Does it find genuinely large files?
- Is it conservative? It should NEVER suggest deleting documents, photos, code, or anything ambiguous
- Does it show sizes and ask for confirmation before touching anything?

**Safe categories to look for:**
- `.dmg` and `.pkg` installers in Downloads
- `node_modules` in old project folders
- Xcode derived data (`~/Library/Developer/Xcode/DerivedData`)
- Homebrew cache (`~/Library/Caches/Homebrew`)
- Old Zoom/meeting recordings
- `.zip` files that have already been extracted
- Trash that hasn't been emptied

**The conversation to have:** After the agent presents its findings, talk about what this means. Your agent has access to everything on this machine. That's why we set up a dedicated user account in Workshop 1. That's why we treat it like an employee -- it can see your files, but we've limited what it can do with them.

**Done when:** The agent finds real large files and the student reviews and optionally deletes some. The important thing isn't the cleanup -- it's the realization of what the agent can access.

---

### Use Case 3: Research & Book a Calendar Event 📅

> Your agent researches something fun to do and books it into your calendar -- then invites you.

**What we're doing:** The agent browses the web to find an interesting event or activity near you, picks a good time, creates a calendar event via gog, and sends an invite to your personal email.

**What this teaches:** Combining browser (research) + gog skill (calendar) + real-world decision making. The agent isn't just following instructions -- it's making choices.

**Important setup note:** The gog skill creates events as the OpenClaw user. The agent needs to **invite the student's personal email** so the event shows up on their calendar.

**Prompt to try:**
> Research something fun to do this weekend in [your city]. Find a specific event or activity, pick a good time, and create a calendar event for it. Make sure to invite [student's personal email] so it shows up on my calendar.

**What to watch for:**
- Does it search for real events/activities?
- Does it pick something reasonable?
- Does the calendar event get created?
- Did the invite arrive at the student's email?

**Close the loop:** Check that the invite actually landed in their inbox. If it didn't, troubleshoot the gog calendar permissions.

---

### Use Case 4: Tweet Something (Optional) 🐦

> Set up X/Twitter integration and post your first automated tweet.

**What we're doing:** Install and configure the xurl skill, then compose and post a real tweet. This is optional -- only if the student has a Twitter/X account they want to connect.

**What this teaches:** How skills extend your agent's abilities. One install and your agent can post, reply, search, and DM on Twitter.

**Setup:**
1. Make sure the xurl skill is available
2. Connect the Twitter/X account (API credentials needed)

*Setup prompt:*
> Set up the xurl skill for Twitter/X. Help me connect my account and post a test tweet.

**Prompt to try:**
> Write a tweet about something interesting you learned while browsing the web today. Keep it casual and authentic. Post it to my Twitter.

**What to watch for:**
- Does the skill install/configure correctly?
- Can the agent compose something that sounds natural?
- Does the tweet actually post?

**Note:** If they don't have Twitter or don't want to connect it, skip this. Not a blocker for the rest of the workshop.

---

### Use Case 5: Meeting Summary → Apple Notes + Google Sheet 📝

> Record or find a meeting recording, transcribe it locally, extract action items, put the summary in Apple Notes, and create a to-do tracker in Google Sheets.

**What we're doing:** The agent processes an audio recording with Whisper (locally -- no data leaves the machine), extracts a summary and action items, saves the summary to Apple Notes, and creates a structured to-do list in a Google Sheet via gog with owners, deadlines, and status columns.

**What this teaches:** The full pipeline -- file handling, local AI processing, text extraction, macOS integration, AND cloud collaboration via Google Sheets. This is a workflow people actually pay for.

**Audio source (best to worst):**
1. **Find a real recording in Google Drive** -- use gog to search their Drive for a meeting recording. This is the best option because it exercises the Drive integration AND gives them a real meeting to summarize.
2. **Pull from Zoom** -- if they use Zoom, recordings are often saved locally or in the cloud. Help them find one.
3. **Share a file in chat** -- they can drop any audio file directly into the Telegram conversation and the agent picks it up.
4. **Use the sample file** -- there's a sample standup recording in this project at `samples/meeting-recording.m4a` (~55 seconds, team standup with action items). Use this as a fallback if they don't have their own.

**Prompt to try (with Drive):**
> Search my Google Drive for any meeting recordings or audio files. Pick one, transcribe it using Whisper, then: (1) save a clean summary with key decisions to Apple Notes, and (2) create a Google Sheet called "Meeting Action Items" with columns for Task, Owner, Deadline, and Status -- populate it with every action item from the meeting.

**Prompt to try (with sample file):**
> I have a meeting recording at samples/meeting-recording.m4a. Please transcribe it using Whisper, then: (1) save a clean summary to Apple Notes, and (2) create a Google Sheet called "Meeting Action Items" with columns for Task, Owner, Deadline, and Status -- populate it with every action item from the meeting.

**What to watch for:**
- Does Whisper transcribe the audio correctly?
- Is the summary clean and useful (not just a raw transcript)?
- Does it actually appear in Apple Notes?
- Is the Google Sheet created with the right columns?
- Are action items structured properly -- task, owner, deadline, status?
- Can the student open the Sheet and see their to-dos?

**The Apple Notes part:** The agent uses AppleScript to create a new note:
```
osascript -e 'tell application "Notes" to make new note at folder "Notes" with properties {name:"Meeting Summary - [date]", body:"[content]"}'
```

**The Google Sheet part:** The agent uses gog to create a new spreadsheet and populate it. The sheet becomes a living to-do tracker the student can share with their team, check off items, and have the agent update later.

**Celebrate:** You just went from raw audio to organized notes in Apple Notes AND a structured to-do tracker in Google Sheets -- all locally transcribed, all automatic. This is the kind of workflow that turns a 30-minute post-meeting chore into a one-sentence prompt.

---

### Use Case 6: Morning News Briefing ☀️

> Set up a cron job that delivers a personalized news briefing to your Telegram AND email every morning.

**What we're doing:** Creating a scheduled job that runs every morning, browses news sources relevant to YOUR interests, sends a quick summary to Telegram, and emails a nicely formatted briefing to the student's personal email via gog.

**What this teaches:** Cron jobs (autonomous scheduling) + browser (web research) + email (gog) + personalization. This is the "employee that works while you sleep" moment. It also exercises email sending -- something we set up but haven't used in a use case yet.

**Step 1: Figure out their interests.**
Ask the student: What topics do you care about? Tech? Finance? Local news? Industry-specific stuff? And what's your personal email where you want the briefing delivered?

**Step 2: Set up the cron job.**
*Prompt to try:*
> Set up a daily cron job that runs at 7:30am. Every morning, browse [Hacker News / TechCrunch / Bloomberg / their preferred sources] and: (1) send me a quick Telegram summary of the top 5 stories relevant to [their interests] with headlines and one-sentence summaries, and (2) send a nicely formatted email with the full briefing to [student's personal email] -- include links, a brief intro, and a sign-off. Subject line: "Your Morning Briefing - [date]".

**Step 3: Verify it's scheduled.**
Check that the cron job exists and is set for the right time.

**What to watch for:**
- Is the cron job actually created?
- Is the timing correct (right timezone!)?
- Does a test run produce a good summary on Telegram?
- Does the briefing email arrive at the student's inbox?
- Is the email well-formatted and useful?
- Are the stories actually relevant to their interests?

**Pro tip to share:** Run the cron job manually first to test: make the agent do a briefing right now. Check both Telegram and email. Once it looks good, the schedule takes over.

**The moment:** Tomorrow morning, they'll wake up to a personalized news briefing waiting in both their Telegram and their inbox. No one asked for it. The agent just did it. That's the difference between a tool and an employee.

---

### Use Case 7: Your Own Automation 💡

> You've seen what's possible. Now build something that solves YOUR problem.

**What we're doing:** The student picks their own automation and builds it with your help. This is where the workshop becomes personal.

**Help them brainstorm.** Ask:
- What's something you do every day that's repetitive?
- What information do you wish was just... there when you woke up?
- Is there a task you keep putting off because it's tedious?
- What would your perfect AI employee do for you?

**Ideas to spark inspiration:**
- **Inbox zero:** Every hour, check email, auto-reply to simple ones, draft responses for complex ones, flag urgent ones on Telegram
- **Grocery list:** "Add milk" via Telegram -> agent maintains a running Google Sheet, orders when the list is long enough
- **LinkedIn outreach:** Daily, find 5 relevant people in your industry, draft personalized connection requests, send for your approval
- **Competitor watch:** Weekly, check 3 competitor websites for changes, summarize what's new
- **Expense tracking:** Forward receipts to the agent's email, it extracts amounts and categories, updates a Google Sheet
- **Daily journal prompt:** Every evening at 9pm, send a thoughtful question based on what happened that day

**The goal:** At least one working automation that combines 2+ features and solves a real problem they have.

**Done when:** They've tested it, it works, and they're excited about it.

---

## Running the Workshop

**Show progress visually:**
- `[ ]` = we haven't gotten here yet
- `[~]` = in progress
- `[x]` = done and verified!
- `[--]` = skipped (totally fine)

**For setup (Part 1):** Move quickly. This should take 15-20 minutes. The foundation from Workshop 1 does most of the heavy lifting.

**For use cases (Part 2):** Take your time. This is where learning happens. Let them experiment, fail, retry. Each use case should feel like a small victory.

**Close every loop.** Configure AND test. The golden rule: "...and verify it works."

**If something breaks:** Stay calm, stay encouraging. "That's normal. Let's figure out what happened." Debugging is part of the learning.

---

## The Finish Line

When all use cases are complete:

```
🎉 Workshop 2 COMPLETE!

Look at what you built today:

Setup:
✅ Ack emojis -- you always know what's happening
✅ Google Workspace -- Gmail, Calendar, Drive via gog
✅ Exec approvals -- configured your way
✅ 1Password -- secure access, no passwords exposed
✅ Skills system -- extensible, marketplace skill installed

Use Cases:
🎵 Played music via browser automation
🗂️ Scanned your filesystem and cleaned up safe-to-delete files
📅 Researched an event and booked it into your calendar
🐦 Posted a tweet (or skipped -- that's cool too)
📝 Transcribed a meeting → Apple Notes + Google Sheet to-do tracker
☀️ Set up a morning news briefing that runs every day
💡 Built your own custom automation

Workshop 1: You gave your agent a desk, phone, email, and internet.
Workshop 2: You taught it to work, play, research, schedule, and think.

Tomorrow morning you'll wake up to a personalized news briefing 
you didn't ask for. Your calendar has a fun event you didn't 
have to search for. Your meeting notes are in Apple Notes.

That's not a chatbot. That's a teammate. Welcome to the future. 🚀
```

---

## Handy Commands to Share

These work in Telegram -- daily shortcuts:

| Command | What it does |
|---|---|
| **/models** | Switch to cheaper model for simple tasks, Opus for complex ones |
| **/restart** | Restart agent if stuck |
| **/context** | See context window usage |
| **/status** | Model, usage, cost, uptime |
| **/reasoning** | Think harder on tough problems |
| **/tasks** | See background tasks |

---

## Key Lessons to Weave In

**Close the loop:** "Set it up" is never enough. Always: "...and verify it works."

**The setup tax:** OpenClaw was built for tinkerers. Things break. That's normal. But once it works, it works forever.

**Everything connects:**
- **Cron** = WHEN to act
- **Browser** = HOW to act on the web
- **1Password** = SAFE access
- **Skills** = NEW abilities
- **gog** = Gmail, Calendar, Drive
- **Files** = data IN and OUT
- **Ack emojis** = YOU stay in the loop

**The employee mindset:** Don't accept "I tried but it didn't work." Your agent should test its own work. Train it to close its own loops.
