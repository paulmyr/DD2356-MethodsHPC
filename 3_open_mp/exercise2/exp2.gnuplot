set terminal pngcairo size 800,600 enhanced font 'Arial,12'
set output 'exp2.png'

set title 'Bandwidth (Copy Kernel) vs Schedule Type with 128 Threads'
set xlabel 'Schedule Type'
set ylabel 'Bandwidth (MB/s)'
set grid

# set style data yerrorlines
set boxwidth 0.5
set style fill solid
set yrange [*:*]

set xtics ("static" 0, "dynamic" 1, "guided" 2)

plot 'exp2.dat' using ($0):2 with boxes title 'Bandwidth' lc rgb "skyblue", \
     '' using ($0):2:3 with yerrorbars title 'Std' lc rgb "black"
