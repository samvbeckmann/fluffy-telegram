ARGS=(
     "../../../Datasets/pop_failures.tsv 50"
)

for i in "${ARGS[@]}";
	do
	echo "$i" && ./runner.out $i
done
