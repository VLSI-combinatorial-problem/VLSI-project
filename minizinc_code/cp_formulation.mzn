%%%  CP for VLSI problem  %%%
include "globals.mzn";
include "cumulative.mzn";


int: w;
int: n;
int: max_h = 12;  %% REMEMBER TO CHANGE
array[1..n] of int: circuits_w;
array[1..n] of int: circuits_h;

var 1..max_h: h;
array[1..n] of var 0..w-1: x_positions;
array[1..n] of var 0..max_h: y_positions;
array[1..max_h, 1..w] of var 0..1: dual;

%%% Base Contraints

constraint cumulative(y_positions, circuits_h, circuits_w, w); % Cumulative task fixing w
constraint cumulative(x_positions, circuits_w, circuits_h, h); % Cumulative task fixing h
constraint forall(i in 2..n, j in 1..i-1)(y_positions[i] + circuits_h[i] <= y_positions[j] \/ y_positions[j] + circuits_h[j] <= y_positions[i] \/ x_positions[i] + circuits_w[i] <= x_positions[j] \/ x_positions[j] + circuits_w[j] <= x_positions[i]); % do not overlap
constraint forall(i in 1..n)(circuits_h[i] + y_positions[i] <= h); % Respect maximum heigth
constraint forall(i in 1..n)(circuits_w[i] + x_positions[i] <= w); % Respect maximum width

%%% Dual

%constraint forall(k in 1..n, i in 1..max_h, j in 1..w)((y_positions[k] + circuits_h[k] >= i /\ y_positions[k] <= i /\ x_positions[k] + circuits_w[k] >= j /\ x_positions[j] <= j) <-> (dual[i, j] = 1));

%%% Impied Contraints



%%% Symmetry breaking


solve minimize h;
