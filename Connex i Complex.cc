#include <iostream>
#include <vector>
#include <stack>

using namespace std;

void leer_grafo(vector<vector<int>>& grafo, const int& n) {
	
	for (int i = 0; i < n; ++i) {
	   int vecino;
	   int node;
	   cin >> node;
	   while (cin >> vecino and vecino != -1) {
			grafo[node].push_back(vecino);
			grafo[vecino].push_back(node);
	   }
		
	}

}


void escribir_grafo(const vector<vector<int>>& grafo) {
	int n = grafo.size();
	cout << "El nombre de nodes es: " << n << endl;
	
	for (int i = 0; i < n; ++i) {
	   cout << i << ":";
	   for (int j : grafo[i]) {
	   		cout << " " << j; 
		}
	   cout << endl;
	}
	
}


void cycles(const vector<vector<int> > &M, vector<bool> &visited, vector<int> &altura, const int &node, int &height, int &nr_cycles, int ant) {
	altura[node] = height;
	++height;
	visited[node] = true;	
	
	for (int j = 0; j < M[node].size(); ++j) {   

		int v = M[node][j];
		if (v != ant) { 
		  if (visited[v] == true and altura[v] < altura[node]) {
			++nr_cycles;
		  }
		  if (visited[v] == false) cycles(M, visited, altura, v, height, nr_cycles, node);
		}
	}
}

void dfs(const vector<vector<int> > &M, vector<bool> &visitats, const int &node) {
	stack<int> S;
	S.push(node);
	visitats[node] = true;
	int m = M[0].size();
	
	while (not S.empty()) {
		 int currentNode = S.top();
		 S.pop();
		 for (int j = 0; j < M[currentNode].size(); ++j) {
		    int l = M[currentNode][j];
		    if (not visitats[l] and l) {
			  S.push(l);
			  visitats[l] = true;
		    }
		 }
	}
}

pair<int, bool> countCC(const vector<vector<int> > &M) {
	int cc = 0;
	int n = M.size();
	vector<bool> visitats(n, false);
	bool complexes = true;
	
	for (int i = 0; i < n; ++i) {
	   if (not visitats[i]) {
		 dfs(M, visitats, i);
		 ++cc;	
		 if (complexes) {
		   vector<int> altura(n, 1); 
		   vector<bool> visited (n, false);
		   int a = 1;
		   int nr_c = 0;
		   cycles(M, visited, altura, i, a, nr_c, -1);
		   cout << "nr_c : " << nr_c << endl;
		   
		   if (nr_c <= 1) complexes = false;
			
		}
	   }
	}
	return make_pair(cc, complexes);
}

int main() {
	int n;
	cin >> n;
	
	vector<vector<int>> graph(n);
	leer_grafo(graph, n);
	escribir_grafo(graph);
	pair <int, bool> p  = countCC(graph);
	if (p.second == true) cout << "El nombre de components connexes del graf es : " << p.first << " El graf es complex" << endl;
	else cout << "Nombre de components connexes del graf: " << p.first << " El graf no es complex" << endl;

	
}
