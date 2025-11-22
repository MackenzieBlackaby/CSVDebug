from pathlib import Path
from os import system, name as osName
from sys import exit as sysExit

system("cls" if osName == "nt" else "clear")

BOLD = "\033[1m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"


def readLines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n").rstrip("\r") for line in f]


def getLinesAround(current: int, count: int, lineList: list):
    lowerBound = max(0, current - count)
    upperBound = min(len(lineList), current + count + 1)
    return lineList[lowerBound:upperBound]


def comp(a: int, b: int):
    return a if a > b else b


def highlightDifferences(model: str, test: str):
    outModel = []
    outTest = []

    maxLen = max(len(model), len(test))

    for i in range(maxLen):
        chModel = model[i] if i < len(model) else ""
        chTest = test[i] if i < len(test) else ""

        if chModel == chTest:
            outModel.append(chModel)
            outTest.append(chTest)
        else:
            if chModel:
                outModel.append(f"{GREEN}{chModel}{RESET}")
            if chTest:
                outTest.append(f"{RED}{chTest}{RESET}")

    return "".join(outModel), "".join(outTest)


linesToSliceAround = 5
modelPrefix = Path("model")
suffix = ".csv"

testPaths = sorted(
    p for p in Path(".").glob(f"*{suffix}") if p.is_file() and p.parent != modelPrefix
)
modelPaths = []

for p in testPaths:
    modelFile = modelPrefix / p.name
    if not modelFile.exists():
        sysExit(
            f'\n{BOLD}{RED}[ERROR]:{RESET} Missing model file for "{p.name}". Please put the corresponding file in the model directory :)\n'
        )
    modelPaths.append(modelFile)

for i, (testPath, modelPath) in enumerate(zip(testPaths, modelPaths), start=1):
    testLines = readLines(testPath)
    modelLines = readLines(modelPath)

    print(f"Checking file {i} ({testPath})...")

    maxLen = max(len(testLines), len(modelLines))
    isError = False
    skip = False

    for l in range(maxLen):
        testLine = testLines[l] if l < len(testLines) else "<NO LINE>"
        modelLine = modelLines[l] if l < len(modelLines) else "<NO LINE>"

        if testLine != modelLine:
            hlModel, hlTest = highlightDifferences(modelLine, testLine)
            print(f"\n{BOLD}{RED}[#]    Mismatch at line {l + 1}:{RESET}\n")
            print(f"[!]    Model:     {"{ "}{hlModel}{" }"}{RESET}")
            print(f"[?]    Yours:     {"{ "}{hlTest}{" }"}{RESET}")
            while True:
                print(
                    '\nInput "p" to print surrounding lines, "o" to override this error, or "s" to skip this file'
                )
                temp = input("\n[*]: ").strip().lower()
                if temp[0] == "p":
                    print("\n---")
                    start = max(0, l - linesToSliceAround)
                    end = min(maxLen, l + linesToSliceAround + 1)
                    for j in range(start, end):
                        label = f"Line {j + 1}"
                        if j == l:
                            label += f"{BOLD}{RED} [ERROR] {RESET}"
                        print(label)
                        currentModelLine = (
                            "EOF" if j >= len(modelLines) else modelLines[j]
                        )
                        currentTestLine = "EOF" if j >= len(testLines) else testLines[j]
                        hlCMod, hlCTest = highlightDifferences(
                            currentModelLine, currentTestLine
                        )
                        print("              [  Model  ]: " + hlCMod)
                        print("              [  Yours  ]: " + hlCTest)
                        print("---")
                    print("\n")
                elif temp[0] == "s":
                    skip = True
                    break
                elif temp[0] == "o":
                    break
        if skip:
            break
    if not isError:
        print(f"{BOLD}{GREEN}[ :) ] File {i} ({testPath}) matches perfectly.{RESET}\n")
