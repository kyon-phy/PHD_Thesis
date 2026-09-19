---
name: atlas-u1-thesis-writing
description: "Draft, revise, review, or source-check this ATLAS U1 thesis on tau + missing transverse momentum + jets/b-jets. Covers physics and scientific English, not unrelated writing or compilation-only tasks."
---

# ATLAS U1 Thesis Writing

Use the project's AGENTS.md for source roles, audience, physics priorities,
British English, review categories, and LaTeX conventions. This skill adds the
user's local preferences and source lookup routes; it does not repeat that guide.
Project rules override conflicting global writing guidance.
The local preferences below record later user corrections and supersede
conflicting legacy wording in the synced AGENTS.md or supporting guides.

## Local writing preferences

- Search the user's INT note and associated analysis paper first, including
  their references, before consulting other articles or doctoral theses. When
  outside sources conflict with these two documents, give the two documents'
  content priority. Use outside sources for missing background and original
  reference checks without importing conflicting analysis choices. Check
  versions and scope, and record unresolved discrepancies in author-facing
  notes. Between the two priority documents, the INT note remains controlling
  for analysis definitions and implementation. These content and search
  priorities do not change the citation restrictions below.
- Never cite the user's own analysis INT note or associated tau + missing
  transverse momentum leptoquark search paper, including public versions.
  Identify them by title and content, not only by a citation key or filename:
  `ANA_EXOT_2025_06_INT1` / `ANA-EXOT-2025-06-INT1`, and *Search for a
  leptoquark in events with a hadronically decaying tau-lepton and missing
  transverse momentum using pp collisions at sqrt(s) = 13 TeV with the ATLAS
  detector* (`arXiv:2606.02067`, `CERN-EP-2026-136`,
  `ATL-COM-PHYS-2026-015`, formerly `ATLAS2026LQTauNu`). Their information
  and materials may be used in drafting, with the INT note taking priority for
  analysis definitions, but the two documents must not be cited or named as the
  source in prose, captions, footnotes or bibliographies. When the material used
  has references in the note or paper, check and directly cite those same
  relevant original public sources. Preserve the claim-to-reference association
  and use BibTeX keys, not the source documents' reference numbers, following the
  global writing skill's citation rule. State this analysis's own choices without
  self-citation when they have no separate underlying reference. Keep provenance
  in author-facing notes outside the manuscript. Internal notes and TWiki pages
  are also excluded from citations. Check both citation calls and bibliography
  entries, then regenerate affected PDFs when cleaning up existing citations.
- Do not repeat nearby conditions, benchmark assumptions, definitions, or
  mechanisms. Use a concise cross-reference when needed; repeat only if omission
  would create ambiguity or change the scientific scope.
- Once signal regions (SRs) have been introduced, use SR or the established
  one-b/zero-b SR names instead of category/categories when referring to them.
  Preserve the existing SR1b/SR0b notation and macros, `\SR` and `\bVetoSR`.
  Do not rename object-reconstruction types, truth-level selections, CRs or VRs
  as SRs; retain the actual meaning of each selection or classification.
- Stop an overview at its complete physical or methodological endpoint. Do not
  add a detail that is too specific for that level yet abstract because its
  quantities or operations are undefined. In the MC overview, reaching comparison
  with collision data is sufficient; weights and normalisation belong where they
  are explained concretely, not in a vague trailing clause.
- Keep the background-sample introduction to the backgrounds used in the
  analysis; the subsection's purpose is MC configuration. Do not repeat background
  motivation or import the later data-driven estimation discussion.
- Use the aliases defined in Preamble/preamble.tex for recurring quantities and
  common background processes, such as `\et`, `\mpt`, `\met`, `\mT`, `\pT`, `\gU`,
  `\MU`, `\MLQ`, `\zll`, `\zee`, `\zmumu`, `\wtaunu`, and `\ttbar`, instead
  of repeating their LaTeX expansions. Consult the preamble for the full list.
  After introducing missing transverse momentum, use `\mpt` for its vector and
  `\met` for its magnitude in subsequent prose and equations.
  Preserve the distinction between M_U and M_LQ; do not redefine existing aliases.

## Two independent readers (explicit opt-in only)

Reader review is off by default in both LOCAL_REFINE and FULL_SECTION_REVIEW.
Run the two read-only readers only when the user explicitly enables reader review;
ordinary revision or section/chapter review requests do not activate them. This
supersedes the earlier always-on rule. Activation is limited to the requested
task/span, not later edits, unless the user explicitly requests a wider period.
Keep the primary agent's context, physics, terminology and concision checks.
Review-only requests do not permit edits.

The editable native Codex profiles are the source of truth for reader prompts:

- [`.codex/agents/thesis-general-physics-reader.toml`](../../../.codex/agents/thesis-general-physics-reader.toml):
  a physics PhD without HEP background checks the main logic, necessary first-use
  explanation, and thesis depth without ATLAS-internal digressions.
- [`.codex/agents/thesis-hep-reader.toml`](../../../.codex/agents/thesis-hep-reader.toml):
  a HEP scholar checks science, methods, key assumptions, terminology, and natural
  standard HEP academic phrasing, verifying relevant actual sources when needed.

Both profiles currently default to Extra High (`xhigh`) and inherit the parent
model; dispatch uses the current profile values if the user edits them. Only when
reader review is enabled, read
[paragraph-readers.md](references/paragraph-readers.md) before dispatch for context
assembly, native/fallback execution, feedback, and bounded verification. Re-read
the profiles before each dispatch so user edits take effect; do not duplicate
their prompts or assume a task name automatically loads a profile. After both
reports, apply warranted smallest corrections and tell the user each reader's
findings and what changed, or why no change was made. Preserve the local depth
and non-repetition rules above throughout this process.

## Sources and targeted checks

Treat sources/ and
`/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/`
as read-only reference libraries. Consult relevant articles from both when
available; do not modify, rename, move, or delete them.

Load a supporting guide only when the task needs its additional detail:

- [Source routing](references/source-routing.md): locating sources and checking
  analysis content, numerical values, conventions, or source disagreements.
- [Physics checklist](references/physics-checklist.md): substantive physics
  review, not ordinary wording corrections. Checks are not a list of content to
  insert into every paragraph.
- [Explanation patterns](references/thesis-explanation-patterns.md): unresolved
  first-use background or explanation structure, not routine sentence edits.
- [Writing/LaTeX review](references/writing-latex-review.md): detailed review
  presentation, captions, or LaTeX conventions not already resolved by AGENTS.md.

Do not load all guides or re-read papers for a purely linguistic local change.
For a complete section/subsection or chapter review (including up to a progress
marker), use FULL_SECTION_REVIEW in the global academic-writing-pipeline skill.
For frequent local refinements, use LOCAL_REFINE without writing-gate scripts.
Neither mode automatically launches readers; full review still adds the global
validation records. Both respect the local depth and non-repetition preferences above.
Compile when requested or when syntax/layout verification is material.
