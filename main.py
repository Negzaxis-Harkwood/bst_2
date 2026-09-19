import sys
import tkinter as tk
from tkinter import scrolledtext


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

#global list to store readings
stored_readings = [183,]

def handle_reading(reading):
    try:
        new_reading = int(reading)
    except ValueError:
        print("Please enter a valid number.")
        return
    
    prev_reading = stored_readings[-1]

    print(f"Reading received: {reading}")
    if new_reading > prev_reading:
        print(f"Your resting blood sugar is up {new_reading - prev_reading} points")
    else:
        print(f"Your resting blood sugar is down {prev_reading - new_reading} points")



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