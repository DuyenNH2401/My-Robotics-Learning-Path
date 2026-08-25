---
aliases: [log, logger]
tags: [ros2, concept, logging]
area: concepts
level: beginner
distributions:
  primary: lyrical
  compared: [jazzy, humble]
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html
translation-status: complete
---

# Logging

[[Node|Node]] dùng log để xuất thông tin về sự kiện và trạng thái. Đây là một phương tiện [[Introspection|introspection]]: log hỗ trợ xác minh hệ thống đang chạy như mong muốn hoặc truy lại chuỗi sự kiện dẫn đến lỗi.

Logger severity, từ cao đến thấp, là `Fatal`, `Error`, `Warn`, `Info`, `Debug`. Mặc định `Info`; chỉ message ở mức mặc định và nghiêm trọng hơn được hiển thị. `Fatal` báo hệ thống sắp kết thúc để tự bảo vệ; `Error` báo vấn đề lớn ngăn hoạt động đúng; `Warn` báo hoạt động bất thường; `Info` báo sự kiện/trạng thái; `Debug` mô tả chi tiết từng bước.

## Thực hành

- [[Xem log bằng rqt_console]] dùng [[rqt_console]] để gom, lọc và xem log, đồng thời đặt `--log-level WARN`.

## Liên quan

- [[rqt_console]]
- [[Node]]
- [[Introspection]]
