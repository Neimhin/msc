set -e
for reg in 0.0 0.000001 0.00001 0.001 0.01 0.1 1 10 100 1000; do
	pref=exp/iibiv/$reg
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size 20000 \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--l1-reg 0.001
	fi
	
	python  src/iibiii_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf
done