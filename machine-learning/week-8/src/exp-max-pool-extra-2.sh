set -e
for count in 50000; do
	pref=exp/max-pool-extra-2/$count
	if [ ! -f $pref.history.csv ]; then
		python src/iibiii.py \
			--train-size $count \
			--output-history-csv $pref.history.csv \
			--save-model-to $pref.model.h5 \
			--save-fit-time $pref.time.txt \
			--evaluation-file $pref.eval \
			--max-pool \
			--extra-layers \
			--extra-layers-2 \
			--l1-reg 0.0001 | tee $pref.log
	fi
	
	python  src/iibiii_plot.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss.pdf \
		--suptitle "MaxPool with $count training samples and \$L_1=0.0001\$ and 2 extra modules"
done
