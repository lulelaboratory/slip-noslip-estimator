import tkinter as tk
from tkinter import ttk, messagebox, font, filedialog
import tkinter.font as tkFont
import tempfile
import webbrowser
import datetime
import platform
import os
from tkinter.scrolledtext import ScrolledText

# MIT License text
MIT_LICENSE = """MIT License

Copyright (c) {} Le Lu (lulelaboratory@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""".format(datetime.datetime.now().year)

VERSION = "1.01"
AUTHOR = "Le Lu"
EMAIL = "lulelaboratory@gmail.com"
APP_NAME = "Slip/No-Slip Estimator"

# Color scheme for a professional look
COLORS = {
    "primary": "#1976d2",      # Primary blue
    "primary_dark": "#0d47a1", # Darker blue
    "primary_light": "#bbdefb", # Light blue
    "accent": "#ff9800",       # Orange accent
    "text_primary": "#212121", # Near black for main text
    "text_secondary": "#757575", # Gray for secondary text
    "divider": "#bdbdbd",      # Light gray for dividers
    "success": "#4caf50",      # Green for success/no-slip
    "error": "#f44336",        # Red for warnings/slip
    "background": "#f5f8fa",   # Light blue-gray background
    "card": "#ffffff",         # White for card backgrounds
}

def calculate():
    try:
        # Show calculation in progress
        status_var.set("Calculating...")
        root.update_idletasks()
        
        # Read input values from the GUI
        gap_nm = float(gap_entry.get())
        gap_m = gap_nm * 1e-9  # convert nm to m
        sliding_speed = float(speed_entry.get())
        mu = float(viscosity_entry.get())
        lambda_friction = float(friction_entry.get())
        # New parameters for shear-dependent slip length
        gamma_crit = float(crit_shear_entry.get())
        exponent = float(exp_entry.get())
        
        # Calculate shear rate (1/s): γ = U / h
        shear_rate = sliding_speed / gap_m
        
        # Calculate shear stress (Pa): τ = μ × γ
        shear_stress = mu * shear_rate
        
        # Baseline slip length (m) at low shear: b₀ = μ / λ
        b0 = mu / lambda_friction
        
        # Effective slip length (m) including sliding (shear) effect:
        # bₑff = b₀ * [1 + (γ / γ_c)^m]
        b_eff = b0 * (1 + (shear_rate / gamma_crit)**exponent)
        
        # Compare effective slip length to gap height to decide on boundary condition
        ratio = b_eff / gap_m
        if ratio < 0.01:
            recommendation = "No-slip condition is appropriate"
            rec_label.config(fg=COLORS["success"])
            cfd_suggestion = "For CFD simulation: Use a no-slip boundary condition (e.g., u = 0 at the wall)."
        else:
            recommendation = "Slip condition should be considered"
            rec_label.config(fg=COLORS["error"])
            cfd_suggestion = f"For CFD simulation: Use a Navier slip boundary condition with a slip length of {b_eff:.3e} m."
        
        # Clear previous results
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)
        
        # Insert detailed results with formatting
        results_text.insert(tk.END, "CALCULATION RESULTS\n", "heading")
        results_text.insert(tk.END, "═" * 50 + "\n\n", "separator")
        
        results_text.insert(tk.END, "Gap (m): ", "param")
        results_text.insert(tk.END, f"{gap_m:.3e}\n", "value")
        
        results_text.insert(tk.END, "Sliding Speed (m/s): ", "param")
        results_text.insert(tk.END, f"{sliding_speed:.3e}\n", "value")
        
        results_text.insert(tk.END, "Shear Rate (1/s): ", "param")
        results_text.insert(tk.END, f"{shear_rate:.3e}\n", "value")
        
        results_text.insert(tk.END, "Shear Stress (Pa): ", "param")
        results_text.insert(tk.END, f"{shear_stress:.3e}\n", "value")
        
        results_text.insert(tk.END, "Baseline Slip Length, b₀ (m): ", "param")
        results_text.insert(tk.END, f"{b0:.3e}\n", "value")
        
        results_text.insert(tk.END, "Effective Slip Length, bₑff (m): ", "param")
        results_text.insert(tk.END, f"{b_eff:.3e}\n", "value")
        
        results_text.insert(tk.END, "Slip Length / Gap: ", "param")
        results_text.insert(tk.END, f"{ratio:.3e}\n\n", "value")
        
        results_text.insert(tk.END, "RECOMMENDATION\n", "heading")
        results_text.insert(tk.END, "═" * 50 + "\n\n", "separator")
        
        if ratio < 0.01:
            results_text.insert(tk.END, recommendation + "\n\n", "recommend_noslip")
        else:
            results_text.insert(tk.END, recommendation + "\n\n", "recommend_slip")
            
        results_text.insert(tk.END, cfd_suggestion + "\n", "cfd_suggestion")
        
        results_text.config(state=tk.DISABLED)
        
        # Update recommendation label
        rec_label.config(text=recommendation)
        
        # Update status
        status_var.set("Ready - Last calculation: " + datetime.datetime.now().strftime("%H:%M:%S"))
        
    except Exception as e:
        # Handle errors
        messagebox.showerror("Error", f"Calculation error: {str(e)}")
        status_var.set("Error occurred during calculation")
        rec_label.config(text="")

def show_methodology():
    # HTML content for the methodology page with MathJax and MLA references
    methodology_html = r"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Methodology: Slip vs. No-Slip with Sliding Effect</title>
        <!-- Load MathJax for beautiful math formatting -->
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 20px; 
                color: #212121; 
                line-height: 1.6;
                background-color: #f5f8fa;
                max-width: 900px;
                margin: 0 auto;
                padding: 30px;
            }
            h1, h2 { font-weight: normal; color: #1976d2; }
            h1 { border-bottom: 2px solid #1976d2; padding-bottom: 10px; }
            h2 { margin-top: 30px; }
            .equation { 
                margin: 1.5em 0; 
                background-color: #ffffff; 
                padding: 15px; 
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
            .ref { 
                margin-top: 40px; 
                font-size: 0.95em; 
                border-top: 1px solid #bdbdbd; 
                padding-top: 20px; 
            }
            footer { 
                margin-top: 50px; 
                font-size: 0.85em; 
                color: #757575; 
                text-align: center;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
            }
            ul { padding-left: 25px; }
            li { margin-bottom: 8px; }
        </style>
    </head>
    <body>
        <h1>Methodology: Slip vs. No-Slip with Sliding Effect</h1>
        
        <h2>1. Input Parameters and Definitions</h2>
        <ul>
            <li><strong>h</strong>: Gap height (m). Default is 100 nm (1e-7 m).</li>
            <li><strong>U</strong>: Sliding speed (m/s). Default is 1 m/s.</li>
            <li><strong>&mu;</strong>: Water viscosity (Pa·s). Default is 1e-3 Pa·s.</li>
            <li><strong>&lambda;</strong>: Interfacial friction coefficient (Pa·s/m). Default is 1e7 Pa·s/m.</li>
            <li><strong>&gamma;<sub>c</sub></strong>: Critical shear rate (1/s) at which slip increases. Default is 1e7 1/s.</li>
            <li><strong>m</strong>: Exponent controlling slip sensitivity to shear. Default is 2.</li>
        </ul>
        
        <h2>2. Fundamental Equations</h2>
        <div class="equation">
            <p><strong>Shear Rate:</strong></p>
            $$ \gamma = \frac{U}{h} $$
        </div>
        
        <div class="equation">
            <p><strong>Shear Stress:</strong></p>
            $$ \tau = \mu \cdot \gamma $$
        </div>
        
        <div class="equation">
            <p><strong>Baseline Slip Length:</strong></p>
            $$ b_0 = \frac{\mu}{\lambda} $$
        </div>
        
        <div class="equation">
            <p><strong>Effective Slip Length:</strong></p>
            $$ b_{\text{eff}} = b_0 \left[ 1 + \left(\frac{\gamma}{\gamma_c}\right)^m \right] $$
        </div>
        
        <h2>3. Decision Criterion</h2>
        <div class="equation">
            <p>Slip Ratio:</p>
            $$ \text{Slip Ratio} = \frac{b_{\text{eff}}}{h} $$
        </div>
        <p>
            If $$ \frac{b_{\text{eff}}}{h} < 0.01 $$, then assume <strong>No-Slip</strong>.<br>
            If $$ \frac{b_{\text{eff}}}{h} \geq 0.01 $$, then slip is significant and a <strong>Slip</strong> condition should be used.
        </p>
        
        <h2>4. Rationale</h2>
        <p>
            At low shear rates, \( b_{\text{eff}} \) approximates \( b_0 \). At higher shear rates, the additional sliding effect increases the effective slip length,
            capturing the shear-dependent behavior observed in experiments.
        </p>
        <p>
            The computed shear rate and shear stress provide insight into the flow conditions, indicating that high shear may amplify slip effects.
        </p>
        
        <div class="ref">
            <h2>References</h2>
            <p>Thompson, P. A., and S. M. Troian. "A General Boundary Condition for Liquid Flow at Solid Surfaces." <em>Nature</em>, vol. 389, no. 6649, 1997, pp. 360–362.</p>
            <p>Neto, C., D. R. Evans, E. Bonaccurso, H.-J. Butt, and V. S. J. Craig. "Fluid Slip in Diverse Regimes: A Review of Experimental Studies." <em>Reports on Progress in Physics</em>, vol. 68, no. 12, 2005, pp. 2859–2897.</p>
            <p>Bocquet, Lydéric, and Jean-Louis Barrat. "Hydrodynamic Boundary Conditions, Correlation between Friction and Slip at a Fluid/Solid Interface." <em>Soft Matter</em>, vol. 3, no. 4, 2007, pp. 685–693.</p>
        </div>
        
        <footer>
            &copy; """ + str(datetime.datetime.now().year) + """ Le Lu (lulelaboratory@gmail.com) - MIT License
        </footer>
    </body>
    </html>
    """
    # Write the HTML content to a temporary file and open it in the default web browser
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
        f.write(methodology_html)
        temp_file_path = f.name
    webbrowser.open("file://" + temp_file_path)

def show_about():
    """Display About dialog with license information"""
    about_window = tk.Toplevel(root)
    about_window.title(f"About {APP_NAME}")
    about_window.geometry("600x500")
    about_window.resizable(False, False)
    about_window.transient(root)
    about_window.grab_set()
    
    # Make it a modal dialog
    about_window.focus_set()
    
    # Add padding
    frame = ttk.Frame(about_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_font = font.Font(family="Segoe UI", size=16, weight="bold")
    title = ttk.Label(frame, text=APP_NAME, font=title_font, foreground="#000000")
    title.pack(pady=(0, 10))
    
    # Logo - Fix: Use explicit background color instead of trying to get it from the frame
    logo_canvas = tk.Canvas(frame, width=100, height=100, highlightthickness=0, bg=COLORS["background"])
    logo_canvas.pack(pady=(0, 20))
    logo_canvas.create_oval(10, 10, 90, 90, fill=COLORS["primary"], outline="")
    logo_canvas.create_text(50, 50, text="S/NS", fill="white", font=("Segoe UI", 20, "bold"))
    
    # Version and author info
    info_text = f"Version {VERSION}\nAuthor: {AUTHOR}\nEmail: {EMAIL}"
    info = ttk.Label(frame, text=info_text, font=("Segoe UI", 10))
    info.pack(pady=(0, 20))
    
    # Description
    desc = ttk.Label(frame, 
                     text=f"{APP_NAME} is a practical tool to help users decide what boundary condition, slip or no-slip, should be used for CFD simulations.", 
                     wraplength=550, 
                     justify="center",
                     font=("Segoe UI", 10))
    desc.pack(pady=(0, 20))
    
    # License text (scrollable)
    license_frame = ttk.LabelFrame(frame, text="MIT License")
    license_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    license_text = ScrolledText(license_frame, wrap=tk.WORD, width=60, height=10, font=("Consolas", 9))
    license_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    license_text.insert(tk.END, MIT_LICENSE)
    license_text.config(state=tk.DISABLED)
    
    # Close button
    close_btn = ttk.Button(frame, text="Close", command=about_window.destroy, style="Accent.TButton")
    close_btn.pack(pady=(0, 10))

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        
        # Create a toplevel window
        tip = tk.Toplevel(widget)
        tip.wm_overrideredirect(True)
        tip.wm_geometry(f"+{x}+{y}")
        
        # Add a label with the tooltip text
        label = ttk.Label(tip, text=text, justify=tk.LEFT,
                         background="#ffffff", relief=tk.SOLID, borderwidth=1,
                         font=("Segoe UI", "9", "normal"), padding=(8, 6))
        label.pack(ipadx=1)
        
        tooltip_data[widget] = tip
    
    def leave(event):
        if widget in tooltip_data:
            tooltip_data[widget].destroy()
            del tooltip_data[widget]
    
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

def export_results():
    """Export the calculation results to a text file"""
    if not results_text.get(1.0, tk.END).strip():
        messagebox.showinfo("Export Results", "No results to export.")
        return
        
    try:
        # Get filename from user
        filename = tk.filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Results"
        )
        
        if not filename:  # User cancelled
            return
            
        # Prepare export content
        export_content = (
            f"{APP_NAME} - Results Export\n"
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Version: {VERSION}\n"
            f"Author: {AUTHOR} ({EMAIL})\n"
            f"{'=' * 50}\n\n"
        )
        
        # Add input parameters - use ASCII-compatible alternatives for special characters
        export_content += "INPUT PARAMETERS:\n"
        export_content += f"Gap Height: {gap_entry.get()} nm\n"
        export_content += f"Sliding Speed: {speed_entry.get()} m/s\n"
        export_content += f"Water Viscosity: {viscosity_entry.get()} Pa·s\n"
        export_content += f"Interfacial Friction: {friction_entry.get()} Pa·s/m\n"
        export_content += f"Critical Shear Rate: {crit_shear_entry.get()} 1/s\n"
        export_content += f"Exponent (m): {exp_entry.get()}\n\n"
        
        # Add calculation results (plain text without formatting)
        export_content += "CALCULATION RESULTS:\n"
        # Get text without tags
        result_text = results_text.get(1.0, tk.END)
        export_content += result_text
        
        # Write to file with explicit UTF-8 encoding
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(export_content)
            
        messagebox.showinfo("Export Complete", f"Results exported successfully to:\n{filename}")
        
    except Exception as e:
        messagebox.showerror("Export Error", f"Error exporting results: {str(e)}")
        # Add fallback export with simplified ASCII if encoding was the issue
        if 'codec' in str(e).lower() or 'encoding' in str(e).lower():
            try:
                # Ask user if they want to try with simplified ASCII instead
                if messagebox.askyesno("Encoding Error", 
                                        "There was an encoding error. Would you like to try exporting with simplified characters?"):
                    # Replace Unicode characters with ASCII alternatives
                    simplified_content = export_content.replace("μ", "u")
                    simplified_content = simplified_content.replace("λ", "lambda")
                    simplified_content = simplified_content.replace("γ", "gamma")
                    simplified_content = simplified_content.replace("₀", "0")
                    simplified_content = simplified_content.replace("ₑff", "eff")
                    simplified_content = simplified_content.replace("·", ".")
                    
                    # Write with simplified content
                    with open(filename, 'w', encoding='ascii', errors='replace') as f:
                        f.write(simplified_content)
                    
                    messagebox.showinfo("Export Complete", 
                                        f"Results exported with simplified characters to:\n{filename}")
            except Exception as ex:
                messagebox.showerror("Export Error", f"Could not export with simplified characters: {str(ex)}")

def create_header_section(parent, title, **kwargs):
    """Create a borderless section with a prominent title"""
    # Container frame
    section_frame = ttk.Frame(parent, padding="0", **kwargs)
    
    # Title label
    title_label = ttk.Label(section_frame, text=title, 
                           font=("Segoe UI", 15, "bold"),
                           foreground="#000000",
                           background=COLORS["background"],
                           padding=(5, 10, 5, 10))
    title_label.pack(anchor="w", fill="x")
    
    # Content frame
    content_frame = ttk.Frame(section_frame, padding="15")
    content_frame.pack(fill="both", expand=True)
    
    return section_frame, content_frame

# Store tooltips data
tooltip_data = {}

# Create the main window
root = tk.Tk()
root.title(f"{APP_NAME} v{VERSION}")
root.geometry("900x750")  # Set initial window size
root.minsize(800, 650)    # Set minimum window size

# Set the application icon (if available)
if os.path.exists("icon.ico"):
    root.iconbitmap("icon.ico")

# Configure theme and style
style = ttk.Style()
if "clam" in style.theme_names():  # Check if theme is available
    style.theme_use("clam")

# Define custom styles
style.configure("TFrame", background=COLORS["background"])
style.configure("TLabelframe", background=COLORS["background"])
style.configure("TLabelframe.Label", foreground="#000000", font=("Segoe UI", 12, "bold"))
style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text_primary"], font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#000000", background=COLORS["background"])
style.configure("Subheader.TLabel", font=("Segoe UI", 12, "bold"), foreground="#000000", background=COLORS["background"])
style.configure("TButton", font=("Segoe UI", 10))
style.configure("Accent.TButton", background=COLORS["accent"])
style.configure("Calculate.TButton", font=("Segoe UI", 12, "bold"))
style.configure("TEntry", font=("Segoe UI", 10))

# Create a custom style for section headers with larger font and NO borders
style.configure("SectionHeader.TLabelframe", background=COLORS["background"], borderwidth=0, relief="flat")
style.configure("SectionHeader.TLabelframe.Label", foreground="#000000", font=("Segoe UI", 15, "bold"))

# Create main container with padding
main_container = ttk.Frame(root, padding="20")
main_container.pack(fill=tk.BOTH, expand=True)

# Application title and logo
header_frame = ttk.Frame(main_container)
header_frame.pack(fill=tk.X, pady=(0, 20))

# Add a logo
logo_canvas = tk.Canvas(header_frame, width=70, height=70, bg=COLORS["background"], highlightthickness=0)
logo_canvas.pack(side=tk.LEFT, padx=(0, 15))
logo_canvas.create_oval(5, 5, 65, 65, fill=COLORS["primary"], outline="")
logo_canvas.create_text(35, 35, text="S/NS", fill="white", font=("Segoe UI", 16, "bold"))

# Title and subtitle
title_frame = ttk.Frame(header_frame)
title_frame.pack(side=tk.LEFT)
title_label = ttk.Label(title_frame, text=APP_NAME, style="Header.TLabel")
title_label.pack(anchor="w")
subtitle_label = ttk.Label(title_frame, 
                         text="A practical tool for CFD boundary condition selection",
                         font=("Segoe UI", 10, "italic"),
                         foreground=COLORS["text_secondary"])
subtitle_label.pack(anchor="w")

# Create a menu bar with Help menu including Methodology
menubar = tk.Menu(root)
root.config(menu=menubar)

# File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Export Results", command=export_results)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Help menu
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Methodology", command=show_methodology)
help_menu.add_command(label="About", command=show_about)

# Create a paned window to divide input and output areas
main_paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
main_paned.pack(fill=tk.BOTH, expand=True)

# Input frame (left side)
input_frame = ttk.Frame(main_paned, padding=15)
main_paned.add(input_frame, weight=1)

# Input parameters section with completely removed border
input_section, input_params_frame = create_header_section(input_frame, "Input Parameters")
input_section.pack(fill=tk.BOTH, expand=True)

# Create a grid for input parameters with consistent layout
row = 0

# Gap height
ttk.Label(input_params_frame, text="Gap Height (nm):", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="W", pady=8)
gap_entry = ttk.Entry(input_params_frame, width=20, font=("Segoe UI", 10))
gap_entry.insert(0, "100")  # Default: 100 nm
gap_entry.grid(row=row, column=1, sticky="EW", pady=8, padx=(10, 0))
create_tooltip(gap_entry, "Distance between surfaces (nanometers)")
row += 1

# Sliding Speed
ttk.Label(input_params_frame, text="Sliding Speed (m/s):", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="W", pady=8)
speed_entry = ttk.Entry(input_params_frame, width=20, font=("Segoe UI", 10))
speed_entry.insert(0, "1")  # Default: 1 m/s
speed_entry.grid(row=row, column=1, sticky="EW", pady=8, padx=(10, 0))
create_tooltip(speed_entry, "Relative velocity between surfaces")
row += 1

# Water Viscosity
ttk.Label(input_params_frame, text="Water Viscosity (Pa·s):", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="W", pady=8)
viscosity_entry = ttk.Entry(input_params_frame, width=20, font=("Segoe UI", 10))
viscosity_entry.insert(0, "0.001")  # Default: 0.001 Pa·s
viscosity_entry.grid(row=row, column=1, sticky="EW", pady=8, padx=(10, 0))
create_tooltip(viscosity_entry, "Fluid dynamic viscosity (default for water: 0.001 Pa·s)")
row += 1

# Interfacial Friction
ttk.Label(input_params_frame, text="Interfacial Friction (Pa·s/m):", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="W", pady=8)
friction_entry = ttk.Entry(input_params_frame, width=20, font=("Segoe UI", 10))
friction_entry.insert(0, "1e7")  # Default: 1e7 Pa·s/m
friction_entry.grid(row=row, column=1, sticky="EW", pady=8, padx=(10, 0))
create_tooltip(friction_entry, "Surface friction coefficient (typical range: 1e6-1e8 Pa·s/m)")
row += 1

# Critical Shear Rate
ttk.Label(input_params_frame, text="Critical Shear Rate (1/s):", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="W", pady=8)
crit_shear_entry = ttk.Entry(input_params_frame, width=20, font=("Segoe UI", 10))
crit_shear_entry.insert(0, "1e7")  # Default: 1e7 1/s
crit_shear_entry.grid(row=row, column=1, sticky="EW", pady=8, padx=(10, 0))
create_tooltip(crit_shear_entry, "Shear rate at which slip effects increase significantly")
row += 1

# Exponent
ttk.Label(input_params_frame, text="Exponent (m):", font=("Segoe UI", 10)).grid(row=row, column=0, sticky="W", pady=8)
exp_entry = ttk.Entry(input_params_frame, width=20, font=("Segoe UI", 10))
exp_entry.insert(0, "2")  # Default: 2
exp_entry.grid(row=row, column=1, sticky="EW", pady=8, padx=(10, 0))
create_tooltip(exp_entry, "Controls how rapidly slip increases with shear rate")
row += 1

# Configure the grid to expand properly
for i in range(2):
    input_params_frame.columnconfigure(i, weight=1)

# Criteria section with completely removed border
criteria_section, criteria_content = create_header_section(input_frame, "Decision Criteria")
criteria_section.pack(fill=tk.X, pady=15)

criteria_text = (
    "• Baseline slip length: b₀ = μ / λ\n"
    "• Effective slip length: bₑff = b₀ [1 + (γ / γ₍c₎)^m]\n"
    "• If bₑff/h < 0.01: No-Slip condition\n"
    "• If bₑff/h ≥ 0.01: Slip condition recommended"
)
criteria_label = ttk.Label(criteria_content, text=criteria_text, justify="left", font=("Segoe UI", 10))
criteria_label.pack(pady=5)

# Calculate button with more prominent styling
calc_button_frame = ttk.Frame(input_frame)
calc_button_frame.pack(fill=tk.X, pady=15)

calc_button = ttk.Button(calc_button_frame, text="Calculate", command=calculate, style="Calculate.TButton")
calc_button.pack(fill=tk.X, ipady=8)

# Results frame (right side) with improved styling
results_frame = ttk.Frame(main_paned, padding=15)
main_paned.add(results_frame, weight=2)

# Results section with completely removed border
results_section, results_content = create_header_section(results_frame, "Results")
results_section.pack(fill=tk.BOTH, expand=True)

# Recommendation label (prominent display)
rec_frame = ttk.Frame(results_content)
rec_frame.pack(fill=tk.X, pady=(5, 15))

# Change from ttk.Label to tk.Label to allow direct foreground color configuration
rec_label = tk.Label(rec_frame, text="", font=("Segoe UI", 14, "bold"), anchor="center", bg=COLORS["background"])
rec_label.pack(fill=tk.X, pady=10)

# Add a separator
separator = ttk.Separator(results_content, orient="horizontal")
separator.pack(fill=tk.X, pady=5)

# Text widget for detailed results with better formatting
results_text = ScrolledText(results_content, height=20, width=50, wrap=tk.WORD, font=("Segoe UI", 10))
results_text.pack(fill=tk.BOTH, expand=True, pady=5)

# Configure text widget tags for formatting
results_text.tag_configure("heading", font=("Segoe UI", 12, "bold"), foreground=COLORS["primary"])
results_text.tag_configure("separator", foreground=COLORS["divider"])
results_text.tag_configure("param", foreground=COLORS["primary_dark"], font=("Segoe UI", 10, "bold"))
results_text.tag_configure("value", foreground=COLORS["text_primary"])
results_text.tag_configure("recommend_noslip", foreground=COLORS["success"], font=("Segoe UI", 12, "bold"))
results_text.tag_configure("recommend_slip", foreground=COLORS["error"], font=("Segoe UI", 12, "bold"))
results_text.tag_configure("cfd_suggestion", foreground=COLORS["text_secondary"], font=("Segoe UI", 10, "italic"))

# Initial state
results_text.insert(tk.END, "Enter parameters and click 'Calculate' to see results.", "heading")
results_text.config(state=tk.DISABLED)

# Status bar with modern styling
status_frame = ttk.Frame(main_container)
status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))

status_var = tk.StringVar()
status_var.set("Ready")
status_bar = ttk.Label(status_frame, textvariable=status_var, relief=tk.GROOVE, anchor=tk.W, padding=(5, 3))
status_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)

# Version and license information
license_label = ttk.Label(
    status_frame, 
    text=f"v{VERSION} | © {datetime.datetime.now().year} {AUTHOR} | MIT License", 
    anchor=tk.E,
    font=("Segoe UI", 8),
    foreground=COLORS["text_secondary"]
)
license_label.pack(side=tk.RIGHT, padx=5)

# Set initial sash position (40% for input, 60% for results)
def set_sash_position():
    width = main_paned.winfo_width()
    if width > 1:  # Only set if window has been drawn
        main_paned.sashpos(0, int(width * 0.4))
        
# Schedule the sash position update after the window is drawn
root.after(100, set_sash_position)

# Start the GUI event loop
root.mainloop()
