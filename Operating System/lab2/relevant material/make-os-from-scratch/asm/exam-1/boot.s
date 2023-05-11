section .text
global start
start:
mov eax,4;
mov ebx,1;
mov ecx,msg;
mov edx,14;
int 80h;
mov eax,1;
int 80h;
msg:
db "hello world",0ah,0dh
