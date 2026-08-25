---
tags:
  - ros2
  - testing
  - gtest
  - cpp
  - unit-tests
  - ament_cmake_gtest
  - intermediate
created: 2026-08-25
aliases:
  - Viết Unit Test C++ với GTest
  - Writing Basic Tests with C++ with GTest
---

# 🧱 Viết Unit Test C++ với Google Test (ament_cmake_gtest)

> [!INFO] **Mục tiêu bài học**
> Học cách tích hợp **Google Test (GTest)** vào một package C++ (`ament_cmake`), cấu hình điều kiện `if(BUILD_TESTING)` trong `CMakeLists.txt`, sử dụng macro `ament_add_gtest` và thực thi các assertion kiểm tra logic thuật toán.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 15 phút
> - **Bài trước:** [[02 - Running Tests from Command Line|Chạy Kiểm thử từ Dòng lệnh với colcon]]
> - **Bài song song (Python):** [[04 - Writing Unit Tests with Python and Pytest|Viết Unit Test Python với Pytest]]
> - **Bài tiếp theo:** [[05 - Writing Integration Tests with launch_testing|Viết Integration Test với launch_testing]]

---

## 📖 Bối cảnh (Background)

Trong hệ sinh thái C++ của ROS 2, **Google Test (GTest)** là framework kiểm thử đơn vị tiêu chuẩn. Package `ament_cmake_gtest` đóng gói sẵn GTest giúp việc khai báo bài test trong CMake trở nên cực kỳ gọn gàng.

---

## 🛠️ Triển khai mã nguồn GTest (Tasks)

### 1. Viết File Test (`test/tutorial_test.cpp`)

Tạo thư mục `test/` trong package C++ của bạn và thêm file `tutorial_test.cpp`:

```cpp
#include <gtest/gtest.h>

// Định nghĩa Test Case 1: Kiểm tra phép toán cơ bản
TEST(TestMathLogic, BasicAssertions)
{
  EXPECT_STRNE("hello", "world");
  EXPECT_EQ(7 * 6, 42);
}

// Định nghĩa Test Case 2: Kiểm tra hàm xử lý của Robot
TEST(TestRobotKinematics, DistanceCalculation)
{
  double x = 3.0;
  double y = 4.0;
  double distance = std::sqrt(x * x + y * y);
  
  // ASSERT_EQ sẽ dừng ngay test case nếu fail
  ASSERT_DOUBLE_EQ(distance, 5.0);
}

int main(int argc, char ** argv)
{
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
```

> [!NOTE] **Phân biệt `ASSERT_*` và `EXPECT_*`:**
> - **`EXPECT_*`:** Ghi nhận lỗi nếu thất bại nhưng **vẫn tiếp tục** chạy các dòng lệnh tiếp theo trong test case.
> - **`ASSERT_*`:** Nếu thất bại, **dừng ngay lập tức** test case hiện tại để tránh gây lỗi phân đoạn (Segmentation Fault) cho các dòng sau.

---

### 2. Khai báo Dependency trong `package.xml`
Thêm thẻ `<test_depend>`:

```xml
<test_depend>ament_cmake_gtest</test_depend>
```

---

### 3. Cấu hình `CMakeLists.txt`

Toàn bộ mã kiểm thử bắt buộc phải được bọc trong khối điều kiện `if(BUILD_TESTING)`:

```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  # 1. Đăng ký executable GTest
  ament_add_gtest(${PROJECT_NAME}_tutorial_test test/tutorial_test.cpp)

  # 2. Cấu hình Include Directories
  target_include_directories(${PROJECT_NAME}_tutorial_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
  )

  # 3. Liên kết với thư viện logic của package (nếu có)
  # target_link_libraries(${PROJECT_NAME}_tutorial_test ${PROJECT_NAME})
endif()
```

---

### 4. Biên dịch và Thực thi Test

```bash
cd ~/ros2_ws
colcon test --packages-select my_cpp_package
colcon test-result --all --verbose
```

---

## 📌 Tóm tắt (Summary)
- Sử dụng `ament_add_gtest` trong khối `if(BUILD_TESTING)`.
- Kết hợp `EXPECT_*` và `ASSERT_*` để kiểm tra toàn diện các module C++.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[02 - Running Tests from Command Line|Chạy Kiểm thử từ Dòng lệnh với colcon]]
- 🐍 Phiên bản Python: [[04 - Writing Unit Tests with Python and Pytest|Viết Unit Test Python với Pytest]]
- ➡️ Bài tiếp theo: [[05 - Writing Integration Tests with launch_testing|Viết Integration Test với launch_testing]]
