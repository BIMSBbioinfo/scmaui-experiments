 
## TODO List

- [x] Batch effect
	- [x]  Without batch effect handling
	- [x]  Covariates
	- [x]  Adversory
	- [x]  Both
	- [x]  Include Site in the batch effect handling


- [x]  	Reconstruction loss
	- [x]  Bigger decoder model

- [x]  Data Preprocessing
	- [x] Log1p transformation for GEX
	
- [ ] Scheduler 
   - [ ] Learning rate 
   - [ ] KL loss
   - [ ] Adversary

- [ ] Benchmarking with other methods
   - [ ] Conventional methods (e.g. PCA + SVM)
   - [ ] Seurat
   - [ ] scMOFA
   - [ ] scvi

- [ ] New dataset 
   - [x] Internal ATAC + GEX 
   - [ ] 10xGenome

- [ ] Single modality does not work...
	- [ ] 	Try single modality with other dataset

- [ ] Encoder joint loss
	- [ ] compare results without encoder joint loss  	

- [ ] 	Imputation 
	- [ ] Separate evaluations (missing / non-missing / non-NaN value)	
	- [ ] Create better plots
	- [ ] Previous work investigation 
		- [ ] MOFA
		- [ ] Open Problems winners 	
