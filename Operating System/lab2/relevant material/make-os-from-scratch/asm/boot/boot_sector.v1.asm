;
; 一个简单的boot sector无限循环
;
;bits 16

loop_label:
jmp     loop_label      ;无限循环跳转,也可以不用标号而写作jmp $

times 510-($-$$) db 0   ;填充程序到512个字节

dw 0xaa55               ;让bios识别此扇区为可启动扇区的魔数

