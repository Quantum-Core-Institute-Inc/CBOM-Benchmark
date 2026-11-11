cmake_minimum_required(VERSION 3.20)
project(telemetry_agent C)

find_package(OpenSSL 1.1 REQUIRED)
find_package(libsodium REQUIRED)
find_package(ZLIB REQUIRED)

add_executable(telemetry_agent src/agent.c)
target_link_libraries(telemetry_agent PRIVATE OpenSSL::SSL OpenSSL::Crypto libsodium::libsodium ZLIB::ZLIB)
