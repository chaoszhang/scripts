#include<iostream>
#include<fstream>
#include<string>
#include<vector>

using namespace std;

int main(int argc, char** argv){
	vector<string> names, seqs;
	int BLOCKSIZE = 1000000;
    ifstream fin(argv[1]);
	string line;
	while(getline(fin, line)){
		if (line[0] == '>') {
			names.push_back(line);
			seqs.emplace_back();
		}
		else seqs.back() += line;
	}
	
	if (argc > 3) BLOCKSIZE = stoi(argv[3]);
	
	for (int mpos = 0; mpos * BLOCKSIZE < seqs[0].size(); mpos++){
		ofstream fout(string(argv[2]) + "." + to_string(mpos));
		for (int i = 0; i < names.size(); i++){
			fout << names[i] << endl << seqs[i].substr(mpos * BLOCKSIZE, BLOCKSIZE) << endl;
		}
	}
    return 0;
}