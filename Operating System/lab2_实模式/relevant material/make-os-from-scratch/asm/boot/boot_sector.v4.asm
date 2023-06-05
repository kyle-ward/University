;
; 一个简单的boot sector 栈的使用
; 期望：打印出CBA
;
;bits 16

mov ah, 0x0e            ;设置tele-type mode

mov bp, 0x8000
mov sp, bp

push 'A'                ;每次push的是一个字，即2字节
push 'B'
push 'C'

pop bx
mov al, bl
int 0x10

pop bx
mov al, bl
int 0x10

mov al, [0x7ffe]        ;0x8000-0x2
int 0x10

jmp $

times 510-($-$$) db 0   ;填充程序到512个字节
dw 0xaa55               ;让bios识别此扇区为可启动扇区的魔数
