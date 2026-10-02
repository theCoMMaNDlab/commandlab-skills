---
date_created: 2026-10-02 Fri
date_modified: 2026-10-02 Fri
description: Give feedback on a slide presentation (conference talk, group meeting, thesis defense, seminar) exported to PDF against the CoMMaND lab's slide guidelines — slide numbers, required acknowledgements (with funding) and conclusion slides, consistent capitalization, meaningful and colorblind-safe color, no figure captions or A/B/C panel letters, text density (fragments not sentences), few large figures, reference format, talk length versus slide count, builds, font size, and borderless callout boxes. Runs a bundled script for the mechanical checks, then looks at the rendered slides for the visual ones. Use this whenever someone shares slides or a Keynote/PowerPoint/PDF deck and asks for feedback, a review, or a check before a talk, including requests like "can you look over my talk," "are my slides too busy," or "review my defense slides."
name: presentation-review
---

## Presentation feedback

This skill encodes the CoMMaND lab's guidelines for reviewing slide decks. Like `writing-review`, it produces a punch list of terse, specific comments, each anchored to a slide number and a quote or element, never vague advice. Silence is a valid outcome: don't mention what's already fine, and don't close with a summary sentence.

Two kinds of checks, done in this order:

1. **Mechanical checks** run by `scripts/check_slides.py` on the PDF. These need no judgment; the script reports slide, quote, and what's wrong.
2. **Visual checks** done by looking at the rendered slides, for the things a script can't see (color meaning, figure legibility, contrast).

### Why PDF

The lab uses Keynote, and a `.key` file can't be read directly. PDF gives text, font sizes, and geometry for the script, and renders to images for the visual pass. Ask for the export to be made like this: **File > Export To > PDF**, and in the options **turn on printing each stage of builds** (the exact label may vary by Keynote version). That makes every build its own page, which the length and animation checks depend on. If they send a `.pptx` or `.key`, ask them to export to PDF rather than guessing.

## Workflow

1. **Get the PDF and the talk length.** Ask for the intended length in **minutes** if it wasn't given. The length check can't run without it.
2. **Check for a specific ask first** ("is my intro too long?", "does slide 12 work?") and answer it first and completely.
3. **Run the script.** It needs `pymupdf` (`pip install -r requirements.txt` from the repo root, ideally in a venv):
   ```bash
   python <skill-dir>/scripts/check_slides.py talk.pdf --minutes 15
   ```
   If `pymupdf` isn't installed, say so and either install it (ask first) or skip to step 4 and state that the mechanical checks were done by eye instead.
4. **Render and look.** Convert pages to images (`pdftoppm -r 80 -png talk.pdf slide`) and view them. View every slide, not a sample. Use this for the visual checks below and to confirm or dismiss each script finding marked "(check)".
5. **Write up** using the output format below.
6. **Offer the optional passes** (below) in one line.

What the script does and doesn't see:
- Figure regions are detected (raster images plus dense clusters of vector paths), and text in or beside them is treated as figure labels. Small figure labels are summarized per slide ("Figure text size") instead of listed one by one; body text under 18 pt is listed individually.
- Text hidden underneath other text is ignored. So are footer-band citations (the dark bar at the bottom: they're still checked for reference format) and the title slide's name and affiliation block (names and institutions are proper nouns).
- **Panel letters and captions baked into an image are invisible to it**, since they aren't live text. Look for them on the render of every slide with a multi-part figure; the script only catches letters and captions that are real text.
- Capitalization findings are candidates: the script names the mid-text capitalized words, and you decide which are proper nouns.

Treat script output as a first draft. Drop a finding you looked at and found to be a false hit (a proper noun flagged as inconsistent capitalization, a plot frame flagged as a text box). Never pass along a "(check)" item you haven't confirmed.

## Rules for all feedback

- Only raise a point you can pin to a slide number and a quote or element. Report slide numbers as they appear on the slide, which with every build exported is the PDF page number.
- Never tell the person to go check something themselves; do the check and report the instance.
- Check every slide individually. Authors are consistent on most slides and slip on a few.
- Say why when it isn't obvious (for example, "red/green isn't colorblind-safe"), in a clause, not a paragraph.

## Guidelines

### Slide numbers
Every slide must have a visible slide number. This is a hard requirement: flag every slide missing one, including the title slide.

### Length
- Target is about **one slide per minute**, plus 2–3 extra (title, acknowledgements, thank you/questions). More than minutes + 3 gets flagged.
- Judge by the **last slide number**, not the number of distinct slides, since each build is its own page.
- **Animations:** if the deck has no builds (no page is the previous page plus something new), say builds would help on dense slides, or ask whether the PDF was exported with each stage of builds. Don't assume they weren't used.

### Capitalization
- **Consistency is the only rule.** Title case, sentence case, and lowercase are all acceptable for titles, body text, and labels; the deck just has to pick one per element type and keep it. Short labels (axis labels, legends, callouts) are fine with no caps at all.
- The worst offenders are random capitalization ("Trump Types," "Like This Randomly") and capitalizing every noun, as in German.
- This differs from `writing-review`, which wants sentence case for paper titles; slides don't follow that rule.
- Also check capitalization of the same term across slides ("Finite Element" on one slide, "finite element" on another).
- **Respect proper nouns and acronyms, but actually decide.** Capitals from a proper noun (a person, place, organization, brand, or named method: "Minnesota," "Gaussian") or from the spelled-out form of an acronym ("Irritable Bowel Syndrome" next to "IBS-D") are correct; don't flag them. The script can't tell these apart from stray capitals, so it names each mid-text capitalized word in its finding. For every one, ask whether it really is a proper noun. If it isn't ("Model," "Results"), flag it; never assume a lone capital is a proper noun just because it is lone.

### Text density
- Body text should be **sentence fragments** as bullets, never full sentences, and definitely never a paragraph.
- Left-aligned text should be bullets; free-standing text should be a short label. Centered titles and labels are exceptions.
- A bullet longer than about 15 words is no longer a fragment.
- Roughly 40 words of body text is the upper end for one slide.

### Figures
- A few (at most about three), **large**, easy-to-read images per slide. Flag a slide with a grid of small plots crammed together, even if it is a single composite image.
- Axis labels, tick labels, and legends must be readable at projection size, and axes need units.
- Flag text laid over a busy image or plot.
- **No figure captions.** The slide title and the talk carry the message; flag any "Figure 1: ..." style caption. A short source credit on a figure taken from someone else's work is fine and required; that is a citation, not a caption.
- **No A, B, C panel letters.** Those are for papers. Flag letters on subfigures; refer to panels by position or by what they show instead.

### Required slides
- **Acknowledgements and funding** are always needed, but they can live on the thank you/questions slide, and logos and photos are enough (no text or grant number required). Flag only if there is no acknowledgements or thank-you slide at all, or if none shows any funder. The script can't read logos, so look at the render before flagging.
- A **conclusion slide** is always needed, whatever it's called: conclusions, key points, findings, future directions, or takeaways. Flag it if missing.
- The title, acknowledgements, and thank you/questions slides are the 2–3 extras allowed on top of one slide per minute.

### Color
- **Color must mean something**, and mean the same thing on every slide. If blue is "healthy tissue" on slide 5, it is not "model prediction" on slide 9. Use the script's palette table to compare slides.
- **Avoid red/green**: not colorblind-safe, and strongly coded as good/go versus bad/stop. Use it only for those meanings, and even then pair it with a non-color cue (✗ versus ✓). Suggest an alternative palette when flagging.
- Check contrast (light gray on white, text on a colored fill).

### Boxes
Don't box text just because it's there. If something needs to stand out, prefer a **colored fill with no border line**. Flag outlined text boxes.

### References
- Author–year is usually enough ("Smith 2019"), optionally with a journal abbreviation, and maybe a DOI. Nothing beyond that (no volume, pages, or full author list).
- **Numeric citations** ([1], [2]) must have the full reference on the same slide, not on a final reference slide.

### Equations
When a slide has an equation, suggest **under-brackets** that label each term, if the terms aren't already explained. This is a suggestion, not a violation. Only raise it for a specific equation on a specific slide.

### Other
- **Font size:** body text under about 18 pt gets flagged.
- **Consistency across slides:** fonts (more than two families), title size and position, bullet style, and symbols or notation for the same quantity.
- **Alignment:** titles that jump around between slides, misaligned elements.
- **Contrast** and **text over images** (see above).
- **Claim titles:** a title that states a claim ("Stiffness Drops 40% After Cycling") beats a topic ("Results"), but it isn't always possible. Only suggest a rewording when you have a specific, better title to offer ("reword to: ..."). If a title is just a topic that can't sensibly be a claim, say nothing.
- **Outline or roadmap slides** are optional. Fine if present; never flag their absence.
- **Acronyms:** don't flag undefined acronyms one by one, since speakers often define them aloud. Report the count and list of distinct acronyms (the script gives this), and remind the speaker to define each on the slide or verbally. Many acronyms (roughly more than ten) is worth saying plainly.
- **Backup slides** after the final slide are optional. Don't flag their absence.

## Optional passes

Offer after the checklist; run only if asked or if they wanted full feedback up front.

- **Flow and story:** does the talk go from motivation to aims, methods, results, and takeaway (an outline slide is not required)? Do the slide order and transitions make sense? Cite specific slides.
- **Speaker view:** where timing is likely to be tight, based on the density of slides relative to the minutes available.
- **Figure design:** apply the `figure-review` skill if plotting source code is available.

## Output format

Group under short headers matching the categories above (Slide numbers, Length, Capitalization, Text density, Figures, Color, References, and so on) and skip empty ones. A specific question from the person goes in its own section at the top. Every point reads as slide → quote or element → what's wrong, for example:

> Slide 7: "Results Were Significantly Higher In The Treated Group" is title case, but the other bullet text in the deck is sentence case.

Put the length verdict at the top of its section as a number: "42 slides for a 30-minute talk; 33 is the ceiling."

The script's own output is a starting point, not the deliverable: rewrite it into this format after confirming each item.
