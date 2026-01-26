path = rCUsersalperanasiolmayanlogdaosyasi.txt
current = None
count,input_data = 0,str(input(''))
string = []

with open(path,'r') as f0
    current = f0.read()

string.append(f'{current}n')
string.append(f'{input_data}n')

with open(path,'w') as f1
    for a in string
        f1.write(f'ntimecoden{a}')

with open(path,'r') as f2
    main = f2.read()
    print(main)