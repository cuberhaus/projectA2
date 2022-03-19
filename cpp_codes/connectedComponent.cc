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

void dfs(const vector<vector<int> > &M, vector<bool> &visitats, const int &node)
{
    stack<int> S;
    S.push(node);
    visitats[node] = true;
    int m = M[0].size();
    while (not S.empty())
    {
        int currentNode = S.top();
        S.pop();
        for (int j = 0; j < M.size(); ++j)
        {
            if (not visitats[j] and M[currentNode][j])
            {
                S.push(j);
                visitats[j] = true;
            }
        }
    }
}

int countCC(const vector<vector<int> > &M)
{
    int cc = 0;
    int n = M.size();
    vector<bool> visitats(n, false);
    for (int i = 0; i < n; ++i)
    {
        if (not visitats[i])
        {
            dfs(M, visitats, i);
            ++cc;
        }
    }
    return cc;
}

float generateNumber()
{
    return (float(rand()) / float(RAND_MAX) );
}

int main()
{
    srand((unsigned int)time(NULL));
    vector<vector<int> > graph =
    {
        {0, 1, 1, 1},
        {1, 0, 1, 0},
        {1, 1, 0, 0},
        {1, 0, 0, 0}
    };
    vector<vector<int> > graph2 =
    {
        {0, 0, 0, 0},
        {0, 0, 0, 0},
        {0, 0, 0, 0},
        {0, 0, 0, 0}
    };
    int cc = countCC(graph2);
    cout << "Nombre de components connexes del graf: " << cc << endl;
    printMatrix(graph2);

    cc = countCC(graph);
    cout << "Nombre de components connexes del graf: " << cc << endl;
    printMatrix(graph);
    float f = generateNumber();
    cout << f << endl;
}
