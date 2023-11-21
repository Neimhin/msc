set -e
for count in 1000 5000 10000 20000 40000 50000; do
	pref=exp/d/$count
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size $count \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--evaluation-file $pref.eval.txt \
			--extra-layers \
			--epochs 40 \
			--l1-reg 0.0001 | tee $pref.log

	fi
	python  src/iibiii_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf \
		--suptitle "Two extra layers, $count training samples, \$L_1=0.0001\$"
done

