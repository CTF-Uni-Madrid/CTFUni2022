all:
	gcc items2.c -no-pie -o items2
	patchelf \
		--set-interpreter ./ld-linux-x86-64.so.2 \
		--set-rpath . \
		./items2

clean:
	rm items2