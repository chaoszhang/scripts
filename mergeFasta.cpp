#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<unordered_map>

using namespace std;

void add(unordered_map<string, string> &seqs, const string &name, const string &seq, int L){
	seqs[name].resize(L, '-');
	seqs[name] += seq;
}

int main(int argc, char** argv){
	string file;
	ifstream flist(argv[1]);
	unordered_map<string, string> seqs;
	int L = 0;
	while (flist >> file){
		ifstream fin(file);
		string line, name, seq;
		while(getline(fin, line)){
			if (line[0] == '>'){
				if (seq.size()) add(seqs, name, seq, L);
				name = line;
				seq = "";
			}
			else seq += line;
		}
		add(seqs, name, seq, L);
		L += seq.size();
	}

	for (auto &e: seqs){
		e.second.resize(L, '-');
		cout << e.first << endl << e.second << endl;
	}
    return 0;
}