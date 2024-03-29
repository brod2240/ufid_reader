cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)


project(usbTest_project C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)


pico_sdk_init()

add_executable(usbTest
    usbTest.c    
)



pico_enable_stdio_usb(usbTest 1)
pico_enable_stdio_uart(usbTest 0)

pico_add_extra_outputs(usbTest)

target_link_libraries(usbTest 
  pico_stdlib

)