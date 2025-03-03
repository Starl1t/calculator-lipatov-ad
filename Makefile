# Google Test root directory
GTEST_DIR = googletest/googletest

# Google Test headers
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h

# Flags
CFLAGS = -Wall -Wextra -Wpedantic -Werror -std=c11
CPPFLAGS = -isystem $(GTEST_DIR)/include
CXXFLAGS = -g -Wall -Wextra -pthread

$(shell mkdir -p build/gtest)

# Python tests
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

all: build/app.exe build/unit-tests.exe

clean:
	rm -rf build
	rm -rf $(VENV)
	rm -rf tests/integration/__pycache__
	rm -rf .pytest_cache
	
run-int: build/app.exe
	build/app.exe

run-float: build/app.exe
	build/app.exe --float

run-unit-test: build/unit-tests.exe
	build/unit-tests.exe

# Creates venv
$(VENV)/bin/activate:
	python3 -m venv $(VENV)

# Installs Pytest
requirements: $(VENV)/bin/activate
	$(PIP) install pytest

# Executes integration tests
run-integration-tests: build/app.exe requirements
	$(PYTEST) tests/integration/integration_tests.py

build/app.exe:
	gcc $(CFLAGS) src/main.c -o build/app.exe

# build/app-test.o:
#	gcc $(CFLAGS) -DGTEST -c src/main.c -o build/app-test.o
	
build/unit-tests.exe: build/gtest/gtest_main.a
	g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/unit_tests.cpp \
		build/gtest/gtest_main.a \
		-o build/unit-tests.exe

####################################
# BUILD GOOGLE TEST STATIC LIBRARY #
####################################

# Google Test object files
build/gtest/gtest-all.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	g++ $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest-all.cc -o $@

build/gtest/gtest_main.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	g++ $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

# Google Test static libraries
build/gtest/gtest_main.a: build/gtest/gtest-all.o build/gtest/gtest_main.o
	@ar rv $@ $^ -o $@
