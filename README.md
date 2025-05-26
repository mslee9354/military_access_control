# Military Access Control

This repository contains a simple prototype for training an autoencoder on normal access logs and a GUI program to detect anomalous gate access. Each access record is evaluated together with the previous latent representation so that unusual sequences can be detected.

## Training the Model

Run the training script to learn an autoencoder from the sample dataset in `data/normal_access_logs.csv` (written in Korean). The file contains 1000 realistic access records and all soldier IDs follow the pattern `24-76xxxxxx` or `23-67xxxxxx`.
If you want to recreate the dataset you can execute `generate_data.py` which will build a new random set of 1000 records.

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

## Building the C++ GUI

For environments where Python is not desired you can compile a small Qt based GUI written in C++ using libtorch. The source is located under `cpp/access_control_gui.cpp`.
Make sure you have Qt and libtorch installed and then build with a command similar to:

```bash
g++ cpp/access_control_gui.cpp -o access_gui `pkg-config --cflags --libs Qt5Widgets` \
    -I/path/to/libtorch/include -I/path/to/libtorch/include/torch/csrc/api/include \
    -L/path/to/libtorch/lib -ltorch -lc10 -Wl,-rpath,/path/to/libtorch/lib
```

Place the resulting executable next to `model.pth` and `encoding.json` so it can load the trained network.
