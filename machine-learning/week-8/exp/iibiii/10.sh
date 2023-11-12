count=$1
pref=exp/iibiii/$count
if [ ! -f $pref.history.csv ]; then
	python src/iibiii.py \
		--train-size $count \
		--output-history-csv $pref.history.csv \
		--save-model-to $pref.model.h5 \
		--l1-reg 0.001
fi

python  src/iibiii_plot.py \
	--history-csv $pref.history.csv \
	--fig $pref.acc-loss.pdf
