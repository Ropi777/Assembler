'''
Assembler for riscv32 processor, translate single assembler file into machine code
'''

# Complete list of Riscv32 basic instruction set  
# instructions will be translated by lookig to table by instruction name
instr_table = {
  "add":   {"type":"R-FORMAT", "func7":"0000000","func3":"000", "opcode":"0110011"},
  "sub":   {"type":"R-FORMAT", "func7":"0100000","func3":"000", "opcode":"0110011"},
  "addi":  {"type":"R-FORMAT","func3":"000", "opcode":"0010011"},
  "xor":   {"type":"R-FORMAT", "func7":"0000000","func3":"100", "opcode":"0110011"},
  "srl":   {"type":"R-FORMAT", "func7":"0000000","func3":"101", "opcode":"0110011"},
  "sra":   {"type":"R-FORMAT", "func7":"0100000","func3":"101", "opcode":"0110011"},
  "or":    {"type":"R-FORMAT", "func7":"0000000","func3":"110", "opcode":"0110011"},
  "and":   {"type":"R-FORMAT", "func7":"0000000","func3":"111", "opcode":"0110011"}, 
  "sll":   {"type":"R-FORMAT", "func7":"0000000","func3":"001", "opcode":"0110011"},
  "lr.d":  {"type":"R-FORMAT", "func7":"0001000", "func3":"011","opcode":"0110011"},
  "lr.d":  {"type":"R-FORMAT", "func7":"0001100", "func3":"011","opcode":"0110011"},

  "lb":    {"type":"I-FORMAT", "func3":"000", "opcode":"0000011"},
  "lh":    {"type":"I-FORMAT", "func3":"001", "opcode":"0000011"},
  "lw":    {"type":"I-FORMAT", "func3":"010", "opcode":"0000011"},
  "ld":    {"type":"I-FORMAT", "func3":"011","opcode":"0000011"},
  "lbu":   {"type":"I-FORMAT", "func3":"100", "opcode":"0000011"},
  "lhu":   {"type":"I-FORMAT", "func3":"101", "opcode":"0000011"},
  "lwu":   {"type":"I-FORMAT", "func3":"110", "opcode":"0000011"},
  "addi":  {"type":"I-FORMAT", "func3":"000", "opcode":"0010011"},
  "slli":  {"type":"I-FORMAT", "func3":"001","opcode":"0010011","imm[11:5]":"0000000"}, 
  "xori":  {"type":"I-FORMAT", "func3":"100","opcode":"0010011"},
  "srli":  {"type":"I-FORMAT", "func3":"101","opcode":"0010011","imm[11:5]":"0000000"},
  "srai":  {"type":"I-FORMAT", "func3":"101","opcode":"0010011","imm[11:5]":"0100000"},
  "ori":   {"type":"I-FORMAT", "func3":"110","opcode":"0010011"},
  "andi":  {"type":"I-FORMAT", "func3":"111","opcode":"0010011"}, 
  "jalr":  {"type":"I-FORMAT", "func3":"000","opcode":"1100111"},

  "sb":    {"type":"S-FORMAT", "func3":"000","opcode":"0100011"},
  "sd":    {"type":"S-FORMAT", "func3":"111","opcode":"0100011"},
  "sh":    {"type":"S-FORMAT", "func3":"001","opcode":"0100011"},
  "sw":    {"type":"S-FORMAT", "func3":"010","opcode":"0100011"},
  
  "beq":   {"type":"B-FORMAT", "func3":"000","opcode":"1100011"},
  "bne":   {"type":"B-FORMAT", "func3":"001","opcode":"1100011"},
  "blt":   {"type":"B-FORMAT", "func3":"100","opcode":"1100011"},
  "bge":   {"type":"B-FORMAT", "func3":"101","opcode":"1100011"},
  "bltu":  {"type":"B-FORMAT", "func3":"110","opcode":"1100011"},
  "bgeu":  {"type":"B-FORMAT", "func3":"111","opcode":"1100011"},

  "lui":   {"type":"U-FORMAT","opcode":"0110111"},
  "jal":   {"type":"J-FORMAT","opcode":"1101111"},
}


def tokenize(instruction):
  #get rid of , and '\n'
  instruction = instruction.replace(",", "")
  instruction = instruction.replace('\n', "")
  #get rid of comments
  len_instr = len(instruction)
  i = 1
  comment = False
  #ignore everything after //
  while(i < len_instr and not comment):
    if (instruction[i-1] == '/' and instruction[i] == '/'):
      comment = True
    else:
      i += 1
  if(comment):
    instruction = instruction[:i-1]

  temp = instruction.split(" ")
  
  #remove spaces and newlines
  tokens = []
  for word in temp:
    if not(word in ['\n', ' ', '\t', '']):
      tokens.append(word)

  return tokens


#replace pseudo with real instructions
#translate li x9, 123 -> addi x9, x0, 123
            #mv x10, x11 -> addi x10 x11 x0
            # j label -> jal x0, label
            # and x9 15 -> andi x9 15
 
def replace_pseudo(instruction):
  if instruction[0] == "li":
    instruction[0] = "addi"
    temp = instruction[-1]
    instruction[-1] = "x0"
    instruction.append(temp)
  elif instruction[0] == "mv":
    instruction[0] == addi
    instruction.append("x0")
  elif instruction[0] == "j":
    instruction[0] = "jal"
    temp = instruction[1]
    instruction[0] = "x0"
    instruction.append(temp)
  elif instruction[0] == "and" and instruction[-1][0] != "x":
    instruction[0] = "andi"
    
  return instruction

def tokenize_program(program_instructions):
  tokenized = []
  for line in program_instructions:
    tokenized_line = tokenize(line)
    if (len(tokenized_line) != 0):
      tokenized_line = replace_pseudo(tokenized_line)
      tokenized.append(tokenized_line)
  return tokenized

#travel code and put [labels:adress] into table, starting adress at 8000
#then remove labels from code
def labelles(program):
  label_less = []
  adress = 8000
  labels = {}

  for line in program:
    possible_label = line[0]
    if(possible_label[-1] == ":"):
      labels[possible_label[:-1]] = adress
      if (len(line) > 1):
        label_less.append(line[1:])
    else:
      label_less.append(line)
    adress += 4

  i = 0
  adress = 8000
  #translate usage of labels to jumps in code
  len_p = len(label_less)
  for i in range(len_p):
    j = 0
    len_line = len(label_less[i])
    for j in range(len_line):
      if label_less[i][j] in labels:
        label_less[i][j] = str(adress - labels[label_less[i][j]])
    adress += 8000
  
  for label in labels:
    print(label)
  
  return label_less

#translate register name starting with x to binary name
def reg_to_binary(reg):
  word = bin(int(reg[1:]))[2:]
  while(len(word) < 6):
    word = "0" + word
  return word

def to_binary(nr,size):
  word = bin(int(nr))[2:]
  while(len(word) < size + 1):
    word = "0" + word
  return word


#translate assembly instruction to machine code
def get_shift(word):
  i = 0
  len_w = len(word)
  while(i < len_w and word[i] != '('):
    i += 1
  return word[:i]

def get_reg(word):
  i = 0
  len_w= len(word)
  while(i < len_w and word[i] != '('):
    i += 1
  return word[i+1:-1]
    
def translate(instruction):
  instr_name = instruction[0]
  instr = instr_table[instr_name]
  instr_type = instr["type"]

  #generate 32bits instructions based on it's format
  if (instr_name == "addi"):
    imm_11_0 = to_binary(get_shift(instruction[3]),12)[::-1] 
    rs1 = reg_to_binary(instruction[2])
    func3 = instr["func3"]
    rd = reg_to_binary(instruction[1])
    opcode = instr["opcode"]
    return imm_11_0+rs1+func3+rd+opcode
 
 elif(instr_type == "R-FORMAT"):
    func7 = instr["func7"]
    rs2 = reg_to_binary(instruction[2]) # source1
    rs1 = reg_to_binary(instruction[2]) # source2
    func3 = instr["func3"]
    rd = reg_to_binary(instruction[1]) # destination
    opcode = instr["opcode"]
    return func7+rs2+rs1+func3+rd+opcode

  elif (instr_type == "I-FORMAT"):

    if (len(instruction) == 4):
      rs1 = reg_to_binary(instruction[2])
      imm_11_0 = to_binary(instruction[3],12)[::-1]
    else:
      imm_11_0 = to_binary(get_shift(instruction[2]),12)[::-1] # 2(x6) -> 00000000010 -> 01000000000 
      rs1 = reg_to_binary(get_reg(instruction[2])) # 2(x6) -> x6 -> 6 -> 110
    func3 = instr["func3"]
    rd = reg_to_binary(instruction[1])
    opcode = instr["opcode"]
    return imm_11_0+rs1+func3+rd+opcode

  elif (instr_type == "S-FORMAT"):
    imm = to_binary(get_shift(instruction[2], 12))[::-1]
    imm_11_5 = imm[0:7]
    rs2 = reg_to_binary(get_reg(instruction[2]))
    rs1 = reg_to_binary(instruction[1])
    func3 = instr["func3"]
    imm_4_0 = imm[7:11]
    opcode = instr["opcode"]
    return imm_11_5+rs2+rs1+func3+imm_4_0+opcode

  elif (instr_type == "B-FORMAT"):
    imm = to_binary(instruction[3], 12)[::-1]
    imm_11_5 = imm[0:8] 
    rs2 = reg_to_binary(instruction[2])
    rs1 = reg_to_binary(instruction[1])
    func3 = instr["func3"]
    imm_4_1 = imm[7:11]
    imm_11 = imm[0]
    opcode = instr["opcode"]
    return imm_11_5+rs2+rs1+func3+imm_4_1+imm_11+opcode

elif (instr_type == "U-FORMAT"):
    imm = to_binary(instruction[2], 32)[::-1]
    imm_31_12 = imm[0:19]
    rd = reg_to_binary(instruction[1], 6)
    opcode = instr["U-FORMAT"]
    return imm_31_12 + rd + opcode
    return iimm_31_12+rd+opcode

elif(instr_type == "J-FORMAT" ):
    imm = to_binary(instruction[2], 32)[::-1]
    imm_20 = imm[12]
    imm_10_1 = imm[21:31]
    imm_11 = imm[20]
    imm_19_12 = imm [12:19]
    rd = rs1 = reg_to_binary(instruction[1],6)
    opcode = instr["U-FORMAT"]
    return imm_20+imm_10_1+imm_11+iimm_19_12+rd+opcode

else:
    print("There is not such instrucion")
    return -42

def translate_to_binary(program):
  binary = []
  for line in program:
    binary.append(translate(line))
  return binary

def read_program(source, output):
  instructions = []
  #read lines of assembly code from source
  src =  open (source, 'r')
  for line in src:
    instructions.append(line)
  src.close()
  return instructions
  #dest = open(output, "w")
  #for instruction in machine_code:
  #  dest.write(instruction)
  #dest.close()

if __name__ == '__main__':
  src = input("")
  out = input("")
  program = read_program(src, out)
  tokenized = tokenize_program(program)
  tokenized = labelles(tokenized)
  binary = translate_to_binary(tokenized)
  for line in tokenized:
    print(line)
  for line in binary:
    print(line)
