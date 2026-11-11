# Optional: rendered web page with a "copy LaTeX" button

Only build this when the user asks for a page (the default is the compiled PDF; see SKILL.md).
Browser MathJax cannot reproduce the lab macros exactly (`\boldmath`, `\sffamily`), so the page is a close preview; the compiled PDF is the exact version.

## Page setup

- Load MathJax 3 SVG from cdnjs: `https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-svg.js` (SVG follows the text colour, so light and dark themes both work).
  The Artifact CSP blocks external stylesheets, so do not use KaTeX CSS.
- Define the macros for MathJax only (the page *source* shown to the user keeps the lab macros):

```javascript
window.MathJax = {
  tex: {
    macros: {
      ten: ["\\boldsymbol{#1}", 1],
      tenf: ["\\boldsymbol{\\mathsf{#1}}", 1],
      scas: ["{\\scriptstyle\\mathrm{#1}}", 1],
      tens: ["{\\scriptstyle\\boldsymbol{#1}}", 1],
      sca: ["\\mathrm{#1}", 1],
      mat: ["\\mathbf{#1}", 1],
    },
  },
};
```

- Write the equations on the page in the lab macros (so what is displayed is what is copied).
- Use `\( ... \)` inline and `\[ \begin{align} ... \end{align} \]` for display; wrap each display block in a container with `overflow-x: auto` so long equations scroll on a phone.
- Add a **"Copy LaTeX (lab macros)"** button per derivation (and one for the whole page) that copies the original source text with `navigator.clipboard.writeText`, falling back to a hidden `<textarea>` and `document.execCommand("copy")` if the clipboard API is blocked.
  Keep the source in a `<script type="text/plain">` block so it is not typeset.
- Load the `artifact-design` skill before writing the page.
