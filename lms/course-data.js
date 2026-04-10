var COURSES = [
    {
        id: 'openclaw-sprint-c1',
        title: 'OpenClaw Sprint C1',
        subtitle: 'A 4-week hands-on course — install, automate, secure, and scale your own AI agent',
        type: 'course',
        modules: [
            {
                id: 'workshop-1',
                title: 'Getting Started',
                subtitle: 'Install OpenClaw, connect Telegram, enable voice, email, and browser access',
                number: 1,
                label: 'Workshop 1',
                slidesUrl: '../workshop-1-presentation.html',
                materialUrl: '../skills/openclaw-workshop-1/SKILL.md',
                slideCount: 110
            },
            {
                id: 'workshop-2',
                title: 'Power Features',
                subtitle: 'Google Workspace, 1Password, skills marketplace, and 7 hands-on automations',
                number: 2,
                label: 'Workshop 2',
                slidesUrl: '../workshop-2-presentation.html',
                materialUrl: '../skills/openclaw-workshop-2/SKILL.md',
                slideCount: 98
            },
            {
                id: 'workshop-3',
                title: 'Security, Threads & Multi-Agent',
                subtitle: 'Prompt injection attacks, five levels of isolation, multi-agent architecture, cost management',
                number: 3,
                label: 'Workshop 3',
                slidesUrl: '../workshop-3-presentation.html',
                materialUrl: '../skills/openclaw-workshop-3/SKILL.md',
                slideCount: 77
            },
            {
                id: 'workshop-4',
                title: 'Demo Day & What\'s Next',
                subtitle: 'The Anthropic ban, switching providers, alternatives ecosystem, and live student demos',
                number: 4,
                label: 'Workshop 4',
                slidesUrl: '../workshop-4-presentation.html',
                materialUrl: '../skills/openclaw-workshop-4/SKILL.md',
                slideCount: 38
            }
        ]
    },
    {
        id: 'f4f-webinar',
        title: 'Founders for Founders — OpenClaw Webinar',
        subtitle: 'From chat tools to your own AI employee — why OpenClaw matters and what it can do',
        type: 'webinar',
        modules: [
            {
                id: 'webinar-main',
                title: 'Founders for Founders — OpenClaw Webinar',
                subtitle: 'From chat tools to your own AI employee',
                number: 1,
                label: 'Webinar',
                slidesUrl: '../webinar/openclaw-webinar.html',
                materialUrl: null,
                slideCount: 57
            }
        ]
    },
    {
        id: 'nova-webinar',
        title: 'Nova OpenClaw Webinar',
        subtitle: 'Answers to the most common questions about OpenClaw — setup, security, costs, and use cases',
        type: 'webinar',
        modules: [
            {
                id: 'webinar-qa',
                title: 'Nova OpenClaw Webinar',
                subtitle: 'Q&A session with speaker notes and slide-by-slide breakdown',
                number: 1,
                label: 'Webinar',
                slidesUrl: '../webinar/openclaw-webinar-qa.html',
                materialUrl: '../webinar/openclaw-webinar-qa-notes.md',
                slideCount: 62
            }
        ]
    }
];

// Helper to find a module by id across all courses
function findModule(moduleId) {
    for (var i = 0; i < COURSES.length; i++) {
        for (var j = 0; j < COURSES[i].modules.length; j++) {
            if (COURSES[i].modules[j].id === moduleId) {
                return { course: COURSES[i], module: COURSES[i].modules[j] };
            }
        }
    }
    return null;
}
