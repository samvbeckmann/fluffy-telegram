objects := runner.cpp SVM/SMO.cpp
CFLAGS=-std=c++14 -O3 -larmadillo

analyzermake: $(objects)
	g++ $(CFLAGS) -g -o runner.out $(objects)
