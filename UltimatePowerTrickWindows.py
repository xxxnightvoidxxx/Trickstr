import os
import re
import tkinter as tk
from tkinter import messagebox, ttk

# Helper function to run shell commands
def run_command(command):
    """Run a shell command and return its output."""
    stream = os.popen(command)
    output = stream.read()
    stream.close()
    return output

# Function to unlock and configure the Ultimate Performance power plan
def unlock_and_configure():
    try:
        # Step 1: Unlock the "Ultimate Performance" power plan
        print("Unlocking 'Ultimate Performance' power plan...")
        run_command("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61")

        # Step 2: Get the GUID of the newly created "Ultimate Performance" plan
        print("Fetching GUID of 'Ultimate Performance'...")
        output = run_command("powercfg /list")
        match = re.search(r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\s*\(Ultimate Performance\)", output)
        if not match:
            print("Failed to find 'Ultimate Performance' plan.")
            messagebox.showerror("Error", "Failed to find 'Ultimate Performance' plan.")
            return
        ultimate_guid = match.group(1)
        print(f"Found 'Ultimate Performance' GUID: {ultimate_guid}")

        # Step 3: Delete the existing "High Performance" plan (if it exists)
        print("Deleting existing 'High Performance' plan...")
        output = run_command("powercfg /list")
        match = re.search(r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\s*\(High performance\)", output)
        if match:
            high_performance_guid = match.group(1)
            run_command(f"powercfg /delete {high_performance_guid}")
            print(f"Deleted 'High Performance' plan with GUID: {high_performance_guid}")

        # Step 4: Rename the "Ultimate Performance" plan to "High Performance"
        print("Renaming 'Ultimate Performance' to 'High Performance'...")
        run_command(f'powercfg /changename {ultimate_guid} "High Performance"')

        # Step 5: Activate the renamed "High Performance" plan
        print("Activating 'High Performance' plan...")
        run_command(f"powercfg /setactive {ultimate_guid}")

        # Show confirmation message
        messagebox.showinfo(
            "Success",
            "The Ultimate Power Plan has been Unlocked, and disguised as High Power Plan.\n"
            "Please proceed to Graphics settings, and apply your programs to High Performance!!"
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the GUI
def create_gui():
    # Initialize the main window
    root = tk.Tk()
    root.title("Tricktsr")
    root.geometry("500x300")
    root.configure(bg="black")
    root.attributes("-alpha", 0.9)  # Transparency effect

    # Style configuration for ttk widgets
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", foreground="red", background="black", font=("Arial", 12, "bold"))
    style.map("TButton", background=[("active", "black")], foreground=[("active", "red")])
    style.configure("TLabel", foreground="red", background="black", font=("Arial", 14, "bold"))

    # Title Label
    title_label = tk.Label(
        root,
        text="Trickstr",
        bg="black",
        fg="red",
        font=("Arial", 16, "bold"),
    )
    title_label.pack(pady=20)

    # Description Label
    description_label = tk.Label(
        root,
        text="Activate Trickstr",
        bg="black",
        fg="red",
        font=("Arial", 12),
    )
    description_label.pack(pady=10)

    # Activate Button
    activate_button = ttk.Button(
        root,
        text="Activate",
        command=unlock_and_configure,
    )
    activate_button.pack(pady=20)

    # Exit Button
    exit_button = ttk.Button(
        root,
        text="Exit",
        command=root.destroy,
    )
    exit_button.pack(pady=10)

    # Run the GUI
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()