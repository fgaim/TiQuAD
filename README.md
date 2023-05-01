# TiQuAD: Tigrinya Question Answering Dataset

## Paper

This repository contains datasets and models that accompany the paper [Question-Answering in a Low-resourced Language: Benchmark Dataset and Models for Tigrinya](https://aclanthology.org/2023.acl-long.661/) published at the ACL 2023 conference.

## Overview

TiQuAD is the first manually annotated Question-Answering (QA) dataset for the Tigrinya language.
The dataset contains over 10.6K annotations (6.5K unique questions) across 572 paragraphs extracted from 290 news articles of various genres.
TiQuAD follows the Machine Reading Comprehension formulation of the SQuAD where each question is answered by text span that is marked in the corresponding paragraph.
The paper presents the details of the dataset construction process with qualitative analysis and extensive experiments with monolingual and multilingual Transformer-based language models.
In addition to the native dataset, a machine-translated version of the SQuAD v1.1 is used as training data.
The two datasets are made available for research purposes.

## Datasets

The datasets will soon be made available on HuggingFace Datasets.

## Models

The models will soon be made available on HuggingFace Hub.

## Results

```text
                                                            ╭───────────────────┬─────────────────╮
╭────┬─────────────────┬───────────────────┬────────┬───────┤    TiQuAD Dev     │  TiQuAD Test    │
│    │ Dataset         │ Model             │ Epochs │ Batch │   EM    │   F1    │  EM    │  F1    │
├────┼─────────────────┼───────────────────┼────────┼───────┼─────────┼─────────┼────────┼────────┤
│  1 │ MT              │ tielectra-small   │      3 │    16 │   38.54 │   46.04 │  39.25 │  48.36 │
│  2 │ MT              │ tiroberta-base    │      3 │    16 │   48.5  │   56.39 │  48.17 │  58.81 │
│  3 │ MT              │ afriberta_base    │      3 │    16 │   40.36 │   48.72 │  40.68 │  52.96 │
│  4 │ MT              │ xlm-roberta-base  │      3 │    16 │   51.71 │   59.64 │  53.17 │  62.61 │
│  5 │ MT              │ xlm-roberta-large │      3 │    16 │   59.85 │   67.06 │  61.55 │  70.85 │
│  6 │ Native          │ tielectra-small   │      5 │     8 │   36.19 │   43.06 │  28.81 │  37    │
│  7 │ Native          │ tiroberta-base    │      5 │     8 │   56.21 │   64.36 │  53.08 │  61.82 │
│  8 │ Native          │ afriberta_base    │      5 │     8 │   38.01 │   44.85 │  35.06 │  44.24 │
│  9 │ Native          │ xlm-roberta-base  │      5 │     8 │   56.53 │   65.37 │  55.75 │  65.49 │
│ 10 │ Native          │ xlm-roberta-large │      5 │     8 │   63.17 │   71.32 │  64.94 │  72.62 │
│ 11 │ MT+Native       │ tielectra-small   │      3 │    16 │   46.36 │   53.6  │  47.46 │  56.64 │
│ 12 │ MT+Native       │ tiroberta-base    │      3 │    16 │   62.42 │   70.12 │  62.18 │  70.42 │
│ 13 │ MT+Native       │ afriberta_base    │      3 │    16 │   52.68 │   59.38 │  47.37 │  58.35 │
│ 14 │ MT+Native       │ xlm-roberta-base  │      3 │    16 │   61.99 │   70.44 │  64.76 │  73.53 │
│ 15 │ MT+Native       │ xlm-roberta-large │      3 │    16 │   70.88 │   77.96 │  74.67 │  82.31 │
│ 16 │ SQuAD           │ tielectra-small   │      3 │    16 │    9.85 │   20.91 │   9.81 │  20.41 │
│ 17 │ SQuAD           │ tiroberta-base    │      3 │    16 │   10.71 │   20.88 │  10.88 │  20.69 │
│ 18 │ SQuAD           │ afriberta_base    │      3 │    16 │   20.24 │   32.05 │  20.52 │  32.95 │
│ 19 │ SQuAD           │ xlm-roberta-base  │      3 │    16 │   17.99 │   27.81 │  22.66 │  34.44 │
│ 20 │ SQuAD           │ xlm-roberta-large │      3 │    16 │   29.12 │   40.26 │  34.7  │  43.96 │
│ 21 │ SQuAD+MT        │ tielectra-small   │      3 │    16 │   37.69 │   46.06 │  39.07 │  49.07 │
│ 22 │ SQuAD+MT        │ tiroberta-base    │      3 │    16 │   51.28 │   59.25 │  51.12 │  60.75 │
│ 23 │ SQuAD+MT        │ afriberta_base    │      3 │    16 │   44.33 │   51.43 │  45.58 │  56.36 │
│ 24 │ SQuAD+MT        │ xlm-roberta-base  │      3 │    16 │   52.89 │   61.06 │  57.36 │  66.37 │
│ 25 │ SQuAD+MT        │ xlm-roberta-large │      3 │    16 │   61.03 │   67.75 │  61.91 │  71.05 │
│ 26 │ SQuAD+Native    │ tielectra-small   │      3 │    16 │   33.73 │   41.51 │  32.74 │  40.53 │
│ 27 │ SQuAD+Native    │ tiroberta-base    │      3 │    16 │   57.07 │   65.75 │  59.05 │  67.3  │
│ 28 │ SQuAD+Native    │ afriberta_base    │      3 │    16 │   51.93 │   59.66 │  51.38 │  62.13 │
│ 29 │ SQuAD+Native    │ xlm-roberta-base  │      3 │    16 │   62.42 │   69.95 │  63.07 │  71.76 │
│ 30 │ SQuAD+Native    │ xlm-roberta-large │      3 │    16 │   67.24 │   76.19 │  71.54 │  78.39 │
│ 31 │ SQuAD+MT+Native │ tielectra-small   │      3 │    16 │   45.72 │   53.4  │  47.73 │  57.1  │
│ 32 │ SQuAD+MT+Native │ tiroberta-base    │      3 │    16 │   65.2  │   71.88 │  62.53 │  71.08 │
│ 33 │ SQuAD+MT+Native │ afriberta_base    │      3 │    16 │   51.93 │   59.47 │  53.26 │  63.22 │
│ 34 │ SQuAD+MT+Native │ xlm-roberta-base  │      3 │    16 │   64.78 │   72.8  │  68.06 │  76.58 │
│ 35 │ SQuAD+MT+Native │ xlm-roberta-large │      3 │    16 │   72.59 │   79.66 │  74.13 │  81.39 │
╰────┴─────────────────┴───────────────────┴────────┴───────┴─────────┴─────────┴────────┴────────╯

MT: Machine Translated train set SQuAD v1.1 -- Tigrinya
Native: TiQuAD train set -- Tigrinya
SQuAD: SQuAD v1.1 train set -- English
```

## Citation

This work can be cited as follows:

*Plain*

> Fitsum Gaim, Wonsuk Yang, Hancheol Park, and Jong Park. 2023. Question-Answering in a Low-resourced Language: Benchmark Dataset and Models for Tigrinya. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 11857–11870, Toronto, Canada. Association for Computational Linguistics.

*BibTex*

```bibtex
@inproceedings{gaim-etal-2023-tiquad,
    title = "Question-Answering in a Low-resourced Language: Benchmark Dataset and Models for {T}igrinya",
    author = "Fitsum Gaim and Wonsuk Yang and Hancheol Park and Jong C. Park",
    booktitle = "Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.acl-long.661",
    pages = "11857--11870",
}
```

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://licensebuttons.net/l/by-sa/4.0/88x31.png" /></a>
