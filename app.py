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

    # Energy diagram
    x = np.linspace(0, 1, 400)
    reactant_energy = 0.0
    product_energy = prod_offset_kJ
    barrier_height = Ea_kJ
    energy = reactant_energy + (product_energy - reactant_energy) * x
    energy += barrier_height * np.exp(-((x - 0.5) / 0.08) ** 2)

    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(x, energy, lw=2)
    ax1.fill_between(x, energy, np.min(energy)-10, alpha=0.05)
    ax1.plot([0.05], [reactant_energy], marker='o')
    ax1.text(0.05, reactant_energy+2, "Reactant\n(0 kJ/mol)", ha='left')
    ts_y = np.max(energy)
    ax1.plot([0.5], [ts_y], marker='^')
    ax1.text(0.5, ts_y+2, f"TS\n{barrier_height:.1f} kJ/mol", ha='center')
    ax1.plot([0.95], [product_energy], marker='o')
    ax1.text(0.95, product_energy+2, f"Product\n{product_energy:.1f} kJ/mol", ha='right')
    ax1.set_title("Reaction Energy Diagram")
    ax1.set_xlabel("Reaction coordinate")
    ax1.set_ylabel("Energy (kJ/mol)")
    ax1.set_ylim(min(product_energy,0)-30, barrier_height+40)

    # Arrhenius k vs T
    T_vals = np.linspace(200,1200,500)
    k_vals = arrhenius_k(Ea, T_vals, A)
    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.plot(T_vals, k_vals, lw=2)
    ax2.set_yscale('log')
    ax2.scatter([T_now], [k_now], zorder=5)
    ax2.set_xlabel("Temperature (K)")
    ax2.set_ylabel("Rate constant k (s^-1) [log scale]")
