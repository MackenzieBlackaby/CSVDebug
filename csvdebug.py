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


def highlightDifferences(model: str, target: str):
    outModel = []
    outTest = []

    maxLen = max(len(modelLine), len(testLine))

    for i in range(maxLen):
        chModel = modelLine[i] if i < len(modelLine) else ""
        chTest = testLine[i] if i < len(testLine) else ""

        if chModel == chTest:
            outModel.append(chModel)
            outTest.append(chTest)
        else:
            if chModel:
                outModel.append(f"{RED}{chModel}{RESET}")
            if chTest:
                outTest.append(f"{GREEN}{chTest}{RESET}")

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
            hlModel, hlTest = highlightDifferences(testLine, modelLine)
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
                    start = max(0, 1 - linesToSliceAround)
                    end = min(maxLen, 2 + linesToSliceAround)
                    for j in range(start, end):
                        label = f"Line {j + 1}"
                        if j == 1:
                            label += f"{BOLD}{RED} [ERROR] {RESET}"
                        print(label)
                        print(
                            "              [  Model  ]: "
                            + ("EOF" if j >= len(modelLines) else modelLines[j])
                        )
                        print(
                            "              [  Yours   ]: "
                            + ("EOF" if j >= len(testLines) else testLines[j])
                        )
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
