---
name: openclaw-workshop-4
description: "OpenClaw Workshop 4: Demo Day & What's Next. The Anthropic ban explained, updating OpenClaw, switching to OpenAI, alternatives (Claude Cowork, NanoClaw, Nanobot), and demo presentations. Use when the user says 'workshop 4', 'demo day', or has completed workshop 3."
---

# OpenClaw Workshop 4: Demo Day & What's Next

## Your Role

This is the final workshop. Today covers important changes in the OpenClaw ecosystem, then finishes with demos -- their moment to show what they built.

Today's agenda:
1. **The Anthropic Ban** -- what happened and what it means
2. **Updating OpenClaw & Switching to OpenAI** -- practical migration
3. **Alternatives** -- Claude Cowork, NanoClaw, Nanobot, and others
4. **Demo Day** -- each student presents what they built

When you run this workshop:

1. **Start with the ban** -- set the context, this is why the rest of the session matters
2. **Cover the practical response** -- updating, switching providers
3. **Show the landscape** -- alternatives they should know about
4. **End with demos** -- this is their moment, give it all the time it needs. No time limits.

---

## The Welcome

Welcome to the final workshop! Before demos, we need to talk about something important. The OpenClaw ecosystem changed significantly this week. You need to know what happened, what your options are, and how to keep your agents running.

Then we'll finish with the best part -- demos. Everyone presents what they built. No time limits. Take as long as you need.

---

## Chapter 1: The Anthropic Ban -- What Happened

> On April 4, 2026, Anthropic blocked Claude subscriptions from being used with OpenClaw and other third-party agent frameworks.

---

### What Changed

**Before (worked):**
- You had a Claude Pro ($20/mo) or Max ($200/mo) subscription
- You pointed OpenClaw at your Claude account via OAuth
- Your subscription covered all the tokens your agent used
- Cost was predictable and flat

**After April 4, 2026 (blocked):**
- Claude Pro and Max subscriptions can no longer be used with third-party frameworks like OpenClaw
- If you want to use Claude with OpenClaw, you must use the API with pay-as-you-go billing
- This means costs can go from $200/month to potentially thousands, depending on usage

### Why Anthropic Did This

- OpenClaw users were consuming massive amounts of tokens under flat-rate subscriptions
- A single agent running 24/7 with cron jobs, browser automation, and email processing can use 10-50x what a normal chat user consumes
- Anthropic was losing money on heavy agent users
- They needed to align pricing with actual usage

### The Timeline

| When | What |
|---|---|
| **Nov 2025** | OpenClaw (then Clawdbot) launches, goes viral |
| **Jan 2026** | Anthropic starts fingerprinting and suspending accounts using OpenClaw |
| **Jan 2026** | Security audit: 512 vulnerabilities, 8 critical |
| **Feb 2026** | Peter Steinberger (OpenClaw creator) joins OpenAI |
| **Apr 4, 2026** | Anthropic officially blocks third-party framework usage on subscription plans |

### Impact

- Thousands of users woke up to their agents not working
- Some users reported cost increases of up to 50x when switching to API billing
- The community scrambled to find alternatives

*Discuss:* This is a lesson about platform risk. When you build on someone else's platform, they can change the rules overnight. This is why understanding your options matters.

### What This Means for You

**If you were using Claude subscription with OpenClaw:**
- Your agent stopped working on April 4
- You need to either: switch to API billing, switch to OpenAI, or switch to an alternative

**If you were using API keys:**
- Nothing changed -- API access still works
- But you should know about the alternatives anyway

**If you had startup credits:**
- Your credits still work with the API
- This is the most cost-effective path if you have them

---

## Chapter 2: Updating OpenClaw & Switching to OpenAI

> Keep your agent current, and move to a provider that welcomes you.

---

### Updating OpenClaw

**Check your version:**
```bash
openclaw --version
```

**Update to latest:**
```bash
openclaw update
```

*Prompt to try:*
> What version of OpenClaw am I running? Check if there's a newer version. Back up my workspace, update, then verify all channels, cron jobs, and skills still work. Run `openclaw security audit` afterward.

---

### Why OpenAI

After Anthropic's ban, OpenAI became the default choice because:

1. **ChatGPT Plus/Pro subscription includes Codex OAuth** -- explicitly permits third-party integration
2. **OpenAI publicly welcomes OpenClaw** -- no ban risk
3. **Codex 5.3 and GPT-5.4 are strong models** -- comparable to Claude for most agent tasks
4. **Peter Steinberger (OpenClaw creator) now works at OpenAI** -- alignment between the projects

### Migration Steps

**Step 1: Get an OpenAI account**
Sign up for ChatGPT Plus ($20/mo) or Pro ($200/mo). For API usage, create a developer account at platform.openai.com.

**Step 2: Configure OpenClaw for OpenAI**

*Prompt to try:*
> Switch my OpenClaw to use OpenAI as the model provider. I want to use Codex 5.3 as my default model. Walk me through the configuration.

**Step 3: Set up embeddings separately**
Important: Codex does not include embeddings. You need a separate API key.

*Prompt to try:*
> Set up OpenAI text-embeddings-3 for my agent's memory system. This is separate from the Codex model.

**Step 4: Tune your agent**
Claude and GPT respond differently to the same prompts. Expect to spend a few days tuning SOUL.md, AGENTS.md, and cron prompts.

*Prompt to try:*
> Review my SOUL.md and AGENTS.md. Are there any instructions that are Claude-specific? Suggest changes for OpenAI models.

**Step 5: Test everything**

*Prompt to try:*
> Full systems check: send a test message on Telegram, send a test email, run a cron job, do a web search. Confirm everything works with the new model.

### The Multi-Provider Strategy

Don't lock into one provider. OpenClaw's config supports multiple model providers:

| Task | Model | Why |
|---|---|---|
| General daily use | **Codex 5.3** (subscription) | Covered by ChatGPT plan |
| Complex analysis | **Claude Opus** (API) | Pay per token, worth it |
| Routine cron jobs | **Kimi 2.5 / Minimax** | Cheap, fast, good enough |

*Prompt to try:*
> Configure my agent to use Codex 5.3 as default, Claude Opus via API for tasks tagged as "complex", and Kimi 2.5 for my daily news briefing cron.

---

## Chapter 3: Alternatives

> OpenClaw isn't the only option. Here's the landscape.

---

### Claude Cowork (by Anthropic)

Anthropic's own answer to OpenClaw. Desktop-focused, not messaging-focused.

**What it is:**
- Desktop agent for knowledge work -- reads, edits, and creates files on your machine
- Computer use -- clicks, scrolls, opens apps, navigates your screen
- Dispatch -- assign tasks from your iPhone, return to finished work on desktop
- Included with Claude Pro/Max subscription (no ban issues -- it's Anthropic's own product)

**Best for:** Desktop automation, document workflows, browser tasks on your computer

**Not great for:** Always-on messaging (Telegram, WhatsApp), cron jobs, multi-channel communication

**The key difference:** OpenClaw is an always-on messaging assistant you text anytime. Claude Cowork is a desktop agent you assign tasks to. They're complementary, not competing.

### NanoClaw -- Security-First

- Built specifically to solve OpenClaw's security problems
- Each agent runs in an isolated Docker container
- No access to host filesystem, network, or other containers
- Best for: people who care deeply about security
- Tradeoff: smaller ecosystem, fewer skills

### Nanobot -- Lightweight

- OpenClaw core features in 4,000 lines of Python (vs OpenClaw's massive codebase)
- 26,800+ GitHub stars
- Entire codebase readable in hours
- Best for: developers who want to understand and modify their agent
- Tradeoff: fewer features, less polish

### KiloClaw -- Managed Hosting

- Managed OpenClaw -- you don't run your own server
- Independent security assessment: 60+ adversarial tests, zero cross-tenant vulnerabilities
- Best for: people who don't want to manage infrastructure
- Tradeoff: monthly cost, less control

### IronClaw -- Enterprise

- Zero-trust security model
- Suitable for regulated industries
- Best for: enterprise teams with compliance requirements
- Tradeoff: complex setup, enterprise pricing

### Hosted OpenClaw Services

StartClaw, SimpleClaw, MyClaw, UniClaw -- someone else runs OpenClaw for you. Easy setup, no hardware. Best for non-technical users.

### How to Choose

| If you need... | Choose | Why |
|---|---|---|
| Desktop automation | Claude Cowork | Native Anthropic, no ban risk |
| Maximum security | NanoClaw | Container isolation, zero-trust |
| Simplicity | Nanobot | Small codebase, easy to understand |
| No infrastructure | KiloClaw or hosted | Managed for you |
| Enterprise compliance | IronClaw | Zero-trust, audit-ready |
| Maximum flexibility | Stay on OpenClaw | Largest ecosystem, most features |

*Discuss:* The skills you learned -- agent architecture, security thinking, prompt engineering, automation design -- transfer to any platform. OpenClaw is a tool, not a religion.

---

## Chapter 4: Demo Day

> Show what your agent can do. No time limits. Take as long as you need.

---

### Demo Format

Each student presents:

1. **What does your agent do?** -- one sentence summary, who it helps, what problem it solves
2. **Live demo** -- show it working. Send a message, watch it respond. Show the automation in action.
3. **What surprised you?** -- one thing you didn't expect, good or bad
4. **What's next?** -- what would you build next if you had another week?

**Rules:**
- Live demos only -- no slides, no screenshots (unless the agent is down)
- It's OK if something breaks -- that's part of the story
- Celebrate what works, learn from what doesn't
- Take your time -- no rush

---

### What to Watch For

As students present, highlight:

**Architecture choices:**
- Did they use threads, subagents, or multiple agents?
- How did they handle security (tool restrictions, session isolation)?
- What model are they using and why?

**Creative use cases:**
- What problems did they solve that weren't in the workshops?
- Any unexpected combinations of features?

**Common struggles:**
- What kept breaking?
- What took longer than expected?
- What would they do differently?

---

### After All Demos

Group discussion:
- **Best automation** -- which demo was most useful in daily life?
- **Most creative** -- which demo surprised everyone?
- **Lessons learned** -- what did the group learn collectively?
- **What's next** -- where does each person go from here?

---

## Running the Workshop

**Chapter 1 (Anthropic Ban):** 10 minutes. Important context. Frame it as platform risk lesson and opportunity to become multi-provider.

**Chapter 2 (Update & Switch):** 15 minutes. Hands-on for affected students. Multi-provider strategy is the key takeaway.

**Chapter 3 (Alternatives):** 10 minutes. Informational. Make sure they know Claude Cowork exists -- it's Anthropic's direct response.

**Chapter 4 (Demo Day):** All remaining time. No limits. Every student presents. Celebrate everything.

---

## The Finish Line

```
🎉 Workshop 4 COMPLETE! COURSE COMPLETE!

🚨 Ecosystem:
✅ Understand the Anthropic ban and why it happened
✅ Know how to update OpenClaw and switch to OpenAI
✅ Know the multi-provider strategy
✅ Know the alternatives (Claude Cowork, NanoClaw, Nanobot, KiloClaw)

🎤 Demo Day:
✅ Presented your agent to the group
✅ Celebrated wins, learned from struggles
✅ Got inspired by what others built

The OpenClaw Course Journey:
  Workshop 1: Built the foundation
  Workshop 2: Made it useful
  Workshop 3: Made it secure and scalable
  Workshop 4: Navigated change and showed the world

You started with nothing. Now you have:
- A working AI agent (or team of agents)
- Real automations that save you hours
- Security knowledge to protect yourself
- The ability to switch providers and platforms
- A community of fellow builders

The course is over. The building never stops. 🦞
```

---

## Key Lessons to Weave In

**Platform risk is real.** Anthropic changed the rules overnight. Build with flexibility -- never depend on a single provider.

**The multi-provider strategy is the answer.** Use the best model for each task. Default to the cheapest option. Use expensive models only when quality demands it.

**OpenClaw is a tool, not a religion.** If something better comes along, switch. The skills you learned transfer to any platform.

**Claude Cowork and OpenClaw are complementary.** Desktop automation vs always-on messaging agent. You might want both.

**You are the builder.** The most important thing you gained from this course isn't OpenClaw. It's the mindset. You see automation opportunities everywhere. That's the real skill.
