---
aliases: [Recording and playing back data, Ghi và phát lại dữ liệu]
tags: [ros2, rosbag, cli, topic, service, action]
area: tutorials
level: beginner
distributions:
  primary: lyrical
  compared: [jazzy, humble]
sources:
  lyrical: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
  jazzy: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
  humble: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html
translation-status: complete
---

# Ghi và phát lại dữ liệu

## Nguồn

- Lyrical: [Recording and playing back data](https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)
- Jazzy: [Recording and playing back data](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)
- Humble: [Recording and playing back data](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

## Mục tiêu

Ghi dữ liệu publish trên topic, service và action để phát lại, kiểm tra bất cứ lúc nào.

## Điều kiện tiên quyết

- `ros2 bag` có trong bản cài ROS 2 thường dùng; source ROS 2 trong mỗi terminal mới.
- Hoàn thành [[Tìm hiểu về node]], [[Tìm hiểu về topic]], [[Tìm hiểu về service]], [[Tìm hiểu về action]] và [[Sử dụng turtlesim, ros2 và rqt]].

## Nội dung

[[rosbag|`ros2 bag`]] là CLI ghi dữ liệu đi qua bất kỳ số lượng topic, service và action nào vào database. Dữ liệu có thể phát lại để tái tạo test/thí nghiệm, chia sẻ công việc và giúp người khác tái tạo nó.

## Quản lý topic data

### 1. Setup

Khởi động `/turtlesim` và `/teleop_turtle`:

```console
$ ros2 run turtlesim turtlesim_node
```

```console
$ ros2 run turtlesim turtle_teleop_key
```

Tạo thư mục nơi lưu recording. Linux/macOS:

```console
$ mkdir bag_files
$ cd bag_files
```

Windows:

```console
$ md bag_files
$ cd bag_files
```

### 2. Chọn topic

```console
$ ros2 topic list
/parameter_events
/rosout
/turtle1/cmd_vel
/turtle1/color_sensor
/turtle1/pose
```

`/turtle_teleop` publish command điều khiển turtle lên `/turtle1/cmd_vel`. Xem message của nó:

```console
$ ros2 topic echo /turtle1/cmd_vel
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

Ban đầu chưa có output vì teleop chưa publish; focus terminal teleop rồi dùng arrow keys.

### 3. Ghi topic

Ghi một topic theo cú pháp:

```console
$ ros2 bag record --topics <topic_name>
```

Tại thư mục `bag_files`:

```console
$ ros2 bag record --topics /turtle1/cmd_vel
[INFO] [rosbag2_storage]: Opened database 'rosbag2_2019_10_11-05_18_45'.
[INFO] [rosbag2_transport]: Listening for topics...
[INFO] [rosbag2_transport]: Subscribed to topic '/turtle1/cmd_vel'
[INFO] [rosbag2_transport]: All requested topics are subscribed. Stopping discovery...
```

Di chuyển turtle theo một mẫu dễ nhận ra, rồi `Ctrl-C`. Bag directory mới tên dạng `rosbag2_year_month_day-hour_minute_second` có `metadata.yaml` và file bag định dạng đã ghi.

Ghi nhiều topic và đặt tên directory:

```console
$ ros2 bag record -o subset --topics /turtle1/cmd_vel /turtle1/pose
[INFO] [rosbag2_storage]: Opened database 'subset'.
[INFO] [rosbag2_transport]: Listening for topics...
[INFO] [rosbag2_transport]: Subscribed to topic '/turtle1/cmd_vel'
[INFO] [rosbag2_transport]: Subscribed to topic '/turtle1/pose'
[INFO] [rosbag2_transport]: All requested topics are subscribed. Stopping discovery...
```

`-o subset` đặt tên bag directory; các topic đứng sau `--topics`, cách nhau bằng space. `-a` ghi mọi topic trên hệ thống.

Tách recording theo thời lượng (`-d <max_bag_duration>`) hoặc dung lượng (`-b <max_bag_size>`), tránh file quá lớn và giảm mất mát khi recording hỏng:

```console
$ ros2 bag record -o subset_split -d 5 --topics /turtle1/cmd_vel /turtle1/pose
[INFO] [rosbag2_recorder]: Press SPACE for pausing/resuming
[INFO] [rosbag2_recorder]: Listening for topics...
[INFO] [rosbag2_recorder]: Event publisher thread: Starting
[INFO] [rosbag2_recorder]: Recording...
[INFO] [rosbag2_recorder]: Subscribed to topic '/turtle1/cmd_vel'
[INFO] [rosbag2_recorder]: Subscribed to topic '/turtle1/pose'
[INFO] [rosbag2_recorder]: All requested topics are subscribed. Stopping discovery...
[INFO] [rosbag2_cpp]: Writing remaining messages from cache to the bag. It may take a while
```

Chạy ít nhất 15 giây rồi `Ctrl-C`; `subset_split` sẽ có `0_subset_split_YYYY_MM_DD-HH_MM_SS.mcap`, `1_subset_split_YYYY_MM_DD-HH_MM_SS.mcap`, v.v.

### 4. Kiểm tra topic data

```console
$ ros2 bag info <bag_name>
```

```console
$ ros2 bag info subset
Files:             subset_0.mcap
Bag size:          228.5 KiB
Storage id:        mcap
ROS Distro:        lyrical
Duration:          48.47s
Start:             Oct 11 2019 06:09:09.12 (1570799349.12)
End                Oct 11 2019 06:09:57.60 (1570799397.60)
Messages:          3013
Topic information: Topic: /turtle1/cmd_vel | Type: geometry_msgs/msg/Twist | Count: 9 | Serialization Format: cdr
                   Topic: /turtle1/pose | Type: turtlesim_msgs/msg/Pose | Count: 3004 | Serialization Format: cdr
Services:          0
Service information:
Actions:           0
Action information:
```

`ros2 bag info subset_split/0_subset_split_YYYY_MM_DD-HH_MM_SS.mcap` chỉ hiển thị phần 5 giây đó.

### 5. Phát topic data

Dừng teleop bằng `Ctrl-C`, để cửa sổ turtlesim hiện ra, rồi chạy:

```console
$ ros2 bag play subset
[INFO] [rosbag2_player]: Set rate to 1
[INFO] [rosbag2_player]: Adding keyboard callbacks.
[INFO] [rosbag2_player]: Press SPACE for Pause/Resume
[INFO] [rosbag2_player]: Press CURSOR_RIGHT for Play Next Message
[INFO] [rosbag2_player]: Press CURSOR_UP for Increase Rate 10%
[INFO] [rosbag2_player]: Press CURSOR_DOWN for Decrease Rate 10%
Progress bar enabled at 3 Hz.
Progress bar [?]: [R]unning, [P]aused, [B]urst, [D]elayed, [S]topped
[INFO] [rosbag2_player]: Playback until timestamp: -1
```

Turtle đi lại cùng đường đã ghi, nhưng không chính xác 100% vì `turtlesim` nhạy với thay đổi nhỏ về timing. Vì `subset` có `/turtle1/pose`, play chạy lâu bằng thời gian turtlesim chạy: `/turtlesim` liên tục publish pose. Kiểm tra tần suất bằng:

```console
$ ros2 topic hz /turtle1/pose
```

Có thể ghi hai bag riêng rồi phát đồng bộ theo thứ tự message ban đầu:

```console
$ ros2 bag record -o subset_cmd_vel --topics /turtle1/cmd_vel
```

```console
$ ros2 bag record -o subset_pose --topics /turtle1/pose
```

```console
$ ros2 bag play -i subset_cmd_vel -i subset_pose
```

`--message-order {received,sent}` chọn time nhận hay publish để sắp message; mặc định `received`.

## Quản lý service data

Để ghi service, phải bật Service Introspection trên node. Chạy server và client:

```console
$ ros2 run demo_nodes_cpp introspection_service --ros-args -p service_configure_introspection:=contents
```

```console
$ ros2 run demo_nodes_cpp introspection_client --ros-args -p client_configure_introspection:=contents
```

Kiểm tra giao tiếp đã được introspect:

```console
$ ros2 service list
/add_two_ints
/introspection_client/describe_parameters
/introspection_client/get_parameter_types
/introspection_client/get_parameters
/introspection_client/get_type_description
/introspection_client/list_parameters
/introspection_client/set_parameters
/introspection_client/set_parameters_atomically
/introspection_service/describe_parameters
/introspection_service/get_parameter_types
/introspection_service/get_parameters
/introspection_service/get_type_description
/introspection_service/list_parameters
/introspection_service/set_parameters
/introspection_service/set_parameters_atomically
```

```console
$ ros2 service echo --flow-style /add_two_ints
info:
  event_type: REQUEST_SENT
  stamp:
    sec: 1713995389
    nanosec: 386809259
  client_gid: [1, 15, 96, 219, 162, 1, 108, 201, 0, 0, 0, 0, 0, 0, 21, 3]
  sequence_number: 133
request: [{a: 2, b: 3}]
response: []
---
```

Ghi một hoặc tất cả service (có thể ghi cùng topic):

```console
$ ros2 bag record --service <service_names>
```

```console
$ ros2 bag record --all-services
```

```console
$ ros2 bag record --service /add_two_ints
[INFO] [1713995957.643573503] [rosbag2_recorder]: Press SPACE for pausing/resuming
[INFO] [1713995957.662067587] [rosbag2_recorder]: Event publisher thread: Starting
[INFO] [1713995957.662067614] [rosbag2_recorder]: Listening for topics...
[INFO] [1713995957.666048323] [rosbag2_recorder]: Subscribed to topic '/add_two_ints/_service_event'
[INFO] [1713995957.666092458] [rosbag2_recorder]: Recording...
```

`Ctrl-C` để dừng. Kiểm tra và phát lại request sau khi dừng `introspection_client`:

```console
$ ros2 bag info <bag_file_name>
Files:             rosbag2_2024_04_24-14_59_17_0.mcap
Bag size:          15.1 KiB
Storage id:        mcap
ROS Distro:        lyrical
Duration:          9.211s
Start:             Apr 24 2024 14:59:17.676 (1713995957.676)
End:               Apr 24 2024 14:59:26.888 (1713995966.888)
Messages:          0
Topic information:
Service:           1
Service information: Service: /add_two_ints | Type: example_interfaces/srv/AddTwoInts | Event Count: 78 | Serialization Format: cdr
```

```console
$ ros2 bag play --publish-service-requests <bag_file_name>
[INFO] [1713997477.870856190] [rosbag2_player]: Set rate to 1
[INFO] [1713997477.877417477] [rosbag2_player]: Adding keyboard callbacks.
[INFO] [1713997477.877442404] [rosbag2_player]: Press SPACE for Pause/Resume
[INFO] [1713997477.877447855] [rosbag2_player]: Press CURSOR_RIGHT for Play Next Message
[INFO] [1713997477.877452655] [rosbag2_player]: Press CURSOR_UP for Increase Rate 10%
[INFO] [1713997477.877456954] [rosbag2_player]: Press CURSOR_DOWN for Decrease Rate 10%
[INFO] [1713997477.877573647] [rosbag2_player]: Playback until timestamp: -1
```

Playback gửi request từ bag đến `/add_two_ints`; terminal server lại in:

```console
[INFO] [1713997478.090466075] [introspection_service]: Incoming request
a: 2 b: 3
```

Để xác minh, chạy trước `ros2 service echo --flow-style /add_two_ints`. Output có `REQUEST_RECEIVED` với `request: [{a: 2, b: 3}]` và `RESPONSE_SENT` với `response: [{sum: 5}]`.

## Quản lý action data

Lyrical yêu cầu Action Introspection. Chạy server và client:

```console
$ ros2 run action_tutorials_py fibonacci_action_server --ros-args -p action_server_configure_introspection:=contents
```

```console
$ ros2 run action_tutorials_cpp fibonacci_action_client --ros-args -p action_client_configure_introspection:=contents
```

```console
$ ros2 action list
/fibonacci
```

`ros2 action echo --flow-style /fibonacci` hiển thị event khi introspection đang bật:

```console
$ ros2 action echo --flow-style /fibonacci
interface: GOAL_SERVICE
info:
  event_type: REQUEST_SENT
  stamp:
    sec: 1744917904
    nanosec: 760683446
  client_gid: [1, 15, 165, 231, 234, 109, 65, 202, 0, 0, 0, 0, 0, 0, 19, 4]
  sequence_number: 1
request: [{goal_id: {uuid: [81, 55, 121, 145, 81, 66, 209, 93, 214, 113, 255, 100, 120, 6, 102, 83]}, goal: {order: 10}}]
response: []
---
...
```

```console
$ ros2 bag record --action <action_names>
```

```console
$ ros2 bag record --all-actions
```

```console
$ ros2 bag record --action /fibonacci
[INFO] [1744953225.214114862] [rosbag2_recorder]: Press SPACE for pausing/resuming
[INFO] [1744953225.218369761] [rosbag2_recorder]: Listening for topics...
[INFO] [1744953225.218386223] [rosbag2_recorder]: Event publisher thread: Starting
[INFO] [1744953225.218580294] [rosbag2_recorder]: Recording...
[INFO] [1744953225.725417634] [rosbag2_recorder]: Subscribed to topic '/fibonacci/_action/cancel_goal/_service_event'
[INFO] [1744953225.727901848] [rosbag2_recorder]: Subscribed to topic '/fibonacci/_action/feedback'
[INFO] [1744953225.729655213] [rosbag2_recorder]: Subscribed to topic '/fibonacci/_action/get_result/_service_event'
[INFO] [1744953225.731315612] [rosbag2_recorder]: Subscribed to topic '/fibonacci/_action/send_goal/_service_event'
[INFO] [1744953225.735061252] [rosbag2_recorder]: Subscribed to topic '/fibonacci/_action/status'
```

Sau `Ctrl-C`, kiểm tra bag:

```console
$ ros2 bag info <bag_file_name>
Files:             rosbag2_2025_04_17-22_20_40_0.mcap
Bag size:          20.7 KiB
Storage id:        mcap
ROS Distro:        lyrical
Duration:          9.019568080s
Start:             Apr 17 2025 22:20:47.263125070 (1744953647.263125070)
End:               Apr 17 2025 22:20:56.282693150 (1744953656.282693150)
Messages:          0
Topic information:
Services:          0
Service information:
Actions:           1
Action information:
  Action: /fibonacci | Type: example_interfaces/action/Fibonacci | Topics: 2 | Service: 3 | Serialization Format: cdr
    Topic: feedback | Count: 9
    Topic: status | Count: 3
    Service: send_goal | Event Count: 4
    Service: cancel_goal | Event Count: 0
    Service: get_result | Event Count: 4
```

Dừng `fibonacci_action_client`, rồi phát lại goal như action client:

```console
$ ros2 bag play --send-actions-as-client <bag_file_name>
[INFO] [1744953720.691068674] [rosbag2_player]: Set rate to 1
[INFO] [1744953720.702365209] [rosbag2_player]: Adding keyboard callbacks.
[INFO] [1744953720.702409447] [rosbag2_player]: Press SPACE for Pause/Resume
[INFO] [1744953720.702423063] [rosbag2_player]: Press CURSOR_RIGHT for Play Next Message
[INFO] [1744953720.702431404] [rosbag2_player]: Press CURSOR_UP for Increase Rate 10%
[INFO] [1744953720.702437677] [rosbag2_player]: Press CURSOR_DOWN for Decrease Rate 10%
Progress bar enabled at 3 Hz.
Progress bar [?]: [R]unning, [P]aused, [B]urst, [D]elayed, [S]topped
[INFO] [1744953720.702577680] [rosbag2_player]: Playback until timestamp: -1
```

`fibonacci_action_server` lại in `Executing goal...` và feedback dãy Fibonacci:

```console
[INFO] [1744953720.815577088] [fibonacci_action_server]: Executing goal...
[INFO] [1744953720.815927050] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1])
[INFO] [1744953721.816509658] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2])
[INFO] [1744953722.817220270] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3])
[INFO] [1744953723.817876426] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5])
[INFO] [1744953724.818498515] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5, 8])
[INFO] [1744953725.819182228] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5, 8, 13])
[INFO] [1744953726.820032562] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5, 8, 13, 21])
[INFO] [1744953727.820738690] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
[INFO] [1744953728.821449308] [fibonacci_action_server]: Feedback: array('i', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
```

Có thể chạy trước `ros2 action echo --flow-style /fibonacci` để quan sát `STATUS_TOPIC`, `GOAL_SERVICE` và `FEEDBACK_TOPIC` trong lúc phát lại.

## Khác biệt phiên bản

> [!info] ROS 2 Jazzy
> Tutorial Jazzy ghi topic và service nhưng chưa có phần ghi/phát action. So với Lyrical, Jazzy dùng cú pháp topic cũ (`ros2 bag record <topic_name>`; không có `--topics`), không có tách file `-d`/`-b`, không có play nhiều bag `-i`, output `ros2 bag info` không có trường service/action và ví dụ pose dùng `turtlesim/msg/Pose`. Ví dụ service vẫn ghi `ROS Distro: rolling` trong output tài liệu.

> [!warning] ROS 2 Humble
> Tutorial Humble chỉ ghi/phát topic. Cú pháp topic cũ không có `--topics`; chưa có ghi service/action, tách file, play nhiều bag hoặc các thông tin service/action của Lyrical. Output Humble dùng `Storage id: sqlite3` và `turtlesim/msg/Pose`.

## Kiến thức liên quan

- [[rosbag]]
- [[Topic]]
- [[Service]]
- [[Action]]
- [[Introspection]]

## Bước tiếp theo

Bạn đã hoàn thành Beginner: CLI Tools. Tiếp tục với Beginner: Client Libraries.
