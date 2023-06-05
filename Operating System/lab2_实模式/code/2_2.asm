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


mov dh, 0x0c
mov dl, 0x0c
mov bh, 0
mov ah, 2
int 10h


mov al, '2'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '1'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '3'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '0'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '7'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '2'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '6'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h

call right
mov al, '1'
mov bh, 0x00
mov bl, 0x04
mov cx, 1
mov ah, 9
int 10h


jmp $ ; 死循环

up:
	mov bx, 0
	mov ah, 3
	int 10

	dec dh

	mov bh, 0
	mov ah, 2
	int 10h
	ret

down:
	mov bx, 0
	mov ah, 3
	int 10

	inc dh

	mov bh, 0
	mov ah, 2
	int 10h
	ret

left:
	mov bx, 0
	mov ah, 3
	int 10

	dec dl

	mov bh, 0
	mov ah, 2
	int 10h
	ret

right:
	mov bx, 0
	mov ah, 3
	int 10

	inc dl

	mov bh, 0
	mov ah, 2
	int 10h
	ret



times 510 - ($ - $$) db 0
db 0x55, 0xaa


;  qemu-system-i386 -hda hd.img -serial null -parallel stdio 

;  nasm -f bin 2_2.asm -o 2_2.bin

;  qemu-img create hd.img 10m

;  dd if=2_2.bin of=hd.img bs=512 count=1 seek=0 conv=notrunc

