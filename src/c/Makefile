CC = gcc
CFLAGS = -Wall -Wextra -O3
TARGET = ../../bin/scanner.exe
SRCS = scanner.c

all: $(TARGET)

$(TARGET): $(SRCS) dictionaries.h
	@mkdir -p ../../bin
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

clean:
	rm -f $(TARGET)
