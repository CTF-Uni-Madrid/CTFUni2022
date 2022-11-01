#include <bits/stdc++.h>
using namespace std;
bool solve;
int sum, total,n,val;

int coinchange(vector<int>& a, int v, int n, vector<vector<int> >& dp, int steps){
    if(v==0 && steps<=total) solve=true;
    if(solve) return 1;
    if (v == 0) return dp[n][v] = 1;
    if (n == 0) return 0;
    if (dp[n][v] != -1) return dp[n][v];
    if (a[n - 1] <= v) return dp[n][v] = coinchange(a, v - a[n - 1], n, dp,steps+1) + coinchange(a, v, n - 1, dp,steps);
    else  return dp[n][v] = coinchange(a, v, n - 1, dp,steps);
}
int coinchangeBT(vector<int>& a, int v, int n, int steps){
    if(v==0 && steps<=total) solve=true;
    if(solve) return 1;
    if (v == 0) return 1;
    if (n == 0) return 0;
    if (a[n - 1] <= v) return coinchangeBT(a, v - a[n - 1], n,steps+1) + coinchangeBT(a, v, n - 1,steps);
    else  return coinchangeBT(a, v, n - 1,steps);
}
int main() {
    freopen("C:\\Users\\isaac\\Documents\\GitHub\\ciber\\CTFUni\\CandadoInteligente\\flag.txt", "a", stdout);
    for (int i = 0; i < 232; i++) {
        const string path = "C:\\Users\\isaac\\Documents\\GitHub\\ciber\\CTFUni\\CandadoInteligente\\locks\\lock_"+(to_string(i))+".secret";
        freopen(path.c_str(), "r", stdin);
        solve = false;
        scanf("%d %d", &sum, &total);
        scanf("%d", &n);
        vector<int> a;
        for (int x = 0; x < n; x++) {
            scanf("%d", &val);
            a.push_back(val);
        }
        sort(a.begin(), a.end());
        vector<vector<int> > dp(n + 1, vector<int>(sum + 1, -1));
        //coinchange(a, sum, n, dp, 0);
        coinchangeBT(a, sum, n, 0);
        if (solve) cout << 1;
        else cout << 0;
    }
}
