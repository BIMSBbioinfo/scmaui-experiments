from scmaui.data import load_data
from scmaui.data import SCDataset
from scmaui.utils import init_model_params
from scmaui.ensembles import EnsembleVAE
import os, glob, pickle, h5py, scanpy
import numpy as np
def get_model_params(dataset, args=None):
    params = init_model_params()

    modalities = dataset.modalities()
    params['input_modality'] = modalities[0]
    params['output_modality'] = modalities[1]

    params.update(dataset.adversarial_config())
    params.update(dataset.conditional_config())
    params.update({'losses': dataset.losses})

    if args is not None:

        params = OrderedDict(
          [
            ('nlayers_encoder', args.nlayers_encoder),
            ('nunits_encoder', args.nunits_encoder),
            ('nlayers_decoder', args.nlayers_decoder),
            ('nunits_decoder', args.nunits_decoder),
            ('dropout_input', args.dropout_input),
            ('dropout_encoder', args.dropout_encoder),
            ('dropout_decoder', args.dropout_decoder),
            ('nunits_adversary', args.nunits_adversary),
            ('nlayers_adversary', 2),
            ('nlatent', args.nlatent),
            #('losses', args.loss),
            ('nmixcomp', args.nmixcomp),
          ]
        )
        params.update(nparams)

    return params

HOME_DIR = "/omics/groups/OE0219/internal/Yunhee/"
RES_DIR = os.path.join(HOME_DIR, "scmaui/practice/GSE194122_analysis/res/scmaui/", "data_norm_mse_gex" + "/")

#adatas = load_data(["/omics/groups/OE0219/internal/Yunhee/GSE194122_express_ATAC/gex_small.hdf5", 
#                    "/omics/groups/OE0219/internal/Yunhee/GSE194122_express_ATAC/atac_small.hdf5"], names=['gex', 'atac'])
adatas = load_data(["/omics/groups/OE0219/internal/Yunhee/scmaui/practice/GSE194122_analysis/data/gex_train.hdf5", 
                    "/omics/groups/OE0219/internal/Yunhee/scmaui/practice/GSE194122_analysis/data/atac_train.hdf5"], names=['gex', 'atac'])

scanpy.pp.log1p(adatas["input"][0])

dataset = SCDataset(adatas, losses=['mse', 'negbinom'],
                    union=True, adversarial=["DonorID", "Site"],
                    conditional=['DonorID', "Site"])#

dataset = dataset.sample(1000)
params = get_model_params(dataset)


# Create a model
ensemble = EnsembleVAE(params=params, ensemble_size=1)
res_dirs = glob.glob(RES_DIR+"/*")

for res_dir in res_dirs:
  #res_dir = os.path.join(RES_DIR+"/1652967465.9564958/")

  f_h5 = os.path.join(res_dir+"/", "imputed.h5")
  if os.path.exists(f_h5):
    print(f"{f_h5} already exists. Remove the file.")
    os.remove(f_h5)

  ensemble.load(res_dir)
  imputed_res = ensemble.impute(dataset)
  print(imputed_res[0])

  hf = h5py.File(f_h5, "w")

  for idx, imputed in enumerate(imputed_res):
    hf.create_dataset(str(params['input_modality'][idx])+"_impute", data=imputed)  

  for idx,x in enumerate(dataset.adata["input"]):
    hf.create_dataset(str(params['input_modality'][idx])+"_gt", data=x.X.toarray())     
  hf.close()
  del imputed_res
