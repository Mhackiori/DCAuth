<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/FrancescoMarchiori/STIXnet">
    <img src="https://i.postimg.cc/6qZmF610/tba-removebg-preview.png" alt="Logo" width="150" height="120">
  </a>

  <h1 align="center">Your Battery is (Not) Safe</h1>

  <p align="center">
    Battery Identification<br />
    <a href="https://github.com/Mhackiori"><strong>Work in progress »</strong></a>
    <br />
    <br />
    <a href="https://www.math.unipd.it/~conti/">Mauro Conti</a>
    ·
    <a href="https://www.math.unipd.it/~fmarchio/">Francesco Marchiori</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#abstract">Abstract</a>
    </li>
    <li>
      <a href="#datasets">Datasets</a>
    </li>
  </ol>
</details>

<div id="abstract"></div>

## 🧩 Introduction

Work in progress.


<div id="datasets"></div>

## 📚 Datasets

| **Dataset** | **Cells** | **Equipment** | **Cycling** | **Temperature** | **Data** |
|---|---|---|---|---|---|
| [CALCE](https://web.calce.umd.edu/batteries/data.htm) | • INR 18650-20R (NMC/Graphite)<br>• ANR26650M1A (LFP)<br>• CS2 (LCO)<br>• CX2 (LCO)<br>• PL Samples (LCO/Graphite)<br>• K2 (LFP) | • Arbin BT2000<br>• Arbin BT2000<br>• Arbin BT2000 and CADEX Battery Tester<br>• Arbin BT2000 and CADEX Battery Tester<br>• Arbin BT2000<br>• N.A. | • 1) Charge to 100%, discharge using a negative pulse current relaxation duration at every 10% SOC, recharge with positive pulse current<br>  2) Charge battery to cut-off voltage of 4.2V at constant current of 1C-rate, charge at constant voltage until its current is reduced to 0.01C, discharge at constant rate of C/20 until the voltage drops to 2.5V, fully charge at constant rate of C/20 to 4.2V<br>  3) Driving profiles performed for 80% battery level and 50% battery level<br>• Run DST and FUDS, run Low Current OCV-SOC test<br>• 1) Constant current of 0.5C<br>  2) Constant current of 1C<br>  3) Constant current discharge alternated between 0.11, 0.22, 0.55, 1.1, 1.65, and 2.2 Amps<br>  4) Constant current discharge of 0.55A, randomized cutoff voltage<br>  5) Full charge and discharge at 0.22A, then cycled between 3.77V and 2.7V with a 0.55A discharge current<br>  6) Full charge and discharge at 0.22A, then cycled between 4.2V and 3.77V with a 0.55A discharge current<br>• 1) Constant current of 0.5C<br>  2) Constant current of 0.5C<br>  3) Constant current discharge of 3C<br>  4) Constant current discharge of 0.5C, cutoff voltage at 2.7V, after charging discharged with pulsed current alternating between 0.5C and 1C until 3.2V<br>  5) Constant current discharge of 1C, cutoff voltage at 2.7V, temperature raised by 10 every 10 cycles<br>  6) Discharge rate of 0.5C for 1m, 5m rest, discharge rate of 1C for 1m, 5m rest, discharge rate of 2C for 1m, 5m rest (repeated until cutoff voltage)<br>• Charged with CCCV profile at C/2, discharged with C/2 current until lower limit for SOC, constant current charge at C/2 until upper limit, 30m relax<br>• Constant current discharge at 2.6A until 4.2 V, constant current charge until current < 0.08A, 3m rest | • 0, 25, 45<br>• -10, 0, 10, 20, 25, 30, 40, 50<br>• N.A.<br>• 25<br>• 25<br>• N.A. | Driving Profiles: Dynamic stress test DST, Federal Urban Driving Schedule FUDS, US06 Highway Driving Schedule, and Beijing Dynamic Stress Test BJDST |
| [TRI](https://data.matr.io/1/) | • APR18650M1A (LFP/Graphite) | Arbin LBT 48ch (Cycling) | • CC-CV charge until 80% SOC with one of 72 different one-step and two-step charging policies, CC-CV discharge at 4C to 2V with cutoff of C/50<br>• 107 different charging protocols depending on fixed SOC ranges | 30 |  |
| [SANDIA](https://www.batteryarchive.org/snl_study.html) | • APR18650M1A (LFP/Graphite)<br>• NCR18650B (NCA)<br>• 18650HG2 (NMC) | Arbin LBT21084 | Charged at 0.5C rate, different combinations of depth of discharge, discharge rate, and temperature<br>- DOD $\in$ [20%-80%, 40%-60%, 0%-100%]<br>- Discharge Rate $\in$ [0.5C, 1C, 2C, 3C (except NCA)] | 15, 25, 35 |  |
| [Oxford](https://howey.eng.ox.ac.uk/data-and-code/) | • SLPB533459H4 (LCO)<br>• NCR18650BD (NCA) | Maccor 4200 | 1-C and pseudo-OCV cycles recorded every 100 cycles of drive cycles | 40 |  |
| [HNEI](https://www.batteryarchive.org/study_summaries.html) | • ICR18650 C2 (LCO/NMC) | Multi-channel Arbin battery tester | Cycled at 1.5C to 100% DOD for more than 1000 cycles | 5 - 45 |  |
| [EVERLASTING_1](https://dx.doi.org/10.4121/14377295) | • INR18650 MJ1 (NMC) | Maccor, Scienlab (Drive Profiles) |  | 0, 10, 25, 45 | Driving profiles recorded by VOLTIA |
| [EVERLASTING_2](https://doi.org/10.4121/14377184) | • INR18650 MJ1 (NMC) | Maccor |  |  |  |
<!--| [KIT](https://dx.doi.org/10.5445/IR/1000094469) | • N.A. (NMC/Graphite) |  SM-500-C90 (Inverter) |  |  | Battery system composed by batteries, inverted and BMS connected to a CAN bus |-->
| [UCL](https://dx.doi.org/10.5522/04/12159462.v1) | • INR18650 MJ1 (NMC/Graphite) | Maccor |  |  |  |
| [Berkley](https://datadryad.org/stash/dataset/doi:10.6078/D1MS3X) | • Sanyo 18650 (LCO/Graphite) |  |  |  |  |
<!--| [Zhang](https://doi.org/10.17632/c5dxwn6w92.1) | • N.A. (NMC/Graphite) |  |  |  |  |-->
<!--| [Diao](https://doi.org/10.17632/c35zbmn7j8.1) | • N.A. (LCO/Graphite) |  |  |  |  |-->
<!--| [Burzynski](https://dx.doi.org/10.17632/k6v83s2xdm.1) | • ICR18650-26F (NMC/Carbon) |  |  |  |  |-->