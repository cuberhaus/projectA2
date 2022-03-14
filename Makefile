all: Generador.x Connex_i_Complex.x

Generador.x: Generador.cc
	g++ -std=c++17 Generador.cc -o Generador.x

Connex_i_Complex.x: Connex_i_Complex.cc
	g++ -o Connex_i_Complex.x Connex_i_Complex.cc

clean: 
	rm -r *.x Geometric/ Binomial/ OutGeometric/ OutBinomial/
