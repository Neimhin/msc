set -e
for count in 10 50000 1000 5000 10000 20000 30000 40000; do
	pref=exp/iibiii/$count
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size $count \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--l1-reg 0.001
	fi
	
	python  src/iibiii_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf
done
