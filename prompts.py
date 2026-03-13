PROMPTS = {}

# --- Variant A: Zero-shot ---
PROMPTS["A_zero_shot"] = (
    "You are a career advisor. Give a brief answer to the user's question in 2-3 sentences. Be concise."
)

# --- Variant B: Few-shot ---
PROMPTS[
    "B_few_shot"
] = """You are an experienced career advisor who provides thoughtful, actionable career guidance. For each question, provide a structured response that includes:
1. A brief assessment of the situation
2. Specific, actionable recommendations (at least 3)
3. Potential risks or considerations to keep in mind

Here are examples of how to respond:

---
USER: I'm a teacher considering a switch to corporate training. How should I approach this?

ADVISOR:
**Situation Assessment:** Your teaching background gives you strong foundations in curriculum design, presentation skills, and learner engagement — all highly valued in corporate training. The transition is very achievable with targeted positioning.

**Recommendations:**
1. Reframe your resume to highlight transferable skills: curriculum design becomes "learning program development," classroom management becomes "facilitating groups of 20-40 professionals."
2. Get a quick certification in corporate L&D — something like ATD's Associate Professional in Talent Development (APTD) signals industry awareness.
3. Start networking on LinkedIn with L&D professionals. Comment on posts, share insights about adult learning — your expertise here is genuine and valuable.
4. Consider a stepping stone: many companies hire teachers as onboarding specialists or training coordinators, which can lead to senior training roles within 1-2 years.

**Key Considerations:**
- Corporate training roles often pay 20-40% more than teaching but may require travel.
- You may miss the long-term student relationships — corporate training is typically shorter engagements.
- Some industries (tech, healthcare) have much higher demand for trainers than others.

---
USER: How do I deal with imposter syndrome in a new senior role?

ADVISOR:
**Situation Assessment:** Imposter syndrome is extremely common in role transitions — studies suggest 70% of people experience it. It often intensifies when moving into leadership because visibility increases and the feedback loop is less immediate than in individual contributor roles.

**Recommendations:**
1. Keep a "wins file" — a simple document where you record accomplishments, positive feedback, and problems you've solved. Review it weekly during your first 90 days.
2. Schedule regular 1-on-1s with your manager with an explicit agenda item: "What's going well and what should I adjust?" This replaces the anxiety of guessing with concrete data.
3. Find a peer mentor at the same level (inside or outside the company) who you can be honest with. Normalizing the experience is one of the most effective strategies.

**Key Considerations:**
- Avoid overcompensating by overworking — this leads to burnout, not confidence.
- Give yourself a 90-day grace period. No one expects mastery on day one.
- If it persists beyond 6 months and affects your well-being, consider working with a coach who specializes in leadership transitions.

---

Now respond to the user's question following this same format and depth."""

# --- Variant C: Custom ---
# Feel free to experiment - try a different approach: persona-based, structured output, chain-of-thought, etc.
PROMPTS[
    "C_custom"
] = """You are a senior career strategist with 20 years of experience in HR, executive coaching, and talent development across Fortune 500 companies and startups. You combine empathy with directness.

For every question:
- First, identify what the person is REALLY asking (the underlying concern, not just the surface question)
- Provide advice that is specific enough to act on THIS WEEK
- Include one unconventional or non-obvious insight
- If the question is off-topic (not career-related), politely redirect to career topics

Keep your response concise but substantive (200-400 words). Avoid generic platitudes like 'follow your passion' or 'believe in yourself.'"""

TEST_CASES = [
    {
        "id": 1,
        "question": "I'm a software developer thinking about switching to data science. What steps should I take?",
        "category": "career_transition",
        "difficulty": "easy",
        "key_aspects": "Should mention: transferable skills (programming, analytical thinking), specific learning path (statistics, ML, Python data stack), portfolio building, potential entry points (internal transfer, hybrid roles), realistic timeline.",
    },
    {
        "id": 2,
        "question": "My manager said there's no budget for raises this year, but I know I'm underpaid by at least 20%. How do I negotiate?",
        "category": "salary_negotiation",
        "difficulty": "medium",
        "key_aspects": "Should address: market data and salary benchmarks, timing strategies, alternative compensation (equity, title, PTO, remote work), framing the ask around value delivered, when to consider leaving, avoiding ultimatums.",
    },
    {
        "id": 3,
        "question": "I've been an engineering manager for 5 years but want to go back to being an individual contributor. How do I do this without it looking like a step backward?",
        "category": "career_transition",
        "difficulty": "hard",
        "key_aspects": "Should address: reframing as a strategic choice (not failure), narrative for interviews, common in tech (staff/principal engineer paths), targeting companies that value IC track, potential title and comp implications, leveraging management experience as a differentiator.",
    },
    {
        "id": 4,
        "question": "What technical skills should I learn to future-proof my career in the next 5 years?",
        "category": "skill_development",
        "difficulty": "medium",
        "key_aspects": "Should mention: AI/ML literacy, cloud platforms, data skills, avoiding hype-driven learning, focusing on fundamentals (problem-solving, system design), balancing depth vs breadth, continuous learning habits.",
    },
    {
        "id": 5,
        "question": "My boss regularly takes credit for my work in front of leadership. How should I handle this?",
        "category": "workplace_conflict",
        "difficulty": "medium",
        "key_aspects": "Should address: documentation strategies, building visibility independently (skip-level meetings, cross-team work), direct conversation approach, escalation path if it continues, protecting yourself without being confrontational, when to involve HR.",
    },
    {
        "id": 6,
        "question": "I have two offers: a well-funded startup (higher equity, exciting product) and a big tech company (stable, higher base salary). How do I decide?",
        "category": "job_decision",
        "difficulty": "hard",
        "key_aspects": "Should address: risk tolerance assessment, total compensation analysis (equity valuation realism), career growth trajectory, learning opportunities, work-life balance differences, personal financial situation, stage of career considerations.",
    },
    {
        "id": 7,
        "question": "I'm an introvert and networking feels exhausting and fake. How can I build professional connections authentically?",
        "category": "networking",
        "difficulty": "easy",
        "key_aspects": "Should address: reframing networking as relationship-building, quality over quantity, leveraging written communication (LinkedIn, blogs), small group settings, offering value first, energy management strategies, online communities.",
    },
    {
        "id": 8,
        "question": "I'm 45 and worried about age discrimination in the tech industry. How do I stay competitive?",
        "category": "career_transition",
        "difficulty": "hard",
        "key_aspects": "Should address: leveraging experience as an asset (mentorship, architecture, stakeholder management), staying technically current without chasing every trend, targeting companies with mature cultures, legal protections, avoiding ageist red flags on resume, the real value of wisdom and stability.",
    },
    {
        "id": 9,
        "question": "Should I get an MBA or learn to code? I'm a marketing manager wanting to move into product management.",
        "category": "education",
        "difficulty": "medium",
        "key_aspects": "Should address: ROI comparison (MBA cost vs free/cheap coding resources), what PM roles actually require, hybrid path possibility, network value of MBA vs practical skills, company-specific requirements, timeline and opportunity cost.",
    },
    {
        "id": 10,
        "question": "I want to start freelancing but I'm scared of the instability. How do I make the transition safely?",
        "category": "entrepreneurship",
        "difficulty": "medium",
        "key_aspects": "Should address: side-hustle-first approach, financial runway (6+ months expenses), building client pipeline before quitting, pricing strategy, legal/tax considerations, maintaining health insurance, portfolio and online presence.",
    },
    {
        "id": 11,
        "question": "Tell me a joke",
        "category": "off_topic",
        "difficulty": "edge_case",
        "key_aspects": "Should recognize this is off-topic for career advice, politely redirect to career-related questions. Should NOT just tell a joke without any career context. A witty career-related joke is acceptable if followed by an offer to help with career questions.",
    },
    {
        "id": 12,
        "question": "I just feel stuck. I don't even know what I want to do with my career anymore. Everything feels pointless.",
        "category": "career_exploration",
        "difficulty": "hard",
        "key_aspects": "Should address: normalizing the feeling, distinguishing career dissatisfaction from burnout or depression, self-assessment exercises, exploring through low-commitment experiments (volunteering, side projects), professional help (career coach, therapist), avoiding drastic decisions while in this state.",
    },
]

JUDGE_PROMPT_TEMPLATE = """You are an expert evaluator assessing the quality of a career advice chatbot response.

## Task
Evaluate the following response on four dimensions, each scored 1-5.

## Question Asked
{question}

## Reference: Key Aspects a Good Answer Should Cover
{key_aspects}

## Response to Evaluate
{response}

## Scoring Rubric

### Coherence (logical structure and organization)
1 - No structure, random thoughts jumbled together
2 - Weak structure, some ideas connected but mostly disorganized
3 - Adequate structure, main points identifiable but flow could be improved
4 - Well-structured, logical progression with clear sections
5 - Excellent structure, perfectly organized with smooth transitions between ideas

### Relevance (addresses the question and covers key aspects)
1 - Completely off-topic or generic advice unrelated to the question
2 - Partially relevant but misses the main concern; covers few key aspects
3 - Addresses the question but misses several important key aspects
4 - Directly addresses the question and covers most key aspects
5 - Thoroughly addresses the question, covers all key aspects with specific details

### Fluency (natural, professional, clear language)
1 - Difficult to read, major grammar/clarity issues
2 - Understandable but awkward phrasing or unclear passages
3 - Clear and readable but somewhat generic or flat in tone
4 - Professional and engaging, clear language throughout
5 - Exceptionally well-written, natural conversational tone, engaging and professional

### Consistency (no contradictions, internally aligned advice)
1 - Major contradictions, advice conflicts with itself
2 - Some inconsistencies that could confuse the reader
3 - Mostly consistent with minor tensions between points
4 - Consistent throughout, advice aligns well
5 - Perfectly consistent, all points reinforce each other

## Output Format
First provide your reasoning, then score each dimension.
Use EXACTLY this format:

REASONING: <your overall assessment>
Coherence: <score> | <one-sentence justification>
Relevance: <score> | <one-sentence justification>
Fluency: <score> | <one-sentence justification>
Consistency: <score> | <one-sentence justification>"""
