#ifndef MANAGER_H
#define MANAGER_H

#include "pipe.h"
#include "compressor_station.h"
#include <unordered_map>
#include <vector>
#include <string>

class Manager {
private:
    std::unordered_map<int, Pipe> pipes;
    std::unordered_map<int, CompressorStation> stations;
    int nextPipeId = 1;
    int nextStationId = 1;

public:
    void addPipe();
    void addStation();
    void viewAll();
    void batchEditPipes();
    void saveToFile();
    void loadFromFile();
    void deletePipe();
    void deleteStation();
    void showMenu();
    void run();
};

#endif