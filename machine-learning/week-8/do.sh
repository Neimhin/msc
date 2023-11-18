
pref=exp/iibiv/100
	echo plot reg 100
	python  src/iibiv_plot_lim.py \
		--history-csv $pref.history.csv \
		--fig $pref.acc-loss-lim.pdf \
		--suptitle "Training with \$L_1=100\$."
