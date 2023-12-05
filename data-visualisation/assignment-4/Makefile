
data/fatalities_isr_pse_conflict_2000_to_2023.csv: data/fatalities_isr_pse_conflict_2000_to_2023.zip
	unzip $<
	mv fatalities_isr_pse_conflict_2000_to_2023.csv data/

data/fatalities_isr_pse_conflict_2000_to_2023.json: data/fatalities_isr_pse_conflict_2000_to_2023.csv
	python src/csv_to_json.py $< $@
