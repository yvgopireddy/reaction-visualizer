# app.py — Reaction Energy Visualizer (Streamlit)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

R = 8.314  # J/(mol*K)


def arrhenius_k(Ea_joule, T, A):
    return A * np.exp(-Ea_joule / (R * T))


def make_figs(Ea_kJ=50.0, T_now=298.0, logA=13.0, prod_offset_kJ=-20.0):
    Ea = Ea_kJ * 1000.0
    A = 10 ** logA
    k_now = arrhenius_k(Ea, T_now, A)

    # --- Reaction energy diagram ---
    x = np.linspace(0, 1, 400)
    reactant_energy = 0.0
    product_energy = prod_offset_kJ
    barrier_height = Ea_kJ

    energy = reactant_energy + (product_energy - reactant_energy) * x
    energy += barrier_height * np.exp(-((x - 0.5) / 0.08) ** 2)

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(x, energy, lw=2)
    ax1.fill_between(x, energy, np.min(energy) - 10, alpha=0.05)
    ax1.plot([0.05], [reactant_energy], marker='o')
    ax1.text(0.05, reactant_energy + 2, "Reactant\n(0 kJ/mol)", ha='left')
    ts_y = np.max(energy)
    ax1.plot([0.5], [ts_y], marker='^')
    ax1.text(0.5, ts_y + 2, f"TS\n{barrier_height:.1f} kJ/mol", ha='center')
    ax1.plot([0.95], [product_energy], marker='o')
    ax1.text(0.95, product_energy + 2, f"Product\n{product_energy:.1f} kJ/mol", ha='right')
    ax1.set_title("Reaction Energy Diagram")
    ax1.set_xlabel("Reaction coordinate")
    ax1.set_ylabel("Energy (kJ/mol)")
    ax1.set_ylim(min(product_energy, 0) - 30, barrier_height + 40)
    fig1.tight_layout()

    # --- Arrhenius plot: k vs T ---
    T_vals = np.linspace(200, 1200, 500)
    k_vals = arrhenius_k(Ea, T_vals, A)

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(T_vals, k_vals, lw=2)
    ax2.set_yscale('log')
    ax2.scatter([T_now], [k_now], zorder=5, color='red')
    ax2.annotate(
        f"T = {T_now:.0f} K\nk = {k_now:.3e} s\u207b\u00b9",
        xy=(T_now, k_now), xytext=(10, 10), textcoords='offset points'
    )
    ax2.set_title("Arrhenius Plot: Rate Constant vs Temperature")
    ax2.set_xlabel("Temperature (K)")
    ax2.set_ylabel("Rate constant k (s\u207b\u00b9) [log scale]")
    fig2.tight_layout()

    return fig1, fig2, k_now


def main():
    st.set_page_config(page_title="Reaction Energy Visualizer", layout="wide")
    st.title("\u2697\ufe0f Reaction Energy Visualizer")
    st.write(
        "Explore how activation energy, temperature, and the pre-exponential "
        "factor shape a reaction's energy profile and rate constant, using the "
        "Arrhenius equation."
    )

    st.sidebar.header("Reaction parameters")
    Ea_kJ = st.sidebar.slider("Activation energy Ea (kJ/mol)", 10.0, 200.0, 50.0, 1.0)
    T_now = st.sidebar.slider("Temperature T (K)", 200.0, 1000.0, 298.0, 1.0)
    logA = st.sidebar.slider("log\u2081\u2080(A) \u2014 pre-exponential factor", 8.0, 16.0, 13.0, 0.1)
    prod_offset_kJ = st.sidebar.slider("Product energy offset (kJ/mol)", -100.0, 50.0, -20.0, 1.0)

    fig1, fig2, k_now = make_figs(Ea_kJ, T_now, logA, prod_offset_kJ)

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)
    with col2:
        st.pyplot(fig2)

    st.metric("Rate constant k at current T", f"{k_now:.4e} s\u207b\u00b9")

    with st.expander("About the Arrhenius equation"):
        st.latex(r"k = A \cdot e^{-E_a / RT}")
        st.write(
            "Ea is activation energy, T is temperature in Kelvin, R is the gas "
            "constant (8.314 J/mol\u00b7K), and A is the pre-exponential (frequency) factor."
        )


if __name__ == "__main__":
    main()
