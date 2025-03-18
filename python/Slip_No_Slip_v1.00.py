import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import tempfile
import webbrowser

def calculate():
    try:
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
            recommendation = "No-slip condition is appropriate."
            rec_label.config(fg="blue")
            cfd_suggestion = "For CFD simulation: Use a no-slip boundary condition (e.g., u = 0 at the wall)."
        else:
            recommendation = "Slip condition should be considered."
            rec_label.config(fg="red")
            cfd_suggestion = f"For CFD simulation: Use a Navier slip boundary condition with a slip length of {b_eff:.3e} m."
        
        # Prepare the detailed output text
        details_text = (
            f"Gap (m): {gap_m:.3e}\n"
            f"Sliding Speed (m/s): {sliding_speed:.3e}\n"
            f"Shear Rate (1/s): {shear_rate:.3e}\n"
            f"Shear Stress (Pa): {shear_stress:.3e}\n"
            f"Baseline Slip Length, b₀ (m): {b0:.3e}\n"
            f"Effective Slip Length, bₑff (m): {b_eff:.3e}\n"
            f"Slip Length / Gap: {ratio:.3e}\n"
        )
        
        # Update the detailed output, recommendation, and CFD suggestion labels
        output_label.config(text=details_text)
        rec_label.config(text=f"Recommendation: {recommendation}")
        cfd_label.config(text=cfd_suggestion)
    except Exception as e:
        output_label.config(text=f"Error: {e}")
        rec_label.config(text="")
        cfd_label.config(text="")

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
            body { font-family: Arial, sans-serif; margin: 20px; color: #000; }
            h1, h2 { font-weight: normal; }
            .equation { margin: 1em 0; }
            .ref { margin-top: 20px; font-size: 0.9em; }
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
    </body>
    </html>
    """
    # Write the HTML content to a temporary file and open it in the default web browser
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
        f.write(methodology_html)
        temp_file_path = f.name
    webbrowser.open("file://" + temp_file_path)

# Create the main window
root = tk.Tk()
root.title("Slip/No-Slip Estimator with Sliding Effect")

# Create a main frame with padding and a border for better appearance
main_frame = ttk.Frame(root, padding="15")
main_frame.grid(row=0, column=0, sticky="NSEW")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create a menu bar with a 'Help' menu including 'Methodology'
menubar = tk.Menu(root)
root.config(menu=menubar)
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Methodology", command=show_methodology)

# Create labels and entry fields for input parameters
ttk.Label(main_frame, text="Gap Height (nm):").grid(row=0, column=0, sticky="W", pady=2)
gap_entry = ttk.Entry(main_frame, width=20)
gap_entry.insert(0, "100")  # Default: 100 nm
gap_entry.grid(row=0, column=1, pady=2)

ttk.Label(main_frame, text="Sliding Speed (m/s):").grid(row=1, column=0, sticky="W", pady=2)
speed_entry = ttk.Entry(main_frame, width=20)
speed_entry.insert(0, "1")  # Default: 1 m/s
speed_entry.grid(row=1, column=1, pady=2)

ttk.Label(main_frame, text="Water Viscosity (Pa·s, default 1e-3):").grid(row=2, column=0, sticky="W", pady=2)
viscosity_entry = ttk.Entry(main_frame, width=20)
viscosity_entry.insert(0, "0.001")
viscosity_entry.grid(row=2, column=1, pady=2)

ttk.Label(main_frame, text="Interfacial Friction (Pa·s/m):").grid(row=3, column=0, sticky="W", pady=2)
friction_entry = ttk.Entry(main_frame, width=20)
friction_entry.insert(0, "1e7")  # Default for hydrophilic surfaces
friction_entry.grid(row=3, column=1, pady=2)

ttk.Label(main_frame, text="Critical Shear Rate (1/s):").grid(row=4, column=0, sticky="W", pady=2)
crit_shear_entry = ttk.Entry(main_frame, width=20)
crit_shear_entry.insert(0, "1e7")  # Default: 1e7 1/s
crit_shear_entry.grid(row=4, column=1, pady=2)

ttk.Label(main_frame, text="Exponent (m):").grid(row=5, column=0, sticky="W", pady=2)
exp_entry = ttk.Entry(main_frame, width=20)
exp_entry.insert(0, "2")  # Default: 2
exp_entry.grid(row=5, column=1, pady=2)

# Display Criteria on the GUI
criteria_text = (
    "Criteria:\n"
    "1. Baseline slip length: b₀ = μ / λ.\n"
    "2. Effective slip length: bₑff = b₀ [1 + (γ / γ₍c₎)^m].\n"
    "3. Slip ratio: bₑff / h.\n"
    "   - If bₑff/h < 0.01, assume No-Slip.\n"
    "   - If bₑff/h ≥ 0.01, slip is significant.\n"
    "4. Also compute shear rate (γ = U / h) and shear stress (τ = μ × γ)."
)
criteria_label = ttk.Label(main_frame, text=criteria_text, justify="left", wraplength=350)
criteria_label.grid(row=6, column=0, columnspan=2, pady=(10, 5))

# Calculate button
calc_button = ttk.Button(main_frame, text="Calculate", command=calculate)
calc_button.grid(row=7, column=0, columnspan=2, pady=10)

# Output labels for details and recommendation
output_label = ttk.Label(main_frame, text="", justify="left", font=("Helvetica", 10))
output_label.grid(row=8, column=0, columnspan=2, pady=(5, 5))

# Create a bold font for the recommendation label
bold_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
rec_label = tk.Label(main_frame, text="", font=bold_font, justify="center")
rec_label.grid(row=9, column=0, columnspan=2, pady=(10, 5))

# Create a label for CFD suggestion
cfd_label = tk.Label(main_frame, text="", font=("Helvetica", 10, "italic"), justify="center")
cfd_label.grid(row=10, column=0, columnspan=2, pady=(5, 10))

# Start the GUI event loop
root.mainloop()
