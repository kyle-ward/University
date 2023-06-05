org 0x7c00
[bits 16]


	_UR equ 1
	_DR equ 2
	_DL equ 3
	_UL equ 4
	w1 equ 400
	w2 equ 400 ;10

c1 dw w1
c2 dw w2
direction db _DR
color db 0x01
character db '0'
x dw 2
y dw 0

;20

init:
	xor eax, eax ; eax = 0
	mov ds, ax
	mov gs, ax
	mov ax, 0xb800
	mov gs, ax
	mov si, 0
	mov di, 0
;30
loopTowait:
	dec word[c1]
	jnz loopTowait
	mov word[c1], w1
	dec word[c2]
	jnz loopTowait
	mov word[c1], w1
	mov word[c2], w2

	mov al, 1 ;40
	cmp byte[direction], al
	jz UpRight

	mov al, 2
	cmp byte[direction], al
	jz DownRight

	mov al, 3
	cmp byte[direction], al
	jz DownLeft

	mov al, 4
	cmp byte[direction], al
	jz UpLeft
	jmp $




UpRight:
	dec word[x]
	inc word[y]

	mov bx, word[y]
	mov ax, 80
	sub ax, bx
	cmp ax, 0
	jz URToUpLeft

	mov bx, word[x]
	mov ax, 0
	sub ax, bx
	cmp ax, 0
	jg URToDownRight
	jmp show
URToUpLeft:
	mov word[y], 78
	mov byte[direction], _UL
	jmp show
URToDownRight:
	mov word[x], 1
	mov byte[direction], _DR
	jmp show




DownRight:
	inc word[x]
	inc word[y]

	mov bx, word[y]
	mov ax, 80
	sub ax, bx
	cmp ax, 0
	jz DRToDownLeft

	mov bx, word[x]
	mov ax, 25
	sub ax, bx
	cmp ax, 0
	jz DRToUpRight
	jmp show
DRToUpRight:
	mov word[x], 23
	mov byte[direction], _UR
	jmp show
DRToDownLeft:
	mov word[y], 78
	mov byte[direction], _DL
	jmp show




DownLeft:
	inc word[x]
	dec word[y]

	mov ax, 25
	mov bx, word[x]
	sub ax, bx
	cmp ax, 0
	jz DLToUpLeft

	mov ax, 0
	mov bx, word[y]
	sub ax, bx
	cmp ax, 0
	jg DLToDownRight
	jmp show
DLToUpLeft:
	mov word[x], 23
	mov byte[direction], _UL
	jmp show
DLToDownRight:
	mov word[y], 1
	mov byte[direction], _DR
	jmp show




UpLeft:
	dec word[x]
	dec word[y]

	mov ax, 0
	mov bx, word[x]
	sub ax, bx
	cmp ax, 0
	jg ULToDownLeft

	mov ax, 0
	mov bx, word[y]
	sub ax, bx
	cmp ax, 0
	jg ULToUpRight
	jmp show
ULToDownLeft:
	mov word[x], 1
	mov byte[direction], _DL
	jmp show
ULToUpRight:
	mov word[y], 1
	mov byte[direction], _UR
	jmp show	







show:
	xor ax, ax
	mov ax, word[x]
	mov bx, 80
	mul bx
	add ax, word[y]
	mov bx, 2
	mul bx
	mov bx, ax
	mov al, byte[character]
	mov ah, byte[color]
	mov [gs:bx], ax

	xor ax, ax
	mov ax, word[x]
	mov bx, 80
	mul bx
	mov bx, word[y]
	neg bx
	add bx, 79
	add ax, bx
	mov bx, 2
	mul bx
	mov bx, ax
	mov al, byte[character]
	mov ah, byte[color]
	mov [gs:bx], ax
	

	inc byte[color]
	inc byte[character]
	cmp byte[color], 8
	jl color_next
	mov byte[color], 1
color_next:
	cmp byte[character], '9'
	jl character_next
	mov byte[character], '0'
character_next:
	jmp loopTowait
	


jmp $ ; 死循环


times 510 - ($ - $$) db 0
db 0x55, 0xaa

;  qemu-system-i386 -hda hd.img -serial null -parallel stdio 

;  nasm -f bin assignment4.asm -o assignment4.bin

;  qemu-img create hd.img 10m

;  dd if=assignment4.bin of=hd.img bs=512 count=1 seek=0 conv=notrunc












