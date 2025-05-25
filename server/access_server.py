import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import base64
import hashlib

# Placeholder text analysis function simulating KoAlpaca
# In a real environment this would call the KoAlpaca model
# to analyze the text and return "예" or "아니요".
# This stub returns "예" if both purpose and destination are non-empty
# and do not contain suspicious keywords; otherwise "아니요".
SUSPICIOUS = ["공격", "위협", "테러"]

def analyze_text(purpose: str, dest: str) -> str:
    text = purpose + " " + dest
    for word in SUSPICIOUS:
        if word in text:
            return "아니요"
    if purpose.strip() and dest.strip():
        return "예"
    return "아니요"

# Simple pseudo QR code generation using base64 string.
# This does NOT create a real QR code but provides a short text
# that could be used in place of one for this example.
def make_pseudo_qr(data: dict) -> str:
    raw = json.dumps(data)
    encoded = base64.urlsafe_b64encode(raw.encode()).decode()
    return encoded


def decode_pseudo_qr(encoded: str) -> dict:
    try:
        raw = base64.urlsafe_b64decode(encoded.encode()).decode()
        return json.loads(raw)
    except Exception:
        return {}


class AccessApp:
    def __init__(self, root):
        self.root = root
        root.title("Gate Access Control")

        tk.Label(root, text="성명").grid(row=0, column=0)
        tk.Label(root, text="생년월일 (YYYYMMDD)").grid(row=1, column=0)
        tk.Label(root, text="계급").grid(row=2, column=0)
        tk.Label(root, text="군번").grid(row=3, column=0)

        self.name_entry = tk.Entry(root)
        self.birth_entry = tk.Entry(root)
        self.rank_entry = tk.Entry(root)
        self.sn_entry = tk.Entry(root)

        self.name_entry.grid(row=0, column=1)
        self.birth_entry.grid(row=1, column=1)
        self.rank_entry.grid(row=2, column=1)
        self.sn_entry.grid(row=3, column=1)

        tk.Button(root, text="QR 생성", command=self.generate_qr).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="QR 스캔", command=self.scan_qr).grid(row=5, column=0, columnspan=2)

    def generate_qr(self):
        data = {
            "name": self.name_entry.get(),
            "birth": self.birth_entry.get(),
            "rank": self.rank_entry.get(),
            "service_number": self.sn_entry.get(),
        }
        qr = make_pseudo_qr(data)
        messagebox.showinfo("생성된 코드", qr)

    def scan_qr(self):
        code = simpledialog.askstring("QR 코드", "스캔된 코드를 입력하세요")
        info = decode_pseudo_qr(code or "")
        if not info:
            messagebox.showerror("오류", "유효하지 않은 코드")
            return
        purpose = simpledialog.askstring("출입 목적", "출입 목적을 입력하세요")
        dest = simpledialog.askstring("행선지", "행선지를 입력하세요")
        result = analyze_text(purpose or "", dest or "")
        info_text = f"성명: {info.get('name')}\n생년월일: {info.get('birth')}\n계급: {info.get('rank')}\n군번: {info.get('service_number')}"
        messagebox.showinfo("출입 허가 여부", f"{info_text}\n출입 허가: {result}")


def main():
    root = tk.Tk()
    app = AccessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
