---
tags:
  - ros2
  - python
  - asyncio
  - async-node
  - coroutines
  - intermediate
created: 2026-08-25
aliases:
  - Viết Async Node với asyncio (Python)
  - Writing an async node with asyncio (Python)
---

# ⚡ Viết Async Node với asyncio trong Python (rclpy.experimental.AsyncNode)

> [!INFO] **Mục tiêu bài học**
> Làm quen với **`AsyncNode`** — API thế hệ mới thuần **`asyncio`** của ROS 2 Python, cho phép sử dụng cú pháp `async def` / `await` trực tiếp bên trong các callback của node mà không làm nghẽn (block) event loop hay gây lỗi deadlock.
> - **Cấp độ:** Intermediate
> - **Thời lượng ước tính:** 20 phút
> - **Yêu cầu:** Python 3.12+ (ROS 2 Jazz/Rolling hoặc mới hơn)
> - **Bài trước:** [[04 - Writing Action Server and Client (Python)|Viết Action Server và Client (Python)]]
> - **Bài tiếp theo:** [[06 - Writing a Composable Node (C++)|Viết Composable Node (C++)]]

---

## 📖 Bối cảnh (Background)

Trong các node `rclpy.node.Node` tiêu chuẩn, các callback chạy trên executor tùy biến của ROS 2. Nếu bạn gọi một Service hoặc thực hiện tác vụ I/O dài hạn từ bên trong một callback, hệ thống rất dễ rơi vào trạng thái nghẽn tiến trình (*Deadlock*).

**`AsyncNode`** (nằm trong `rclpy.experimental`) giải quyết triệt để vấn đề này bằng cách đưa toàn bộ vòng đời node chạy trên **`asyncio Event Loop`** của Python:
- Cho phép `await` bất kỳ tác vụ bất đồng bộ nào (gọi Service lồng nhau, gọi HTTP API, đọc ghi database, sleep theo ROS Clock).
- Kết hợp hoàn hảo với hệ sinh thái thư viện `asyncio` hiện đại (FastAPI, aiohttp, asyncpg...).
- Hỗ trợ xử lý song song nhiều request cùng lúc với tùy chọn `concurrent=True`.

---

## 🛠️ Các bước thực hiện (Tasks)

### 1. Tạo Package `python_async_node`
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python python_async_node --dependencies rclpy example_interfaces
```

---

### 2. Viết Async Service Server (`async_service.py`)
Tạo file `python_async_node/async_service.py`:

```python
import asyncio
from example_interfaces.srv import Trigger
import rclpy
from rclpy.experimental import AsyncNode


class TriggerServer(AsyncNode):

    def __init__(self):
        super().__init__('trigger_server')
        # Tạo Service với async callback
        self._service = self.create_service(
            Trigger, 'trigger', self._callback
        )

    # Callback là một async coroutine
    async def _callback(self, _request, response):
        self.get_logger().info('Nhan yeu cau Trigger, dang xu ly bat dong bo...')
        # Await theo thoi gian mo phong cua ROS 2
        await self.get_clock().sleep(2.0)
        response.success = True
        response.message = 'Da hoan thanh sau 2 giay non-blocking!'
        return response


async def _async_main():
    with rclpy.init():
        node = TriggerServer()
        # await node.run() tuong duong voi rclpy.spin() nhung non-blocking
        await node.run()


def main():
    asyncio.run(_async_main())


if __name__ == '__main__':
    main()
```

---

### 3. Viết Async Service Client (`async_client.py`)
Tạo file `python_async_node/async_client.py`:

```python
import asyncio
from example_interfaces.srv import Trigger
import rclpy
from rclpy.experimental import AsyncNode


async def _async_main():
    with rclpy.init():
        # Su dung context manager `async with` tu dong khoi tao va cleanup node
        async with AsyncNode('trigger_client') as node:
            client = node.create_client(Trigger, 'trigger')

            node.get_logger().info('Dang cho Service trigger...')
            await client.wait_for_service()
            node.get_logger().info('Service san sang, dang gui request...')

            request = Trigger.Request()
            # Await truc tiep ket qua tra ve ma khong can Future
            response = await client.call(request)

            node.get_logger().info(
                f'Server phan hoi: success={response.success}, message="{response.message}"'
            )


def main():
    asyncio.run(_async_main())


if __name__ == '__main__':
    main()
```

---

## 🚀 Các kỹ thuật mở rộng với AsyncNode

### 1. Gọi hàm đồng bộ dạng Blocking an toàn với `asyncio.to_thread`
Nếu bạn cần gọi một thư viện đồng bộ (như `urllib`, `requests`, thuật toán nặng), hãy bọc nó trong `asyncio.to_thread` để không làm đứng event loop:

```python
import asyncio
import urllib.request

async def _callback(self, _request, response):
    def fetch_data():
        with urllib.request.urlopen('https://api.github.com') as resp:
            return resp.status
            
    # Chay tren worker thread rieng va await ket qua
    status = await asyncio.to_thread(fetch_data)
    response.message = f'Status: {status}'
    return response
```

### 2. Gọi một Service khác ngay từ bên trong Callback (Nested Calls)
Với `AsyncNode`, bạn có thể thoải mái gọi một Service khác từ bên trong callback mà **không bao giờ bị Deadlock**:

```python
async def _callback(self, _request, response):
    await self._other_client.wait_for_service()
    nested_res = await self._other_client.call(nested_req)
    response.message = f'Ket qua: {nested_res.sum}'
    return response
```

### 3. Xử lý đồng thời nhiều Request với `concurrent=True`
Mặc định service xử lý tuần tự từng request. Đặt `concurrent=True` để mỗi request đến sẽ được dispatch thành một asyncio Task riêng biệt:

```python
self._service = self.create_service(
    Trigger, 'trigger', self._callback, concurrent=True
)
```

---

## 📌 Tóm tắt (Summary)
- `AsyncNode` mang sức mạnh của lập trình bất đồng bộ hiện đại (`async`/`await`) vào ROS 2 Python.
- Giúp loại bỏ hoàn toàn các lỗi Callback Deadlock phổ biến khi gọi Service lồng nhau hoặc xử lý I/O.

---

## 🔗 Liên kết & Bài tiếp theo
- ⬅️ Bài trước: [[04 - Writing Action Server and Client (Python)|Viết Action Server và Client (Python)]]
- ➡️ Bài tiếp theo: [[06 - Writing a Composable Node (C++)|Viết Composable Node (C++)]]
