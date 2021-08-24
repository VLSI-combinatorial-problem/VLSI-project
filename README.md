# VLSI project

We  aim  at  comparing  Constraint  Programming  (CP)  and 
SatisfiabilityModulo  Theories  (SMT)  techniques  in  order  to  solve 
problems  of  Very  Large  ScaleIntegration  (VLSI).    
We  have  built  two  models:  one  using  MiniZinc  with  the  standard CP
theory  while  the  other  one  employes  a  similar  problem  model  expressed  
in  First Order  Logic  with  new  specific  contraints.   
A particular implementation in SAT is also available.

## Table of Contents

* [About the Project](#about-the-project)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
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



