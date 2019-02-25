cmake_minimum_required(VERSION 3.6)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

#add_executable(example example.cpp)
#target_link_libraries(example ${CONAN_LIBS})
add_executable(spdlog_setup_unit_test
  unit_test.cpp
)

set_property(TARGET spdlog_setup_unit_test PROPERTY CXX_STANDARD 11)

add_test(spdlog_setup_unit_test spdlog_setup_unit_test -s)

# Catch2 do not have modular CMake mechanism
if (EXISTS ${CMAKE_SOURCE_DIR}/../../deps/spdlog/CMakeLists.txt)
  target_include_directories(spdlog_setup_unit_test
    PRIVATE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../../deps/Catch2/single_include>)
endif()

target_include_directories(spdlog_setup_unit_test
  PUBLIC
    ${CMAKE_SOURCE_DIR}/included
)

target_link_libraries(spdlog_setup_unit_test
  PRIVATE
    spdlog_setup
    Threads::Threads)

if(SPDLOG_SETUP_INCLUDE_TEST_COVERAGE)
  target_compile_options(spdlog_setup_unit_test
    PRIVATE
      -coverage)

  target_link_libraries(spdlog_setup_unit_test
    PRIVATE
      --coverage)
endif()
