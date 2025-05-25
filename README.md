# Military Access Control

This repository contains a simple prototype for training an autoencoder on normal access logs and a GUI program to detect anomalous gate access. Each access record is evaluated together with the previous latent representation so that unusual sequences can be detected.

## Training the Model

Run the training script to learn an autoencoder from the sample dataset in `data/normal_access_logs.csv` (the dataset is written in Korean and soldier IDs follow `24-76xxxxxx` or `23-67xxxxxx`):

```bash
python train_autoencoder.py
```

This will produce `model.pth` and `encoding.json` that store the trained weights and encoding mappings.

## Running the GUI

After training, start the GUI to evaluate new access requests:

```bash
python access_control_gui.py
```

The GUI allows input of soldier ID and selection of purpose, destination, and time slot. It reports whether the entry is considered normal or anomalous based on the reconstruction error.
The program keeps the previous latent state so consecutive accesses can influence anomaly detection.
