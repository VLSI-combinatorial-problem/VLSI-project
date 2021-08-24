%%%  CP for VLSI problem  %%%
include "globals.mzn";
include "cumulative.mzn";
include "lex_lesseq.mzn";
include "diffn.mzn";


int: w;  % maximum width (param)
int: n;  % number of chips (param)
set of int: CHIPS = 1..n;  % macro for range 1 to n
array[CHIPS] of int: chips_w;  % chips' widths (param)
array[CHIPS] of int: chips_h;  % chips' heigth (param)

int: max_h = sum(chips_h);  % device length upper bound
int: chips_total_area = sum(k in CHIPS)(chips_w[k] * chips_h[k]);
int: min_h = chips_total_area div w;  % device length lower bound

var min_h..max_h: h;  % device length (var)
array[CHIPS] of var 0..w - min(chips_w): x_positions;  % chips coordinates x (var)
array[CHIPS] of var 0..max_h - min(chips_h): y_positions;  % chips coordinates y (var)

%%% Base Contraints

constraint cumulative(y_positions, chips_h, chips_w, w); % Cumulative task fixed w

%constraint forall(i in 2..n, j in 1..i-1)(
%y_positions[i] + chips_h[i] <= y_positions[j] 
%\/ y_positions[j] + chips_h[j] <= y_positions[i] 
%\/ x_positions[i] + chips_w[i] <= x_positions[j]
%\/ x_positions[j] + chips_w[j] <= x_positions[i]); % do not overlap

constraint diffn_nonstrict(x_positions, y_positions, chips_w, chips_h);

constraint max(i in CHIPS)(chips_h[i] + y_positions[i]) <= h; % Respect device heigth
constraint max(i in CHIPS)(chips_w[i] + x_positions[i]) <= w; % Respect device width

% IMPLIED
%constraint forall(u in 0..w-min(chips_w))(sum(i in CHIPS)(if (x_positions[i]<= u /\ x_positions[i] + chips_w[i] > u) then chips_h[i] else 0 endif) <= h);

%constraint symmetry_breaking_constraint(
%  lex_lesseq([x_positions[k] | k in CHIPS], [w - x_positions[k] - chips_w[k] | k in CHIPS])
%);


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
    "Problem solution h = ", show(h), "\n",
];








