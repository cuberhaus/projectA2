#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>
#include <math.h>
#include <unistd.h>
#include <filesystem>

using namespace std;

struct Point {
    double x;
    double y;
};


void escribir_grafo(const vector<vector<int>>& grafo, ofstream& file) {
	int n = grafo.size();
	file << n << endl;
	for (int i = 0; i < n; ++i) {
	   file << to_string(i);
	   for (int j : grafo[i]) {
	   		file << " " << j; 
	   }
	   file << " -1" << endl;
	}
}

const void printPointVector(const vector<Point> &V) {
	int n = V.size();
	for (int i = 0; i < n; i++) cout << "(" << V[i].x << "," << V[i].y << ")" << " ";
    cout << endl;
}

float generateNumber() {
	return (float(rand()) / float(RAND_MAX));
}

Point readPoint() {
    Point a;
    cin >> a.x >> a.y;
    return a;
}

double distance(Point a, Point b) {
    return sqrt(pow(b.x-a.x, 2)+pow(b.y-a.y, 2));
}

vector< vector<int> > binomialRandomGraph(int n, float p) { 
    vector< vector<int> > G(n);
    for (int i = 0; i<n; ++i) {
	   for (int j = i; j<n; ++j) {
		  if (j != i and generateNumber()<=p) G[i].push_back(j);
		}
	}
    
    return G;
}

vector< vector<int> > randomGeometricGraph(int n, float r) { 
    vector<Point> V(n);
    for (int i = 0; i<n; ++i) {
	   V[i].x = generateNumber();
	   V[i].y = generateNumber();
    }
    vector< vector<int> > G(n);
    for (int i = 0; i<n; ++i){
	   for (int j = i; j<n; ++j){
		  if (i != j and distance(V[i], V[j])<=r) {
			G[i].push_back(j);
		  }
	   }
	}
    
//     printPointVector(V);
    return G;
}


void generate_graphs(const int& iterations, string& type_graph) {
	
	filesystem::create_directories(type_graph);
	chdir(&type_graph[0]);
	
	for (int n = 20; n <= iterations; n += 20) {
	   string it1 = to_string(n);
	   for (int i = 1; i <= 100; ++i) {
		  for (int j = 0; j < 20; ++j) {  
		     ofstream file;
			 float p_r = i/100.0;
			 
			 stringstream s;
			 s << p_r;
			 string it2 = s.str();
			 string it3 = to_string(j);
			 
			 //Creates directory of the numbers of nodes 
			 filesystem::create_directories(it1);
	         chdir(&it1[0]);
			 
			 //Creates directory of the numbers of p_r
			 filesystem::create_directories(it2);
	         chdir(&it2[0]);
			 
			 file.open(type_graph+" iteracions: "+it3);
			 // return to directory n
			 chdir("..");
			 
			 vector< vector<int> > G;
			 if (type_graph == "Binomial") G = binomialRandomGraph(n, p_r); 
			 else G = randomGeometricGraph(n, p_r);
		     escribir_grafo(G, file);
			 chdir("..");
		   }
		}
	}
	chdir("..");

}

int main()
{
    srand((int)time(0));
	int iterations;
	
	cout << "Introdueix el nombre de iteracions per generar el graf Binomial" << endl; 
	cout << "(cada iteracio va variant de 20 en 20): " << endl;
	cin >> iterations; 
    
	string type_graph = "Binomial";
	generate_graphs(iterations, type_graph);
	
	cout << "Introdueix el nombre de iteracions per generar el graf Geometric" << endl;
	cout << "(cada iteracio va variant de 20 en 20): " << endl;
	cin >> iterations; 
		
	type_graph = "Geometric";
	generate_graphs(iterations, type_graph);
}
