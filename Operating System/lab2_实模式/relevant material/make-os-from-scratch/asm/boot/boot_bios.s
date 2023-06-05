org 07c00h

mov ax,cx
mov ds,ax
mov es,ax
call clear_screen
mov ah,0;
mov al,06ah ;设置图形模式 0x6a 位800 600 16中颜色

int 10h
;画 一条直线
mov bh,0x0 ;视频页
mov dx,300 ;y坐标
mov cx,100 ;x坐标
mov ah,0x0c ;功能号
mov al,9 ;像素值 像素颜色
lib:
 int 10h

inc cx
cmp cx,700
jne lib
jmp $
clear_screen:
 mov ah,0x06
 mov al,0
 mov cx, 0x00
 mov dh,24
 mov dl,40
 mov bh,0x07
 int 10h
 ret

BootMessage: db "He"
times 510-($-$$) db 0 ;填充剩下的空间，使生成的二进制代码恰好为512字节
dw 0xaa55
