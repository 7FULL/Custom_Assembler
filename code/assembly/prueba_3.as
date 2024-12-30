var myVar 5         // Define a variable myVar with value 5

LOADI reg1 10       // Load immediate value 10 into reg1
LOADI reg2 15       // Load immediate value 15 into reg2
ADD reg3 reg1 reg2  // Add reg1 and reg2, store the result in reg3
STORE reg3 myVar    // Store the value of reg3 into memory address of myVar

LOAD reg4 myVar     // Load the value of myVar into reg4
SUB reg5 reg4 reg1  // Subtract reg1 from reg4, store the result in reg5

CMP reg3 reg2       // Compare reg3 with reg2
JEQ END             // Jump to END if reg3 equals reg2
JNE LOOP            // Jump to LOOP if reg3 not equal to reg2

LOOP:
    LOAD 2 10       // Load immediate value 42 into reg6
    STORE reg6 15       // Store value 42 into memory address 15
    HLT                 // Halt the execution

END:
    HLT                 // Halt the execution
