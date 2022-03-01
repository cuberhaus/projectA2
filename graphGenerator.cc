#include <iostream>
#include <vector>
#include <queue>
#include <stack>
#include <cstdlib>
#include <ctime>
#include <math.h>

using namespace std;

struct Point
{
    double x;
    double y;
};


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

const void printPointVector(const vector<Point> &V)
{
	int n = V.size();
	for (int i = 0; i < n; i++) cout << "(" << V[i].x << "," << V[i].y << ")";
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

vector< vector<int> > binomialRandomGraph(int n, float p)
{ 
    vector< vector<int> > G(n, vector<int> (n, 0));
    for(int i = 0; i<n; ++i){
        for(int j = i; j<n; ++j){
            if(i==j) G[i][j] = 1;
            else{
                if(generateNumber()<=p){
                    G[i][j] = G[j][i] = 1;
                }
                else{
                    G[i][j] = G[j][i] = 0;
                }
            }
        }
    }
    return G;
}

vector< vector<int> > randomGeometricGraph(int n, float r)
{ 
    vector<Point> V(n);
    for(int i = 0; i<n; ++i){
        V[i].x = generateNumber();
        V[i].y = generateNumber();
    }
    vector< vector<int> > G(n, vector<int> (n, 0));
    for(int i = 0; i<n; ++i){
        for(int j = i; j<n; ++j){
            if(i==j) G[i][j] = 1;
            else{
                if(distance(V[i], V[j])<=r){
                    G[i][j] = G[j][i] = 1;
                }
                else{
                    G[i][j] = G[j][i] = 0;
                }
            }
        }
    }
    printPointVector(V);
    return G;
}

int main()
{
    srand((int)time(0));
	int n;
    float p, r;
    cout << "Introdueix n i p del graf G(n, p): " << endl;
    cin >> n >> p;
	vector< vector<int> > G = binomialRandomGraph(n, p);
    cout << "Binomial Random Graph:" << endl;
	printMatrix(G);
    
    cout << "Introdueix n i r del graf G(n, r): " << endl;
    cin >> n >> r;
    cout << "Random Geometric Graph:" << endl;
    vector< vector<int> > F = randomGeometricGraph(n, r);
	printMatrix(F);

}