// file_reader.cpp
// LICENSE: Nothing(do what ever you want!)
#include <iostream>
using namespace std;

int main(int argc, char *argv[]){
    fstream config;
    config.open(argv[1], ios::in);
    if(config){
        cout << "Reading Data" << endl;
        vector<string> data;
        string tmp;
        while(getline(config,tmp)){
            data.push_back(tmp);
        }
        cout << "Redirect to terminal:" << endl;
        for(int i = 0;i < data.size();i++){
            cout << data[i] << endl;
        }
        config.close();
    }
    else{
        cout << "File NOT Found" << endl;
    }
    cout << "Press any key to Continue...";
    cin.clear();
    cin.sync();
    cin.get();
    return 0;
}
