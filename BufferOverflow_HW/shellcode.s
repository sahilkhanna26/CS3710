; shellcode.s

global shellcode
	
	jmp shellcode
	
section .text

string db "Sahil Khanna, your grade on this assignment is an A"

shellcode:    
    xor rax, rax
    mov al, 1
    mov rdi, rax
    lea rsi, [rel string]
    xor rdx, rdx
    mov dl, 51
    syscall
    mov al, 60
    xor rdi, rdi
    syscall
	
