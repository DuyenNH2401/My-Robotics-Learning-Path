cmake_minimum_required(VERSION 3.20)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# 2. Tìm các package phụ thuộc
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

# 3. Tạo executable và link dependencies
add_executable(number_publisher src/number_publisher.cpp)
target_link_libraries(number_publisher PRIVATE
  rclcpp::rclcpp
  example_interfaces::example_interfaces
)

# 4. Install target
install(TARGETS
  number_publisher
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 5. BẮT BUỘC ở cuối cùng
ament_package()