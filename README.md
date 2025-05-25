# Military Access Control Example

This repository contains a minimal example of a gate access control system.
It demonstrates a Python server with a simple GUI and a placeholder Flutter
client.

* `server/` – Python Tkinter application that generates and scans a pseudo
  QR code. After scanning, it asks for purpose and destination and performs a
  stub analysis simulating KoAlpaca.
* `mobile_client/` – Skeleton Flutter project showing where a mobile QR
  scanner would be implemented.

These examples are intentionally simple and omit real QR generation and model
integration because this environment lacks the necessary dependencies.
