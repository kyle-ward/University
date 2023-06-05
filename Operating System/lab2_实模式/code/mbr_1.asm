org 0x7c00
[bits 16]
xor ax, ax ; eax = 0

mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

mov sp, 0x7c00 
mov ax, 0xb800
mov gs, ax
mov ah, 0x17 ;bgc=blue, color=white
mov al, '2'
mov [gs:2 * 972], ax ;12*80+12

mov al, '1'
mov [gs:2 * 973], ax

mov al, '3'
mov [gs:2 * 974], ax

mov al, '0'
mov [gs:2 * 975], ax

mov al, '7'
mov [gs:2 * 976], ax

mov al, '2'
mov [gs:2 * 977], ax

mov al, '6'
mov [gs:2 * 978], ax

mov al, '1'
mov [gs:2 * 979], ax


jmp $ ; 死循环

times 510 - ($ - $$) db 0
db 0x55, 0xaa
