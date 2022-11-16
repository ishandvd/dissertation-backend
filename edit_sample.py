appendText1 = '['
appendText2 = ']'
with open("sample_wd.py", 'r') as names:
    with open("sample_wd2.py", 'a') as updatedNames:
        for name in names:
            updatedNames.write(str(name.rstrip().split("    ")[1:]) + ',\n')