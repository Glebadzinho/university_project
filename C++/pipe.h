#ifndef PIPE_H
#define PIPE_H

#include <string>
#include <fstream>

class Pipe {
public:
    int id;
    std::string name;
    double length;
    int diameter;
    bool inRepair;

    void inputForNew(int newId);
    friend std::ostream& operator<<(std::ostream& os, const Pipe& p);
    void saveToFile(std::ofstream& ofs);
    bool loadFromFile(std::ifstream& ifs);
};

#endif