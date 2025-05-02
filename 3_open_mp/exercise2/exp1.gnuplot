set terminal pngcairo size 800,600 enhanced font 'Arial,12'
set output 'exp1.png'

set title 'Bandwidth vs Number of Threads'
set xlabel 'Threads'
set ylabel 'Bandwidth (MB/s)'
set grid

set style data yerrorlines
set xrange [0:130]
set xtics ( "1" 1, "32" 32, "64" 64, "128" 128 )

plot 'exp1.dat' using 1:2:3 with yerrorlines title 'Bandwidth'
