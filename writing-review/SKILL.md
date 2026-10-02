---
date_created: 2026-08-29 Sat
date_modified: 2026-09-17 Thu
description: Give feedback on an academic paper, thesis chapter, or manuscript draft (LaTeX source, .docx, .pdf, or pasted text) against the CoMMaND lab's writing guidelines — author/funding checklist, formatting and style rules (title case, Oxford commas, acronym usage, equation punctuation, brackets, tables, figure captions and ordering, Latin phrases, number spelling), LaTeX-specific typesetting (one-sentence-per-line, tensor notation, siunitx, autoref, sub/superscripts, biblatex, preamble), and an optional figure-design pass. Use this whenever someone shares a paper draft and asks for feedback, review, proofreading, or a formatting/style check — including requests like "can you review my draft," "check this against our style guide," "does this paper have any formatting issues," or "give feedback on this section" — even if they don't mention "guidelines" explicitly. Also use it when reviewing a paper's accompanying GitHub repository.
name: writing-review
---

## Academic writing feedback

This skill encodes the CoMMaND lab's guidelines for reviewing paper drafts. It produces the kind of feedback a meticulous coauthor would leave in margin comments: terse, specific, and anchored to an exact spot in the document — never vague reassurances or vague warnings.

Not everything in the lab's writing guidelines can actually be checked from the document itself — things like whether the author list is *complete* (not just internally consistent), CRediT contribution assignment, or the Zotero → BibLaTeX export workflow require ground truth or a human decision this skill has no access to. Those live in the lab's [Writing style guide](https://drive.google.com/open?id=1JjN-z04sPDuR-2nwmUV6B3Vk3tdtVNaU4u-D1NsQYBs) as a human checklist instead — mention it exists when relevant, but don't try to check its items yourself.

### Why precision matters here

A comment like "verify the acronyms are all defined" is useless to a writer — they can't act on it without redoing the check themselves. A comment like "the acronym FEA is used in Section 3.2 before being defined; it's first defined in Section 4.1" is something they can fix in five seconds. Every comment this skill produces must be the second kind. If a rule can't be pinned to a quote, a section name, or a figure/equation/table number, do not raise it.

Likewise, silence is a valid outcome. A section with no problems gets no comment and no mention — not even "this section looks good." The final output should read like a punch list, not a review essay.

## Workflow

1. **Figure out what you're looking at.** Get the full source if at all possible — a LaTeX project (all `.tex` files, not just the one the person pasted) gives you far more to check than a PDF export, since several rules (one-sentence-per-line, `\autoref`, `siunitx`, tensor macros, subscript fonts, bibliography backend, preamble) only exist at the source level. If only a PDF or plain text is available, skip the TeX-only checks in `references/tex-rules.md` and say so briefly, rather than silently doing less.
2. **Check for a specific ask first.** If the person has flagged a specific question, section, or concern ("does my intro make the contribution clear?", "can you sanity-check Equation 4?"), address that directly and completely before doing anything else. It leads the response.
3. **Run the author checklist** (below) and the **style and formatting rules** (below) against the whole document. These are the default, always-on checks — do them regardless of whether the person asked for "formatting feedback" specifically, since that's the core purpose of this skill.
4. **If the source is LaTeX**, also apply `references/tex-rules.md`.
5. **If a GitHub repository accompanies the paper**, also apply the `code-review` skill's `references/repo-rules.md`.
6. **Write up the mechanical findings** using the output format below.
7. **Then offer the optional passes** (below) rather than staying silent about them — a short line like "I can also look at argument/structure, clarity, grammar, citations, and figure design if you want — just say so" after the mechanical findings. Only actually run them if asked, or if the person asked for general/full feedback up front (in which case fold them into the same response instead of offering first).

## Rules for all feedback

- Only raise a point if you can point to its exact location: quote the offending text, name the section/subsection, or cite the equation, figure, or table number. If you can't point to a specific instance, don't mention it.
- Never write a comment that just tells the person to go check something themselves ("ensure all acronyms are defined," "verify the tenses are consistent"). Either do the check and report the specific instance, or leave it out.
- Don't mention what's already correct. If a whole category (e.g., Oxford commas, figure ordering) has zero violations, omit that category from the output entirely — don't write "no issues found here."
- Don't close with a summary sentence like "overall the writing is clear" or "the formatting is mostly correct." The list of specific comments is the entire deliverable.
- Check every instance of a repeated pattern individually — every numbered equation, every figure reference, every acronym occurrence, every entry in a list — rather than sampling a few, judging them consistent, and extrapolating to the rest. Authors are reliably inconsistent even when they're mostly right, and "mostly right" is exactly where the exceptions get missed. If working from a low-resolution render (e.g., a PDF page image) makes an instance hard to verify, re-inspect it at higher fidelity instead of treating the uncertainty as a reason to skip it or wave it through.

## Author checklist

Check these regardless of document type:

- **Author list and affiliations — internal consistency only.** You can only verify internal consistency, not ground truth — check that every author listed in the byline has a matching affiliation marker, that affiliation numbers/symbols are used consistently, and that no author appears with a different name spelling elsewhere (e.g., in the acknowledgements or a citation to the authors' own prior work). Whether the list is *complete* or the affiliations are *correct* is a human checklist item (see the Writing style guide linked above) — don't try to verify that, and don't guess.
- **Funding statement.** The acknowledgements section must state funding and include at least one grant/award number. If acknowledgements exist but contain no grant number, or funding is mentioned elsewhere (e.g., a footnote) but not in acknowledgements, flag it with a quote of what's there.
- **Compilation.** If you have the full LaTeX source and a working LaTeX install (or can invoke one), actually try to compile it and report real errors/warnings with the log line that produced them. If you only have a partial source or no compiler available, say so rather than claiming it compiles cleanly.
- **Roman (upright) formatting for abbreviations in math.** In display or inline equations, any subscript, superscript, or standalone symbol that represents an abbreviation or initialism (e.g., a subscript "max" or "eq" meaning "equilibrium") should be upright/roman, not italic math font. Any of `\mathrm{}`, `\rm{}`, `\text{}`, or the lab's `\scas{}` macro satisfies this — none is mandatory, you're only flagging plain math-italic. Quote the specific equation and symbol.
- **Tense.** Use present tense for general truths and established facts, and past tense for what you did or found (e.g., "the sample is heated" is fine as a general description of the method, but "we observed X" — not "we observe X" — for a specific result). Flag a sentence using the wrong tense for what it's describing, or a tense shift within a section with no such reason behind it. Quote the sentence(s).

## Optional passes

Offer these after the mechanical checklist (step 7 above); only run them when asked, or when the person wanted general/full feedback from the start. They're more subjective than the checklist and shouldn't be run reflexively on every draft, but they shouldn't be forgotten either.

- **Argument and structure**: Is the contribution stated clearly? Is the logic sound and well organized? Do the introduction and conclusion actually do their jobs — introduction moving from the general concept to the specific research focus, discussion moving back from the specific findings to the general concept? Are there transitions between sections, and between paragraphs within a section, or does it just jump? Point to the specific paragraph or sentence that is (or should be) doing this work.
- **Clarity and style**: Is the writing concise and precise? Is the tone appropriate for academic work — results and discussion stated with appropriate confidence, not hedging on your own findings? Are there gaps where a subject needed more explanation or introduction before being used? Is every specialized/domain term (not just acronyms) defined on first use? Quote specific sentences that are jargon-heavy, vague, wordy, or under-explained, and say what's unclear about them.
- **Grammar and mechanics**: Flag specific grammatical errors, awkward phrasing, or unclear sentences by quoting them.
- **Citations and evidence**: Are specific claims left unsupported? Quote the claim and note the missing citation, or point out inconsistent citation style (e.g., mixing numeric and author-year within the same document).
- **Figure design**: apply the `figure-review` skill (axis units, no embedded titles, color/layout conventions if matplotlib source is available). Production-workflow items (raw image format, Keynote/Illustrator lettering, reworking figures for slides) aren't checkable at all — they're on the human checklist in the Writing style guide.

## Style and formatting rules

Apply these to the whole document (or all documents, if it's a multi-file LaTeX project). Each rule below should be checked against the actual text — quote the violation when you report it.

1. **Sentence case titles.** Document and section titles should be sentence case (only the first word and proper nouns capitalized), not title case. Quote any title that isn't.
2. **Oxford comma.** Every list of three or more items needs a comma before the final "and"/"or." Quote lists that are missing it.
3. **Acronyms.** Track every acronym through the document:
   - Flag an acronym used before its definition within the same section, or defined twice within the same section without being used in between.
   - It's correct — not an error — for an acronym to be defined once on first use in the abstract and again on first use in the main text; don't flag that as a duplicate definition.
   - Redefinition inside a figure caption is also fine and shouldn't be flagged.
   - If the document uses more than about three non-standard acronyms, suggest cutting some for readability, and list which ones you'd consider cutting. Standard acronyms that don't count toward this: MRI, FEA, DNA, RNA, ASD, CSF.
   - Flag an acronym that's defined but only ever used once afterward — it's not saving anything and should just be spelled out instead.
4. **Display equations.** A display equation is grammatically part of the sentence that contains it — it never starts a new sentence on its own, even when what follows it reads like it could stand alone. A bare equation followed by a participial phrase ("representing X," "where Y is...") is a sentence fragment, not an independent sentence, no matter how complete it feels in isolation — don't be talked out of flagging it by the fact that the equation could be read as a subject.
   Check every display equation in both directions, one at a time — don't sample a few and extrapolate; a paper with correctly-punctuated equations 1–8 can still break at 9, 23, or 27:
   - **Before the equation:** if the text immediately preceding it is already a grammatically complete, independently-punctuated sentence (i.e., it ends in a period), that's a violation — the equation must instead be attached to that sentence with a comma (or no punctuation, if it continues a clause with no pause). This holds even if the equation is followed by something that superficially reads like its own sentence.
   - **After the equation number:** check the case of the very next word. Lowercase continuation (`where`, `with`, `and`, a variable name, etc.) requires the equation to end in a comma. A new sentence or heading (capitalized) requires a period. No punctuation at all, a period before a lowercase continuation, or a comma before a capitalized new sentence — all of these are violations.
   - Quote the equation number, the exact punctuation (or lack of it) immediately before it, and the first few words of what follows, on both sides.
   - When working from a PDF/image rather than source text, a comma, a period, and no punctuation at all can look identical at multi-page-batch render resolution. Re-read each equation's immediate context as its own single-page (or tighter) crop before concluding what the punctuation is — don't wave the check off as "hard to tell from the image" and skip it.
5. **Brackets and parentheses.**
   - Square brackets `[]` should group mathematical expressions; parentheses `()` should hold function arguments. Quote any expression using the wrong one.
   - Flag missing spaces where a parenthetical runs directly into surrounding prose text with no space before `(` or after `)`.
   - Check that citations and reference parentheses are used correctly and consistently.
6. **Tables.** Tables should use booktabs-style rules (no vertical lines, minimal horizontal lines), and units belong in the column or row headers rather than repeated in every cell, wherever that's more compact. Cite the specific table.
7. **Figure captions.**
   - Each caption must open with one sentence describing the figure as a whole before getting into subfigure details.
   - Subfigures should be labeled A, B, C, ... (two subfigures may instead use "left"/"right").
   - In the body text, the finding should come first and the figure citation second — e.g., "...correlates with X (Figure 1)," not "Figure 1 shows that...". Quote any sentence that leads with the figure reference.
8. **Figure ordering.** Figures (and subfigures) must be introduced and referenced in the order they appear. Flag any reference that's out of order, and flag any figure that's never referenced in the text at all.
9. **Latin phrases.** *in vivo*, *in vitro*, *in silico*, *in situ*, and similar Latin phrases must be italicized. Quote any instance that isn't.
10. **Spelling out numbers.** Integers below 10 should be spelled out in prose ("three samples," not "3 samples"). This doesn't apply to numbers with units, percentages, table contents, or numbers inside math. Quote the sentence.
11. **Capitalized cross-references.** `Table`, `Figure`, `Equation`, and `Section` should be capitalized when referring to a specific numbered one in text ("Table 1," not "table 1"). Quote the offending reference.
12. **Overused transitional words.** "However," "furthermore," "thereby," "thus," "also," "additionally," "moreover," and similar transitions are fine individually but shouldn't be leaned on as connective tissue between most sentences in a paragraph. Flag a paragraph where several sentences in a row each open with one.
13. **Long or run-on sentences.** Flag a sentence long enough, or with enough independent clauses strung together, that it's genuinely hard to follow — not every sentence over some fixed length. Quote it and suggest where it could split.
14. **Em dashes.** Flag use of an em dash (—) in prose; the lab prefers a semicolon or splitting into two sentences instead. Quote the sentence.
15. **Inconsistent capitalization.** Beyond title case (rule 1), flag a term capitalized inconsistently across the document (e.g., a named method or material capitalized in some places and lowercase in others with no grammatical reason).
16. **Passive voice and first person.** Flag inconsistent use within a section that should read uniformly — e.g., switching between "we measured" and "the measurement was taken" without reason. Don't flag passive voice or first person on their own; only the inconsistency.
17. **Keywords.** If the venue/template expects a keywords list (e.g., there's a placeholder or a keywords command in the source), flag if it's empty or missing.

## Paper-specific requirements

- An **author contributions statement** must be present somewhere in the document. Flag if missing.
- **Acknowledgements** must include a funding statement with at least one grant number (this duplicates the author-checklist item above — only raise it once, in whichever section of your feedback fits best).

## Output format

Group findings under short headers that match the categories above (e.g., "Author checklist," "Style and formatting," "TeX-specific," "Repository"), and use numbered or bulleted points only within a category — never wrap the whole response in generic bullet fluff. Skip any category with nothing to report. If the person asked a specific question, answer it in its own section at the top, before the checklist findings. Every point should read as: location → quote/reference → what's wrong. For example: "Section 3.1: 'the FEA model was validated' — FEA is used here before its first definition in Section 4.2."

For further detail on rules that only apply to specific situations, see:
- `references/tex-rules.md` — additional rules that only apply when reviewing LaTeX source files directly (not just compiled output), including the preamble check.
- `../code-review/references/repo-rules.md` — additional rules for a paper's accompanying GitHub repository (owned by the `code-review` skill since it applies to any lab repo, not just paper ones).
- `references/preamble.tex` — the lab's canonical LaTeX preamble (packages + macros). Point someone here if they're starting a new manuscript and ask what to include.
