set terminal pngcairo size 800,600 enhanced font 'Arial,12'
set output 'strong_scaling.png'

set title 'Strong scaling'
set xlabel 'Number of nodes'
set ylabel 'Runtime (s)'
set grid

plot 'strong_scaling.dat' using 1:2 with linespoints 
