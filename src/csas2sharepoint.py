import subprocess
import glob
import os

# Nastavení cest a parametrů
env_path = "/cesta/k/.env"  # upravte dle potřeby
statements_dir = "statements"
sharepoint_folder = "Shared documents/files"  # upravte dle potřeby

# 1. Stažení výpisů ve formátu ABO
os.makedirs(statements_dir, exist_ok=True)
subprocess.run([
    "csas-statement-downloader",
    statements_dir,
    "abo-standard",
    env_path
], check=True)

# 2. Nahrání ABO souborů na SharePoint
abo_files = glob.glob(f"{statements_dir}/*.abo")
if abo_files:
    subprocess.run([
        "file2sharepoint",
        f"{statements_dir}/*.abo",
        sharepoint_folder,
        env_path
    ], check=True)
else:
    print("Žádné ABO soubory ke nahrání.")
