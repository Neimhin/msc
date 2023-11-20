set -e
pref=exp/d/default
if [ ! -f $pref.history.csv ]; then
	count=40000
	python src/iibiii.py \
		--train-size $count \
		--output-history-csv $pref.history.csv \
		--save-model-to $pref.model.h5 \
		--save-fit-time $pref.time.txt \
		--evaluation-file $pref.eval.txt \
		--extra-layers \
		--l1-reg 0.0001 | tee $pref.log

fi

python  src/iibiii_plot.py \
	--history-csv $pref.history.csv \
	--fig $pref.acc-loss.pdf
