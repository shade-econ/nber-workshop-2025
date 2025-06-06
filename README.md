# Spring 2025 NBER workshop
This repo, still under construction, provides materials and code for the Spring 2025 heterogeneous-agent macro workshop at the NBER. See the [workshop NBER page for an agenda](https://www.nber.org/conferences/heterogeneous-agent-macroeconomics-workshop-spring-2025).

While this repo is under construction, feel free to check out the [repo for the 2023 workshop](https://github.com/shade-econ/nber-workshop-2023).

## Lectures

### Wednesday, June 4
1. [The Standard Incomplete Markets (SIM) Model](https://shade-econ.github.io/nber-workshop-2025/lecture1_sim.pdf), Matthew Rognlie. [[notebook w/figures]](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture1_sim.ipynb)
   
     * For more on computation and the SIM model, see [supplementary notebook on computation](https://github.com/shade-econ/nber-workshop-2025/blob/main/supplements/sim_steady_state_computation.ipynb) and [accompanying video lectures from a previous year](https://github.com/shade-econ/nber-workshop-2023/tree/main?tab=readme-ov-file#first-lecture-online). Also see the [additional notebook on speeding up code](https://github.com/shade-econ/nber-workshop-2025/blob/main/supplements/sim_steady_state_speed.ipynb). The two notebooks explain the details of [`sim_steady_state.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/sim_steady_state.py) and [`sim_steady_state_fast.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/sim_steady_state_fast.py), two modules for basic SIM steady-state computation.

2. [Intro to HANK: Fiscal Policy](https://shade-econ.github.io/nber-workshop-2025/lecture2_fiscalpolicy.pdf), Ludwig Straub. [[notebook w/figures]](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture2_fiscal.ipynb)

3. [Intro to the Sequence Space and Jacobians](https://shade-econ.github.io/nber-workshop-2025/lecture3_sequence_space.pdf), Matthew Rognlie. [[notebook w/figures]](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture3_sequence_space.ipynb).

   * See end of notebook for hands-on implementation of fake news algorithm, which is generalized in [`sim_fake_news.py`](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/sim_fake_news.py). Also see [note from a previous class](https://mrognlie.github.io/econ411-3/econ411_3_lecture7_supplement.pdf) explaining the algorithm.

4. [Intro to HANK: Monetary Policy](https://shade-econ.github.io/nber-workshop-2025/lecture4_monetary.pdf), Adrien Auclert.

5. Tutorial 1: Intro to HANK, Ludwig Straub.
   * Version with blanks: [Notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%201%20Intro%20to%20HANK%20with%20blanks.ipynb) [HTML](https://raw.githack.com/shade-econ/nber-workshop-2025/main/tutorials/Tutorial%201%20Intro%20to%20HANK%20with%20blanks.html
)
   * Version without blanks: [Notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%201%20Intro%20to%20HANK%20no%20blanks.ipynb) [HTML](https://raw.githack.com/shade-econ/nber-workshop-2025/main/tutorials/Tutorial%201%20Intro%20to%20HANK%20no%20blanks.html)

### Thursday, June 5
6. Tutorial 2: SSJ approach and toolkit, Matthew Rognlie.
   * Version with blanks: [Notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%202%20SSJ%20approach%20and%20toolkit%20with%20blanks.ipynb) [HTML](https://raw.githack.com/shade-econ/nber-workshop-2025/main/tutorials/Tutorial%202%20SSJ%20approach%20and%20toolkit%20with%20blanks.html)
   * Version without blanks: [Notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/tutorials/Tutorial%202%20SSJ%20approach%20and%20toolkit.ipynb) [HTML](https://raw.githack.com/shade-econ/nber-workshop-2025/main/tutorials/Tutorial%202%20SSJ%20approach%20and%20toolkit.html)

8. [Monetary Policy Topics](https://shade-econ.github.io/nber-workshop-2025/lecture5_monetary_topics.pdf), Adrien Auclert.

9. [Estimation](https://shade-econ.github.io/nber-workshop-2025/lecture6_estimation.pdf), Adrien Auclert and Matthew Rognlie. [Notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture6_estimation.ipynb)

10. [Open Economy](https://shade-econ.github.io/nber-workshop-2025/lecture7_open_economy.pdf), Ludwig Straub. [Notebook](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture7_open_economy.ipynb)

11. [Determinacy and Large-Scale Models](https://shade-econ.github.io/nber-workshop-2025/lecture8_determinacy.pdf), Matthew Rognlie. [[notebook w/figures]](https://github.com/shade-econ/nber-workshop-2025/blob/main/notebooks/lecture8_determinacy.ipynb)

12. [HA Models from FRB Economists and Life-Cycle Jacobians](https://shade-econ.github.io/nber-workshop-2025/ha_frb.pdf), Mateo Velasquez-Giraldo. [Repo](https://github.com/Mv77/LC-SSJ_public?tab=readme-ov-file)

12. [HANK in Continuous Time](https://shade-econ.github.io/nber-workshop-2025/ha_frb.pdf), Adrien Bilal [Repo](https://github.com/ShlokG/CT-SSJ/)