# Google Test root directory
GTEST_DIR = googletest/googletest

# Google Test headers
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h $(GTEST_DIR)/include/gtest/internal/*.h

# Flags
CFLAGS = -Wall -Wextra -Wpedantic -Werror -std=c11
CPPFLAGS = -isystem $(GTEST_DIR)/include
CXXFLAGS = -g -Wall -Wextra -pthread

$(shell mkdir -p build/gtest)

all: build/app.exe unit-tests.exe

clean:
	rm -rf build

run-int: build/app.exe
	build/app.exe

run-float: build/app.exe
	build/app.exe --float

run-unit-test: build/unit-tests.exe
	build/unit-tests.exe

build/app.exe:
	gcc $(CFLAFS) src/main.c -o build/app.exe

build/app-test.o:
	gcc (CFLAFS) -DGTEST -c src/main.c -o build/app-test.o
	
build/unit-tests.exe: build/gtest/gtest_main.a build/app-test.o
	g++ -isystem $(GTEST_DIR)/include -pthread \
		tests/unit/unit_tests.cpp \
		build/gtest/gtest_main.a build/app-test.o \
		-o build/unit-tests.exe

####################################
# BUILD GOOGLE TEST STATIC LIBRARY #
####################################

# Google Test object files
build/test/gtest-all.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	g++ $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest-all.cc -o $@

build/test/gtest_main.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)
	g++ $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

# Google Test static libraries
build/test/gtest_main.a: build/test/gtest-all.o build/test/gtest_main.o
	@ar rv $@ $^ -o $@
