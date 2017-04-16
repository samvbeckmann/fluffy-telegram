ARGS=(
     "../../Datasets/pop_failures.tsv 50"
     "../../Datasets/banknote_authentication.tsv 50"
     "../../Datasets/diagnostic.tsv 50"
     "../../Datasets/diabetes.tsv 50"
     "../../Datasets/two-spirals.tsv 50"
     "../../Datasets/fertility.tsv 50"
)

for i in "${ARGS[@]}";
	do
	echo "$i" && ../runner.out $i
done
