CC = gcc
LD = ld
ASM = nasm
CFLAGS = -f bin

bootNew.bin: boot.s
	$(ASM) $(FLAGS) -o bootNew.bin boot.s
	
bootNew.o: boot.s
	$(ASM) -f elf32 -o bootNew.o boot.s

bootNew: bootNew.o
	$(CC) -m32 -static -o bootNew bootNew.o
