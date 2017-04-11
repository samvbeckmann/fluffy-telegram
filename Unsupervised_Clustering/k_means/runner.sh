ARGS=(
     "../generator/out/File100.tsv 2 10"
     "../generator/out/File100.tsv 3 10"
     "../generator/out/File100.tsv 6 10"
     "../generator/out/File100.tsv 8 10"
 
     "../generator/out/File101.tsv 2 10" 
     "../generator/out/File101.tsv 3 10" 
     "../generator/out/File101.tsv 6 10" 
     "../generator/out/File101.tsv 8 10" 
 
     "../generator/out/File102.tsv 2 10"
     "../generator/out/File102.tsv 3 10" 
     "../generator/out/File102.tsv 6 10" 
     "../generator/out/File102.tsv 8 10" 
 
     "../generator/out/File103.tsv 2 10"
     "../generator/out/File103.tsv 3 10"
     "../generator/out/File103.tsv 6 10"
     "../generator/out/File103.tsv 8 10"

     "../generator/out/File104.tsv 5 10"
     "../generator/out/File105.tsv 5 10"
     "../generator/out/File106.tsv 5 10"
     "../generator/out/File107.tsv 5 10"
 
     "../generator/out/File108.tsv 10 10"
     "../generator/out/File109.tsv 10 10"
     "../generator/out/File110.tsv 10 10"
     "../generator/out/File111.tsv 10 10"
 
     "../generator/out/File200.tsv 5 10"
     "../generator/out/File201.tsv 5 10"
     "../generator/out/File202.tsv 5 10"
 
     "../generator/out/File300.tsv 5 10"
 	
     "../generator/out/File400.tsv 5 10"
     "../generator/out/File401.tsv 5 10"
     "../generator/out/File402.tsv 5 10"
)

for i in "${ARGS[@]}";
	do
	echo "$i" && python3 artificial_test.py $i
done
