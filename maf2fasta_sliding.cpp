#include<iostream>
#include<fstream>
#include<sstream>
#include<unordered_map>
#include<unordered_set>
#include<string>
#include<vector>

using namespace std;

vector<string> lines, names, seqs;
unordered_map<string, int> name2id;
int len;

int getID(string fullname){
	int i = fullname.find_first_of('.');
	string realname = fullname.substr(0, i);
	if (!name2id.count(realname)){
		name2id[realname] = names.size();
		names.push_back(realname);
		string temp;
		for (i = 0; i < len; i++) temp += '-';
		seqs.push_back(temp);
	}
	return name2id[realname];
}

void process(){
	int pos;
	string ref;
	for (int i = 0; i < lines.size(); i++){
		string s0, s1, s4, s6;
		int i2, i3, i5;
		stringstream line(lines[i]);
		line >> s0 >> s1 >> i2 >> i3 >> s4 >> i5 >> s6;
		//cerr << s0 << '\t' << s1 << '\t' << i2 << '\t' << i3 << '\t' << s4 << '\t' << i5 << '\t' << s6 << endl;
		if (i == 0){
			len = i5 + 1;
			pos = i2;
			ref = s6;
		}
		int id = getID(s1);
		for (int j = 0, k = pos; j < ref.size(); j++){
			if (ref[j] != '-') seqs[id][k++] = s6[j];
		}
		//cerr << endl << seqs[id] << endl;
		
	}
	lines.clear();
}

int main(int argc, char** argv){
    ifstream fin(argv[1]);
	string line;
	while(getline(fin, line)){
		if (line[0] == 's') lines.push_back(line);
		if (line[0] == 'a' && lines.size() > 0) process();
	}
	process();
	
	for (int mpos = 0; mpos * 1000000 < seqs[0].size(); mpos++){
		ofstream fout(string(argv[2]) + "." + to_string(mpos));
		for (int i = 0; i < names.size(); i++){
			fout << ">" << names[i] << endl << seqs[i].substr(mpos * 1000000, 1000000) << endl;
		}
	}
    return 0;
}
