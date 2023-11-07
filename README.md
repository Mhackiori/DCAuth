<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Mhackiori/DCAuth">
    <img src="https://i.postimg.cc/HnXjDFpq/DCAuth.png" alt="Logo" width="350" height="100">
  </a>

  <h1 align="center">Your Battery Is A Blast!</h1>

  <p align="center">Safeguarding Against Counterfeit Batteries with Authentication
    <br />
    <a href="https://arxiv.org/abs/2309.03607"><strong>Preprint available »</strong></a>
    <br />
    <br />
    <a href="https://www.math.unipd.it/~fmarchio/">Francesco Marchiori</a>
    ·
    <a href="https://www.math.unipd.it/~conti/">Mauro Conti</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li>
      <a href="#abstract">Abstract</a>
    </li>
    <li>
      <a href="#citation">Citation</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#flowchart">Flowchart</a>
    </li>
    <li>
      <a href="#datasets">Datasets</a>
    </li>
    <li>
      <a href="#models">Models</a>
    </li>
  </ol>
</details>

<div id="abstract"></div>

## 🧩 Abstract

>Lithium-ion (Li-ion) batteries are the primary power source in various applications due to their high energy and power density. Their market was estimated to be up to 48 billion U.S. dollars in 2022. However, the widespread adoption of Li-ion batteries has resulted in counterfeit cell production, which can pose safety hazards to users. Counterfeit cells can cause explosions or fires, and their prevalence in the market makes it difficult for users to detect fake cells. Indeed, current battery authentication methods can be susceptible to advanced counterfeiting techniques and are often not adaptable to various cells and systems. In this paper, we improve the state of the art on battery authentication by proposing two novel methodologies, **DCAuth** and **EISthentication**, which leverage the internal characteristics of each cell through Machine Learning models. Our methods automatically authenticate lithium-ion battery models and architectures using data from their regular usage without the need for any external device. They are also resilient to the most common and critical counterfeit practices and can scale to several batteries and devices. To evaluate the effectiveness of our proposed methodologies, we analyze time-series data from a total of 20 datasets that we have processed to extract meaningful features for our analysis. Our methods achieve high accuracy in battery authentication for both architectures (up to 0.99) and models (up to 0.96). Moreover, our methods offer comparable identification performances. By using our proposed methodologies, manufacturers can ensure that devices only use legitimate batteries, guaranteeing the operational state of any system and safety measures for the users.

<p align="right"><a href="#top">(back to top)</a></p>
<div id="citation"></div>

## 🗣️ Citation

Please, cite this work when reffering to DCAuth.

```
@misc{marchiori2023battery,
      title={Your Battery Is a Blast! Safeguarding Against Counterfeit Batteries with Authentication}, 
      author={Francesco Marchiori and Mauro Conti},
      year={2023},
      eprint={2309.03607},
      archivePrefix={arXiv},
      primaryClass={cs.CR}
}
```

<p align="right"><a href="#top">(back to top)</a></p>
<div id="usage"></div>

## ⚙️ Usage

First, start by cloning the repository.

```bash
git clone https://github.com/Mhackiori/DCAuth.git
cd DCAuth
```

Then, install the required Python packages by running:

```bash
pip install -r requirements.txt
```

You now need to add the datasets in the repository. You can do this by downloading the zip file [here](https://figshare.com/s/a621342d486cfcc352f7) and extracting it in this repository.

To replicate the results in our paper, you simply need to execute the [Jupyter Notebook](https://github.com/Mhackiori/DCAuth/blob/main/DCAuth.ipynb).

<p align="right"><a href="#top">(back to top)</a></p>
<div id="flowchart"></div>

## 🚥 Flowchart

In the next Figure, we summarize the functioning of the whole system by showing a flowchart of the different steps happening before the authentication response.

![Flowchart](https://i.postimg.cc/KzDMRcPL/04-Flowchart-1.png "Flowchart")

<p align="right"><a href="#top">(back to top)</a></p>
<div id="datasets"></div>

## 📚 Datasets

Here is the list of the datasets used for DCAuth.

| **Name** | **Battery** | **Data** |
|---|---|---|
| Berkley | Sanyo 18650 (LCO/Graphite) | CCCV, MCC, CP-CV, and Boostcharge cy-<br>cles at various C-rates. |
| CALCE_1 | INR 18650-20R (NMC/Graphite) | Low Current and Incremental Current OCV<br>tests, Dynamic Test Profiles. |
| CALCE_2 | ANR26650M1A (LFP) | Low Current OCV tests, Dynamic Test Pro-<br>files. |
| CALCE_3 | CS2 (LCO) | CCCV with different discharging protocols. |
| CALCE_4 | CX2 (LCO) | CCCV with different discharging protocols. |
| CALCE_5 | PL Samples (LCO/Graphite) | CCCV cycles on different SOC ranges. |
| EVERLASTING_1 | INR18650 MJ1 (NMC) | Aged at different C-rated and temperature<br>within a 10-90% SOC window. |
| EVERLASTING_2 | NR18650 MJ1 (NMC) | Aged at different C-rated and temperature<br>within a 10-90% SOC window. |
| HNEI | ICR18650 C2 (LCO/NMC) | Cycled at 1.5C to 100% DOD for more than<br>1000 cycles at room temperature. |
| OX | SLPB533459H4 (LCO) | 1-C charge, 1-C discharge, pseudo-OCV<br>charge, pseudo-OCV discharge. |
| OX_1 | SLPB533459H4 (LCO) | CCCV charge and CCCV discharge. |
| OX_2 | NCR18650BD (NCA) | Different combined profile groups with ref-<br>erence performance tests. |
| SNL | • APR18650M1A (LFP)<br>• NCR18650B (NCA)<br>• LG 18650HG2 (NMC) | Charged at 0.5C, discharged at 3C. Cycled<br>at three different SOC ranges (0-100, 20-80,<br>40-60) at CC or CCCV. |
| TRI_1 | APR18650M1A (LFP/Graphite) | Batteries charged with a one-step or two-<br>step fast-charging policy depending on<br>SOC. |
| TRI_2 | APR18650M1A (LFP/Graphite) | Cells are cycles with one of 224 six-step 10-<br>minutes fast charging protocols. |
| UCL | INR18650 MJ1 (NMC/Graphite) | CC charging at 1.5 A until 4.2 V. Discharging<br>at 4.0 A to 2.5 V. |
| UL-PUR | NCR18650B (NCA) | Discharged to 2.7 V (CC), charged to 4.2 V<br>(CCCV). |

<p align="right"><a href="#top">(back to top)</a></p>
<div id="models"></div>

## 🤖 Models

Here is the list of the models used for DCAuth and their hyperparameters tuned during Grid Search.

| **Models** | **Hyperparameters** |
|---|---|
| AdaBoost (AB) | • Number of estimators |
| Decision Tree (DT) | • Criterion<br>• Maximum Depth |
| Gaussian Naive Bayes (GNB) | • Variance Smoothing |
| Nearest Neighbors (KNN) | • Number of neighbors<br>• Weight function |
| Neural Network (NN) | • Hidden layer sizes<br>• Activation function<br>• Solver |
| Quadratic Discriminant Analysis (QDA) | • Regularization Parameter |
| Random Forest (RF) | • Criterion<br>• Number of estimators |
| Support Vector Machine (SVM) | • Kernel<br>• Regularization parameter<br>• Kernel coefficient |

<p align="right"><a href="#top">(back to top)</a></p>