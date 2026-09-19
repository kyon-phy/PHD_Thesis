---
name: academic-writing-pipeline
description: "Draft, revise, or review academic prose and scientific arguments: manuscripts, reviewer responses, grants, abstracts, captions, figure interpretation, and sentence-by-sentence editing. Not for compilation-only or writing-tool maintenance."
---

# Academic Writing Pipeline

Project-specific rules, AGENTS.md, and skills take precedence over this global
skill where they conflict. System/developer instructions and the user's current
explicit request retain their higher priority.

## User-specific writing contract

- Deliver one best version unless alternatives are requested or an unresolved
  scientific/strategy choice requires the user. Logic-only requests get reasoning,
  not unsolicited English prose; a local edit does not reopen the whole passage.
- Use the current assembled draft. Accepted text, Chinese reasoning, terminology,
  deletions, and rejected formulations remain binding until superseded. When the
  user reports a mismatch, identify the mismatch and fix only the authorised span.
- Preserve the subject, relation, condition, causal direction, and claim strength.
  When expressing the user's Chinese reasoning in English, mentally back-translate
  the changed text to check that meaning; LOCAL_REFINE needs no written receipt.
- Keep representation, conditional attribution, association, and causal mechanism
  distinct. For figures/statistics, preserve the observation unit, aggregation,
  comparison, and quantifier scope; a local score is not a global conclusion.
  Explain limitations through supported conditions, not invented causes.

## Personal writing preferences

These preferences consolidate the existing global contract and the Thesis
project's writing guidance. Keep project-specific physics, notation, and source
roles in the project. In drafting and editing, prioritise the user's recorded
preferences and accepted wording over generic AI wording habits. Choose an
idiomatic expression that preserves scientific precision and the intended
relationship. Record later explicit wording preferences in this section.

- **Requested scope:** In local edits, add or change only what the user
  requested. A request to specify working points does not authorise adding other
  selection requirements or expanding nearby explanations. Source support and
  general completeness are not reasons to enlarge the scope. Preserve unrelated
  accepted text and the user's concurrent edits.
- **Working-point choices:** State the working points used in the analysis in
  one short sentence, including the baseline/signal distinction and any
  additional requirement. Follow that choice statement with a brief explanation
  of the working point's actual conditions, such as detector-quality requirements,
  isolation limits or classifier-score thresholds, and their physical meaning.
  Explain concrete differences between working points; names or "more stringent"
  alone are insufficient. Preserve existing adequate definitions without repeating
  them. These explanations cover conditions that define the working point, not
  unrelated object or event selections. Do not append object-role explanations.
  For quantitative performance, give only a short statement of the approximate
  signal efficiency. Do not add rejection values or detailed benchmark samples,
  kinematic ranges and measurement conditions unless explicitly requested.
  Retain only essential qualifiers, such as high momentum or the prong category,
  to avoid misleading generalisations. Keep the full source conditions in
  author-facing notes. Match the algorithm and working-point version, distinguish
  nominal targets from typical performance, and do not treat a sample-dependent
  efficiency as an exact universal constant.
- **Voice and sentences:** Use professional British scientific English unless
  the user or target venue requires otherwise. Write directly, concretely, and
  with restraint. State the main point early, then give the mechanism or reason
  and relevant quantitative detail. Prefer short-to-medium sentences with one
  main logical point; avoid rhetorical filler and vague qualifiers.
- **Passive voice and topic placement:** Prefer passive constructions when
  describing physical and experimental facts or procedures, where natural and
  scientifically accurate. Put the object, quantity, or concept being introduced
  at the beginning of the sentence whenever possible, rather than delaying it
  until the end. Preserve the physical meaning and causal relationship.
- **Itemised explanations:** In each `itemize` entry, use the concept named in
  `\textbf{...}`, or a very closely related term, as the grammatical subject of
  the opening explanatory sentence. Where natural, make the bold label itself
  the subject and continue directly with the predicate. Keep the explanation
  centred on the labelled concept.
- **Manuscript citations and source narration:** Do not mention internal notes
  in thesis or paper prose, or explicitly narrate which documents the analysis
  or description follows. Support the relevant statement directly with
  `\cite{...}`. Cite publicly accessible papers, official public notes, or other
  suitable sources available online; do not cite internal notes, TWiki pages,
  or other internal material. Internal sources may still guide drafting and
  fact-checking. Never cite the user's own analysis INT note or the associated
  ATLAS leptoquark search paper, *Search for a leptoquark in events with a
  hadronically decaying tau-lepton and missing transverse momentum using pp
  collisions at sqrt(s) = 13 TeV with the ATLAS detector*, even when a public
  version exists. Their information and materials may be used to develop the
  manuscript, following the project's source priorities and originality rules.
  Do not cite or attribute the content to these two documents in manuscript
  prose, captions, footnotes or bibliographies. When a reused statement, method,
  equation, numerical result or figure has references in either document, trace
  those references, check the corresponding original sources, and cite the same
  relevant publicly accessible sources directly with `\cite{...}`. Preserve the
  association between each claim and its original references. Do not drop those
  references because the two intermediate documents cannot be cited, or replace
  them arbitrarily. Match references by bibliographic identity and reuse existing
  BibTeX keys where possible. Let the thesis generate its own citation numbers,
  rather than copying reference numbers from the note or paper. The ban on
  internal notes and TWiki still applies to references found in those documents.
  State the user's own analysis choices without self-citation when they have no
  separate underlying reference.
  Record any unresolved need for a public supporting reference
  in author-facing notes outside the manuscript, without inventing a substitute.
- **Source search and conflict priority:** For this thesis, search the user's
  INT note and associated analysis paper first, including their relevant passages
  and cited references, before expanding to other articles or doctoral theses.
  Give their content priority when another article or thesis conflicts with them.
  Use other sources to fill gaps, explain background and check the original
  references, without replacing the analysis definitions with another study's
  choices. Check versions and scope when a conflict appears. If the two priority
  documents disagree with each other, follow the project's established rule
  giving the INT note priority for analysis definitions and implementation, and
  record any unresolved discrepancy in author-facing notes. Source priority
  does not permit citing either document or citing a reference that fails to
  support the statement.
- **Audience and depth:** Explain specialist concepts when first needed by the
  intended reader. Let relevance determine depth. Add essential background even
  when this makes a passage longer; avoid textbook digressions and repeated
  definitions once the explanation is established.
- **First use across the manuscript:** Check earlier chapters and sections
  before expanding a term or defining its abbreviation or symbol. Once the full
  term and its abbreviation or symbol have been introduced, use the established
  abbreviation or symbol in subsequent prose, preserving the existing LaTeX
  macro where applicable. Do not repeat the full term or its definition merely
  because a new chapter or section begins.
  Prefer established symbols in running prose to reduce wording, including in
  phrases such as "the $\pT$ sum". Use the project's existing macros,
  such as `$\pT$` or `$\pt$`, `$\met$`, and `$\et$`, instead of spelling out
  the corresponding quantities again. Preserve distinctions between total and
  transverse quantities and between scalar and vector sums. When summing scalar
  quantities such as $\pT$ or $\et$, write "sum" without the redundant qualifier
  "scalar". Explicitly write "vector sum" when vectors are added.
  Do not introduce
  unnecessary new symbols merely to shorten ordinary explanatory prose.
- **Concrete vocabulary:** Prefer ordinary disciplinary language and name the
  actual process, quantity, condition, method, or uncertainty. Keep established
  technical terms; do not coin labels or rotate synonyms for stylistic variety.
  Minimise abstract process descriptions such as "compatible measurements are
  included in a further fit". State the concrete input, action, or physical purpose
  when it helps the explanation; otherwise omit the procedural detail. Do not
  replace a rejected abstract phrase with another generic statement about fitting,
  updating, or refining.
  Avoid `content` in manuscript prose. For measured inputs and observables,
  use `variable` or `variables`, such as `track-hit variables`, or name the
  quantity directly. Recast the wording where needed to preserve its meaning.
  When listing inputs, variables, or components, prefer `include` to `describe`.
  State what is included directly, rather than saying that the inputs describe it.
  State the physical relation in simple words. When explaining an inferred
  origin, prefer direct wording such as `the track is from the primary vertex`.
  Preserve the uncertainty through a verb such as `suggest` or a modal such as
  `may`, without adding abstract compatibility wording. The user's accepted
  pattern is: "Small absolute values of both quantities suggest that the track
  is from the primary vertex." Retain technical compatibility terminology when
  compatibility itself is the quantity or statistical conclusion being discussed.
- **Disliked wording:** Avoid `account for` and its inflected forms in new or
  revised prose. State the intended relation directly, choosing wording that
  preserves the physical meaning rather than applying a fixed synonym.
  Avoid `approach` in explanatory prose. For geometry and separation, use
  `distance`, such as `minimum transverse distance`, and name the relevant
  objects explicitly. For a methodological meaning, use `method` or another
  concrete term that preserves the meaning.
  Avoid `exploit` and its inflected forms. Prefer a simple verb such as `use`,
  or recast the sentence naturally while preserving the physical relationship.
  Avoid `subsequently`. Prefer common words such as `then` for sequence or
  `further` for an additional step, choosing the word that preserves the intended
  relationship rather than applying a fixed substitution.
- **Paragraph context:** Judge a sentence in its paragraph, preserving what the
  preceding text establishes and what follows next. Do not repeat nearby
  conditions, assumptions, definitions, mechanisms, or operations merely to make
  a local replacement self-contained. Check for repetition of meaning, not just
  repeated words. Explain each point once in the appropriate place; changing
  vocabulary, sentence structure, or perspective does not justify explaining
  the same thing again. In adjacent steps or items, do not present an already
  described operation as another step through rewording. Delete or merge a
  repeated statement that adds no necessary information. If two distinct stages
  really need separate descriptions, state their concrete difference clearly.
  Use a concise cross-reference when sufficient.
  Keep supporting details and limitations subordinate to the paragraph's role
  and the paper's main question.
- **Logical connections:** Make established causal or inferential links between
  adjacent statements explicit more often, using natural connectives such as
  `because`, `therefore`, `consequently`, or `thereby`. Match the connective to the
  actual relationship; do not invent causality or add one mechanically.
  For reconstruction and other stepwise procedures, connect each necessary step
  to its purpose and show how its output is used in the next step. For example,
  a selected production vertex provides the reference for track association,
  and the selected decay tracks determine the prong multiplicity. Use `first`
  and `then` where useful to mark the actual sequence, together
  with these concrete dependencies. Keep the links brief and within the
  requested depth.
  Explain the immediate reason for the specific choice or dependence at issue,
  including why a setting changes with a particular quantity. Start at the nearest
  relevant physical fact and keep the causal chain short. Clearer logic does not
  require tracing the explanation back to first principles or more remote
  mechanisms. Add those links, or distinguish a proxy from the underlying
  quantity, only when needed to understand the local passage.
  When shortening an explanation, retain the key physical terms for the mechanism
  and geometry, such as `boost` and `closely aligned`. A compact causal phrase,
  such as the user's wording `close to the electron due to the boost effect`,
  can explain the immediate relation without expanding the full causal chain.
  Removing a lengthy explanation does not mean removing its essential keywords.
  Generic benefits such as "reducing contamination" or "improving efficiency"
  cannot replace the reason for the specific dependence. Do not rephrase such
  benefits repeatedly while leaving the logical link unexplained.
- **Punctuation:** Avoid semicolons in prose almost entirely, especially to join
  clauses or sentences. Use a suitable connective or split the sentence. Avoid
  em/en dashes in prose unless project conventions require them. These preferences
  do not override required code, mathematical, or machine-readable syntax.
- **Purpose and stopping point:** Explain an operation's purpose or an
  intermediate output's use when needed to follow the argument. Stop an overview
  at its complete physical or methodological endpoint. Put implementation details
  where their quantities and operations can be explained concretely. Do not force
  a purpose/result tail onto every sentence, configuration, or overview.
- **Brief introductions:** The first sentence of each section or subsection must
  explicitly introduce its topic, with the principal object discussed in that
  part of the chapter as its grammatical subject. For example, an Identification
  subsection can begin with "Hadronic tau decays are identified using an RNN
  ...". Put the
  main object and the section's purpose before the supporting variables or tools.
  Within a paragraph, introduce its main topic or method and its role before
  describing its inputs, mechanisms or other details. For example, state that
  an RNN is used for identification before explaining its input variables.
  Let the following sentences develop the topic already introduced.
  Keep chapter and section openings short: establish
  the scope, outline the main physical or methodological steps, and introduce
  the necessary keywords. Leave detailed definitions, mechanisms, and correction
  procedures to the relevant sections. Use the user's shortened opening as the
  reference for length and depth; do not restore deleted exposition or expand
  each keyword into a mini-review unless needed for correctness or to follow
  the immediate argument.
- **Captions and quantitative detail:** Identify what is plotted and the
  conditions, comparisons, and uncertainty definitions needed to read the figure.
  Keep detail proportionate to that purpose. Omit exact thresholds or calendar
  years when they add no necessary information; for example, use `Run~2` when
  that period label is sufficient. Preserve numbers or dates that define the
  scientific scope or are needed for the argument.
- **Short figure captions:** Always use `\caption[short title]{full caption}`
  for figure captions. The short title is used in the List of Figures and must
  contain no citation commands, reference numbers, or source attribution.
  Keep source citations in the full caption only, so reading the List of Figures
  does not change citation order or introduce references into its entries.
  Attach the source directly to the end of the relevant caption sentence as
  `...~\cite{key}.` Do not add wording such as `reproduced from Ref.`,
  `refer from Ref.`, or a separate sentence merely announcing the source.
- **Original phrasing and claim strength:** Reconstruct explanations from the
  supported scientific point in the user's own direct style. Do not copy source
  sentences or make superficial synonym substitutions. Use restrained claims and
  preserve distinctions such as excluded, constrained, compatible with, and
  motivated by.
- **Preposition preference:** Avoid `relative to` where a natural alternative
  preserves the meaning. Prefer `with`, `with respect to`, or `for`, choosing the
  expression that fits the actual relation. Recast the sentence when needed
  instead of mechanically substituting prepositions or changing a comparison,
  reference value, or normalisation. Apply this preference to new or revised
  prose without expanding a local edit to unrelated accepted text.

## Proportionate workflow

Choose by the user's requested scope, not the length of pasted context:

- **FULL_SECTION_REVIEW:** a comprehensive review of a complete section,
  subsection, or chapter, including a bounded chapter review up to a named
  progress marker. Automatically load and follow
  [full-review.md](references/full-review.md). This activates the larger
  validation records without requiring the user to ask separately for each
  check. Independent readers remain opt-in in both modes. A review alone does not
  authorise edits.
- **LOCAL_REFINE:** word, sentence, or paragraph refinements and frequent
  sentence-by-sentence collaboration. Also use this for several explicit local
  corrections, even across a chapter. Do not load full-review resources merely
  because the context is long, many edits have accumulated, or compilation is
  needed. A later explicit whole-section/chapter review switches to full mode.

For LOCAL_REFINE, use the compact workflow below.
If the user fixes the intended change, make the local patch directly, reread it
in context, and inspect the diff for file edits. Ordinary wording decisions,
sentence count, file type, or formatting repairs do not justify a larger process.
In user-paced sentence editing, stop at the current sentence until the user
accepts or replaces it; this does not require a session manifest.

For an open-ended passage rewrite, first settle its question, evidence order,
claim boundary, and paragraph roles. Then check the assembled passage for gaps,
repetition, unsupported inference, and displaced emphasis. Results should build
an evidence argument, not list actions; synthesis follows the evidence it uses.
Outside FULL_SECTION_REVIEW, do not require per-sentence logs. The primary agent
checks the assembled text; extra reader agents run only when explicitly requested.

LOCAL_REFINE needs no JSON receipts, hash authorisations, manifests, gate
scripts, or wrapper scripts. Compile/render only when requested or materially
needed for syntax/layout validation, subject to applicable artifact skills.
Show substantive file edits with a concise diff or before/after comparison.

## Independent readers (explicit opt-in only)

Do not launch independent reader agents by default, including for full-section
or chapter reviews. Enable them only when the user explicitly requests reader
review or independent reviewers; ordinary requests to revise or review prose do
not enable them. This supersedes older always-on and mandatory-reader guidance.
The opt-in applies only to the requested review task/span, not later edits,
unless the user explicitly sets a wider activation period. The primary agent's
normal context, logic, scientific accuracy and concision checks remain active.

When enabled, review the current assembled paragraphs in the requested scope.
Use the project's reader profiles, count, expertise, and execution settings when
defined. Otherwise use one independent reader matched to the document's intended
audience and discipline, without assuming HEP expertise or a two-reader setup.
Give readers the actual paragraph, necessary preceding/following text, existing
definitions and cross-references, neutral paragraph purpose, locked spans, and
authorised scope. Use fresh context (`fork_turns="none"`); do not supply hidden
author intent, intended answers, or another reader's first-pass opinions. Do not
withhold context and then diagnose an already-defined concept as unexplained.

Readers are read-only and must not spawn readers. Their reports do not trigger
another review cycle. The primary agent assesses findings against evidence and
scope, makes only warranted corrections, and reports each reader's findings and
their disposition, including no change or rejection with a reason. Return any
substantively revised affected paragraph to the required readers to verify the
resolution; later changes to visible wording or punctuation also receive the
required readers. Only mechanical build, layout or LaTeX repairs that leave
visible wording and argument unchanged need no new cycle. Continue targeted
in-scope corrections while making evidence-supported progress, following the
project's convergence procedure. Stop and report repeated unresolved critique
without new evidence, irreconcilable factual/context gaps, or a required scope
or authority choice; do not loop for optional stylistic preferences. Ask only
if resolving the issue requires the user's decision. Review-only requests
remain read-only. If a required reader is unavailable, provide useful results
with that check explicitly incomplete;
never invent a report. LOCAL_REFINE still requires no JSON, manifests, or hashes.

## Optional historical resources

This file is the active compact contract. Do not routinely load
`/Users/zang/openclaw/WRITING-RULES.md` or
`/Users/zang/openclaw/memory/cjy-academic-writing-profile.md`.
Consult them only for a relevant preference not resolved here or in the project,
or when the user requests them; project writing voice takes priority.
Keep grant-specific advice out of manuscripts and reviewer responses, and do not
imitate errors from historical drafts.

Existing scripts and detailed gate references are formal-audit tools. Use them
only as routed by full-review.md or when explicitly requested. Their legacy
mandatory-gate language does not apply to LOCAL_REFINE.
Without reader opt-in, do not invoke legacy gates that require an independent
peer or fabricate a reader report to satisfy them; use the active self-check
workflow instead. An unrequested reader review is disabled, not an incomplete check.
