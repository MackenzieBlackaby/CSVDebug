from pathlib import Path
from os import system, name as osName

system("cls" if osName == "nt" else "clear")


def readLines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n").rstrip("\r") for line in f]


def getLinesAround(current: int, count: int, lineList: list):
    lowerBound = max(0, current - count)
    upperBound = min(len(lineList), current + count + 1)
    return lineList[lowerBound:upperBound]


def comp(a: int, b: int):
    return a if a > b else b


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
        raise FileNotFoundError(
            f"Missing model file for {p.name}. Please put the corresponding file in the model directory"
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
            print(f"\n[#]    Mismatch at line {l + 1}:\n")
            print(f"[!]    Model:     {"{ "}{modelLine}{" }"}")
            print(f"[?]    Yours:     {"{ "}{testLine}{" }"}")
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
                            label += " [ERROR]"
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
        print(f"[ :) ] File {i} ({testPath}) matches perfectly.\n")
