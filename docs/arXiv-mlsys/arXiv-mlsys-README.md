# arXiv Paper in MLSys Style

Uses template for LaTeX source to produce a PDF paper in MLSys style.
<https://mlsys.org/Conferences/2026/CallForResearchPapers>

Required packages to be included in the `tex-source` folder:
```text
algorithm.sty
algorithmic.sty
fancyhdr.sty
minted-cache # folder
minted.sty
mlsys2025.bst
mlsys2025.sty
```

Sources in the `tex-source` folder:
```text
paper_template.tex # main file
reference.bib # bibliography
sections # folder with all the sections
figures # folder with all the figures
```

Run command to produce the PDF:
```text
rm -rf build pub && \
mkdir -p pub build && \
TEXINPUTS=tex-source: pdflatex -output-directory=build tex-source/paper_template.tex && \
BIBINPUTS=tex-source: BSTINPUTS=tex-source: openout_any=a bibtex build/paper_template && \
TEXINPUTS=tex-source: pdflatex -output-directory=build tex-source/paper_template.tex && \
TEXINPUTS=tex-source: pdflatex -output-directory=build tex-source/paper_template.tex && \
cp build/paper_template.pdf pub/llm-sql-ggra.pdf && \
rm -rf build
```
or, run `make pdf`.
