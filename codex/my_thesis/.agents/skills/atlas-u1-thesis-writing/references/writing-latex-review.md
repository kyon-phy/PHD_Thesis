# Writing, LaTeX, and Review Procedure

## Writing and editing

- Use professional British scientific English.
- Prefer short-to-medium sentences with one main logical point.
- State the main point early, then give the mechanism or reason and the
  necessary quantitative detail.
- Name the actual process, coupling, CKM element, observable, background, or
  uncertainty instead of using vague referents.
- Avoid rhetorical filler, ornate wording, unnecessary signposting, and
  repeated motivation.
- Preserve the user's structure and terminology when they are correct and
  complete. Make the smallest change that fixes the problem.
- Add necessary background when omission breaks the logical chain, even if the
  revised passage becomes longer.
- Do not make prose more formal merely for stylistic effect.

## Review presentation

For a paragraph or section, report only categories that contain material
findings, normally in this order:

1. source, version, or notation discrepancies;
2. physics errors or potentially misleading interpretations;
3. missing or unclear explanations;
4. structural or logical-flow problems;
5. scientific-English issues; and
6. optional style improvements.

Do not present a style preference as a physics error. If the original is sound,
say so and avoid an unnecessary rewrite.

For a whole section, also check concepts before first use, equation
interpretation, notation across paragraphs, repetition, figure/table purpose,
and citation gaps. Prioritise substantive issues over copy-editing.

For a minor correction, give the corrected sentence directly. For a material
revision, explain the problem briefly and then provide one recommended version;
offer an alternative only when it reflects a genuine depth or interpretation
choice.

## LaTeX

- Provide LaTeX source for text intended for direct thesis insertion. Otherwise
  render mathematics normally unless the user asks for raw source.
- Preserve established labels, citation keys, cross-references, HEP unit
  macros, \(\beta\) indices, chirality labels, flavour-basis conventions, and
  mass symbols.
- Do not invent a macro. Inspect the thesis context or use standard LaTeX when
  the existing macro is unknown.
- Use `$$...$$` for short displayed mathematics and
  `\begin{align}...\end{align}` for longer or multi-line expressions; avoid
  `\[...\]` in thesis-ready text for this project.
- After the full Standard Model gauge group has been defined, use a shorter
  form or "the SM gauge group" when the full notation is not required.
- Motivate each important equation, define new symbols, identify the relevant
  term or scaling, and state the physical consequence.
- Compile only when the user asks or when editing a complete TeX artifact makes
  syntax or layout verification material. Use the LaTeX plugin for compilation
  or environment diagnosis when available.

## Figures, tables, and results

- State what the reader should notice and why it supports the argument.
- Keep captions descriptive; put substantive interpretation in the surrounding
  text unless the caption must be self-contained.
- Do not use a cut table, generator table, or hardware inventory as a substitute
  for physical explanation.
- Use restrained ATLAS-style result language. Distinguish exclusion,
  constraint, preference, compatibility, motivation, and explanatory ability.

## Secondary quality checks

When Academic Writing Toolkit is available, use only the relevant capability:

- paragraph logic for a structural second pass;
- British English for conservative spelling checks;
- citation audit when the user supplies suitable reading-note source lines; or
- BibTeX validation for reference-record structure.

Treat its findings as editorial evidence to assess, not automatic replacements.
It cannot validate the physics, the analysis convention, or whether a source
actually supports a specialised HEP claim.
