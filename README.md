# PET Radioactive Source Localization

## Project Overview

### Purpose

This project is a simplified simulation of **Positron Emission Tomography (PET)**, a widely used medical imaging technique for detecting cancerous cells.

In actual PET scans:
- A small amount of radioactive tracer is injected into the patient.
- Cancer cells absorb more of this tracer due to their higher metabolic activity.
- As the tracer decays, it emits pairs of gamma rays in exactly opposite directions.
- Detectors arranged around the patient pick up these coincident gamma rays.
- By analyzing the detection lines, the exact location of the radioactive source (i.e., the cancer cell) can be inferred.

Our goal is to replicate the core idea in a laboratory setup and apply data analysis to localize a radiation source with high precision.

---

## Laboratory Setup

We simulate the presence of one or two radioactive sources inside a box (representing cancer cells). Detectors are placed around the box to pick up radiation. When two detectors simultaneously register radiation (a coincidence), it implies that the source lies on the line connecting them.

Visual overview of the lab setup:

![image](https://github.com/user-attachments/assets/90e8fcf0-4044-42e6-ace4-37fdc6aaf954)

Source: https://2pf.if.uj.edu.pl/z36

Technical scheme of the detection setup:

![image](https://github.com/user-attachments/assets/4f7252b9-afa7-4bd0-9b85-3ecad3e7e76e)

---

## Experiment Procedure

1. One detector is kept fixed, while the other is rotated in steps.
2. For each angle, we count how many gamma ray coincidences are detected.
3. The data is plotted using OriginLab.
4. We then fit a Gaussian distribution to the plot to find the angle with the highest count — this represents the optimal detection alignment.
5. We repeat this process for different positions of the fixed detector.

Example of a Gaussian fit for a double-source setup:

![image](https://github.com/user-attachments/assets/cfe9f645-ea1a-408a-b1cd-7907790e169e)

---

## Data Processing and Source Localization

Each pair of detectors (fixed + rotated) gives us one line on which the radioactive source must lie. With multiple such lines from various measurements, we compute their intersections.

The radioactive source is expected to be located at the intersection of all these lines — the more precise the data, the more concentrated the intersection region.

---

## Technical Implementation

### Programming Approach

We use an object-oriented programming (OOP) approach to organize the analysis pipeline. Key custom classes include:

- `DataHolder`: Stores experimental results and shared data.
- `Plotter`: Handles all visualizations using Matplotlib.
- `LineCalculator`: Responsible for coordinate transformations and intersection computations using linear algebra.

### Tools and Libraries

- Python
- NumPy
- Matplotlib

---

## Example Output

Below is an example of the computed localization for a single radioactive source. All three lines intersect closely at the same point, verifying our approach:

![single_source](https://github.com/user-attachments/assets/2e17594a-18ed-4a8c-861a-67d023cad28e)

Because of how coincidence detection works, the radioactive source must lie on the line connecting the two detectors that registered it. Multiple such lines provide an accurate triangulation of the source's location.

---

## Summary

This project demonstrates how a simplified PET scanner can be simulated and analyzed using physics, programming, and data visualization techniques. It merges medical imaging principles with hands-on experimentation and code-based analysis — offering insights into both physics and real-world healthcare applications.
