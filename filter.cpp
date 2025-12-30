#include<iostream>
#include<fstream>
#include<string>
#include<vector>

using namespace std;

const int N_STRIDE = 5, STRIDE[N_STRIDE] = {10, 50, 200, 1000, 5000};
const double FP = 0.05;

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
	int n = seqs.size(), len = (seqs[0].size() / STRIDE[N_STRIDE - 1]) * STRIDE[N_STRIDE - 1];
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
	
	vector<bool> strideMask(len / STRIDE[N_STRIDE - 1]);
	vector<int> stride0Uniq(len / STRIDE[0]);
	for (int j = 0; j < len; j++){
		if (cntA[j]) stride0Uniq[j / STRIDE[0]]++;
		if (cntC[j]) stride0Uniq[j / STRIDE[0]]++;
		if (cntG[j]) stride0Uniq[j / STRIDE[0]]++;
		if (cntT[j]) stride0Uniq[j / STRIDE[0]]++;
	}
	
	for (int s = N_STRIDE - 1; s >= 0; s--){
		vector<int> uniqCnt(STRIDE[s] * 2 * 4 + 1);
		int uniqCntTotal = 0;
		vector<int> strideUniq(len / STRIDE[s]);
		for (int j = 0; j < len / STRIDE[0]; j++){
			strideUniq[j * STRIDE[0] / STRIDE[s]] += stride0Uniq[j];
		}
		
		for (int j = 0; j < len / STRIDE[s] - 1; j++){
			if (!strideMask[j] && !strideMask[j + 1]) {
				uniqCnt[strideUniq[j] + strideUniq[j + 1]]++;
				uniqCntTotal++;
			}
		}
		
		vector<int> binCnt(5 * 2 * 4 + 1);
		for (int i = 0; i < STRIDE[s] * 2 * 4 + 1; i++){
			binCnt[i * 5 / STRIDE[s]] += uniqCnt[i];
		}
		for (int i = 0; i < 5 * 2 * 4 + 1; i++){
			cerr << i << " " << binCnt[i] << "\n";
		}
		cerr << endl;
		
		int cnt = uniqCntTotal * FP / 2.0 / N_STRIDE, threshold;
		cerr << "Cnt: " << cnt << endl;
		for (threshold = STRIDE[s] * 2 * 4; threshold > 0; threshold--){
			if (cnt < uniqCnt[threshold]) break;
			cnt -= uniqCnt[threshold];
		}
		cerr << "Threshold: " << threshold << endl << endl;
		
		for (int j = 0; j < len / STRIDE[s] - 1; j++){
			if (strideUniq[j] + strideUniq[j + 1] <= threshold) continue;
			strideMask[j] = true;
			strideMask[j + 1] = true;
		}
		
		if (s > 0){
			vector<bool> newStrideMask(len / STRIDE[s - 1]);
			for (int j = 0; j < len / STRIDE[s - 1] - 1; j++){
				newStrideMask[j] = strideMask[j * STRIDE[s - 1] / STRIDE[s]];
			}
			strideMask = move(newStrideMask);
		}
		else {
			for (int i = 0; i < n; i++){
				for (int j = 0; j < len; j++){
					if (strideMask[j / STRIDE[0]]) seqs[i][j] = 'N';
				}
			}
			
			int maskCnt = 0;
			for (int i = 0; i < strideMask.size(); i++){
				if (strideMask[i]) maskCnt++;
			}
			cerr << "Filter rate: " << maskCnt * 100.0 / strideMask.size() << "%\n";
		}
	}
	
	for (int i = 0; i < n; i++){
		cout << names[i] << endl << seqs[i].substr(0, len) << endl;
	}
	
    return 0;
}