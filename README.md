# Reaction Energy Visualizer

An interactive Streamlit app that visualizes chemical reaction energetics using the Arrhenius equation — see how activation energy, temperature, and the pre-exponential factor shape a reaction's energy profile and rate constant.

## What it does

Given a reaction's activation energy, temperature, pre-exponential factor, and product energy offset, the app generates two plots:

1. **Reaction Energy Diagram** — reactant → transition state → product along the reaction coordinate, with the energy barrier (activation energy) clearly marked.
2. **Arrhenius Plot** — how the rate constant *k* varies with temperature (log scale), with the current operating point highlighted.

## The chemistry behind it

Rate constants are computed from the Arrhenius equation:

```
k = A · exp(−Ea / RT)
```

where `Ea` is activation energy, `T` is temperature in Kelvin, `R` is the gas constant, and `A` is the pre-exponential (frequency) factor.

## Tech stack

- **Python** — core logic
- **Streamlit** — interactive web UI
- **NumPy** — Arrhenius calculations
- **Matplotlib** — energy diagram and rate-constant plots

## Run it locally

```bash
git clone https://github.com/yvgopireddy/reaction-visualizer.git
cd reaction-visualizer
pip install -r requirements.txt
streamlit run app.py
```

## Live demo

[https://reaction-visualizer-kxxv8pzpwfdfve3ofzxd7g.streamlit.app/]

## Possible next steps

- Compare two reactions side by side (e.g. catalyzed vs. uncatalyzed)
- Let users input a custom energy profile instead of the built-in Gaussian barrier shape
- Export the generated diagrams as images
