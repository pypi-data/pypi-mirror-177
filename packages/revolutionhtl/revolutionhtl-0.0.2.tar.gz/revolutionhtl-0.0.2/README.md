# ![REvolutionH-tl logo.](docs/images/Logo_horizontal.png)

Bioinformatics tool the reconstruction of evolutionaty histories. Input: best-match data, Output: event labeled gene trees and reconciliations.

- José Antonio Ramírez-Rafael [jose.ramirezra@cinvestav.mx]
- Maribel Hernandez-Rosales [maribel.hr@cinvestav.mx ]

[Bioinformatics & complex networks lab](https://ira.cinvestav.mx/ingenieriagenetica/dra-maribel-hernandez-rosales/bioinformatica-y-redes-complejas/)

****

REvolutionHtl analyzes putative best matches for the inference of event-labeled gene trees. Moreover, the tool performs tree reconciliation if a species tree is provided.

If you don't have best-match data, you can use proteinortho and the `revolutionhtl.parse_prt` module.

# Install

`pip install --upgrade revolutionhtl` 

**Dependencies**

- pandas
- networkx
- os
- itertools
- argparse
- numpy
- tqdm


# Usage

The pipeline is divided into 5 modules:

0. From proteinortho to putative best matches: [revolutionhtl.parse_prt](docs/parse_prt.md)
1. From best match graph to event-labeled gene tree: [revolutionhtl.is_cBMG](docs/is_cBMG.md)
2. Convert drigraph to BMG:
3. Reconciliation of gene and species trees:
4. Visualization:
