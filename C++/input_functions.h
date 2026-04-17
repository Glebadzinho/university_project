#ifndef INPUT_FUNCTIONS_H
#define INPUT_FUNCTIONS_H

#include <string>

int inputInt(const std::string& prompt, int minVal = 0);
double inputDouble(const std::string& prompt, double minVal = 0.0);
bool inputBool01(const std::string& prompt);
std::string inputString(const std::string& prompt);

#endif