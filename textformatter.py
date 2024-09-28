import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import os

"""
 * Author: GhostOkamiiii  // @guzmanwolfrank : Github
 * Created: [2024]
 * Description: Main stylesheet for [FC Website]
 * Version: 1.0
 * Location: New Jersey / San Francisco / New York
"""

def format_text(text):
    formatted_lines = []
    current_line = ""
    
    for char in text:
        if char == ';':
            formatted_lines.append(current_line.strip() + ';')
            current_line = ""
        elif char in '{}':
            if current_line.strip():
                formatted_lines.append(current_line.strip())
            formatted_lines.append(char)
            if char == '}':
                formatted_lines.extend(['', ''])  # Add two empty lines after '}'
            current_line = ""
        else:
            current_line += char
    
    if current_line.strip():
        formatted_lines.append(current_line.strip())
    
    return '\n'.join(formatted_lines)


class TextFormatterApp:
    def __init__(self, master):
        self.master = master
        master.title("Text Formatter by GhostOkamiiii")
        master.configure(bg='#1E1E1E')
        
        # Make window resizable
        master.resizable(True, True)
        
        # Set the initial window size
        master.geometry("800x600")
        
        # Create a style for rounded corners
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background='#1E1E1E')
        self.style.configure('TButton', background='#1E1E1E', foreground='#00FF00', font=('Arial', 10))
        self.style.configure('TLabel', background='#1E1E1E', foreground='#00FF00', font=('Arial', 10))
        
        # Main content frame with rounded corners
        self.main_frame = ttk.Frame(master, style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Custom title bar
        self.title_bar = ttk.Frame(self.main_frame, style='TFrame')
        self.title_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = ttk.Label(self.title_bar, text="GhostOkaamiiii", style='TLabel')
        self.title_label.pack(side=tk.LEFT, pady=2, padx=10)
        
        # Window control buttons
        self.close_button = ttk.Button(self.title_bar, text='×', command=self.master.destroy, width=3)
        self.close_button.pack(side=tk.RIGHT)
        
        self.maximize_button = ttk.Button(self.title_bar, text='□', command=self.toggle_maximize, width=3)
        self.maximize_button.pack(side=tk.RIGHT)
        
        self.minimize_button = ttk.Button(self.title_bar, text='−', command=self.minimize, width=3)
        self.minimize_button.pack(side=tk.RIGHT)
        
        # Input text area
        self.input_label = ttk.Label(self.main_frame, text="Input Text:", style='TLabel')
        self.input_label.pack(pady=(10,5))
        self.input_text = scrolledtext.ScrolledText(self.main_frame, height=15, bg='#1E1E1E', fg='#00FF00', font=('Arial', 10), insertbackground='#00FF00')
        self.input_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        # Format button
        self.format_button = ttk.Button(self.main_frame, text="Format Text and Save", command=self.format_and_save)
        self.format_button.pack(pady=10)
        
        # Output text area (preview)
        self.output_label = ttk.Label(self.main_frame, text="Formatted Text Preview:", style='TLabel')
        self.output_label.pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(self.main_frame, height=10, wrap=tk.WORD, bg='#1E1E1E', fg='#00FF00', font=('Arial', 10))
        self.output_text.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # Bind events for window dragging
        self.title_bar.bind('<Button-1>', self.start_move)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_move)
        self.title_bar.bind('<B1-Motion>', self.do_move)

    def format_and_save(self):
        input_text = self.input_text.get("1.0", tk.END)
        formatted_text = format_text(input_text)
        
        # Save to file
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "formatted.txt")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(formatted_text)
            
            # Show preview (first 100 lines)
            preview_lines = formatted_text.split('\n')[:100]
            preview_text = '\n'.join(preview_lines)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, preview_text)
            
            messagebox.showinfo("Success", f"Formatted text saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")

    def toggle_maximize(self):
        if self.master.state() == 'zoomed':
            self.master.state('normal')
        else:
            self.master.state('zoomed')

    def minimize(self):
        self.master.iconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextFormatterApp(root)
    root.mainloop()