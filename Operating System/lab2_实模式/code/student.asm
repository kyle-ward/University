; If you meet compile error, try 'sudo apt install gcc-multilib g++-multilib' first

%include "head.include"


; you code here

your_if:
; put your implementation here
mov edx, dword[a1]
cmp edx, 12
jl c1
cmp edx, 24
jl c2
jmp c3

c1:
	shr edx, 1
	add edx, 1
	jmp if_exit

c2:
	sub edx, 24
	neg edx
	imul edx, dword[a1]
	jmp if_exit

c3:
	shl edx, 4
	jmp if_exit

if_exit:
	mov dword[if_flag], edx


;36
your_while:
mov eax, [a2]
; put your implementation here
	cmp eax, 12
	jl while_exit
	
	call my_random
	mov ebx, [a2]
	mov ecx, [while_flag]
	mov byte[ecx + ebx - 12], al
	dec dword[a2]
	jmp your_while

while_exit:


%include "end.include"
your_function:
; put your implementation here
	pushad
	xor eax, eax
loop:
	mov ecx, [your_string]
	cmp byte[ecx + eax], 0
	je function_exit
	pushad
	mov ebx, dword[ecx + eax]
	push ebx
	call print_a_char
	pop ebx
	popad
	add eax, 1
	jmp loop


function_exit:
	popad
	ret












