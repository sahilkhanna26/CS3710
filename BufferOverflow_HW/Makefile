all:
	gcc -g -fno-stack-protector -m64 -fomit-frame-pointer -o grade grade.c
	nasm -g -f elf64 -o shellcode.o shellcode.s
	gcc -g -m64 -c shellcode_test.c
	gcc -g -no-pie -m64 -o shellcode_test shellcode.o shellcode_test.o
	gcc -o attack_shellcode attack_shellcode.c
