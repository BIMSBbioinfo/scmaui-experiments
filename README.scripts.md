## Main workflow: 
This project includes workflows to build _scMaui_ models with different hyperparameters and evaluate those models. Given scripts, you can conduct classification of latents and evaluation of reconstruction. 

 - scmaui_eval.py: Main script to train _scMaui_ model and classify cells (e.g. with respect to _cell_type_)
 - utils.py: Functions for calculating classification AUC

## How to run 

You can start the evaluation by running ```./script/scmaui_eval.py``` code with customised options. 
```bash
python3 ./script/scmaui_eval.py -o ./ --nlatent 100 --kl_weight 0.5 --epochs 300
```

The script has optinal arguments :
```bash
  -h, --help            show this help message and exit
  -o OUT_DIR, --out_dir OUT_DIR
                        Directory to save the results
  --nlayers_encoder NLAYERS_ENCODER
                        Number of layers for the encoder
  --nunits_encoder NUNITS_ENCODER
                        Number of units for the encoder
  --nunits_decoder NUNITS_DECODER
                        Number of units for the decoder
  --nlayers_decoder NLAYERS_DECODER
                        Number of layers for the decoder
  --dropout_input DROPOUT_INPUT
                        Drop out value for input
  --dropout_encoder DROPOUT_ENCODER
                        Drop out value for the encoder
  --dropout_decoder DROPOUT_DECODER
                        Drop out value for the decoder
  --nunits_adversary NUNITS_ADVERSARY
                        Number of units for the adversary
  --nlayers_adversary NLAYERS_ADVERSARY
                        Number of layers for the adversary
  --kl_weight KL_WEIGHT
                        Weight for KL divergence
  --nlatent NLATENT     Number of latents
  --nmixcomp NMIXCOMP   nmixcomp?

```
