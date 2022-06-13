import os, argparse, time, json
import episcanpy as epi

import pkg_resources
from scmaui.data import load_data
from scmaui.data import SCDataset
from scmaui.utils import init_model_params
from scmaui.ensembles import EnsembleVAE

import pandas as pd
import pickle as pk
from sklearn.metrics import roc_curve, auc
from utils import compute_roc

import tensorflow as tf
from collections import OrderedDict
import scanpy

def get_model_params(dataset, args=None):
    params = init_model_params()

    modalities = dataset.modalities()
    params['input_modality'] = modalities[0]
    params['output_modality'] = modalities[1]

    params.update(dataset.adversarial_config())
    params.update(dataset.conditional_config())
    params.update({'losses': dataset.losses})

    if args is not None:

        nparams = OrderedDict(
          [
            ('nlayers_encoder', args.nlayers_encoder),
            ('nunits_encoder', args.nunits_encoder),
            ('nlayers_decoder', args.nlayers_decoder),
            ('nunits_decoder', args.nunits_decoder),
            ('dropout_input', args.dropout_input),
            ('dropout_encoder', args.dropout_encoder),
            ('dropout_decoder', args.dropout_decoder),
            ('nunits_adversary', args.nunits_adversary),
            ('nlayers_adversary', args.nlayers_adversary),
            ('nlatent', args.nlatent),
            ('kl_weight', args.kl_weight),
            ('nmixcomp', args.nmixcomp),
          ]
        )
        params.update(nparams)

    return params


def set_seed(seed: int):
    """
    Helper function for reproducible behavior to set the seed in ``random``, ``numpy``, ``torch`` and/or ``tf`` (if
    installed).

    Args:
        seed (:obj:`int`): The seed to set.
    """
    tf.random.set_seed(seed)

def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--out_dir", type=str, required=True, help="Directory to save the results")
    parser.add_argument("--nlayers_encoder", type=int, default=32, help="Number of layers for the encoder")
    parser.add_argument("--nunits_encoder", type=int, default=5, help="Number of units for the encoder")
    parser.add_argument("--nunits_decoder", type=int, default=20, help="Number of units for the decoder")
    parser.add_argument("--nlayers_decoder", type=int, default=1, help="Number of layers for the decoder")
    parser.add_argument("--dropout_input", type=float, default=0.1, help="Drop out value for input")
    parser.add_argument("--dropout_encoder", type=float, default=0.0, help="Drop out value for the encoder")
    parser.add_argument("--dropout_decoder", type=float, default=0.0, help="Drop out value for the decoder")
    parser.add_argument("--nunits_adversary", type=int, default=128, help="Number of units for the adversary")
    parser.add_argument("--nlayers_adversary", type=int, default=2, help="Number of layers for the adversary")
    parser.add_argument("--kl_weight", type=float, default=0.0, help="Weight for KL divergence")
    parser.add_argument("--nlatent", type=int, default=10, help="Number of latents")
    parser.add_argument("--nmixcomp", type=int, default=1, help="nmixcomp?")
    parser.add_argument("--epochs", type=int, default=600, help="Number of epochs")

    return parser.parse_args()


args = arg_parser()
set_seed(950410)

adatas = load_data(["../data/GSE194122/gex_small.hdf5", 
                    "../data/GSE194122/atac_small.hdf5"], names=['gex', 'atac'])

scanpy.pp.log1p(adatas["input"][0])
epi.pp.filter_features(adatas["input"][1], min_cells=933)

dataset = SCDataset(adatas, losses=['negbinom', 'negbinom'],
                    union=True, adversarial=["DonorID", "Site"],
                    conditional=['DonorID', "Site"])#


# Create a model
ensemble = EnsembleVAE(params=params, ensemble_size=1)

# Fit the model
train_loss = ensemble.fit(dataset, epochs=args.epochs)

#Save results
model_save_dir = os.path.join(args.out_dir, str(time.time())+"/")
if not os.path.exists(model_save_dir): 
    os.mkdir(model_save_dir)
print(f"Save the result : {model_save_dir}")

ensemble.save(model_save_dir)
with open(os.path.join(model_save_dir,"train_param.txt"), "w") as f_param:
    dict_args = vars(args)
    for key in dict_args:
        f_param.write(key+"\t"+str(dict_args[key])+"\n")

for idx,t in enumerate(train_loss):
    t = pd.DataFrame.from_dict(t.history)
    t.to_csv(os.path.join(model_save_dir, "model_hist_%d.csv"%(idx)))


# Extract latents
latent, latent_list = ensemble.encode(dataset)

with open(model_save_dir+"/latents.pickle", "wb") as fp:
    pk.dump(latent, fp)

with open(model_save_dir+"/latent_list.pickle", "wb") as fp:
    pk.dump(latent_list, fp)

# Cell type prediction
rocs = compute_roc(latent_list[0], adatas["input"][0].obs["cell_type"])
auc_val = auc(rocs["mean"]["FPR"], rocs["mean"]["TPR"])
print(f"mean AUC: {auc_val}")

rocs = pd.concat([rocs[k].assign(cell_type=k) for k in rocs.keys()])
rocs.to_csv(os.path.join(model_save_dir, "roc.csv"))

