#include "compressor_station.h"
#include "input_functions.h"
#include <iostream>

using namespace std;

void CompressorStation::inputForNew(int newId) {
    id = newId;
    name = inputString("Station name: ");
    totalWorkshops = inputInt("Total workshops: ");
    while (true) {
        workingWorkshops = inputInt("Working workshops: ");
        if (workingWorkshops <= totalWorkshops) break;
        cout << "Error! Working workshops cannot exceed total workshops.\n";
    }
}

ostream& operator<<(ostream& os, const CompressorStation& s) {
    double unused = 0;
    if (s.totalWorkshops > 0)
        unused = (1.0 - (double)s.workingWorkshops / s.totalWorkshops) * 100;
    os << "ID: " << s.id << " | " << s.name
        << " | Workshops: " << s.workingWorkshops << "/" << s.totalWorkshops
        << " | Unused: " << unused << "%";
    return os;
}

void CompressorStation::saveToFile(ofstream& ofs) {
    ofs << id << "\n" << name << "\n" << totalWorkshops << " " << workingWorkshops << "\n";
}

bool CompressorStation::loadFromFile(ifstream& ifs) {
    if (!(ifs >> id)) return false;
    ifs.ignore(1000, '\n');
    if (!getline(ifs, name)) return false;
    if (!(ifs >> totalWorkshops >> workingWorkshops)) return false;
    ifs.ignore(1000, '\n');
    return true;
}