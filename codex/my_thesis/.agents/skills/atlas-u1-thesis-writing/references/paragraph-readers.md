# Paragraph reader dispatch and reconciliation

Load and use this procedure only when the user explicitly enables reader review.
It is off by default for both local refinements and full-section/chapter reviews.
An ordinary request to revise or review text is not reader opt-in. Activation
covers only the requested task/span; later edits default to no reader agents
unless the user explicitly sets a wider activation period.

Within that enabled task, review the current assembled paragraphs before delivery,
including word or punctuation changes. A passage may be sent as a batch if both readers can cover every
affected paragraph with adequate context; batching does not change review
coverage. For review-only requests, inspect the requested text and report
findings without changing manuscript files. Reader reports are exempt from
further paragraph review, and readers must not edit files or spawn nested readers.

## Context packet

Read the authoritative current draft and assemble the full paragraph with the
proposed local replacement literally inserted. Supply both readers with:

- The actual current paragraph, identified by file/heading or a simple paragraph
  label; include the unchanged prefix and suffix, not just a diff fragment.
- Necessary preceding and following text, established definitions, notation and
  cross-reference targets. Include more adjacent material for openings, closures
  or bridges when needed to judge repetition and continuity. Do not withhold a
  definition and then treat the concept as unexplained.
- The chapter/section context and paragraph purpose stated neutrally, plus exact
  locked spans and the user-approved edit scope. A purpose describes the paragraph's
  document role, not what the reader is supposed to conclude from its prose.

Do not include hidden author intentions, intended answers, reasoning ledgers,
preselected faults, a defence of the draft or the other reader's first-pass
opinions. The general-physics reader uses visible text and definitions to judge
comprehension; do not give it an expert rationale that supplies missing logic.
The HEP reader may inspect relevant real sources using
[source-routing.md](source-routing.md). Provide relevant source locations as
evidence routes, without telling it what verdict to return. Source libraries stay
read-only; claimed verification must identify material actually read. If essential
context is unavailable, report that limitation instead of inventing it.

## Execute the editable profiles

The two profile files linked in SKILL.md contain the maintained role prompts.
Read and parse the current files before each dispatch, including verification
passes; do not keep a stale cached prompt after the user edits a profile. Load
`developer_instructions` and `model_reasoning_effort` from each. Both currently
specify `xhigh` (Extra High) and omit `model`, so inherit the parent model. Ultra
was requested for configuring this workflow, not for reader execution.

Where the available native agent tool supports selecting a configured agent,
select each profile by its configured name and supply its context packet using
a fresh context. Do not assume every tool exposes this selector.

In this session `collaboration.spawn_agent` has no named custom-agent selector.
Use the executable fallback for each profile:

1. Set `task_name` to a unique task label. It is a label only and does not load
   `.codex/agents/*.toml` automatically.
2. Put the profile's complete `developer_instructions` plus the neutral context
   packet in `message`. Pass the parsed `model_reasoning_effort` as
   `reasoning_effort` (`"xhigh"` in the supplied profiles), with
   `fork_turns="none"` and no `model` override. Use
   `collaboration.spawn_agent` directly, not through `functions.exec`.
3. Dispatch both independent readers without waiting for the first report; check
   sources, scope or the diff locally while they run. Keep their first-pass inputs
   independent and collect both reports before deciding corrections.

The TOML profiles request `sandbox_mode="read-only"` where native execution
honours it. The fallback tool cannot set sandbox mode: it inherits runtime
permissions, so enforce the read-only task instructions and do not claim a native
read-only sandbox was applied. Readers are not persistent user tasks; do not
create two sidebar tasks for this workflow. If the tool, a profile or a required
setting is unavailable, identify the missing check; do not silently substitute
one reader, a different effort or a fabricated result.

## Findings, smallest corrections and stopping

Evaluate both reports against the visible text, actual sources, locked wording
and authorised scope. Reader taste is advisory; uncommon wording is not an error
by itself, and synonyms must not change established HEP terms. Distinguish a
verified scientific error, missing explanation, source uncertainty and optional
style. Preserve thesis-level explanation without engineering padding. Do not
reopen locked text or invent assumptions to accommodate a reader.

Apply only evidence-supported corrections inside the authorised span. If the
primary agent makes a substantive change, send the updated complete affected
paragraph and necessary context to both readers using fresh contexts and the
current profiles. Supply only the specific issue that needs verification;
do not ask either reader to adopt the other reader's opinion. Verify resolution
and check for newly introduced problems. A further change to visible wording or
punctuation also goes to both readers, regardless of length. Only mechanical
build, layout or LaTeX repairs that leave visible wording and argument unchanged
can be reported without another cycle.

Continue targeted corrections within the same authorised scope while the text
makes concrete, evidence-supported progress, returning every revised paragraph
to both readers. Do not stop at an arbitrary number of rounds while a new,
clearly supported issue can be fixed. Stop automatic rewriting when the same
unresolved critique recurs without new evidence, a factual or contextual gap
cannot be reconciled, or resolution requires a new scope or authority choice.
Report the evidence and remaining issue; request user direction only when their
decision is needed. Optional stylistic tastes do not justify a loop, and neither
reader must be made to produce a clean verdict. Do not deliver further changed
prose as reviewed until both have reviewed its current version.

Tell the user what **both** readers found and the primary agent's disposition:
what changed, what already required no change, and which suggestion was rejected
or deferred with a concise reason. Even if one or both find nothing substantive,
state that result. Scale feedback to the edit; a local correction needs a short
account, not two long reports. Never call an unperformed source check verified.

LOCAL_REFINE uses the paragraph, context and actual reports directly; it does not
require JSON, a manifest, hashes, receipts or wrapper scripts. FULL_SECTION_REVIEW
records both readers, their coverage and follow-up reports in its review manifest
under the global [full-review.md](/Users/zang/.codex/skills/academic-writing-pipeline/references/full-review.md)
workflow. Returning to local edits ends that recordkeeping requirement. Preserve
completed review records, but do not continue reader dispatch unless the user's
explicit activation covers those follow-up edits.
