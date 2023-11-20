#!/usr/bin/env python

import pandas as pd
import sys
import subprocess
import os

def csv_to_latex_pdf(input_csv, output_pdf="output.pdf"):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_csv)

    # Convert the DataFrame to LaTeX tabular format
    df_to_latex_pdf(df,output_pdf=output_pdf)

def df_to_latex_pdf(df,output_pdf="output.pdf"):
    # Create the tmp directory if it doesn't exist
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        
    latex_tabular = df.to_latex(float_format="%.2f")

    # Wrap the tabular code in a LaTeX document
    latex_document = r"""\documentclass{article}
\usepackage{booktabs}
\begin{document}
\thispagestyle{empty}
    """ + latex_tabular + r"""\end{document}"""

    output_tex = "tmp/output.tex"

    # Save the LaTeX code to a file
    with open(output_tex, 'w') as f:
        f.write(latex_document)

    # Compile the LaTeX file using pdflatex
    subprocess.run(["pdflatex", "-jobname=tmp/output", output_tex])
    subprocess.run(["pdfcrop", "tmp/output.pdf", output_pdf])

    print(f"PDF generated as {output_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input.csv output.pdf")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_pdf = sys.argv[2]
    csv_to_latex_pdf(input_csv, output_pdf)
