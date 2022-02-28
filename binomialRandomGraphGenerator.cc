#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <cstdlib>
#include <ctime>

using namespace std;

const void printMatrix(const vector<vector<int> > &M)
{
	int n = M.size();
	int m = M[0].size();
	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j < m; ++j)
		{
			cout << M[i][j];
		}
		cout << endl;
	}
}

int generateNumber(float p) {
	if((float(rand()) / float(RAND_MAX))<p) return 1;
    return 0;
}

vector< vector<int> > binomialRandomGraphGenerator(int n, float p)
{ 
    vector< vector<int> > G(n, vector<int> (n, 0));
    srand((int)time(0));
    for(int i = 0; i<n; ++i){
        for(int j = i; j<n; ++j){
            if(i==j) G[i][j] = 1;
            else{
                G[i][j] = generateNumber(p);
                G[j][i] = G[i][j];
            }
        }
    }
    return G;
}

int main()
{
	int n;
    float p;
    cout << "Introdueix n i p del graf G(n, p): " << endl;
    cin >> n >> p;
	vector< vector<int> > G = binomialRandomGraphGenerator(n, p);
	printMatrix(G);

}