#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

using number = long long int;

std::vector<number> read_input(std::string filename)
{
    std::ifstream infile(filename);
    std::string line;

    std::getline(infile, line);
    std::stringstream ss(line);
    std::vector<number> input;
    number i;
    while (ss >> i)
    {
        input.push_back(i);
        ss.ignore(1);
    }
    return input;
}

int main(int argc, const char **argv)
{
    std::string filename = "input.txt";
    std::vector<number> input = read_input(filename);

    input[1] = 12;
    input[2] = 2;

    number opcode = input[0];
    number index = 0;
    while(opcode != -1)
    {
        for (int i = index; i < index + 4; i++)
        {
            std::cout << input[i] << ",";
        }
        std::cout << std::endl;
        switch(opcode)
        {
            case 1:
                input[input[index + 3]] = input[input[index + 1]] + input[input[index + 2]];
                break;
            case 2:
                input[input[index + 3]] = input[input[index + 1]] * input[input[index + 2]];
                break;
            default:
                std::cout << "Unknown opcode: " << opcode << std::endl;
                opcode = -1;
        }
        if (opcode != -1)
        {
            index += 4;
            opcode = input[index];
        }
    }

    std::cout << "Running: " << filename << std::endl;
    std::cout << "Part1: " << input[0] << std::endl;
    // std::cout << "Part2: " << part2 << std::endl;

    return 0;
}
