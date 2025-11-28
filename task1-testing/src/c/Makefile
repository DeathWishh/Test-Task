CC=gcc
CFLAGS=-Wall -Wextra -O2 -fPIC
LDFLAGS=-shared

TARGET=libsocks5_parser.so
SOURCES=socks5_parser.c
OBJECTS=$(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $^

clean:
	rm -f $(OBJECTS) $(TARGET)

.PHONY: all clean
