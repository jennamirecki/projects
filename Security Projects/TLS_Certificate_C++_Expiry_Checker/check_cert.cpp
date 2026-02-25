#include <iostream>
#include <cstdlib>
#include <iomanip>
#include <string>
#include <memory>   
#include <sstream>
using namespace std;

string getCertificate(const string &website) {
    string command = "cmd /c \"openssl s_client -servername " + website + " -connect "+ website+":443 < NUL 2>&1 | openssl x509 -noout -dates\"";
    char buffer[256];
    string result = "";
    unique_ptr<FILE, decltype(&_pclose)> pipe( _popen(command.c_str(),"r"),_pclose);
    if (!pipe) {
        return "Error: Could not open pipe";
    }
    
    while (fgets(buffer, sizeof(buffer), pipe.get()) !=nullptr) {
        result += buffer;
    }
    
    return result;
}

int main() 
{   
    string website;
   cout << "Enter a website:";
   cin >> website;
   cout << endl;
   string output = getCertificate(website);
   cout << "Website certificate information:" <<" " <<output << endl;
   cout << endl;
    
   int pos = output.find("notAfter=");
   string notAfter = output.substr(pos+ 9, 20);

   tm time1 ={};
   istringstream(notAfter) >> get_time(&time1,"%b %d %H:%M:%S %Y");
   time_t certTime = _mkgmtime(&time1);
   time_t now = time(nullptr);
   if (difftime(certTime,now) < 0) {
        cout << "Certificate is expired!" << endl; 
   }
   else {
        cout << "Certificate is not expired." << endl;
   }
   return 0;
}