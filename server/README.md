# Python Gate Access Server

This is a minimal example of a gate access control server. It provides a GUI
(Tkinter) that can generate and scan a pseudo QR code representing a person's
information. After scanning, it asks for purpose and destination of the visit
and runs a placeholder analysis (standing in for KoAlpaca) that decides whether
access should be granted.

## Usage

Run the application with:

```bash
python3 access_server.py
```

Because this environment does not include real QR code generation libraries or
KoAlpaca, the code uses a simple base64 string as the "QR" and a heuristic
function for analysis.
