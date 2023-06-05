section .text
global main
main:
   lea dx,[mass]
   mov ah,9
   int 21h
   
   mov ah,4ch
   int 21h

mass:
   db "Hello World",0ah,0dh

