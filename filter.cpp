#include<iostream>
#include<fstream>
#include<string>
#include<vector>

using namespace std;

int STRIDE[3] = {10, 50, 250};
double FP = 0.01;

int main(int argc, char** argv){
	vector<string> names, seqs;
    ifstream fin(argv[1]);
	string line;
	while(getline(fin, line)){
		if (line[0] == '>') {
			names.push_back(line);
			seqs.emplace_back();
		}
		else seqs.back() += line;
	}
	int n = seqs.size(), len = (seqs[0].size() / STRIDE[2]) * STRIDE[2];
	vector<int> cntA(len), cntC(len), cntG(len), cntT(len), cntN(len);
	
	for (int i = 0; i < n; i++){
		for (int j = 0; j < len; j++){
			switch (seqs[i][j]){
				case 'A': case 'a': cntA[j]++; break;
				case 'C': case 'c': cntC[j]++; break;
				case 'G': case 'g': cntG[j]++; break;
				case 'T': case 't': cntT[j]++; break;
				default: cntN[j]++;
			}
		}
	}
	
	for (int s = 2; s >= 0; s--){
		vector<int> strideCnt(len / STRIDE[s]), intervalCnt(STRIDE[s] * 2 * 5 + 1);
		for (int j = 0; j < len; j++){
			if (cntA[j]) strideCnt[j / STRIDE[s]]++;
			if (cntC[j]) strideCnt[j / STRIDE[s]]++;
			if (cntG[j]) strideCnt[j / STRIDE[s]]++;
			if (cntT[j]) strideCnt[j / STRIDE[s]]++;
			if (cntN[j]) strideCnt[j / STRIDE[s]]++;
		}
		
		for (int j = 0; j < len / STRIDE[s] - 1; j++){
			intervalCnt[strideCnt[j] + strideCnt[j + 1]]++;
		}
		
		int cnt = (len / STRIDE[s] - 1) * FP / 2.0 / 3.0, threshold;
		for (threshold = STRIDE[s] * 2 * 5; threshold > 0; threshold--){
			if (cnt < intervalCnt[threshold]) break;
			cnt -= intervalCnt[threshold];
		}
		
		for (int j = 0; j < len / STRIDE[s] - 1; j++){
			if (strideCnt[j] + strideCnt[j + 1] <= threshold) continue;
			for (int i = 0; i < n; i++){
				for (int k = j * STRIDE[s]; k < (j + 2) * STRIDE[s]; k++){
					seqs[i][k] = 'N';
				}
			}
			for (int k = j * STRIDE[s]; k < (j + 2) * STRIDE[s]; k++){
				cntA[k] = 0;
				cntC[k] = 0;
				cntG[k] = 0;
				cntT[k] = 0;
				cntN[k] = n;
			}
		}
	}
	
	for (int i = 0; i < n; i++){
		cout << names[i] << endl << seqs[i].substr(0, len) << endl;
	}
	
    return 0;
}