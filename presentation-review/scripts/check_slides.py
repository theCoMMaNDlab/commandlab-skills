#!/usr/bin/env python3
"""Mechanical checks for a presentation exported to PDF (e.g., from Keynote).

Usage:
    python check_slides.py talk.pdf [--minutes 15]

Prints a markdown punch list grouped by category. Every check here is a
*heuristic* on text, font sizes, and vector/raster geometry extracted from the
PDF -- no LLM involved. Findings marked "(check)" are candidates that a person
(or Claude, looking at the rendered slide) must confirm. Judgment calls the
script cannot make (do colors mean something, is a figure legible, are slide
titles claims) are listed at the end so they are not silently skipped.

Requires: pymupdf  (pip install -r requirements.txt, from the repo root)
"""
from __future__ import annotations

import argparse
import colorsys
import re
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Tunable thresholds (all lengths in points on a 540 pt tall slide; sizes are
# rescaled so a 16:9 or 4:3 slide both read as 540 pt tall)
# --------------------------------------------------------------------------
REFERENCE_SLIDE_HEIGHT_PT = 540.0
MIN_FONT_PT = 18.0                # smaller text is hard to read when projected
MAX_WORDS_PER_SLIDE = 40          # excluding title and slide number
MAX_BULLET_WORDS = 15             # longer than this is no longer a fragment
MIN_SENTENCE_WORDS = 6            # shorter "sentences" still read as fragments
PARAGRAPH_WORDS = 30              # this long is a paragraph regardless
LABEL_MAX_WORDS = 3               # at most this many words counts as a label
MAX_FIGURES = 3                   # more pictures than this reads as crammed
LOGO_AREA_FRAC = 0.02             # pictures below this are logos/icons
MIN_FIGURE_TEXT_PT = 14.0         # axis/tick/legend text below this is hard to read
MIN_VECTOR_PATHS = 15             # a cluster of this many paths is a plot/diagram
PLOT_CLUSTER_GAP_PT = 15.0        # vector paths this close belong to one plot
FIGURE_MERGE_GAP_PT = 2.0         # pictures this close (touching) count as one figure
FOOTER_FRAC = 0.93                # text below this fraction of the height is footer
FIGURE_TEXT_MARGIN_PT = 12.0      # text this close to a figure may be its label
FIGURE_LABEL_MAX_WORDS = 8        # longer text or any bullet is body text, not a label
HIDDEN_TEXT_OVERLAP_FRAC = 0.3    # text this covered by other text is hidden
MAX_NUMERIC_TOKEN_FRAC = 0.25     # text this numeric is a tick-label block, not prose
MIN_WORDS_FOR_MULTI_SENTENCE = 12 # shorter text with "Dr." or "vs." is not 2 sentences
MAX_FONT_FAMILIES = 2
EXTRA_SLIDES = 3                  # title + acknowledgements + thank you
NUMBER_ZONE_FRAC = 0.12           # outer band of the slide where a number lives
MIN_DOMINANT_VOTES = 3            # items needed before a "dominant" style exists
MIN_PALETTE_SATURATION = 0.15     # below this a color is treated as neutral
MIN_HUE_SATURATION = 0.35         # red/green tests ignore washed-out colors
MIN_HUE_VALUE = 0.25              # ... and near-black colors
RED_HUE_MAX_DEG = 20.0
RED_HUE_MIN_DEG = 340.0
GREEN_HUE_RANGE_DEG = (75.0, 165.0)
DEGREES_PER_TURN = 360.0
CENTERED_TOL_FRAC = 0.03          # text centred within this of page centre
LINE_GAP_FRAC = 0.6               # gap > this x line height starts a paragraph
BORDER_MAX_AREA_FRAC = 0.6        # larger outlines are slide frames, not boxes
QUOTE_LEN = 60

BULLET_GLYPHS = "•▪●◦‣■□▸►–—-−·"
SMALL_WORDS = {
    "a", "an", "the", "and", "or", "nor", "but", "of", "in", "on", "at", "to",
    "for", "from", "by", "with", "as", "vs", "via", "per", "is", "are",
}
MATH_FONT_HINTS = ("math", "stix", "cmmi", "cmsy", "cmex", "cmr", "symbol")

SLIDE_NUMBER_RE = re.compile(r"^\s*(\d+)(?:\s*(?:/|of)\s*\d+)?\s*$")
NUMERIC_CITE_RE = re.compile(r"\[\d+(?:\s*[,–—-]\s*\d+)*\]")
NUMBERED_ENTRY_RE = re.compile(r"^\s*(?:\[\d+\]|\d+[.)])\s+\S")
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
REF_LIKE_RE = re.compile(r"[A-Z][A-Za-z\-']+.*\b(?:19|20)\d{2}\b")
REF_DETAIL_RE = re.compile(
    r"\b(?:vol\.?|pp?\.|no\.)\s*\d|\d+\s*\(\d+\)\s*[:,]\s*\d+"
    r"|\b\d+\s*[:,]\s*\d+\s*[–-]\s*\d+",
    re.IGNORECASE,
)
CAPTION_RE = re.compile(r"^\s*(?:fig(?:ure)?\.?|panel)\s*\d+\b", re.IGNORECASE)
PANEL_LABEL_RE = re.compile(r"^\(?[A-Ha-h]\)?[.:]?$")
ACK_RE = re.compile(r"acknowledg|thank|questions", re.IGNORECASE)
ACRONYM_RE = re.compile(r"\b[A-Z]{2,}(?:-[A-Z0-9]+)?s?\b")
FUNDING_RE = re.compile(
    r"\b(?:fund(?:ed|ing)|grant|award|support(?:ed)?|sponsor(?:ed)?|NIH|NSF|DOE|NASA|"
    r"DARPA|DoD|NIST|foundation)\b", re.IGNORECASE)
CONCLUSION_RE = re.compile(
    r"conclusion|key points?|findings|future (?:work|directions)|take-?aways?|"
    r"take[- ]home|summary", re.IGNORECASE)
URL_RE = re.compile(r"https?://|www\.|\.(?:com|org|edu)\b")

CATEGORY_ORDER = [
    "Slide numbers", "Length", "Animations", "Capitalization", "Text density",
    "Bullets", "Font size", "Figure text size", "Figures", "Captions and panel labels", "Required slides", "Color", "Boxes", "References", "Acronyms",
    "Consistency", "Suggestions",
]


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------
@dataclass
class Para:
    """One paragraph (or bullet) of text on a slide."""

    text: str
    size_pt: float
    font: str
    color: str
    top_pt: float
    is_bullet: bool
    left_aligned: bool
    bbox: tuple[float, float, float, float]
    is_title: bool = False
    in_figure: bool = False  # sits on or beside a picture/plot (its labels)
    in_footer: bool = False  # in the footer band (citations, date, slide number)
    hidden: bool = False     # mostly covered by other text, so not visible


@dataclass
class Picture:
    """A figure: one raster or a cluster of touching rasters/vector paths."""

    area_frac: float
    bbox: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)


@dataclass
class Slide:
    index: int
    paras: list[Para] = field(default_factory=list)
    pictures: list[Picture] = field(default_factory=list)
    has_number: bool = False
    line_set: set[str] = field(default_factory=set)
    text_colors: set[str] = field(default_factory=set)
    graphic_colors: set[str] = field(default_factory=set)
    outlines: list[tuple[float, float, float, float]] = field(default_factory=list)
    plot_regions: list[tuple[float, float, float, float]] = field(default_factory=list)
    has_math_font: bool = False


@dataclass
class Finding:
    category: str
    slide: int | None
    message: str


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------
def quote(text: str, limit: int = QUOTE_LEN) -> str:
    """Return a short, quoted excerpt of ``text`` for use in a finding."""
    text = " ".join(text.split())
    return f'"{text[:limit]}{"…" if len(text) > limit else ""}"'


def word_count(text: str) -> int:
    return len(text.split())


def hex_from_int(rgb: int) -> str:
    return f"#{rgb:06X}"


def hex_from_floats(rgb: tuple[float, ...]) -> str:
    r, g, b = (round(c * 255) for c in rgb[:3])
    return f"#{r:02X}{g:02X}{b:02X}"


def hue_class(hex_color: str) -> str | None:
    """Return 'red' or 'green' for clearly red/green colors, else None."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hue, sat, val = colorsys.rgb_to_hsv(r, g, b)
    if sat < MIN_HUE_SATURATION or val < MIN_HUE_VALUE:
        return None
    deg = hue * DEGREES_PER_TURN
    if deg <= RED_HUE_MAX_DEG or deg >= RED_HUE_MIN_DEG:
        return "red"
    if GREEN_HUE_RANGE_DEG[0] <= deg <= GREEN_HUE_RANGE_DEG[1]:
        return "green"
    return None


def is_neutral(hex_color: str) -> bool:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hsv(r, g, b)[1] < MIN_PALETTE_SATURATION


def font_family(name: str) -> str:
    """Strip style suffixes ('Calibri-Bold' -> 'Calibri')."""
    return re.split(r"[-,]", name)[0].replace("MT", "").replace("PS", "").strip()


def looks_like_reference(text: str) -> bool:
    return bool(REF_LIKE_RE.search(text)) and bool(YEAR_RE.search(text))


# --------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------
Rect4 = tuple[float, float, float, float]


def _near(a: Rect4, b: Rect4, gap: float) -> bool:
    return not (a[2] + gap < b[0] or b[2] + gap < a[0]
                or a[3] + gap < b[1] or b[3] + gap < a[1])


def cluster_rects(rects: list[Rect4], gap: float) -> list[tuple[Rect4, int]]:
    """Merge rectangles that overlap or lie within ``gap``; return (bbox, count).

    Union-find over x-sorted rectangles so a page with a few hundred vector paths
    stays fast.
    """
    order = sorted(range(len(rects)), key=lambda i: rects[i][0])
    parent = list(range(len(rects)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for pos, i in enumerate(order):
        for j in order[pos + 1:]:
            if rects[j][0] > rects[i][2] + gap:
                break
            if _near(rects[i], rects[j], gap):
                parent[find(i)] = find(j)
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(rects)):
        groups[find(i)].append(i)
    out = []
    for members in groups.values():
        box = (min(rects[i][0] for i in members), min(rects[i][1] for i in members),
               max(rects[i][2] for i in members), max(rects[i][3] for i in members))
        out.append((box, len(members)))
    return out


def overlap_frac(inner: Rect4, outer: Rect4) -> float:
    """Fraction of ``inner``'s area that lies inside ``outer``."""
    w = min(inner[2], outer[2]) - max(inner[0], outer[0])
    h = min(inner[3], outer[3]) - max(inner[1], outer[1])
    area = (inner[2] - inner[0]) * (inner[3] - inner[1])
    return max(w, 0) * max(h, 0) / area if area > 0 else 0.0


# --------------------------------------------------------------------------
# PDF extraction
# --------------------------------------------------------------------------
def load_slides(path: Path) -> list[Slide]:
    """Parse the PDF into Slide objects (one per page)."""
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # older pymupdf releases
        except ImportError:
            sys.exit("ERROR: pymupdf is not installed. Run: pip install -r requirements.txt (from the repo root)")

    doc = pymupdf.open(path)
    if doc.page_count == 0:
        sys.exit(f"ERROR: {path} has no pages.")
    return [_parse_page(page, number) for number, page in enumerate(doc, start=1)]


def _parse_page(page, index: int) -> Slide:
    scale = REFERENCE_SLIDE_HEIGHT_PT / page.rect.height
    width, height = page.rect.width, page.rect.height
    slide = Slide(index=index)

    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        current: list[dict] = []
        prev_bbox = None
        for line in block["lines"]:
            spans = [s for s in line["spans"] if s["text"].strip()]
            if not spans:
                continue
            text = "".join(s["text"] for s in line["spans"]).strip()
            x0, y0, x1, y1 = line["bbox"]
            in_zone = (y0 < height * NUMBER_ZONE_FRAC
                       or y1 > height * (1 - NUMBER_ZONE_FRAC))
            match = SLIDE_NUMBER_RE.match(text)
            if in_zone and match:  # a slide number: record and exclude from text
                slide.has_number |= int(match.group(1)) == index
                continue
            for s in spans:
                slide.has_math_font |= any(h in s["font"].lower() for h in MATH_FONT_HINTS)
            starts_bullet = text[0] in BULLET_GLYPHS and (len(text) == 1 or text[1] == " ")
            gap_break = (prev_bbox is not None
                         and y0 - prev_bbox[3] > LINE_GAP_FRAC * (prev_bbox[3] - prev_bbox[1]))
            ended = bool(current) and current[-1]["text"].rstrip()[-1:] in ".:!?"
            if not current or starts_bullet or gap_break or ended:
                if current:
                    slide.paras.append(_make_para(current, width, scale))
                current = []
            current.append({"text": text, "bbox": line["bbox"], "spans": spans,
                            "bullet": starts_bullet})
            prev_bbox = line["bbox"]
        if current:
            slide.paras.append(_make_para(current, width, scale))

    # Title = largest text in the top part of the slide.
    top_candidates = [p for p in slide.paras if p.top_pt < REFERENCE_SLIDE_HEIGHT_PT * 0.35]
    if top_candidates:
        max(top_candidates, key=lambda p: p.size_pt).is_title = True

    for p in slide.paras:
        slide.text_colors.add(p.color)
    slide.line_set = {" ".join(p.text.split()) for p in slide.paras}

    page_area = width * height
    unit = 1 / scale  # page units per reference point
    raster_boxes = [tuple(info["bbox"]) for info in page.get_image_info()]
    vector_boxes: list[Rect4] = []
    for drawing in page.get_drawings():
        for key in ("fill", "color"):
            value = drawing.get(key)
            if value and len(value) >= 3:
                slide.graphic_colors.add(hex_from_floats(value))
        rect = tuple(drawing["rect"])
        rect_area = (rect[2] - rect[0]) * (rect[3] - rect[1])
        is_template = (rect[2] - rect[0] > 0.9 * width or rect[1] > FOOTER_FRAC * height
                       or rect_area > 0.5 * page_area)  # footer bar, backgrounds
        if not is_template:
            vector_boxes.append(rect)
        stroked = drawing.get("color") is not None and drawing.get("width", 0) > 0
        if stroked and not is_template and rect_area < BORDER_MAX_AREA_FRAC * page_area:
            slide.outlines.append(rect)

    # Vector plots/diagrams: dense clusters of paths. Rasters are figures already.
    clusters = cluster_rects(vector_boxes, PLOT_CLUSTER_GAP_PT * unit)
    slide.plot_regions = [box for box, n in clusters if n >= MIN_VECTOR_PATHS]
    figure_parts = raster_boxes + slide.plot_regions
    for box, _ in cluster_rects(figure_parts, FIGURE_MERGE_GAP_PT * unit):
        frac = (box[2] - box[0]) * (box[3] - box[1]) / page_area
        if frac >= LOGO_AREA_FRAC:
            slide.pictures.append(Picture(frac, box))

    margin = FIGURE_TEXT_MARGIN_PT * unit
    for p in slide.paras:
        p.in_footer = p.bbox[1] > FOOTER_FRAC * height
        p.hidden = any(overlap_frac(p.bbox, o.bbox) > HIDDEN_TEXT_OVERLAP_FRAC
                       for o in slide.paras if o is not p)
        if p.is_title:
            continue
        cx, cy = (p.bbox[0] + p.bbox[2]) / 2, (p.bbox[1] + p.bbox[3]) / 2
        p.in_figure = (not p.is_bullet and word_count(p.text) <= FIGURE_LABEL_MAX_WORDS
                       and any(b[0] - margin <= cx <= b[2] + margin
                          and b[1] - margin <= cy <= b[3] + margin
                          for b in figure_parts))
    slide.text_colors.discard("#FFFFFF")
    slide.graphic_colors.discard("#FFFFFF")
    return slide


def _make_para(lines: list[dict], page_width: float, scale: float) -> Para:
    spans = [s for ln in lines for s in ln["spans"]]
    text = " ".join(ln["text"] for ln in lines)
    is_bullet = lines[0]["bullet"]
    if is_bullet:
        text = text[1:].strip()
    x0 = min(ln["bbox"][0] for ln in lines)
    y0 = min(ln["bbox"][1] for ln in lines)
    x1 = max(ln["bbox"][2] for ln in lines)
    y1 = max(ln["bbox"][3] for ln in lines)
    centre_offset = abs((x0 + x1) / 2 - page_width / 2) / page_width
    # Representative size/font = the one covering the most characters, so a
    # small superscript or one large first letter does not skew the result.
    chars_by_style: Counter = Counter()
    for sp in spans:
        chars_by_style[(round(sp["size"], 1), sp["font"])] += len(sp["text"].strip())
    (size, font), _ = chars_by_style.most_common(1)[0]
    return Para(
        text=text,
        size_pt=round(size * scale, 1),
        font=font_family(font),
        color=hex_from_int(spans[0]["color"]),
        top_pt=y0 * scale,
        is_bullet=is_bullet,
        left_aligned=centre_offset > CENTERED_TOL_FRAC,
        bbox=(x0, y0, x1, y1),
    )


# --------------------------------------------------------------------------
# Capitalization classification
# --------------------------------------------------------------------------
def cap_styles(text: str) -> set[str]:
    """Return the set of capitalization styles ``text`` is consistent with.

    Styles: 'title case', 'sentence case', 'lowercase'. An empty set means the
    text fits none of them ('mixed'). Acronyms and words containing digits or
    internal capitals (FEA, mRNA, 3D) are ignored; so are small words (the, of)
    when judging title case.
    """
    tokens = [re.sub(r"^\W+|\W+$", "", t) for t in text.split()]
    tokens = [t for t in tokens if re.search(r"[A-Za-z]", t)]
    if not tokens:
        return set()

    def neutral(tok: str) -> bool:
        return bool(re.search(r"\d", tok)) or any(c.isupper() for c in tok[1:])

    content = [t for t in tokens if t.lower() not in SMALL_WORDS and not neutral(t)]
    if not content:
        return {"title case", "sentence case", "lowercase"}
    first_upper = tokens[0][0].isupper()
    styles = set()
    if all(t[0].isupper() for t in content) and first_upper:
        styles.add("title case")
    rest = [t for t in content if t is not tokens[0]]
    if first_upper and all(t[0].islower() for t in rest):
        styles.add("sentence case")
    if all(t[0].islower() for t in tokens if not neutral(t)):
        styles.add("lowercase")
    return styles


def is_numeric_block(text: str) -> bool:
    """True for axis tick runs like 'gyrification index [-] 1.0 2.0 3.0'."""
    tokens = text.split()
    numeric = sum(bool(re.fullmatch(r"[-+]?\d[\d.]*(?:[eE]\d+)?[^\w]*", t)) for t in tokens)
    return bool(tokens) and numeric / len(tokens) > MAX_NUMERIC_TOKEN_FRAC


def is_acronym_expansion(text: str, slide_text: str) -> bool:
    """True if a run of capitalized words spells an acronym used on the slide.

    "Irritable Bowel Syndrome" next to "IBS-D" is capitalized because it expands
    the acronym, so it is not a capitalization error.
    """
    acronyms = {part for tok in ACRONYM_RE.findall(slide_text) for part in tok.split("-")}
    words = [w for w in re.split(r"[\s-]+", text) if w[:1].isalpha()]
    for i in range(len(words)):
        for j in range(i + 2, len(words) + 1):
            window = words[i:j]
            if all(w[0].isupper() for w in window) and "".join(w[0] for w in window) in acronyms:
                return True
    return False


def midtext_capitals(text: str) -> list[str]:
    """Capitalized words after the first word (excluding acronyms and small words).

    The script cannot tell a proper noun ("Minnesota") from a stray capital
    ("Model"), so findings name these words and the reviewer decides.
    """
    tokens = [re.sub(r"^\W+|\W+$", "", t) for t in text.split()]
    tokens = [t for t in tokens if re.search(r"[A-Za-z]", t)]
    return [t for t in tokens[1:]
            if t[0].isupper() and not any(c.isupper() for c in t[1:])
            and not re.search(r"\d", t) and t.lower() not in SMALL_WORDS]


def role_of(p: Para) -> str:
    """title / figure label / label (<= 3 words, not a bullet) / body (bullets and prose)."""
    if p.is_title:
        return "title"
    if p.in_figure:
        return "figure label"
    if p.is_bullet or word_count(p.text) > LABEL_MAX_WORDS:
        return "body"
    return "label"


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
def check_slide_numbers(slides: list[Slide]) -> list[Finding]:
    missing = [s.index for s in slides if not s.has_number]
    if not missing:
        return []
    if len(missing) == len(slides):
        return [Finding("Slide numbers", None,
                        "No slide numbers detected on any slide. (If numbers are "
                        "present but drawn as images, confirm on the render.)")]
    return [Finding("Slide numbers", i, "No slide number detected.") for i in missing]


def check_length(slides: list[Slide], minutes: int | None) -> list[Finding]:
    if minutes is None:
        return [Finding("Length", None,
                        "Talk length not given; length check skipped. Ask for the minutes.")]
    n = len(slides)
    ceiling = minutes + EXTRA_SLIDES
    if n > ceiling:
        return [Finding("Length", None,
                        f"{n} slides for a {minutes}-minute talk; about {minutes} plus 2–3 "
                        f"(title, acknowledgements, thank you) is the target, so {ceiling} is "
                        f"the ceiling. Counts build slides, since each build is exported.")]
    return []


def detect_builds(slides: list[Slide]) -> int:
    """Count consecutive slide pairs where the second only adds to the first."""
    builds = 0
    for a, b in zip(slides, slides[1:]):
        if len(a.line_set) >= 2 and a.line_set < b.line_set:
            builds += 1
    return builds


def check_animations(slides: list[Slide]) -> list[Finding]:
    if detect_builds(slides) == 0:
        return [Finding("Animations", None,
                        "No builds detected (no slide is a strict subset of the next). "
                        "Builds would help on dense slides; if the talk does use builds, "
                        "re-export from Keynote with each stage of builds printed as its own page.")]
    return []


def check_capitalization(slides: list[Slide]) -> list[Finding]:
    """Flag text whose capitalization departs from the deck's norm for its role.

    Roles (title / text / label / figure label) are compared separately. Proper
    nouns and acronym expansions are legitimate capitals, so every finding is a
    candidate to confirm, never an automatic error. The title slide's name and
    affiliation block is skipped.
    """
    findings: list[Finding] = []
    by_role: dict[str, list[tuple[int, Para, set[str]]]] = defaultdict(list)
    for s in slides:
        for p in s.paras:
            if (p.in_footer or p.hidden or looks_like_reference(p.text)
                    or URL_RE.search(p.text) or is_numeric_block(p.text)
                    or (s.index == 1 and not p.is_title)):
                continue
            styles = cap_styles(p.text)
            if is_acronym_expansion(p.text, " ".join(q.text for q in s.paras)):
                continue
            if styles or re.search(r"[A-Za-z]", p.text):
                by_role[role_of(p)].append((s.index, p, styles))

    for role, items in by_role.items():
        votes = Counter(next(iter(st)) for _, _, st in items if len(st) == 1)
        if sum(votes.values()) < MIN_DOMINANT_VOTES:
            continue
        dominant, _ = votes.most_common(1)[0]
        for index, para, styles in items:
            if dominant in styles:
                continue
            found = " or ".join(sorted(styles)) if styles else "no consistent case"
            caps = midtext_capitals(para.text)
            named = f" Capitalized mid-text: {', '.join(caps)}; decide if each is a proper noun." if caps else ""
            findings.append(Finding(
                "Capitalization", index,
                f"{role} {quote(para.text)} reads as {found}; the deck's usual {role} "
                f"style is {dominant}.{named}"))
    return findings


def check_density(slides: list[Slide]) -> list[Finding]:
    findings: list[Finding] = []
    for s in slides:
        body = [p for p in s.paras if not p.is_title and not p.in_figure and not p.in_footer]
        total = sum(word_count(p.text) for p in body)
        if total > MAX_WORDS_PER_SLIDE:
            findings.append(Finding("Text density", s.index,
                                    f"{total} words of body text (limit ~{MAX_WORDS_PER_SLIDE})."))
        for p in body:
            if (p.hidden or looks_like_reference(p.text) or URL_RE.search(p.text)
                    or (s.index == 1)):
                continue
            words = word_count(p.text)
            sentences = len([x for x in re.split(r"(?<=[.!?])\s+", p.text.strip()) if x])
            multi = sentences >= 2 and words >= MIN_WORDS_FOR_MULTI_SENTENCE
            if multi or words >= PARAGRAPH_WORDS:
                findings.append(Finding("Text density", s.index,
                                        f"paragraph ({words} words): {quote(p.text)}"))
            elif p.text.rstrip().endswith(".") and words >= MIN_SENTENCE_WORDS:
                findings.append(Finding("Text density", s.index,
                                        f"full sentence, use a fragment: {quote(p.text)}"))
            elif words > MAX_BULLET_WORDS:
                findings.append(Finding("Text density", s.index,
                                        f"long bullet ({words} words): {quote(p.text)}"))
    return findings


def check_bullets(slides: list[Slide]) -> list[Finding]:
    findings = []
    for s in slides:
        for p in s.paras:
            if (not p.is_title and not p.in_figure and not p.in_footer and not p.is_bullet
                    and p.left_aligned
                    and word_count(p.text) > LABEL_MAX_WORDS
                    and not looks_like_reference(p.text) and not URL_RE.search(p.text)):
                findings.append(Finding(
                    "Bullets", s.index,
                    f"left-aligned text without a bullet: {quote(p.text)} (check: "
                    f"captions and bullets drawn as images can cause false hits)."))
    return findings


def check_captions(slides: list[Slide]) -> list[Finding]:
    """Slides should have no figure captions and no A/B/C panel letters."""
    findings = []
    for s in slides:
        for p in s.paras:
            if p.hidden:  # text drawn underneath other text is not visible
                continue
            if CAPTION_RE.match(p.text):
                findings.append(Finding("Captions and panel labels", s.index,
                                        f"figure caption, remove: {quote(p.text)}"))
            elif PANEL_LABEL_RE.match(p.text.strip()):
                findings.append(Finding("Captions and panel labels", s.index,
                                        f"panel letter {quote(p.text)}, remove "
                                        f"(papers use A/B/C, slides don't)."))
    return findings


def check_required_slides(slides: list[Slide]) -> list[Finding]:
    """Deck needs an acknowledgements/thank-you slide and a conclusion slide.

    Funding may be shown only as logos on the thank-you slide, which this script
    cannot read, so it never judges funding content; it only looks for the slide.
    """
    findings = []
    has_ack = any(ACK_RE.search(p.text) for s in slides for p in s.paras
                  if p.is_title or word_count(p.text) <= 4)
    if not has_ack:
        findings.append(Finding("Required slides", None,
                                "No acknowledgements or thank-you slide found by title "
                                "(check the render: it may be image-only)."))
    if not any(CONCLUSION_RE.search(p.text) for s in slides for p in s.paras if p.is_title):
        findings.append(Finding("Required slides", None,
                                "No conclusion/key points/findings/future directions/"
                                "takeaways slide found by title."))
    return findings


def check_acronyms(slides: list[Slide]) -> list[Finding]:
    """Report the distinct acronyms (all-caps tokens) rather than judging each."""
    seen: dict[str, list[int]] = defaultdict(list)
    for s in slides:
        for p in s.paras:
            if looks_like_reference(p.text):
                continue
            for token in ACRONYM_RE.findall(p.text):
                if s.index not in seen[token]:
                    seen[token].append(s.index)
    if not seen:
        return []
    listing = ", ".join(f"{a} ({'/'.join(map(str, v[:3]))}{'…' if len(v) > 3 else ''})"
                        for a, v in sorted(seen.items()))
    return [Finding("Acronyms", None,
                    f"{len(seen)} distinct acronyms; remind the speaker to define each on "
                    f"the slide or aloud: {listing}")]


def check_font_size(slides: list[Slide]) -> list[Finding]:
    """Body text under MIN_FONT_PT individually; figure labels summarized per slide."""
    findings = []
    for s in slides:
        small = [p for p in s.paras if not looks_like_reference(p.text) and not p.in_footer]
        for p in small:
            if not p.in_figure and p.size_pt < MIN_FONT_PT:
                findings.append(Finding("Font size", s.index,
                                        f"{p.size_pt:g} pt (< {MIN_FONT_PT:g}): {quote(p.text)}"))
        fig_small = [p for p in small if p.in_figure and p.size_pt < MIN_FIGURE_TEXT_PT]
        if fig_small:
            worst = min(fig_small, key=lambda p: p.size_pt)
            findings.append(Finding(
                "Figure text size", s.index,
                f"{len(fig_small)} figure labels under {MIN_FIGURE_TEXT_PT:g} pt, smallest "
                f"{worst.size_pt:g} pt ({quote(worst.text, 30)}); check legibility on the render."))
    return findings


def check_figures(slides: list[Slide]) -> list[Finding]:
    """Flag slides with many separate figures (touching pieces count as one)."""
    return [Finding("Figures", s.index,
                    f"{len(s.pictures)} separate figures/images (limit {MAX_FIGURES}).")
            for s in slides if len(s.pictures) > MAX_FIGURES]


def check_colors(slides: list[Slide]) -> list[Finding]:
    findings = []
    for s in slides:
        colors = s.text_colors | s.graphic_colors
        classes = {c: hue_class(c) for c in colors}
        reds = sorted(c for c, k in classes.items() if k == "red")
        greens = sorted(c for c, k in classes.items() if k == "green")
        if reds and greens:
            findings.append(Finding("Color", s.index,
                                    f"red ({', '.join(reds)}) and green ({', '.join(greens)}) "
                                    f"both used; not colorblind-safe."))
        elif reds or greens:
            kind, used = ("red", reds) if reds else ("green", greens)
            findings.append(Finding("Color", s.index,
                                    f"{kind} used ({', '.join(used)}); only OK for bad/stop or "
                                    f"good/go meanings, and then with a non-color cue (✗/✓)."))
    return findings


def check_boxes(slides: list[Slide]) -> list[Finding]:
    findings = []
    for s in slides:
        for (bx0, by0, bx1, by1) in s.outlines:
            centre = ((bx0 + bx1) / 2, (by0 + by1) / 2)
            if any(r[0] <= centre[0] <= r[2] and r[1] <= centre[1] <= r[3]
                   for r in s.plot_regions):
                continue  # frame of a vector plot, not a text box
            inside = [p for p in s.paras if not p.is_title
                      and p.bbox[0] >= bx0 - 1 and p.bbox[2] <= bx1 + 1
                      and p.bbox[1] >= by0 - 1 and p.bbox[3] <= by1 + 1
                      and word_count(p.text) >= 2 and re.search(r"[A-Za-z]{3}", p.text)]
            if inside:
                findings.append(Finding(
                    "Boxes", s.index,
                    f"outlined box around {quote(inside[0].text)}; prefer a colored fill "
                    f"with no border (check: plot frames can cause false hits)."))
    return findings


def check_references(slides: list[Slide]) -> list[Finding]:
    findings = []
    for s in slides:
        texts = [p.text for p in s.paras]
        if any(NUMERIC_CITE_RE.search(t) for t in texts) and not any(
                NUMBERED_ENTRY_RE.match(t) and YEAR_RE.search(t) for t in texts):
            cite = next(t for t in texts if NUMERIC_CITE_RE.search(t))
            findings.append(Finding("References", s.index,
                                    f"numeric citation in {quote(cite)} but no full reference "
                                    f"entry on this slide."))
        for t in texts:
            if REF_DETAIL_RE.search(t):
                findings.append(Finding("References", s.index,
                                        f"reference has more than author, year, journal "
                                        f"(volume/pages): {quote(t)}"))
    return findings


def check_consistency(slides: list[Slide]) -> list[Finding]:
    findings = []
    sizes = Counter(p.font for s in slides for p in s.paras)
    if len(sizes) > MAX_FONT_FAMILIES:
        findings.append(Finding("Consistency", None,
                                f"{len(sizes)} font families used: "
                                + ", ".join(f"{f} ({n})" for f, n in sizes.most_common())))
    title_sizes = [p.size_pt for s in slides[1:-1] for p in s.paras if p.is_title]
    if len(title_sizes) >= MIN_DOMINANT_VOTES:
        mode = statistics.mode(title_sizes)
        for s in slides[1:-1]:
            for p in s.paras:
                if p.is_title and abs(p.size_pt - mode) > 1:
                    findings.append(Finding("Consistency", s.index,
                                            f"title is {p.size_pt:g} pt; most titles are {mode:g} pt."))
    return findings


def check_suggestions(slides: list[Slide]) -> list[Finding]:
    findings = []
    for s in slides:
        if s.has_math_font:
            findings.append(Finding(
                "Suggestions", s.index,
                "math fonts present; if this slide has an equation, consider under-brackets "
                "labeling each term (confirm on the render)."))
    return findings


def palette_table(slides: list[Slide]) -> str:
    """Markdown table of non-neutral colors and the slides they appear on."""
    usage: dict[str, list[int]] = defaultdict(list)
    for s in slides:
        for c in sorted(s.text_colors | s.graphic_colors):
            if not is_neutral(c):
                usage[c].append(s.index)
    if not usage:
        return ""
    rows = ["| color | hue | slides |", "|---|---|---|"]
    for color, idx in sorted(usage.items(), key=lambda kv: -len(kv[1])):
        rows.append(f"| {color} | {hue_class(color) or ''} | {', '.join(map(str, idx))} |")
    return "\n".join(rows)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
NOT_CHECKED = [
    "Whether each color carries a consistent meaning across slides (use the palette table).",
    "Whether figures are legible at projection size (axis labels, ticks, legends, line weights).",
    "Text/background contrast.",
    "Whether plots are crammed into one image (a multi-panel figure is a single image).",
    "Whether slide titles are claims rather than topics; alignment and margins.",
    "Panel letters (A, B, C) and captions baked into images; only live text is seen here.",
    "Whether raster equations, numeric superscript citations, or image-drawn numbers exist.",
]


def render(findings: list[Finding], slides: list[Slide]) -> str:
    out = [f"# Mechanical slide checks ({len(slides)} slides)\n"]
    for category in CATEGORY_ORDER:
        items = sorted((f for f in findings if f.category == category),
                       key=lambda f: (f.slide or 0))
        if not items:
            continue
        out.append(f"## {category}")
        for f in items:
            where = f"Slide {f.slide}" if f.slide else "Deck"
            out.append(f"- {where}: {f.message}")
        out.append("")
    palette = palette_table(slides)
    if palette:
        out += ["## Palette (for judging color meaning)", palette, ""]
    out += ["## Not checked by this script (needs a look at the rendered slides)"]
    out += [f"- {item}" for item in NOT_CHECKED]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdf", type=Path, help="presentation exported to PDF")
    parser.add_argument("--minutes", type=int, default=None,
                        help="intended talk length in minutes")
    args = parser.parse_args()

    if args.pdf.suffix.lower() != ".pdf":
        sys.exit(f"ERROR: expected a .pdf, got {args.pdf.suffix!r}. In Keynote use "
                 "File > Export To > PDF, with each stage of builds printed.")
    if not args.pdf.is_file():
        sys.exit(f"ERROR: file not found: {args.pdf}")

    slides = load_slides(args.pdf)
    findings: list[Finding] = []
    findings += check_slide_numbers(slides)
    findings += check_length(slides, args.minutes)
    findings += check_animations(slides)
    findings += check_capitalization(slides)
    findings += check_density(slides)
    findings += check_bullets(slides)
    findings += check_font_size(slides)
    findings += check_figures(slides)
    findings += check_captions(slides)
    findings += check_required_slides(slides)
    findings += check_acronyms(slides)
    findings += check_colors(slides)
    findings += check_boxes(slides)
    findings += check_references(slides)
    findings += check_consistency(slides)
    findings += check_suggestions(slides)
    print(render(findings, slides))


if __name__ == "__main__":
    main()
