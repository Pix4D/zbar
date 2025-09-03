cmake_minimum_required(VERSION 3.10)
project(ZBarQRCodeTest)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (APPLE)
    set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
elseif(UNIX)
    set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
endif()

find_package(zbar)

add_executable(testApp main.cpp)
target_link_libraries(testApp
    PRIVATE
       zbar::zbar
)

install(TARGETS testApp)
