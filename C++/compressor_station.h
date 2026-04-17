#ifndef COMPRESSOR_STATION_H
#define COMPRESSOR_STATION_H

#include <string>
#include <fstream>

class CompressorStation {
public:
    int id;
    std::string name;
    int totalWorkshops;
    int workingWorkshops;

    void inputForNew(int newId);
    friend std::ostream& operator<<(std::ostream& os, const CompressorStation& s);
    void saveToFile(std::ofstream& ofs);
    bool loadFromFile(std::ifstream& ifs);
};

#endif