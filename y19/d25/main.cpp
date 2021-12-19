#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using number = long long int;

int main(int argc, const char **argv)
{
    std::string filename = "input.txt";
    std::ifstream infile(filename);
    std::string line;

    while (std::getline(infile, line))
    {
        // number value = std::stoi(line);

    }
    std::cout << "Running: " << filename << std::endl;
    // std::cout << "Part1: " << part1 << std::endl;
    // std::cout << "Part2: " << part2 << std::endl;

    return 0;
}
