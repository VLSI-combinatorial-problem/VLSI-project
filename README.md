# VLSI project

We  aim  at  comparing  Constraint  Programming  (CP)  and 
SatisfiabilityModulo  Theories  (SMT)  techniques  in  order  to  solve 
problems  of  Very  Large  ScaleIntegration  (VLSI).    
We  have  built  two  models:  one  using  MiniZinc  with  the  standard CP
theory  while  the  other  one  employes  a  similar  problem  model  expressed  
in  First Order  Logic  with  new  specific  contraints.   
A particular implementation in SAT is also available.
Check the [FULL REPORT](/Full_Report.pdf) for all the details.


## Table of Contents

* [About the Project](#about-the-project)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Results](#results)
* [Authors](#authors)


## About The Project
Very Large Scale Integration (VLSI) is a well known problem since the modern
digital electronic was born. The core problem consists in finding the best 
disposition of chips on a circuit plate in order to minimize the overall size 
of the device. In our specific case, we have a fixed plate width for every problem
instance and all the chips that must be included respecting the plates'
size constraints. Then the height of the plate must be minimize.

## Prerequisites
The following python packages have to be installed on the machine in order to run our 
implementation of the models:
* matplotlib
* seaborn
* pandas
* numpy
* minizinc

Follow also the minizinc [guide](https://www.minizinc.org/doc-2.5.5/en/installation.html)
to install the minizinc system in order to use the python minizinc package.

## Usage
All usage information is contained separately for each formulation in the respective
directories, which provide README files: [CP](/CP/README.md) and [SMT](/SMT/README.md)

## Results
CP model performance on 40 VLSI instances:  

<p align='center'>
  <img src="/utils/images/cp_plot.png" />
</p>     

SMT model performance on 40 VLSI instances:
<p align='center'>
  <img src="/utils/images/smt_plot.png" />
</p>     

The SAT model implementation has also an explicative plot 
that shows the disposition of the chips (for more details on SAT check the [FULL REPORT](/Full_Report.pdf)):  

<p align='center'>
  <img src="/utils/images/parallelepiped.png" />
</p>    



## Authors
* [**Alessandro Maggio**](https://github.com/AleTM1)
* [**Serban Cristian Tudosie**](https://github.com/CrisSherban)