include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
        message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()

find_package(Threads REQUIRED)

function(swat_add_library)
    set(options)
    set(one_value_args NAME)
    set(multi_value_args SOURCES PUBLIC_HEADERS LINK_LIBRARIES)
    cmake_parse_arguments(MODULE "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})
    
    add_library(${MODULE_NAME} SHARED ${MODULE_SOURCES} ${MODULE_PUBLIC_HEADERS} )
    target_link_libraries(${MODULE_NAME} PUBLIC ${MODULE_LINK_LIBRARIES} )
    set_target_properties(${MODULE_NAME} PROPERTIES PUBLIC_HEADER "${MODULE_PUBLIC_HEADERS}")
    target_compile_options(${MODULE_NAME} PRIVATE -Wno-write-strings -Wno-sign-compare)
    if(NOT("CMAKE_BUILD_TYPE" STREQUAL "Coverage"))
        target_compile_options(${MODULE_NAME} PRIVATE -g -O1)
    endif()
endfunction(swat_add_library)

function(swat_add_executable)
    set(options)
    set(one_value_args NAME)
    set(multi_value_args SOURCES LINK_LIBRARIES)
    cmake_parse_arguments(MODULE "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})

    add_executable(${MODULE_NAME} ${MODULE_SOURCES})
    target_link_libraries(${MODULE_NAME} PUBLIC ${MODULE_LINK_LIBRARIES} )
    target_compile_options(${MODULE_NAME} PRIVATE -Wno-write-strings -Wno-sign-compare)
    if(NOT("CMAKE_BUILD_TYPE" STREQUAL "Coverage"))
        target_compile_options(${MODULE_NAME} PRIVATE -g -O1)
    endif()
endfunction(swat_add_executable)

swat_add_library(
    NAME configservice
    SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/Config.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/ConfigService.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/InsertionOperator.cpp
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/../commandline_input/ConfigService.h
)
target_include_directories(configservice PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../)

swat_add_library(
    NAME swatapi
    SOURCES
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_packet.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_support.cpp
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api_config.cpp
    PUBLIC_HEADERS
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api.h
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_api_config.h
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_defs.h
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_errors.h
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_packet.h
        ${CMAKE_CURRENT_LIST_DIR}/../swat/swat_support.h
    LINK_LIBRARIES
        m pthread configservice
)
target_include_directories(swatapi PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../swat/)

file(GLOB swatini ${CMAKE_CURRENT_LIST_DIR}/../swat/SWAT_config.ini)
file(COPY ${swatini} DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/ini)