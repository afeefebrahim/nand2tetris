import sys
def parse(line):
  
      command =""
      #if line =="" or line[:2] == "//":
      #   return 'emptyline',0
      if '//' in line:
         command = line.split('//')[0]
      else:
         command =line
      if command[0] == '@':
         if command[1:].isdigit(): 
             return 'acommand',command[1:]
      elif command[0] =='(' and command[-1]==')':
         return 'lcommand',command[1:-1]
      else:
         return 'ccommand',command   
def c_command(cmd):
    parts ={}
    if ';' in cmd and '=' in cmd:
       cmd = cmd.replace(';',',')
       cmd = cmd.replace('=',',')
       c =cmd.split(',')
     
       parts['dest'] = c[0]
       parts['comp'] = c[1]
       parts['jmp'] = c[2]
    if ';' in cmd:
       cmd = cmd.replace(';',',')
       c = cmd.split(',')
       parts['dest'] = ""
       parts['comp'] = c[0]
       parts['jmp']  = c[1]
    if '=' in cmd:
       cmd = cmd.replace('=',',')
       c = cmd.split(',')
       parts['dest'] = c[0]
       parts['comp'] = c[1]
       parts['jmp']  = ''
    return parts
def dest1(mnemonic):
   if '\r\n' in mnemonic:
      mnemonic =mnemonic.replace('\r\n','') 
   translate = {'':     '000',
                 'M':    '001',
                 'D':    '010',
                 'MD':   '011',
                 'A':    '100',
                 'AM':   '101',
                 'AD':   '110',
                 'AMD':  '111'}
   return translate[mnemonic]
def comp1(mnemonic):
   if '\r\n' in mnemonic: 
        mnemonic =mnemonic.replace('\r\n','')
   translate = {#a=0
                 '0':  '0101010',
                 '1':  '0111111',
                 '-1': '0111010',
                 'D':  '0001100',
                 'A':  '0110000', 
                 '!D': '0001101',
                 '!A': '0110001',
                 '-D': '0001111',
                 '-A': '0110011',
                 'D+1':'0011111',
                 'A+1':'0110111',
                 'D-1':'0001110',
                 'A-1':'0110010',
                 'D+A':'0000010',
                 'D-A':'0010011',
                 'A-D':'0000111',
                 'D&A':'0000000',
                 'D|A':'0010101',
                 #a=1
                 'M'  :'1110000',
                 '!M' :'1110001',
                 '-M' :'1110011',
                 'M+1':'1110111',
                 'M-1':'1110010',
                 'D+M':'1000010',
                 'D-M':'1010011',
                 'M-D':'1000111',
                 'D&M':'1000000',
                 'D|M':'1010101'}
   return translate[mnemonic]
def jmp1(mnemonic):
   if '\r\n' in mnemonic:
        mnemonic =mnemonic.replace('\r\n','')
   translate = {
                 '':     '000',
                 'JGT' : '001',
                 'JEQ' : '010',
                 'JGE' : '011',
                 'JLT' : '100',
                 'JNE' : '101',
                 'JLE' : '110',
                 'JMP' : '111'}
   return translate[mnemonic] 
def symbol_table(line,address):
    table ={'SP': 0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14,'R15':15, 'SCREEN':0x4000, 'KBD':0x600}
    
    
      table[code] = address
address =0
filename = sys.argv[1]
lines = open(filename).readlines()
s =open(filename.split('.')[0]+'.hack','w')
for line  in lines:
   address = address+1 
   if not line.strip() or line[:2]=='//':
      pass
   else:
      state,cmd =parse(line)   
      
      if state == 'acommand' or state == 'lcommand':
            s.write('{0:0>16}'.format(str(bin(int(cmd))[2:]))+'\n')
      elif state == 'ccommand':
            p = c_command(cmd)
            print state,p 
            s.write('111'+comp1(p['comp'])+dest1(p['dest'])+jmp1(p['jmp'])+'\n')
s.close()      
