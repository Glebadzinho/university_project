#include "input_functions.h"
#include <iostream>

using namespace std;

int inputInt(const string& prompt, int minVal) {
    int x;
    while (true) {
        cout << prompt;
        if (cin >> x && x >= minVal) {
            cin.ignore(1000, '\n');
            return x;
        }
        cout << "Invalid input. Try again.\n";
        cin.clear();
        cin.ignore(1000, '\n');
    }
}

double inputDouble(const string& prompt, double minVal) {
    double x;
    while (true) {
        cout << prompt;
        if (cin >> x && x >= minVal) {
            cin.ignore(1000, '\n');
            return x;
        }
        cout << "Invalid input. Try again.\n";
        cin.clear();
        cin.ignore(1000, '\n');
    }
}

bool inputBool01(const string& prompt) {
    int x;
    while (true) {
        cout << prompt << " (0/1): ";
        if (cin >> x && (x == 0 || x == 1)) {
            cin.ignore(1000, '\n');
            return x == 1;
        }
        cout << "Invalid input. Enter 0 or 1.\n";
        cin.clear();
        cin.ignore(1000, '\n');
    }
}

string inputString(const string& prompt) {
    string s;
    while (true) {
        cout << prompt;
        getline(cin, s);
        if (s.length() > 0) return s;
        cout << "Invalid input. Try again.\n";
    }
}