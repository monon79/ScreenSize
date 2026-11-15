# SoilLab

SoilLab is a Streamlit application for sieve-analysis calculations, particle-size distribution curves, and preliminary well-screen / gravel-pack design support.

## 1. Open the project in VS Code (Windows)

1. Download and extract the SoilLab ZIP file.
2. Open **Visual Studio Code**.
3. Select **File → Open Folder** and choose the extracted `SoilLab` folder (the folder containing `app.py`).
4. If VS Code asks whether you trust the authors, choose **Trust** only if this is the project you downloaded.
5. Open **Terminal → New Terminal**. The terminal should show the SoilLab folder path.

Install the Microsoft **Python** extension in VS Code if it is not already installed (Extensions icon → search `Python` → Microsoft → Install).

## 2. Set up Python (one-time per project folder)

Check Python: 

```powershell
py -3.12 --version
```

Create a virtual environment: 

```powershell
py -3.12 -m venv .venv
```

Install packages into that environment: 

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

In VS Code, press `Ctrl+Shift+P`, choose **Python: Select Interpreter**, and select the interpreter inside this project's `.venv` folder.

## 3. Run SoilLab

In the VS Code terminal, run:

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

Keep the terminal open. Streamlit will show a local address, normally `http://localhost:8501`. Open that address in your browser. To stop the app, click the terminal and press `Ctrl+C`.

If you already have a working Python setup and do not want a virtual environment, use `py -3.12 -m pip install -r requirements.txt`, then `py -3.12 -m streamlit run app.py`.

## 4. Excel input format

The workbook must contain these column names: `sieve_mm` and `retained_g`. Use millimetres for sieve opening, grams for retained mass, and `0` for the pan.

| sieve_mm | retained_g |
|---:|---:|
| 4.75 | 25 |
| 2.00 | 45 |
| 0.425 | 110 |
| 0.250 | 90 |
| 0.150 | 100 |
| 0.075 | 80 |
| 0.0 | 50 |

## 5. Publish a public website

The project can be deployed using Streamlit Community Cloud. Push the project files (not the ZIP file) to a GitHub repository, then create an app at https://share.streamlit.io/ using the repository, branch, and `app.py` as the entrypoint.

## Engineering limitations

- This is a preliminary calculation and educational design-support tool, not a certified well-design package.
- The automatic well-selection logic follows the current interpretation of the user's lecture-slide criteria: homogeneous/uniform formation AND Cu < 3 AND D10 < 0.25 mm, OR an interpreted upper natural-well slot estimate (0.70 × D70) below 0.75 mm. Confirm the interpretation against the original slide/instructor before using it.
- The app displays the interpreted natural-well slot interval as 0.40 × D40 to 0.70 × D70. Confirm this convention before construction.
- Filter-pack D30 is selected at 4, 5, or 6 times aquifer D30. The generated lognormal curve is theoretical; test actual filter-pack material by sieve analysis.
- Do not combine dissimilar aquifer strata into one gradation curve. Analyse each relevant screened interval separately.
- Final design must consider formation stability, fines migration, screen retention, open area, entrance velocity, corrosion, structural strength, development, and manufacturer tolerances.
