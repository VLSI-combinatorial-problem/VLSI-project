%%%  CP for VLSI problem  %%%
include "globals.mzn";
include "cumulative.mzn";
include "lex_lesseq.mzn";
include "diffn.mzn";


int: w;  % maximum width (param)
int: n;  % number of chips (param)
set of int: CHIPS = 1..n;  % macro for range 1 to n
array[CHIPS] of int: chips_w;  % chips' widths (param)
array[CHIPS] of int: chips_h;  % chips' height (param)

int: max_h = sum(chips_h);  % device length upper bound (param)
int: chips_total_area = sum(k in CHIPS)(chips_w[k] * chips_h[k]); (tmp param)
int: min_h = chips_total_area div w;  % device length lower bound (param)

var min_h..max_h: h;  % device length (var)
array[CHIPS] of var 0..w - min(chips_w): x_positions;  % chips coordinates x (var)
array[CHIPS] of var 0..max_h - min(chips_h): y_positions;  % chips coordinates y (var)
array[CHIPS] of var bool: rotations; (var)

array[CHIPS] of var 0..max(max(chips_w), max(chips_h)): chips_w_true;  % chips coordinates x (var)
array[CHIPS] of var 0..max(max(chips_w), max(chips_h)): chips_h_true;  % chips coordinates y (var)

%%% ROTATION CONSTRAINTS
constraint forall(i in CHIPS)
((rotations[i] /\ chips_w_true[i] == chips_h[i] /\ chips_h_true[i] == chips_w[i]) 
xor (not(rotations[i]) /\ chips_w_true[i] == chips_w[i] /\ chips_h_true[i] == chips_h[i]));

%%% CONSTRAINTS
constraint cumulative(y_positions, chips_h_true, chips_w_true, w); % Cumulative task fixed w

constraint diffn_nonstrict(x_positions, y_positions, chips_w_true, chips_h_true);

constraint max(i in CHIPS)(chips_h_true[i] + y_positions[i]) <= h; % Respect device height
constraint max(i in CHIPS)(chips_w_true[i] + x_positions[i]) <= w; % Respect device width


%%% Solver

solve :: seq_search([
    int_search(y_positions, first_fail, indomain_min),
    int_search(x_positions, first_fail, indomain_min),
    int_search([h], smallest, indomain_min)])
    minimize h;

%%% Output

output [
    "x positions = ", show(x_positions), "\n",
    "y positions = ", show(y_positions), "\n",
    "Chips height true = ", show(chips_h_true), "\n",
    "Chips width true = ", show(chips_w_true), "\n",
    "Problem solution h = ", show(h), "\n",
    "rotation array = ", show(rotations), "\n"
];
