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
- Email via IMAP working
- gog skill configured (Gmail, Calendar, Drive access)
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

### Chapter 2: Secure Access

**Step 2: 1Password Integration** *(Optional -- skip if you don't use 1Password)*

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

### Chapter 3: Skills Check

**Step 3: Review Installed Skills**
Skills are pre-built instruction manuals that teach your agent new abilities instantly.

*Setup prompt:*
> Show me what skills are already installed.

Key skills we'll use today:
- **gog** -- Gmail, Calendar, Drive (should already be configured)
- **whisper** -- speech-to-text (should be set up from Workshop 1)
- **xurl** -- Twitter/X (we'll set this up in Use Case 3)

*A word of caution about ClawHub:* Community marketplace has 2,800+ skills, but ~20% are malicious. Always review before installing.

---

### Setup Complete Checkpoint

```
Part 1 done! Quick recap:
✅ Ack emojis -- visual feedback on every message
✅ 1Password -- secure credential access (or skipped)
✅ Skills -- reviewed and ready

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

### Use Case 2: Research & Book a Calendar Event 📅

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

### Use Case 3: Tweet Something (Optional) 🐦

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

### Use Case 4: Meeting Summary → Apple Notes 📝

> Record or find a meeting recording, transcribe it locally, extract action items, and put them in Apple Notes.

**What we're doing:** The agent processes an audio recording with Whisper (locally -- no data leaves the machine), extracts a summary and action items, and inserts them into Apple Notes via AppleScript.

**What this teaches:** The full pipeline -- file handling, local AI processing, text extraction, and macOS integration. This is a workflow people actually pay for.

**Audio source (best to worst):**
1. **Find a real recording in Google Drive** -- use gog to search their Drive for a meeting recording. This is the best option because it exercises the Drive integration AND gives them a real meeting to summarize.
2. **Pull from Zoom** -- if they use Zoom, recordings are often saved locally or in the cloud. Help them find one.
3. **Share a file in chat** -- they can drop any audio file directly into the Telegram conversation and the agent picks it up.
4. **Use the sample file** -- there's a sample standup recording in this project at `samples/meeting-recording.m4a` (~55 seconds, team standup with action items). Use this as a fallback if they don't have their own.

**Prompt to try (with Drive):**
> Search my Google Drive for any meeting recordings or audio files. Pick one, transcribe it using Whisper, create a clean summary with key decisions and action items, and save it to Apple Notes.

**Prompt to try (with sample file):**
> I have a meeting recording at samples/meeting-recording.m4a. Please transcribe it using Whisper, create a clean summary with key decisions and action items, and save it to Apple Notes.

**What to watch for:**
- Does Whisper transcribe the audio correctly?
- Is the summary clean and useful (not just a raw transcript)?
- Are action items clearly identified?
- Does it actually appear in Apple Notes?

**The Apple Notes part:** The agent uses AppleScript to create a new note. Example:
```
osascript -e 'tell application "Notes" to make new note at folder "Notes" with properties {name:"Meeting Summary - [date]", body:"[content]"}'
```

**Celebrate:** You just went from raw audio to organized action items in Apple Notes, all locally, all automatic. This is a workflow that saves hours every week.

---

### Use Case 5: Morning News Briefing ☀️

> Set up a cron job that delivers a personalized news briefing to your Telegram every morning.

**What we're doing:** Creating a scheduled job that runs every morning, browses news sources relevant to YOUR interests, and sends you a concise summary before you start your day.

**What this teaches:** Cron jobs (autonomous scheduling) + browser (web research) + personalization. This is the "employee that works while you sleep" moment.

**Step 1: Figure out their interests.**
Ask the student: What topics do you care about? Tech? Finance? Local news? Industry-specific stuff?

**Step 2: Set up the cron job.**
*Prompt to try:*
> Set up a daily cron job that runs at 7:30am. Every morning, browse [Hacker News / TechCrunch / Bloomberg / their preferred sources] and send me a Telegram summary of the top 5 stories relevant to [their interests]. Keep it concise -- headlines and one-sentence summaries. Add links so I can read more if interested.

**Step 3: Verify it's scheduled.**
Check that the cron job exists and is set for the right time.

**What to watch for:**
- Is the cron job actually created?
- Is the timing correct (right timezone!)?
- Does a test run produce a good summary?
- Are the stories actually relevant to their interests?

**Pro tip to share:** Run the cron job manually first to test: make the agent do a briefing right now. Once it looks good, the schedule takes over.

**The moment:** Tomorrow morning, they'll wake up to a personalized news briefing waiting in their Telegram. No one asked for it. The agent just did it. That's the difference between a tool and an employee.

---

### Use Case 6: Your Own Automation 💡

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
✅ 1Password -- secure access, no passwords exposed
✅ Skills system -- extensible and ready

Use Cases:
🎵 Played music via browser automation
📅 Researched an event and booked it into your calendar
🐦 Posted a tweet (or skipped -- that's cool too)
📝 Transcribed a meeting and put action items in Apple Notes
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
