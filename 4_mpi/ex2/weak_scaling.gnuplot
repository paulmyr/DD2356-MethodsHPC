set terminal pngcairo size 800,600 enhanced font 'Arial,12'
set output 'weak_scaling.png'

set title 'Weak scaling'
set xlabel 'Array size N'
set ylabel 'Runtime (s)'
set grid

plot 'weak_scaling.dat' using 1:2 with linespoints 
