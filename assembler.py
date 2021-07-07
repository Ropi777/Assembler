''' 
RISCV32I ASSEMBLER
'''

import sys

#funct7, funct3, opcode
R_OPCODE = "0110011"
R_FUNCT7 = "0000000"
R_FUNCT3_TABLE = {
  "add":"000",
  "sll":"001",
  "slt":"010",
  "sltu":"011",
  "xor":"100",
  "srl":"101",
  "or":"110",
  "and":"111"
}

I_OPCODE_1 = "0000011"
I_FUNCT3_TABLE_1 = {
  "lb":"000",
  "lh":"001",
  "lw":"010",
  "ld":"011",
  "lbu":"100",
  "lhu":"101",
  "lwu":"110",
  "jalr":"111"
}

I_OPCODE_2 = "0010011"
I_FUNCT3_TABLE_2 = {
  "addi":"000",
  "slli":"001",
  "xori":"010",
  "srli":"011",
  "srai":"100",
  "ori":"101",
  "andi":"110"
}

S_OPCODE = "0100011"
S_FUNCT3_TABLE = {
  "sb":"000",
  "sd":"111",
  "sh":"001",
  "sw":"010"
}

B_OPCODE = "1100011"
B_FUNCT3_TABLE = {
  "beq":"000",
  "bne":"001",
  "blt":"100",
  "bge":"101",
  "bltu":"110",
  "bgeu":"111"
}

U_OPCODE = "0110111"
U_TABLE = {"lui":1}

J_OPCODE = "1101111"
J_TABLE = {"jal":1}


#imm 11:5, funct3, imm4:0, opcode
S_FORMAT = {}

#imm[12] imm[10:5] funct3 imm[4:1] imm[11] opcode
B_FORMAT = {}

#imm[31:12] opcode
U_FORMAT = {}

#imm[20] imm[10:1] imm[11] imm[19:12] opcode
J_FORMAT = {}

BRANCH_TABLE = {}

def tokenize(text):
# translate line of raw text to array of tokens
  text = text.replace(',', ' ')
  
  #skip comments
  i = 0
  while(i < len(text)):
    if(text[i] == '#'):
      break
    i += 1
  text = text[0:i]
  tokens = []
  
  #tokenize
  s = 0
  e = 0
  while(e < len(text)):
    if(text[e] == '"'):
      e += 1
      while(text[e] != '"'):
        e += 1
      e += 1
      tokens.append(text[s:e])
      s = e

    elif(text[e] in ('\n', '\t', ' ')):
      if(s != e):
        tokens.append(text[s:e])
        s = e
      s += 1
      e += 1
    else:
      e += 1

  return tokens

def reg_to_binary(reg):
  word = bin(int(reg[1:]))[2:]
  while(len(word) < 6):
    word = "0" + word
  return word

def to_binary_nr(nr,size):
  word = bin(int(nr))[2:]
  while(len(word) < size + 1):
    word = "0" + word
  return word


def binary(tokenized_prog):
  binary = []
  binary_line = ""
  for line in tokenized_prog:
        if line[0] in R_FUNCT3_TABLE:
          binary_line += R_FUNCT7
          binary_line += reg_to_binary(line[2])
          binary_line += reg_to_binary(line[3])
          binary_line += R_FUNCT3_TABLE[line[0]]
          binary_line += reg_to_binary(line[1])
          binary_line += R_OPCODE

        elif line[0] in I_FUNCT3_TABLE:

        elif line[0] in S_FUNCT3_TABLE:

        elif line[0] in B_FUNCT3_TABLE:

        elif line[0] in U_TABLE:

        elif line[0] in J_TABLE:


if __name__ == '__main__':
  input_name = sys.argv[-2]
  output_name = sys.argv[-1]

  tokenized_program = []
  tokenized_line = []
  ln = 0

  #read code as raw text and transform to array of arrays of tokens
  text = open(input_name, "r")
  line = text.readline()
  while line != '':
    tokenized_line = tokenize(str(line))
    if (tokenized_line):
      if (tokenized_line[0][-1] == ':'):
        BRANCH_TABLE[tokenized_line[0][:-1]] = ln * 4
        tokenized_line = tokenized_line[1:]
      ln += 1
      tokenized_program.append(tokenized_line)
    line = text.readline()

  
  binary_program = binary(tokenized_program)
  text = open(output_name, "w")
  for line in binary_program:
    text.write(line)
  text.close
