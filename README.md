# CSVDebug

## Description

A tool to compare multiple csv files line by line to model csv files. Useful in tasks that require exact matching of a csv file to a desired output.

## Usage

This tool is simple to use.

1. Clone this repository
2. Place your desired "model" csv files in the `./model/` directory
3. Place the files you'd like to test in the root directory of the repo
4. Run the command `py csvdebug.py` and follow the instructions to begin debugging

### Commands

The program will automatically detect both test and model csv files to be run. If there is a csv file in the root that does not have a corresponding csv file in the model directory, the program will throw an exception.

If an error is found, the program will display an error and await one of three letter commands:

- `p` prints the surrounding lines
- `o` overrides the error and continues to the next line
- `s` skips the remainder of the file, if the error is such that all subsequent lines are different

## Directory structure

The directory structure of this program makes it easy to drop into ongoing projects that output files directly to their root directories

```
root/
    csvdebug.py         <---- program
    README.md           <---- readme
    test.csv            <---- example input csv file
    model/
        test.csv        <---- example model csv file
```