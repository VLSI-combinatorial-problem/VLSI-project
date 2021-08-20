%%%  CP for VLSI problem  %%%
include "globals.mzn";
include "cumulative.mzn";
include "lex_lesseq.mzn";
include "diffn.mzn";


int: w;  % maximum width (param)
int: n;  % number of circuits (param)
set of int: CIRCUITS = 1..n;  % macro for range 1 to n
array[CIRCUITS] of int: circuits_w;  % circuits' widths (param)
array[CIRCUITS] of int: circuits_h;  % circuits' heigth (param)

int: max_h = sum(circuits_h) - max(circuits_h);  % device length upper bound
int: circuits_total_area = sum(k in CIRCUITS)(circuits_w[k] * circuits_h[k]);
int: min_h = circuits_total_area div w;  % device length lower bound

var min_h..max_h: h;  % device length (var)
array[CIRCUITS] of var 0..w - min(circuits_w): x_positions;  % circuits coordinates x (var)
array[CIRCUITS] of var 0..max_h - min(circuits_h): y_positions;  % circuits coordinates y (var)

%%% Base Contraints

constraint cumulative(y_positions, circuits_h, circuits_w, w); % Cumulative task fixed w
%constraint forall(i in 2..n, j in 1..i-1)(
%y_positions[i] + circuits_h[i] <= y_positions[j] 
%\/ y_positions[j] + circuits_h[j] <= y_positions[i] 
%\/ x_positions[i] + circuits_w[i] <= x_positions[j]
%\/ x_positions[j] + circuits_w[j] <= x_positions[i]); % do not overlap

constraint diffn_nonstrict(x_positions, y_positions, circuits_w, circuits_h);

constraint max(i in CIRCUITS)(circuits_h[i] + y_positions[i]) <= h; % Respect device heigth
constraint max(i in CIRCUITS)(circuits_w[i] + x_positions[i]) <= w; % Respect device width

%%% Dual model

%array[1..max_h, 1..w] of var 0..n: dual;

%constraint symmetry_breaking_constraint(
%    % Channeling constraint
%    forall(i in 1..max_h, j in 1..w, k in CIRCUITS)((dual[i, j] = k) <-> (
%    positions[k, 2] + circuits_h[k] >= i 
%    /\ positions[k, 2] < i 
%    /\ positions[k, 1] + circuits_w[k] >= j 
%    /\ positions[k, 1] < j))
%    % Lexicographic symmetry breaking constraints
%    /\ lex_lesseq([dual[i, j] | i in 1..max_h, j in reverse(1..w)], [dual[i, j] | i in 1..max_h, j in 1..w])
%);

%constraint symmetry_breaking_constraint(
%  lex_lesseq([x_positions[k] | k in CIRCUITS], [w - x_positions[k] - circuits_w[k] | k in CIRCUITS])
%);


%%% Solver

solve :: seq_search([
    int_search(y_positions, first_fail, indomain_min),
    int_search(x_positions, first_fail, indomain_min),
    int_search([h], smallest, indomain_min)])
    minimize h;

%%% Output

output[show(x_positions), "\n" , show(y_positions), "\n", show(h), "\n"];

% output[if i == 1 /\ j == 1 then "[[" else "" endif ++show(dual[i,j])++if i == max_h /\ j == w then "]]" elseif not(i == max_h) /\ j == w then "],\n[" else "," endif | i in 1..max_h, j in 1..w];








