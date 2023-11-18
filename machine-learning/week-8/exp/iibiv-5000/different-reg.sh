set -e
for reg in 0.0 0.000001 0.00001 0.001 0.01 0.1 1 10 100 1000; do
	pref=exp/iibiv-5000/$reg
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size 5000 \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--l1-reg $reg
	fi
	
	python  src/iibiii_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf
done
