## Goals: 
**scmaui-experiments** aims to evaluate [scMaui](https://github.com/BIMSBbioinfo/scmaui) compared to other single-cell multiomics data integration tools. 
This project also invloves the piplines for handling single-cell multiomics data processing and scrripts for plotting. 

## Current status:
We finished the baseline of scmaui hyperparmeter scan code 
and sucessfully ran it with single-cell gene expression (scGEX) and single-cell ATAC-seq (scATAC) data,
in order to test different sets of hyperparameters.

Four different experiments regarding batch effects have been conducted (no batch effect handling, covariates, adversary, both covariates and adversary). 

Scripts for plotting are provided as jupyter notebook.

## Roles: 
- **Yunhee Jeong**: Impements main codes, scripts and pipelines and conducts analyses. 
- **Jona Ronen**: Guides the direction of analyses as a main contributior of scmaui. 
- **Akalin Atuna**: Manages the project and organises major meetings as a supervisor. 

## Presentations & reports: 
- **Initial meeting (Jan/2022):** Initial meeting about brief description of scmaui ([Slides](https://drive.google.com/file/d/1qP_DQVUcoWM_iiejtUtvTp3BYQkXJG8I/view?usp=sharing)).
- **Project plan (May/2022):** Goal of this project and detailed plans about how to evaluate scmaui. Primary analysis results ([Slides](https://docs.google.com/presentation/d/1vMv_Z-gt0Gls-DlLjIuuG_0KzYh2SrGqdOZG4erJFBU/edit?usp=sharing)). 

## Experiments & failed ideas: 
TODO!! (https://docs.google.com/presentation/d/1vMv_Z-gt0Gls-DlLjIuuG_0KzYh2SrGqdOZG4erJFBU/edit?usp=sharing)

## Draft paper: 
Coming soon!

## Prerequisite reading:  
- scMaui is a single-cell version of Maui with a reinforced way of handling single-cell data: [Maui homepage](https://maui.readthedocs.io/en/latest/)
- Maui code is available on github: [Maui Github](https://github.com/BIMSBbioinfo/maui)
- Adversory batch effects extraction is based on this paper: 
  [Ganin et al. "Unsupervised domain adaptation by backpropagation." International conference on machine learning. PMLR, 2015.](https://arxiv.org/abs/1409.7495)
- Main evaluation data for the project can be found here (scGEX, scATAC and scADT): [Open Problems in Single-Cell analysis](https://openproblems.bio/neurips_docs/data/dataset/)


## Prerequisite skills:
This project code is based on python deep learning library [Tensorflow](https://www.tensorflow.org/tutorials) and [Tensorflow-Keras](https://keras.io/about/).
All functions for training and testing are from [scMaui](https://github.com/BIMSBbioinfo/scmaui).
Multi-omics data is provided as a [AnnData](https://anndata.readthedocs.io/en/latest/) object.
