import os.path
import sys
from Utils.InputUtils import handle_input, handle_csv

inputs = sys.argv


def main():
    print(len(inputs))
    if len(inputs) > 1:
        for arg in inputs[1:]:
            fileLocation = os.path.abspath(arg)
            handle_input(fileLocation)
            return
    else:
        print("Nothing given as input")
        want_csv = input("Would you like to view a csv of stuff? (Y/N)")
        if want_csv == "Y":
            handle_csv()

    return


if __name__ == "__main__":
    main()