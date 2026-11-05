# Chow rings of matroids — research record

Computations, conjectures, notes, and visualizations concerning Chow rings of
matroids, equivariant representations, and Kazhdan–Lusztig and inverse
Kazhdan–Lusztig polynomials. This is a working research archive: exploratory
notebooks and saved results are part of the record, and their presence does not
mean their conclusions have been proved or their code works for every input.

## Finding the research

| Area | Contents and starting points |
| --- | --- |
| [FMSV](FMSV/) | Implementations and experiments around the FMSV paper: `thm1-1.ipynb`, `thm1-2.ipynb`, `thm1-4.ipynb`, equivariant Orlik–Solomon computations, and `mainScripts/`. See also [the paper](references/fmsv24.pdf). |
| [Non-equivariant computations](nonequiv/) | Chow polynomials, Feichtner–Yuzvinsky monomials, braid/uniform matroid computations, character decompositions, and saved data. Start with `fy-monomials_Braid.ipynb` or `FMSV_implementation.ipynb`. |
| [Equivariant Chow rings](equivChow/) | [Written notes](equivChow/main.pdf), their [source](equivChow/main.tex), thagomizer computations, and experiments in `res/`, including deletion formulas. `lean-codes/` contains an early formalization experiment. |
| [Q-polynomials](qpolys/) | Inverse Kazhdan–Lusztig/Q-polynomial work. `db1.py` and `db2.py` supply helpers; `invkl.ipynb`, `invklferroni.ipynb`, and `uniformQs.ipynb` are useful entry points. |
| [Conjectures and tests](qpolys/conjsntests/) | Deletion and parallel-connection experiments, computed examples, and lattice visualizations. `skel.tex`/`skel.pdf` contain written material; `defMobAlg.ipynb/` is a directory containing quantum Möbius algebra experiments. |
| [Reusable calculations](usefulCodes/) | Group actions on edges and flats, fixed points, permutation representations, and induction. |
| [Notes and worked examples](useful-info-n-fns/) | Theorem notes, bibliographies, and braid-matroid examples, with notebooks, TeX sources, and PDFs. |
| [Data](data/) | Matroid records, character tables, computed dimensions/decompositions, and timings. The [data description](data/readme.md) explains the fields. |
| [Posters](poster/) | Poster sources, bibliographies, local styles, and PDF snapshots. |
| [References](references/) | Research papers used by the computations and notes. |
| [Graph visualizations](frontends/) | Graph JSON exports, a generator notebook, and supporting matroid functions. Interactive renderers also live in `qpolys/conjsntests/cytoscape-playground/`. |
| [Animations](manimpg/) | Manim source in `HAModule.py` and complete rendered videos under `media/videos/`. A second animation lives in the Cytoscape playground. |
| [Exploratory writing](playtime/) | Additional mathematical TeX notes and PDF snapshots. |

## Working with the archive

- Most mathematical notebooks need a **SageMath kernel**. Syntax such as `R.<t>`
  and objects such as `matroids` are not ordinary Python. Other notebooks have
  additional imports, including NumPy, pandas, NetworkX, and ipycytoscape.
- Start notebooks and scripts from their own directories when they use relative
  paths. Copies of data and helper modules in different directories are retained
  because local imports and file loading depend on them.
- Keep saved notebook outputs: they record computations that may be expensive
  to repeat. Names such as `test`, `temp`, and `copy` do not imply empty or
  interchangeable content.
- `.sage.py` files are retained, including versions whose `.sage` originals are
  missing. PDFs, standalone HTML exports, figures, final videos, and `.bbl`
  bibliographies are also retained as readable snapshots.
- Compile TeX from the document's directory with its bibliography and local
  styles available. Some historical sources or dependencies are missing; see
  [cleanup notes](docs/cleanup.md) before assuming an old result can be rebuilt.
- The AI-assisted conjecture discussion in `qpolys/deepseekchat.ipynb` is an
  exploratory record, not a verified proof. To run its API call, set
  `NVIDIA_API_KEY` in the environment used by the notebook kernel.
- `dump/` remains an ignored local experiment directory. Its local data,
  machine-learning plan, and environment were preserved; they are not included
  in a fresh clone.
