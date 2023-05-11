%include "boot.inc"

;org 0x7e00
[bits 16]
;空描述符
mov dword [GDT_START_ADDRESS+0x00],0x00
mov dword [GDT_START_ADDRESS+0x04],0x00  

;创建描述符，这是一个数据段，对应0~4GB的线性地址空间
mov dword [GDT_START_ADDRESS+0x08],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x0c],0x00cf9200    ; 粒度为4KB，存储器段描述符 

;建立保护模式下的堆栈段描述符      
mov dword [GDT_START_ADDRESS+0x10],0x00000000    ; 基地址为0x00000000，界限0x0 
mov dword [GDT_START_ADDRESS+0x14],0x00409600    ; 粒度为1个字节

;建立保护模式下的显存描述符   
mov dword [GDT_START_ADDRESS+0x18],0x80007fff    ; 基地址为0x000B8000，界限0x07FFF 
mov dword [GDT_START_ADDRESS+0x1c],0x0040920b    ; 粒度为字节

;创建保护模式下平坦模式代码段描述符
mov dword [GDT_START_ADDRESS+0x20],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x24],0x00cf9800    ; 粒度为4kb，代码段描述符 

;初始化描述符表寄存器GDTR
	mov word [pgdt], 39      ;描述符表的界限   
	lgdt [pgdt]

	in al,0x92                         ;南桥芯片内的端口 
	or al,0000_0010B
	out 0x92,al                        ;打开A20

	cli                                ;中断机制尚未工作
	mov eax,cr0
	or eax,1
	mov cr0,eax                        ;设置PE位


;以下进入保护模式
jmp dword CODE_SELECTOR:protect_mode_begin

;16位的描述符选择子：32位偏移
;清流水线并串行化处理器
[bits 32]           
protect_mode_begin:                              
	_UR equ 1
	_DR equ 2
	_DL equ 3
	_UL equ 4
	w1 equ 400
	w2 equ 400 

c1 dd w1
c2 dd w2
direction db _DR
color db 0x01
character db '0'
x dd 2
y dd 0



init:
	mov eax, DATA_SELECTOR
	mov ds, eax
	mov gs, eax
	mov eax, STACK_SELECTOR
	mov ss, eax
	mov eax, VIDEO_SELECTOR
	mov es, eax
	mov esi, 0
        mov edi, 0

loopTowait:
	dec dword[c1]
	jnz loopTowait
	mov dword[c1], w1
	dec dword[c2]
	jnz loopTowait
	mov dword[c1], w1
	mov dword[c2], w2

	mov al, 1 
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
	dec dword[x]
	inc dword[y]

	mov ebx, dword[y]
	mov eax, 80
	sub eax, ebx
	cmp eax, 0
	jz URToUpLeft

	mov ebx, dword[x]
	mov eax, 0
	sub eax, ebx
	cmp eax, 0
	jg URToDownRight
	jmp show
URToUpLeft:
	mov dword[y], 78
	mov byte[direction], _UL
	jmp show
URToDownRight:
	mov dword[x], 1
	mov byte[direction], _DR
	jmp show




DownRight:
	inc dword[x]
	inc dword[y]

	mov ebx, dword[y]
	mov eax, 80
	sub eax, ebx
	cmp eax, 0
	jz DRToDownLeft

	mov ebx, dword[x]
	mov eax, 25
	sub eax, ebx
	cmp eax, 0
	jz DRToUpRight
	jmp show
DRToUpRight:
	mov dword[x], 23
	mov byte[direction], _UR
	jmp show
DRToDownLeft:
	mov dword[y], 78
	mov byte[direction], _DL
	jmp show




DownLeft:
	inc dword[x]
	dec dword[y]

	mov eax, 25
	mov ebx, dword[x]
	sub eax, ebx
	cmp eax, 0
	jz DLToUpLeft

	mov eax, 0
	mov ebx, dword[y]
	sub eax, ebx
	cmp eax, 0
	jg DLToDownRight
	jmp show
DLToUpLeft:
	mov dword[x], 23
	mov byte[direction], _UL
	jmp show
DLToDownRight:
	mov dword[y], 1
	mov byte[direction], _DR
	jmp show




UpLeft:
	dec dword[x]
	dec dword[y]

	mov eax, 0
	mov ebx, dword[x]
	sub eax, ebx
	cmp eax, 0
	jg ULToDownLeft

	mov eax, 0
	mov ebx, dword[y]
	sub eax, ebx
	cmp eax, 0
	jg ULToUpRight
	jmp show
ULToDownLeft:
	mov dword[x], 1
	mov byte[direction], _DL
	jmp show
ULToUpRight:
	mov dword[y], 1
	mov byte[direction], _UR
	jmp show	


show:
	xor eax, eax
	mov eax, dword[x]
	mov ebx, 80
	mul ebx
	add eax, dword[y]
	mov ebx, 2
	mul ebx
	mov ebx, eax
	mov al, byte[character]
	mov ah, byte[color]
	mov [es:ebx], eax

	xor eax, eax
	mov eax, dword[x]
	mov ebx, 80
	mul ebx
	mov ebx, dword[y]
	neg ebx
	add ebx, 79
	add eax, ebx
	mov ebx, 2
	mul ebx
	mov ebx, eax
	mov al, byte[character]
	mov ah, byte[color]
	mov [es:ebx], eax
	

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


pgdt dw 0
     dd GDT_START_ADDRESS







