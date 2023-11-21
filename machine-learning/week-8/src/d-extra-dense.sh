set -e
for count in 50000; do
	pref=exp/d-extra-dense/$count
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size $count \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--evaluation-file $pref.eval.txt \
			--extra-dense \
			--epochs 20 \
			--l1-reg 0.0001 | tee $pref.log

	fi
	python  src/iibiii_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf \
		--suptitle "Additional Dense(1024) and Dropout(0.5) layers, $count training samples, \$L_1=0.0001\$"
done

