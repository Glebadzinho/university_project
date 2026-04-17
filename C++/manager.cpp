#include "manager.h"
#include "input_functions.h"
#include <iostream>
#include <fstream>

using namespace std;

void Manager::addPipe() {
    Pipe p;
    p.inputForNew(nextPipeId++);
    pipes[p.id] = p;
    cout << "Pipe added.\n";
}

void Manager::addStation() {
    CompressorStation s;
    s.inputForNew(nextStationId++);
    stations[s.id] = s;
    cout << "Station added.\n";
}

void Manager::viewAll() {
    cout << "\n=== PIPES ===\n";
    if (pipes.empty()) {
        cout << "No pipes\n";
    }
    else {
        // Используем итераторы вместо structured bindings
        for (auto it = pipes.begin(); it != pipes.end(); ++it) {
            cout << it->second << "\n";
        }
    }

    cout << "\n=== STATIONS ===\n";
    if (stations.empty()) {
        cout << "No stations\n";
    }
    else {
        // Используем итераторы вместо structured bindings
        for (auto it = stations.begin(); it != stations.end(); ++it) {
            cout << it->second << "\n";
        }
    }
}

void Manager::batchEditPipes() {
    if (pipes.empty()) {
        cout << "No pipes to edit.\n";
        return;
    }

    cout << "\n=== BATCH EDIT PIPES ===\n";
    cout << "1. Edit pipe by ID\n";
    cout << "2. Edit all pipes\n";
    cout << "3. Edit pipes filtered by status\n";
    cout << "Choice: ";

    int choice = inputInt("");

    switch (choice) {
    case 1: {
        int id = inputInt("Enter pipe ID: ");
        auto it = pipes.find(id);
        if (it != pipes.end()) {
            bool newStatus = inputBool01("New repair status?");
            it->second.inRepair = newStatus;
            cout << "Pipe updated.\n";
        }
        else {
            cout << "Pipe not found.\n";
        }
        break;
    }
    case 2: {
        bool newStatus = inputBool01("New repair status for ALL pipes?");
        for (auto it = pipes.begin(); it != pipes.end(); ++it) {
            it->second.inRepair = newStatus;
        }
        cout << "All pipes updated.\n";
        break;
    }
    case 3: {
        bool filterStatus = inputBool01("Filter pipes with repair status (0=no, 1=yes)?");
        bool newStatus = inputBool01("New repair status?");

        int count = 0;
        for (auto it = pipes.begin(); it != pipes.end(); ++it) {
            if (it->second.inRepair == filterStatus) {
                it->second.inRepair = newStatus;
                count++;
            }
        }
        cout << "Updated " << count << " pipes.\n";
        break;
    }
    default:
        cout << "Invalid choice.\n";
        break;
    }
}

void Manager::saveToFile() {
    string fname;
    cout << "Filename: ";
    getline(cin, fname);
    ofstream ofs(fname);
    if (!ofs) {
        cout << "Error saving file\n";
        return;
    }

    ofs << pipes.size() << "\n";
    for (auto it = pipes.begin(); it != pipes.end(); ++it) {
        it->second.saveToFile(ofs);
    }

    ofs << stations.size() << "\n";
    for (auto it = stations.begin(); it != stations.end(); ++it) {
        it->second.saveToFile(ofs);
    }

    cout << "Data saved.\n";
}

void Manager::loadFromFile() {
    string fname;
    cout << "Filename: ";
    getline(cin, fname);
    ifstream ifs(fname);
    if (!ifs) {
        cout << "Error loading file\n";
        return;
    }

    pipes.clear();
    stations.clear();

    int n;
    ifs >> n;
    ifs.ignore(1000, '\n');

    int maxPipeId = 0;
    for (int i = 0; i < n; i++) {
        Pipe p;
        if (p.loadFromFile(ifs)) {
            pipes[p.id] = p;
            if (p.id > maxPipeId) maxPipeId = p.id;
        }
    }
    nextPipeId = maxPipeId + 1;

    ifs >> n;
    ifs.ignore(1000, '\n');

    int maxStationId = 0;
    for (int i = 0; i < n; i++) {
        CompressorStation s;
        if (s.loadFromFile(ifs)) {
            stations[s.id] = s;
            if (s.id > maxStationId) maxStationId = s.id;
        }
    }
    nextStationId = maxStationId + 1;

    cout << "Data loaded. Next Pipe ID: " << nextPipeId
        << ", Next Station ID: " << nextStationId << "\n";
}

void Manager::deletePipe() {
    int id = inputInt("Enter pipe ID to delete: ");
    if (pipes.erase(id)) {
        cout << "Pipe deleted.\n";
        // Находим максимальный ID среди оставшихся труб
        nextPipeId = 1;
        for (auto it = pipes.begin(); it != pipes.end(); ++it) {
            if (it->first >= nextPipeId) nextPipeId = it->first + 1;
        }
    }
    else {
        cout << "Pipe not found.\n";
    }
}

void Manager::deleteStation() {
    int id = inputInt("Enter station ID to delete: ");
    if (stations.erase(id)) {
        cout << "Station deleted.\n";
        // Находим максимальный ID среди оставшихся станций
        nextStationId = 1;
        for (auto it = stations.begin(); it != stations.end(); ++it) {
            if (it->first >= nextStationId) nextStationId = it->first + 1;
        }
    }
    else {
        cout << "Station not found.\n";
    }
}

void Manager::showMenu() {
    cout << "\n=== MANAGEMENT SYSTEM ===\n"
        << "1. Add pipe\n"
        << "2. Add station\n"
        << "3. View all\n"
        << "4. Batch edit pipe\n"
        << "5. Save\n"
        << "6. Load\n"
        << "7. Delete pipe\n"
        << "8. Delete station\n"
        << "9. Exit\n"
        << "Choice: ";
}

void Manager::run() {
    int choice = 0;
    do {
        showMenu();
        choice = inputInt("");
        switch (choice) {
        case 1: addPipe(); break;
        case 2: addStation(); break;
        case 3: viewAll(); break;
        case 4: batchEditPipes(); break;
        case 5: saveToFile(); break;
        case 6: loadFromFile(); break;
        case 7: deletePipe(); break;
        case 8: deleteStation(); break;
        case 9: cout << "Exit\n"; break;
        default: cout << "Invalid choice\n"; break;
        }
    } while (choice != 9);
}