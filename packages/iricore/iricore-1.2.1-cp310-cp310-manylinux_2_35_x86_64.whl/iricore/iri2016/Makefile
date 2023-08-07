default:
	gfortran -c *.for python_interface.f90 -fPIC -O3 -pg -w
	gfortran test.f90 *.o -fPIC -O3 -w -pg -o libiri2016
	rm *.o
	mv libiri2016 ../