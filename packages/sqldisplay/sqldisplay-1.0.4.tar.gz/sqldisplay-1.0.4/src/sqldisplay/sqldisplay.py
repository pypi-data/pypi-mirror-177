def format(desc, result):
    for record in result:
        i = 0
        for column in desc:
            print(f"{desc[i][0]}: {record[i]}")
            i += 1
