import json
import pandas as pd
import torch
import torch.nn as nn

DATA_PATH = 'data/normal_access_logs.csv'
MODEL_PATH = 'model.pth'
ENCODING_PATH = 'encoding.json'
EPOCHS = 10
LR = 0.01
LATENT_DIM = 3

class AutoEncoder(nn.Module):
    def __init__(self, input_dim, latent_dim=LATENT_DIM):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, latent_dim),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, input_dim),
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


def load_data(path):
    df = pd.read_csv(path)
    soldier_vals = sorted(df['soldier_id'].unique())
    purpose_vals = sorted(df['purpose'].unique())
    destination_vals = sorted(df['destination'].unique())
    time_vals = sorted(df['time_slot'].unique())
    enc = {
        'soldier_id': {v: i for i, v in enumerate(soldier_vals)},
        'purpose': {v: i for i, v in enumerate(purpose_vals)},
        'destination': {v: i for i, v in enumerate(destination_vals)},
        'time_slot': {v: i for i, v in enumerate(time_vals)},
    }
    features = []
    for _, row in df.iterrows():
        features.append([
            enc['soldier_id'][row['soldier_id']],
            enc['purpose'][row['purpose']],
            enc['destination'][row['destination']],
            enc['time_slot'][row['time_slot']],
        ])
    tensor = torch.tensor(features, dtype=torch.float32)
    return tensor, enc


def train():
    data, enc = load_data(DATA_PATH)
    input_dim = data.shape[1] + LATENT_DIM
    model = AutoEncoder(input_dim)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    for _ in range(EPOCHS):
        prev = torch.zeros(LATENT_DIM)
        for row in data:
            inp = torch.cat([prev, row])
            optimizer.zero_grad()
            recon = model(inp)
            loss = criterion(recon, inp)
            loss.backward()
            optimizer.step()
            prev = model.encoder(inp).detach()

    with torch.no_grad():
        prev = torch.zeros(LATENT_DIM)
        errors = []
        for row in data:
            inp = torch.cat([prev, row])
            recon = model(inp)
            mse = ((recon - inp) ** 2).mean().item()
            errors.append(mse)
            prev = model.encoder(inp).detach()
        threshold = float(torch.tensor(errors).mean() + torch.tensor(errors).std() * 3)

    torch.save(model.state_dict(), MODEL_PATH)
    enc['threshold'] = threshold
    with open(ENCODING_PATH, 'w') as f:
        json.dump(enc, f, ensure_ascii=False)
    print('model trained, threshold:', threshold)


if __name__ == '__main__':
    train()
