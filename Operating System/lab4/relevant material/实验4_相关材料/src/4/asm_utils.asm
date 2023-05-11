[bits 32]
global function_from_asm
global function_from_me_asm
extern function_from_C
extern function_from_CPP
extern function_from_me_C
extern function_from_me_CPP

function_from_asm:
    call function_from_C
    call function_from_CPP
    ret

function_from_me_asm:
    call function_from_me_C
    call function_from_me_CPP
    ret
