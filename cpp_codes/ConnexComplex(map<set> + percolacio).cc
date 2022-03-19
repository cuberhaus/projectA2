#include <iostream>
#include <vector>
#include <stack>
#include <math.h>
#include <map>
#include <set> 

using namespace std;

void leer_grafo(map<int, set<int>> &grafo, const int& n) {
    for (int i = 0; i < n; ++i) {
        int vecino;
        int node;
        cin >> node;
        set<int> s1;
        set <int> s2;
        s2.insert(node);
        while (cin >> vecino and vecino != -1) {
            s1.insert(vecino);
            grafo.insert(pair<int, set<int>>(vecino, s2));
        }
        pair<map<int,set<int>>::iterator,bool> it;
        it = grafo.insert(pair<int, set<int>>(node, s1));
        if (it.second  == false) grafo[node].insert(s1.begin(), s1.end());
        
    }

}


void escribir_grafo(const map<int, set<int>> &grafo) {
    int n = grafo.size();
    cout << "El nombre de nodes es: " << n << endl;

    for (int i = 0; i < n; ++i) {
        cout << i << ":";
        for (int j : grafo.at(i)) {
            cout << " " << j;
        }
        cout << endl;
    }

}


void cycles(const map<int, set<int>> &M, vector<bool> &visited, vector<int> &altura, const int &node, int &height, int &nr_cycles, int ant) {
    altura[node] = height;
    ++height;
    visited[node] = true;

    for (int j:M.at(node)) {
        if (j != ant) {
          if (visited[j] == true and altura[j] < altura[node]) {
            ++nr_cycles;
          }
        if (visited[j] == false) cycles(M, visited, altura, j, height, nr_cycles, node);
        }
    }
}

void dfs(const map<int, set<int>> &M, vector<bool> &visitats, const int &node) {
    stack<int> S;
    S.push(node);
    visitats[node] = true;

    while (not S.empty()) {
        int currentNode = S.top();
        S.pop();
        for (int j:M.at(currentNode)) {
            if (not visitats[j] and j) {
                S.push(j);
                visitats[j] = true;
            }
        }
    }
}

pair<int, bool> countCC(const map<int, set<int>> &M) {
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

float generateNumber() {
	return (float(rand()) / float(RAND_MAX));
}

void node_percolation(map<int, set<int>> &M, float p) {
    int graph_size = M.size();
    for (int i = 0; i < graph_size; ++i) { 
       float rand = generateNumber();
	   if (rand > p) {
         M.erase(i);
		 int size = M.size();
		 for (int j = 0; j < size; ++j) M[j].erase(i);
		 if (M[i].size() == 0) M.erase(i);	 
	  }
    }
}


void edge_percolation(map<int, set<int>> &M, float p) {
    int graph_size = M.size();
    for (int i = 0; i < graph_size; ++i) { 
       set<int>::iterator it;
		for (it = M[i].begin(); it != M[i].end(); ++it) {
          float rand = generateNumber();
          if (rand > p) {
            int k = *it;
			++it;
			M[i].erase(k);
			M[k].erase(i);
	      }
       }
    }
}



int main() {
    int n;
    cin >> n;
    
    srand((int)time(0));
    map<int, set<int>> graph;
    leer_grafo(graph, n);
    escribir_grafo(graph);
    pair <int, bool> p  = countCC(graph);
    if (p.second == true) cout << "El nombre de components connexes del graf es : " << p.first << " El graf es complex" << endl;
    else cout << "Nombre de components connexes del graf: " << p.first << " El graf no es complex" << endl;


}
