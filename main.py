import copy

# -A
# 4
# -A OR B
# B OR -C
# A OR -B OR C
# -B



def readInput(filename):
    with open(filename, "r") as file:
        alpha = file.readline().strip().split(" OR ")
        # strip(): removes leading and trailing whitespaces
        while True:
            temp = file.readline()
            if (temp != '\n'):
                n = int(temp)
                break
        KB = []
        for i in range(0,n):
            clause =  file.readline().strip().split(" OR ")
            KB.append(clause)
        # print(KB)
    print('alpha ', alpha)
    print('KB ', KB)
    return alpha, KB

def are_two_opposite_literals(l1, l2):
    if len(l1) == len(l2):
        return False
    elif l1[-1] == l2[-1]:
        return True
    return False

def appendNegateAlphaToKB(alpha, KB):
    # alpha = ['-A']

    for literal in alpha:
        if '-' in literal:
            literal = literal.strip('-')
        else:
            literal = '-' + literal
        KB.append([literal])
        
    print('clauses ', KB)
    return KB

def resolveTwoClauses(clause_one, clause_two):
    temp_clause_one = copy.deepcopy(clause_one)
    temp_clause_two = copy.deepcopy(clause_two)

    resolvents = None

    pop_literal_in_clause_one = []
    pop_literal_in_clause_two = []

    for literal_one in temp_clause_one:
        for literal_two in temp_clause_two:
            if are_two_opposite_literals(literal_one, literal_two):
                pop_literal_in_clause_one.append(literal_one)
                pop_literal_in_clause_two.append(literal_two)
    
    if len(pop_literal_in_clause_one) > 1 or len(pop_literal_in_clause_one) == 0:
        return None


    for literal in pop_literal_in_clause_one:
        temp_clause_one.remove(literal)
    for literal in pop_literal_in_clause_two:
        temp_clause_two.remove(literal)

    new_clause = temp_clause_one + temp_clause_two

    # print('new_clause ', new_clause)
    new_clause = sorted(set(new_clause), key = lambda sub : sub[-1])
    print('new clause ', new_clause)
    return new_clause 

def PL_RESOLUTION(clauses):
    new_clauses_array = []
    while True:
        new_clauses = []
        for i in range(len(clauses)-1):
            for j in range(i+1, len(clauses)):
                new_clause = resolveTwoClauses(clauses[i], clauses[j])
                if new_clause == []:
                    new_clauses.append(new_clause)
                    new_clauses_array.append(new_clauses)
                    return True, new_clauses_array
                if new_clause != None:
                    if new_clause not in clauses and new_clause not in new_clauses:
                        new_clauses.append(new_clause)   
        new_clauses_array.append(new_clauses)
        # print('new_clauses ',new_clauses )
        if new_clauses == []:
            return False, new_clauses_array
        clauses += new_clauses

def writeOutput(isSuccess, new_clauses_array):
    success = 'YES' if isSuccess else 'NO'
    with open('./output/output.txt', 'w') as file:
        i = 0
        for new_clauses in new_clauses_array:
            file.write(str(len(new_clauses)) + '\n')
            for clause in new_clauses:
                if clause == []:
                    file.write("{}\n")
                    break
                explicit_clause = ' OR '.join(clause)
                file.write(explicit_clause + '\n')
                
        file.write(success)

def chooseFileInput():
    print('0. Exit')
    print('1. input1.txt')
    print('2. input2.txt')
    print('3. input3.txt')
    print('4. input4.txt')
    print('5. input5.txt')
    print('Which file do you want to test?')
    selection = input('Enter you decision: ')
    selection = int(selection)
    if selection == 1:
        return 'input1.txt'
    if selection == 2:
        return 'input2.txt'
    if selection == 3:
        return 'input3.txt'
    if selection == 4:
        return 'input4.txt'
    if selection == 5:
        return 'input5.txt'
    else: 
        exit()
        
def main():
    while True:
        inputFilePath = './input/'
        file_name = chooseFileInput()
        inputFilePath += file_name
        alpha, KB = readInput(inputFilePath)
        clauses = appendNegateAlphaToKB(alpha, KB)
        isSuccess, new_clauses_array = PL_RESOLUTION(clauses)
        writeOutput(isSuccess, new_clauses_array)
        print('Result in output/output.txt')
        print('---------------------------')

if __name__ == "__main__":
    main()