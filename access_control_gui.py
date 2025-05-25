import json
import torch
import tkinter as tk
from tkinter import messagebox

MODEL_PATH = 'model.pth'
ENCODING_PATH = 'encoding.json'
LATENT_DIM = 3

class AutoEncoder(torch.nn.Module):
    def __init__(self, input_dim, latent_dim=3):
        super().__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(input_dim, latent_dim),
            torch.nn.ReLU(),
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(latent_dim, input_dim),
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

def load_model_and_enc():
    with open(ENCODING_PATH, 'r') as f:
        enc = json.load(f)
    input_dim = 4 + LATENT_DIM
    model = AutoEncoder(input_dim)
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()
    return model, enc

class App:
    def __init__(self, root, model, enc):
        self.model = model
        self.enc = enc
        self.prev = torch.zeros(LATENT_DIM)
        self.root = root
        root.title('Access Control')
        tk.Label(root, text='Soldier ID').grid(row=0, column=0)
        self.sid_var = tk.Entry(root)
        self.sid_var.grid(row=0, column=1)
        tk.Label(root, text='Purpose').grid(row=1, column=0)
        self.purpose_var = tk.StringVar(root)
        self.purpose_var.set(list(enc['purpose'].keys())[0])
        tk.OptionMenu(root, self.purpose_var, *enc['purpose'].keys()).grid(row=1, column=1)
        tk.Label(root, text='Destination').grid(row=2, column=0)
        self.dest_var = tk.StringVar(root)
        self.dest_var.set(list(enc['destination'].keys())[0])
        tk.OptionMenu(root, self.dest_var, *enc['destination'].keys()).grid(row=2, column=1)
        tk.Label(root, text='Time Slot').grid(row=3, column=0)
        self.time_var = tk.StringVar(root)
        self.time_var.set(list(enc['time_slot'].keys())[0])
        tk.OptionMenu(root, self.time_var, *enc['time_slot'].keys()).grid(row=3, column=1)
        tk.Button(root, text='Check Access', command=self.check).grid(row=4, column=0, columnspan=2)

    def check(self):
        sid_str = self.sid_var.get().strip()
        if sid_str not in self.enc['soldier_id']:
            messagebox.showerror('Error', 'Invalid Soldier ID')
            return
        sid = self.enc['soldier_id'][sid_str]
        purpose = self.enc['purpose'][self.purpose_var.get()]
        dest = self.enc['destination'][self.dest_var.get()]
        time = self.enc['time_slot'][self.time_var.get()]
        feat = torch.tensor([sid, purpose, dest, time], dtype=torch.float32)
        x = torch.cat([self.prev, feat])
        with torch.no_grad():
            recon = self.model(x)
            mse = ((recon - x) ** 2).mean().item()
            self.prev = self.model.encoder(x).detach()
        if mse > self.enc['threshold']:
            messagebox.showwarning('Result', f'Anomalous Access! (error={mse:.4f})')
        else:
            messagebox.showinfo('Result', f'Access Normal (error={mse:.4f})')

def main():
    model, enc = load_model_and_enc()
    root = tk.Tk()
    App(root, model, enc)
    root.mainloop()

if __name__ == '__main__':
    main()
