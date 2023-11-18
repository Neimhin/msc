for f in exp/iibiii/*.history.csv; do
        samples=${f%%.*}
        samples=${samples##*/}
        final_results=`tail -1 $f`
        echo $samples,$final_results
done
