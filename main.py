import sys
import tkinter as tk
from tkinter import scrolledtext
import json
from datetime import date, datetime
from pathlib import Path


class PrintRedirector:
    """Sends anything printed with print() to a Text widget."""

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")

    def flush(self):
        pass

DATA_FILE = Path(__file__).parent / "readings.json"

def load_readings():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []

def save_readings(readings):
    DATA_FILE.write_text(json.dumps(readings, indent=2))

readings = load_readings()


def handle_reading(reading):
    # for what the user is entering to make sure it is a valid number(integer)
    try:
        new_reading = int(reading)
    except ValueError:
        print("Please enter a valid number.")
        return

    print(f"reading received: {new_reading}")


    if readings:
        prev_reading = readings[-1]["reading"]
        diff = new_reading - prev_reading

        if diff > 0:
            print(f"Your resting blood sugar is up {diff} points.")
        elif diff < 0:
            print(f"Your resting blood sugar is down {abs(diff)} points.")
    else:
        print("This is your first reading!")

    # append our json to add the reading to the file
    readings.append({
        "date": date.today().isoformat(),
        "time": datetime.now().strftime("%H:%M"),
        "reading": new_reading
    })
    save_readings(readings)
    print(f"Saved: {new_reading}")



def main():
    root = tk.Tk()
    root.title("Blood Sugar Tracker")
    root.geometry("300x500")
    root.resizable(False, False)

    def on_submit(event=None):
        reading = entry.get().strip()
        if not reading:
            return
        handle_reading(reading)
        entry.delete(0, tk.END)
        entry.focus()

    # Input section
    input_frame = tk.Frame(root)
    input_frame.pack(fill="x", padx=10, pady=(10, 5))

    tk.Label(input_frame, text="Morning reading:").pack(anchor="w")

    entry = tk.Entry(input_frame)
    entry.pack(fill="x", pady=(2, 5))
    entry.bind("<Return>", on_submit)
    entry.focus()

    tk.Button(input_frame, text="Submit", command=on_submit).pack(fill="x")

    # Output section
    tk.Label(root, text="Output:").pack(anchor="w", padx=10)

    output = scrolledtext.ScrolledText(root, state="disabled", wrap="word")
    output.pack(fill="both", expand=True, padx=10, pady=(2, 10))

    # Redirect print() to the output window
    sys.stdout = PrintRedirector(output)

    root.mainloop()


if __name__ == "__main__":
    main()