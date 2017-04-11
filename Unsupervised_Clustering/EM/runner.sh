ARGS=(
     "../generator/out/File100.tsv 3000 2 2 1"
     "../generator/out/File100.tsv 3000 2 3 1"
     "../generator/out/File100.tsv 3000 2 6 1"
     "../generator/out/File100.tsv 3000 2 8 1"
 
     "../generator/out/File101.tsv 3000 2 2 1" 
     "../generator/out/File101.tsv 3000 2 3 1" 
     "../generator/out/File101.tsv 3000 2 6 1" 
     "../generator/out/File101.tsv 3000 2 8 1" 
 
     "../generator/out/File102.tsv 3000 2 2 1"
     "../generator/out/File102.tsv 3000 2 3 1" 
     "../generator/out/File102.tsv 3000 2 6 1" 
     "../generator/out/File102.tsv 3000 2 8 1" 
 
     "../generator/out/File103.tsv 3000 2 2 1"
     "../generator/out/File103.tsv 3000 2 3 1"
     "../generator/out/File103.tsv 3000 2 6 1"
     "../generator/out/File103.tsv 3000 2 8 1"

     "../generator/out/File104.tsv 5000 2 5 1"
     "../generator/out/File105.tsv 5000 2 5 1"
     "../generator/out/File106.tsv 5000 2 5 1"
     "../generator/out/File107.tsv 5000 2 5 1"
 
     "../generator/out/File108.tsv 10000 2 10 1"
     "../generator/out/File109.tsv 10000 2 10 1"
     "../generator/out/File110.tsv 10000 2 10 1"
     "../generator/out/File111.tsv 10000 2 10 1"
 
     "../generator/out/File200.tsv 5000 2 5 1"
     "../generator/out/File201.tsv 5000 2 5 1"
     "../generator/out/File202.tsv 5000 2 5 1"
 
     "../generator/out/File300.tsv 5000 2 5 1"
 	
     "../generator/out/File400.tsv 500 2 5 1"
     "../generator/out/File401.tsv 5000 2 5 1"
     "../generator/out/File402.tsv 50000 2 5 1"
)

for j in `seq 1 50`;
	do
    for i in "${ARGS[@]}";
        do
        echo "$j $i" && ./a.out $i
	done
done
