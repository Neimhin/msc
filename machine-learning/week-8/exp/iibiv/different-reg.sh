set -e
for reg in 0.0 0.00001 0.01 100; do
	pref=exp/iibiv/$reg
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size 20000 \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--l1-reg $reg
	fi
	echo plot reg $reg
	python  src/iibiv_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf \
		--suptitle "Training with \$L_1=$reg\$."
done

	echo plot reg 100
	python  src/iibiv_plot_lim.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss-lim.pdf \
		--suptitle "Training with \$L_1=100\$."
