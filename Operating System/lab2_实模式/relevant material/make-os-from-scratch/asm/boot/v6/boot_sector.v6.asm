;
; 一个简单的boot sector 
;   1.打印数据的16进制字符串表示

;
;bits 16

[bits 16]
[org 0x7c00]

mov dx, 0x1fb6
call print_hex
jmp $

%include "print_hex.asm"

times 510-($-$$) db 0   ;填充程序到512个字节
dw 0xaa55               ;让bios识别此扇区为可启动扇区的魔数
