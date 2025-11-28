.PHONY: all build test clean

all: build

build:
	@echo "Building C library..."
	$(MAKE) -C src/c all
	@echo "Copying library to python directory..."
	cp src/c/libsocks5_parser.so src/python/
	@echo "Build complete!"

test:
	@echo "Running tests..."
	$(MAKE) -C src/c test
	python -m pytest task1-testing/ -v

clean:
	$(MAKE) -C src/c clean
	rm -f src/python/libsocks5_parser.so

run:
	cd src/python && python main.py