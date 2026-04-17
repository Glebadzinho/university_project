#include "pipe.h"
#include "input_functions.h"
#include <iostream>

using namespace std;

void Pipe::inputForNew(int newId) {
    id = newId;
    name = inputString("Pipe name: ");
    length = inputDouble("Length: ");
    diameter = inputInt("Diameter: ");
    inRepair = inputBool01("In repair?");
}

ostream& operator<<(ostream& os, const Pipe& p) {
    os << "ID: " << p.id << " | " << p.name
        << " | Length: " << p.length
        << " | Diameter: " << p.diameter
        << " | Repair: " << (p.inRepair ? "yes" : "no");
    return os;
}

void Pipe::saveToFile(ofstream& ofs) {
    ofs << id << "\n" << name << "\n" << length << " " << diameter << " " << inRepair << "\n";
}

bool Pipe::loadFromFile(ifstream& ifs) {
    int repairFlag;
    if (!(ifs >> id)) return false;
    ifs.ignore(1000, '\n');
    if (!getline(ifs, name)) return false;
    if (!(ifs >> length >> diameter >> repairFlag)) return false;
    inRepair = repairFlag == 1;
    ifs.ignore(1000, '\n');
    return true;
}