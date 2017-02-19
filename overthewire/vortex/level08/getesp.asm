;.arch x86
;.bits 32

BITS 32

section .text


        jmp short end

start:
        pop esi

; 35 "/usr/include/libr/sflib/linux-x86-32/sflib.h" 1
        ; write(1, "ESP ", 4)
        ; ecx = esi + off_esp
	mov ecx, esi
        ; edx = len_esp
	xor edx, edx
	mov dl, len_esp
        ; ebx = 1
	xor ebx, ebx
	inc ebx
	; eax = 4
	xor eax, eax
	mov al, 4
        int 0x80
	
	; ebp = esi + off_hex
	mov eax, esi
	add al, off_hex
	mov ebp, eax
	; eax = esp
	mov eax, esp
	; esp -= len_val
	sub al, len_val
	xchg esp, eax
        ; edi = esp+len_val
	mov edi, eax
	push esi

fmt_x_loop:
	test eax,eax
	jz end_fmt_x
	mov esi,eax
	; and esi,0xf
	and esi,BYTE 0x0f
	dec esi
	movzx ebx,BYTE [ebp+esi+1]
	dec edi
	mov byte[edi],bl
	shr eax,4
	jmp fmt_x_loop
end_fmt_x:
	pop esi

        ; write(1, val, 1)
        mov ecx, edi
        ;mov edx, 8
	xor edx, edx
	mov dl, 8
        ; mov ebx, 1
	xor ebx, ebx
	inc ebx
	; mov eax, 4
	xor eax, eax
	mov al, 4
        int 0x80

        ; write(1, "\n", 1)
        ;lea ecx, [esi + off_nl]
	mov ecx, esi
	add cl, off_nl
        ;mov edx, 1
	xor edx, edx
	inc edx
        ; mov ebx, 1
	xor ebx, ebx
	inc ebx
	; mov eax, 4
	xor eax, eax
	mov al, 4
        int 0x80

	; hijack 0x0804a00c 4 reloc.printf_12
	mov ebx, 0x0804a00c
	mov dword [ebx], 0xdeadbeef

        ; exit(0)
        ; mov ebx, 0
	xor ebx, ebx
	; mov eax, 1
	xor eax, eax
	inc eax
        int 0x80

end:
        call start



;section .data
;	align 1

data:

msg_esp:
	db "ESP "
off_esp: equ msg_esp - data
len_esp: equ $-msg_esp

; NASM syntax use backquote strings for special chars escapes
msg_nl:
	db 0x10
off_nl: equ msg_nl - data
len_nl: equ $-msg_nl

str_hex:
	db "0123456789abcdef"
off_hex: equ str_hex - data
len_hex: equ $-str_hex

len_val: equ 8
