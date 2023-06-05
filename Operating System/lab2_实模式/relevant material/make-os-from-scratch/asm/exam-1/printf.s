extern printf
extern exit

section .data
   format  db  "%d"

section .text

global _start
_start:
   push 2
   push format
   call printf
   push 0
   call exit

