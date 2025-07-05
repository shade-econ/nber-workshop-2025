# Spring 2025 NBER workshop
This repository provides materials and code for the Spring 2025 heterogeneous-agent macro workshop at the NBER.

Slides for each lecture are included below. Most lectures have accompanying notebooks, with code that generates the figures from the slides, or otherwise illustrates the methods of the lecture. Some notebooks require support files that are also contained in the `notebooks/` folder.

Aside from lectures 1 and 3, which use code introduced here, all lecture notebooks and tutorials require installing the [sequence-space Jacobian toolkit](https://github.com/shade-econ/sequence-jacobian). All code is in Python and requires the standard numerical Python libraries (`numpy`, `scipy`, `matplotlib`, `numba`, `pandas`).

Three key references for the lectures are:
* [Fiscal and Monetary Policy with Heterogeneous Agents](https://shade-econ.github.io/annual-review/annual_review_hank.pdf) [[repo](https://github.com/shade-econ/annual-review)], forthcoming in the Annual Review of Economics. This introduces the canonical model, with a calibration similar to the one we use in most of our early lectures, and covers a variety of fiscal and monetary policy exercises.
* [The Intertemporal Keynesian Cross](https://shade-econ.github.io/ikc/ikc.pdf) [[repo](https://shade-econ.github.io/ikc/)], Journal of Political Economy (Dec 2024). This covers fiscal policy, intertemporal MPCs, and the intertemporal Keynesian cross framework in more depth.
* [Using the Sequence-Space Jacobian to Solve and Estimate Heterogeneous-Agent Models](https://shade-econ.github.io/sequence_space_jacobian.pdf), Econometrica (Sep 2021). This covers sequence-space Jacobians as a solution tool, including the fake news algorithm, solving general equilibrium models using DAGs, and estimation.

Feel free to also check out the material from the [spring 2023 NBER workshop](https://github.com/shade-econ/nber-workshop-2023).

# Lectures

### Wednesday, June 4
1. [The Standard Incomplete Markets (SIM) Model](https://shade-econ.github.io/nber-workshop-2025/lecture1_sim.pdf), Matthew Rognlie. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture1_sim.ipynb)]
   
     * For more on computation and the SIM model, see [supplementary notebook on computation](https://github.com/shade-econ/nber-workshop-2025/blob/main/supplements/sim_steady_state_computation.ipynb) and [accompanying video lectures from a previous year](https://github.com/shade-econ/nber-workshop-2023/tree/main?tab=readme-ov-file#first-lecture-online). Also see the [additional notebook on speeding up code](https://github.com/shade-econ/nber-workshop-2025/blob/main/supplements/sim_steady_state_speed.ipynb). The two notebooks explain the details of [`sim_steady_state.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/sim_steady_state.py) and [`sim_steady_state_fast.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/sim_steady_state_fast.py), two modules for basic SIM steady-state computation.

2. [Intro to HANK: Fiscal Policy](https://shade-econ.github.io/nber-workshop-2025/lecture2_fiscalpolicy.pdf), Ludwig Straub. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture2_fiscal.ipynb)] [key papers: [IKC](https://shade-econ.github.io/ikc/ikc.pdf) and [Annual Review](https://shade-econ.github.io/annual-review/annual_review_hank.pdf)]

3. [Intro to the Sequence Space and Jacobians](https://shade-econ.github.io/nber-workshop-2025/lecture3_sequence_space.pdf), Matthew Rognlie. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture3_sequence_space.ipynb)] [key paper: [SSJ](https://shade-econ.github.io/sequence_space_jacobian.pdf)]

   * See end of notebook for hands-on implementation of fake news algorithm, which is generalized in [`sim_fake_news.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/sim_fake_news.py). Also see [note from a previous class](https://mrognlie.github.io/econ411-3/econ411_3_lecture7_supplement.pdf) explaining the algorithm.

4. [Intro to HANK: Monetary Policy](https://shade-econ.github.io/nber-workshop-2025/lecture4_monetary.pdf), Adrien Auclert. [key paper: [Annual Review](https://shade-econ.github.io/annual-review/annual_review_hank.pdf)]

5. [Tutorial 1: Intro to HANK](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%201%20Intro%20to%20HANK%20no%20blanks.ipynb), Ludwig Straub. [[version with blanks](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%201%20Intro%20to%20HANK%20with%20blanks.ipynb)]

### Thursday, June 5
6. [Tutorial 2: SSJ approach and toolkit](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%202%20SSJ%20approach%20and%20toolkit.ipynb), Matthew Rognlie. [[version with blanks](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%202%20SSJ%20approach%20and%20toolkit%20with%20blanks.ipynb)]

7. [Monetary Policy Topics](https://shade-econ.github.io/nber-workshop-2025/lecture5_monetary_topics.pdf), Adrien Auclert. [key paper: [Annual Review](https://shade-econ.github.io/annual-review/annual_review_hank.pdf)]

8. [Estimation](https://shade-econ.github.io/nber-workshop-2025/lecture6_estimation.pdf), Adrien Auclert and Matthew Rognlie. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture6_estimation.ipynb)] [key paper: [SSJ](https://shade-econ.github.io/sequence_space_jacobian.pdf)]

9. [Open Economy](https://shade-econ.github.io/nber-workshop-2025/lecture7_open_economy.pdf), Ludwig Straub. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture7_open_economy.ipynb)] [key paper: [open-economy HANK](https://shade-econ.github.io/ha_oe.pdf)]

10. [Determinacy and Large-Scale Models](https://shade-econ.github.io/nber-workshop-2025/lecture8_determinacy.pdf), Matthew Rognlie. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture8_determinacy.ipynb)] [reference: [determinacy note](https://shade-econ.github.io/ikc/sequence_space_determinacy.pdf)]

11. [HA Models from FRB Economists and Life-Cycle Jacobians](https://shade-econ.github.io/nber-workshop-2025/ha_frb.pdf), Mateo Velasquez-Giraldo. [[repo](https://github.com/Mv77/LC-SSJ_public)]

### Friday, June 6
12. [HANK in Continuous Time](https://shade-econ.github.io/nber-workshop-2025/ha_ctstime.pdf), Adrien Bilal. [[repo](https://github.com/ShlokG/CT-SSJ/)]

13. [Smooth methods for the standard incomplete markets model](https://shade-econ.github.io/nber-workshop-2025/lecture9_smooth.pdf), Matthew Rognlie. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture9_smooth.ipynb)]
    
    * See `notebooks/smooth_sim/` for supporting code; main code in [`smooth_sim.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/smooth_sim/smooth_sim.py)

14. [Second order solutions in sequence space](https://shade-econ.github.io/nber-workshop-2025/lecture10_secondorder.pdf), Adrien Auclert.

15. [Endogenous portfolios and risk premia](https://shade-econ.github.io/nber-workshop-2025/lecture11_portfolios.pdf), Adrien Auclert. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture11_portfolios.ipynb)] [reference: [portfolio note](https://shade-econ.github.io/hank_portfolios_preliminary.pdf)]

16. [Pricing models in the sequence space](https://shade-econ.github.io/nber-workshop-2025/lecture12_pricing_models.pdf), Ludwig Straub. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture12_pricing_models.ipynb)] [key paper: [Phillips curves](https://shade-econ.github.io/new_old_phillips_curves.pdf)]

17. [Information frictions](https://shade-econ.github.io/nber-workshop-2025/lecture13_info_frictions.pdf), Ludwig Straub. [[notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture13_info_frictions.ipynb)] [key paper: [MJMH](https://shade-econ.github.io/mjmh.pdf)]

18. [Optimal long-run policy](https://shade-econ.github.io/nber-workshop-2025/lecture14_optimal_longrun_policy.pdf), Ludwig Straub. [key paper: [Optimal Policy](https://shade-econ.github.io/rss_heterogeneity.pdf)]
