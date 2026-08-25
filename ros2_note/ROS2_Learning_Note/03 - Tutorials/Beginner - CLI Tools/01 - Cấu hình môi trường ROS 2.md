---
aliases:
  - Configuring environment
tags:
  - ros2
  - environment
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared:
    - jazzy
    - humble
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html
translation-status: complete
---

# Cấu hình môi trường ROS 2

## Nguồn

- Lyrical: [Configuring environment](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)
- Jazzy: [Configuring environment](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)
- Humble: [Configuring environment](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Configuring-ROS2-Environment.html)

## Mục tiêu

Chuẩn bị shell để sử dụng các command và package của ROS 2, đồng thời kiểm tra các biến môi trường mà ROS 2 cần.

## Điều kiện tiên quyết

- Một bản ROS 2 đã được cài đặt. Note này không thay thế quy trình installation.
- Biết distribution ROS 2 đang dùng; các ví dụ dưới đây dùng `{DISTRO}` như một chỗ thay bằng tên distribution thực tế.

## Nội dung

### Sourcing setup file

ROS 2 kết hợp các [[Workspace|workspace]] thông qua môi trường shell. Bản ROS 2 cốt lõi là *underlay*; workspace cục bộ được source sau đó là *overlay*. Mỗi setup file được source bổ sung command, package và biến môi trường của lớp đó; vì vậy source đúng distribution trước khi dùng ROS 2.

Trong mỗi shell mới, source setup file phù hợp với nơi đã cài ROS 2:

```console
$ source /opt/ros/{DISTRO}/setup.bash
```

Nếu không dùng `bash`, thay hậu tố bằng shell tương ứng: `setup.bash`, `setup.sh` hoặc `setup.zsh`.

Các ví dụ theo platform trong tài liệu Lyrical là:

```console
$ . ~/ros2_install/ros2-osx/setup.bash
```

```console
$ call C:\\dev\\ros2\\local_setup.bat
```

> [!warning] Đường dẫn cài đặt
> Command chính xác phụ thuộc vào vị trí cài ROS 2. Nếu source thất bại, kiểm tra đường dẫn setup file thay vì dùng nguyên văn một đường dẫn không khớp với bản cài của bạn.

### Automatic sourcing

Để không phải source thủ công trong mỗi shell mới, thêm command vào startup script của shell. Ví dụ Linux với `bash`:

```console
$ echo "source /opt/ros/{DISTRO}/setup.bash" >> ~/.bashrc
```

macOS dùng:

```console
$ echo "source ~/ros2_install/ros2-osx/setup.bash" >> ~/.bash_profile
```

Với Windows PowerShell, tạo `Microsoft.PowerShell_profile.ps1` trong thư mục `WindowsPowerShell` thuộc `My Documents`, rồi đặt vào file:

```console
$ C:\\dev\\ros2_{DISTRO}\\local_setup.ps1
```

Nếu PowerShell hỏi quyền chạy script mỗi khi mở shell, tài liệu đưa command:

```console
$ Unblock-File C:\\dev\\ros2_{DISTRO}\\local_setup.ps1
```

Muốn hoàn tác automatic sourcing, xóa command đã thêm khỏi startup script (hoặc xóa profile PowerShell vừa tạo).

### Kiểm tra biến môi trường

Sau khi source, kiểm tra môi trường trên Linux hoặc macOS:

```console
$ printenv | grep -i ROS
```

Trên Windows:

```console
$ set | findstr -i ROS
```

Kết quả cần có các biến như sau (giá trị `{DISTRO}` là distribution đã source):

```console
ROS_VERSION=2
ROS_PYTHON_VERSION=3
ROS_DISTRO={DISTRO}
```

Nếu các biến không đúng, hãy trở lại phần package installation đã dùng và xác nhận setup file thuộc đúng distribution.

### `ROS_DOMAIN_ID`

Sau khi chọn một số nguyên duy nhất cho nhóm node, đặt domain ID trong Linux:

```console
$ export ROS_DOMAIN_ID=<your_domain_id>
$ echo "export ROS_DOMAIN_ID=<your_domain_id>" >> ~/.bashrc
```

Trên macOS, thay `~/.bashrc` bằng `~/.bash_profile`. Trên Windows:

```console
$ set ROS_DOMAIN_ID=<your_domain_id>
$ setx ROS_DOMAIN_ID <your_domain_id>
```

Command đầu đặt giá trị cho shell hiện tại; command thứ hai của từng platform giữ lại cho các shell sau.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Nội dung, command sourcing, startup script và `ROS_DOMAIN_ID` giống Lyrical. Jazzy cũng dùng `ROS_AUTOMATIC_DISCOVERY_RANGE` để giới hạn phạm vi discovery; không có thao tác bổ sung cho tutorial này.

> [!warning] ROS 2 Humble
> Thay mục `ROS_AUTOMATIC_DISCOVERY_RANGE` của Lyrical/Jazzy bằng `ROS_LOCALHOST_ONLY`. Đặt `ROS_LOCALHOST_ONLY=1` để giới hạn communication vào localhost; topics, services và actions sẽ không hiện với máy khác trong mạng cục bộ.
>
> ```console
> $ export ROS_LOCALHOST_ONLY=1
> $ echo "export ROS_LOCALHOST_ONLY=1" >> ~/.bashrc
> ```
>
> Trên macOS dùng `~/.bash_profile`; trên Windows dùng `set ROS_LOCALHOST_ONLY=1` và `setx ROS_LOCALHOST_ONLY 1`.

## Kiến thức liên quan

- [[Workspace]]
- [[ROS]]
- [[ROS 2 distribution]]

## Bước tiếp theo

- [[Sử dụng turtlesim, ros2 và rqt]]
