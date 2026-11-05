# Repository cleanup — 2026-11-04

The cleanup treats the repository as a research record. It removes files with
no research content or a clear cache/build role, without reorganizing research
paths or rewriting computations. It does not certify mathematical correctness.

## Removed

148 files (about 2.3 MB, including ignored/untracked debris):

| Category | Files | Reason |
| --- | ---: | --- |
| Operating-system metadata | 21 | `.DS_Store` and Windows `:Zone.Identifier` sidecars. |
| Python bytecode | 10 | Cached `.pyc` files; corresponding Python source exists. |
| LaTeX bookkeeping | 30 | Auxiliary files, logs, navigation, synchronization, and build state. Sources, PDFs, styles, figures, and `.bbl` files remain. |
| Manim caches | 79 | Generated text/TeX render assets and partial movie segments. Animation code and all complete videos remain. |
| Empty or identical checkpoints | 3 | Two byte-identical notebook backups and an empty `Untitled` checkpoint. |
| Empty placeholders | 5 | The files listed below had no source cells, outputs, attachments, or text to preserve. |

Empty placeholders removed:

- `qMA.ipynb`
- `equivChow/equivChow.ipynb`
- `qpolys/charpoly-whitney-nbc.ipynb`
- `qpolys/conjsntests/cytoscape-playground/t.ipynb`
- `qpolys/topic-codedump.txt`

No literal references to the removed filenames or paths were found in the
retained source, notebook cells, or text records examined before deletion.
This is a static check, not an execution of every historical workflow.

## Deliberately preserved

- All substantive notebooks, including differing `copy` and `temp` versions,
  and their saved outputs.
- `qpolys/conjsntests/.ipynb_checkpoints/lattice_ux2-checkpoint.ipynb`: this
  tracked checkpoint differs from the main notebook and records an earlier
  visualization. It remains tracked despite the ignore rule for new checkpoints.
- Duplicate datasets and helper modules used through local paths/imports.
- All `.sage.py` files. In particular, `qpolys/db1.sage.py`,
  `nonequiv/UM_characters_decomposition.sage.py`, and
  `nonequiv/uniformMatroid_script.sage.py` have no matching `.sage` source here.
- All PDFs, figures, complete animations, HTML visualizations, references,
  bibliographies, and local TeX styles.
- Existing notebook and bibliography edits, the untracked `poster/DFIKLM`
  source/PDF/bibliography, `poster/text.txt`, and the ignored `dump/` experiment.
- Empty `core.py`: a Python module can be an import target even without content.

## Existing reproducibility gaps

- `equivChow/main.tex` requests `bibliography.bib`, which is absent from that
  directory. Its `main.bbl` and PDF were retained.
- `poster/CFT.pdf` and `useful-info-n-fns/template.pdf` have no matching TeX
  sources here; both PDFs were retained.
- `nonequiv/uniform_streamer.py` and `nonequiv/continuousStream.py` call missing
  `.sage` files. Their generated `.sage.py` counterparts remain available.
- `FMSV/cp-braid-streamer.py` calls `braidMatroid_script.sage`, which is not in
  its own directory. No attempt was made to change historical computations.

## Credential cleanup

The hard-coded API key in `qpolys/deepseekchat.ipynb` was replaced with an
environment-variable lookup. Its conjectures and saved research discussion
were retained. The old key may still exist in Git history and should be revoked
or rotated with its provider; this cleanup does not rewrite history.
