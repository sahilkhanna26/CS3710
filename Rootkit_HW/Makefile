obj-m+=root.o

all:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) modules
	/bin/cp -a sha224sum-fake.py sha224sum

clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) clean