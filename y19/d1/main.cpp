#include <iostream>
#include <fstream>
#include <string>

using number = long long int;

int main(int argc, const char **argv)
{
    std::string filename = "input.txt";
    std::ifstream infile(filename);
    std::string line;

    number part1 = 0;
    number part2 = 0;
    while (std::getline(infile, line))
    {
        number value = std::stoi(line);
        number fuel = value / 3 - 2;
        part1 += fuel;

        while (fuel > 0)
        {
            part2 += fuel;
            fuel = fuel / 3 - 2;
        }
    }
    std::cout << "Running: " << filename << std::endl;
    std::cout << "Part1: " << part1 << std::endl;
    std::cout << "Part2: " << part2 << std::endl;

    return 0;
}
