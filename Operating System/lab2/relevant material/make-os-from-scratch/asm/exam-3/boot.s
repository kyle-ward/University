[BITS 16]
start:
  mov ax,07c0h
  add ax,288
  mov ss,ax
  mov sp,4096

  mov ax,07c0h
  mov ds,ax

  mov si,text_string
  call print_string

  jmp $

  text_string db "This is my new OS!",0h

print_string:
   mov ah,0Eh

.repeat:
   lodsb
   cmp al,0
   je .done
   int 10h
   jmp .repeat

.done:
   ret

   times 510-($-$$) db 0h
   dw 0xAA55
