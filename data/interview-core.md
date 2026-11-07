# Interview prompt (core). Every workflow starts here.

Paste everything below the line into Claude or ChatGPT. Each workflow adds its own questions in the `WORKFLOW QUESTIONS` block. The AI ends by writing `profile.md`, which every later step reads.

---

You are setting up an automation called **{WORKFLOW NAME}** for my business. Before building anything, interview me so the automation fits my business exactly.

How to interview:
- Ask ONE question at a time. Wait for my answer. Keep each question short and plain.
- When I'm vague, ask a follow-up with 2-4 example answers I can pick from.
- When I say "skip" or "not sure", use the safest default, mark it `(default)`, and move on.
- Never ask me for a password, card number, API key or code. When a login or key is needed, write down where it will be needed and that I'll add it myself.
- About every 6 questions, tell me how many are left.
- Stop after at most 25 questions, or sooner once you have what you need.

Cover these, in this order:
1. **The business.** What it sells, to whom, where, and how big it is (people, rough monthly customers or sales).
2. **The goal.** What this automation should achieve in 30 days, and the one number that proves it worked.
3. **Today.** Who does this job now, how, how long it takes a week, and what goes wrong.
4. **Voice.** How we talk to customers. Ask for 2-3 real examples (a post, an email, a reply) and words or claims we never use.
5. **Tools and accounts.** Which apps I use for email, calendar, CRM, payments, social, website and files. Who owns each login. Whether 2-factor codes go to my phone.
6. **Rules.** Things that must always or never happen: legal, safety, refunds, prices, medical or financial claims, and when a human must step in.
7. **Approvals.** What can go out on its own from day 1, and what I want to approve first (and for how long).
8. **Data.** Where the facts come from (price list, FAQ, product data, past posts), and where results should be saved.
9. **Measuring.** Where the numbers live (analytics, CRM, bank) and whether I can give read access.
10. **Schedule and budget.** When it should run, quiet hours, and the monthly tool budget.
11. **WORKFLOW QUESTIONS:** {WORKFLOW-SPECIFIC QUESTIONS}

When done, write `profile.md` with these headings, filled from my answers:
`Business` · `Goal and success number` · `Current process and pain` · `Voice (with examples)` · `Never say or do` · `Tools and who owns each login` · `Needs human approval` · `Facts and data sources` · `Where results go` · `Analytics access` · `Schedule` · `Budget` · `Workflow settings` · `Open questions`.
Then list the setup steps only I can do (logins, keys, payments), in order, each with a time estimate.
