---
name: not-ai
description: Rewrite AI-sounding text into clear, natural plain language. Use when
  the user asks to make text sound less like AI, rewrite in plain language,
  de-AI text, or make writing more natural.
---

# Not AI

Rewrite text in plain language. Write like a knowledgeable person explaining something clearly, not like a press release or academic abstract.

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

## Trigger phrases

- `/not-ai`
- "rewrite this in plain language"
- "make this sound less like AI"
- "make this more natural"
- "de-AI this text"

## Core principles

**Be specific, not symbolic.** State facts directly without inflating their importance. Instead of "stands as a testament to innovation," write "introduced a new approach." If something matters, the facts will show it without editorial commentary.

**Use concrete details.** Replace generic praise with specific information. Rather than "revolutionary titan of industry," write "invented a train-coupling device in 1873." Ground claims in observable facts.

**Vary your patterns.** Mix short and long sentences naturally. Avoid the Rule of Three (exactly three items in lists or parallel structures). Let content determine structure.

**Write like you're explaining to a colleague over coffee.** If you wouldn't say it out loud, don't write it. "We're thrilled to announce our revolutionary approach" becomes "We built X because Y kept breaking."

## Words and phrases to avoid

### Puffery words

delve, embark, craft/crafting, realm, tapestry, symphony, testament, pivotal, intricate, multifaceted, nuanced, unwavering, utilize, leverage, seamless, groundbreaking, revolutionary, cutting-edge, game-changer, unlock, illuminate, unveil, harness, navigate, landscape, journey, elevate, optimize, empower, synergy, ecosystem, captivate, nestled, vibrant, rich heritage, breathtaking, must-see

### Gerund sentence endings

- "highlighting the importance of"
- "emphasizing the need for"
- "reflecting the continued relevance of"
- "underscoring its significance"
- "ensuring that"
- "showcasing"

### Vague attributions

- "some experts say"
- "observers note"
- "industry reports suggest"
- "research indicates" (without citing specific sources)

### Setup phrases

- "It's worth noting that"
- "It's important to remember"
- "No discussion would be complete without"
- "In this article we will"

### Hook questions and dramatic intros

- "The best part?"
- "Here's the thing:"
- "Enter: [thing]"
- "And here's the kicker"
- "Ready to level up?"

### Negation structures

- "Not only... but also"
- "It's not just X, it's Y"
- "No X. No Y. Just Z."

## Structural patterns to avoid

### Sycophantic openings

- "Great question!"
- "Certainly!"
- "I'd be happy to..."
- "Absolutely!"

### Section summaries

Don't end paragraphs or sections by restating the main idea. End where the information naturally concludes.

### Conjunctive overload

Use "moreover," "furthermore," "however," "in addition," "at the same time" sparingly. Varied, less conspicuous transitions read as more human.

### Present participle tails

Sentences that end with "-ing" clauses analyzing significance. "The company expanded into Asia, reflecting its global ambitions" should just be "The company expanded into Asia."

### Future speculation sections

Avoid generic "challenges and prospects" conclusions.

## Formatting and punctuation

**Em dashes:** Use commas, parentheses, colons, or periods instead. Em dashes in place of commas is a strong AI tell.

**Quotation marks:** Use straight quotes ("...") and straight apostrophes ('), not curly ones ("..." and '). Most keyboards produce straight quotes by default.

**Boldface:** Use only for article titles in first sentences. Never for emphasis within prose or as list item headers.

**Lists:** Default to prose. Write "options include X, Y, and Z" rather than bullet points. When lists are truly necessary, items should be at least 1-2 sentences, not fragments with bold headers.

**Headers:** Use sentence case, not Title Case.

## What to do instead

Write with genuine voice. Make every sentence information-dense. Trust the reader's intelligence. Support claims with specific sources or acknowledge uncertainty.

Choose simple words: "affects" not "impacts," "problem" not "challenge," "helps" not "enhances," "use" not "utilize," "about" not "surrounding."

When you finish a draft, delete at least a third. Cut transitions, cut summaries, cut anything that restates rather than adds.

## Workflow

1. **Read the input text** the user provides
2. **Identify AI tells**: scan for puffery words, gerund endings, em dashes, sycophantic phrases, structural patterns listed above
3. **Rewrite section by section**: replace flagged language with concrete, specific alternatives
4. **Cut ruthlessly**: remove transitions, summaries, and restatements
5. **Check formatting**: straight quotes, sentence case headers, minimal bold, prose over lists
6. **Return the rewritten text** with a brief note on major changes made

## Examples

### Before

"We're thrilled to unveil our groundbreaking new platform that leverages cutting-edge AI to revolutionize the customer experience. This game-changing solution seamlessly integrates with your existing ecosystem, empowering teams to unlock new opportunities and navigate the evolving digital landscape. Not only does it optimize workflows, but it also elevates productivity to unprecedented levels."

### After

"Our new platform uses machine learning to answer customer questions faster. It connects to your current tools and reduces the steps needed to complete common tasks."

### Before

"John Smith stands as a pivotal figure in the annals of American industry, a visionary titan whose unwavering commitment to innovation crafted a legacy that continues to illuminate the path forward. His multifaceted contributions to the railroad sector underscore his significance in shaping the nation's economic tapestry."

### After

"John Smith invented a train-coupling device in 1873 that reduced coupling injuries by 90%. He founded three railroad companies and held 47 patents."

## Error handling

| Problem | Solution |
|---------|----------|
| User provides very short text | Apply same principles but note fewer changes needed |
| Text is already plain | Confirm it reads naturally, suggest minor tweaks if any |
| Technical jargon is appropriate | Keep domain-specific terms when writing for experts |
| User wants a specific tone | Ask for clarification before rewriting |
