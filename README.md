# Trò Chơi 2048 với AI

Dự án triển khai AI chơi trò chơi 2048 sử dụng thuật toán Expectimax với tối ưu hóa heuristic.

## Tổng Quan
- **Trò Chơi**: 2048, lưới 4x4 nơi các ô số trượt và hợp nhất để đạt ô 2048.
- **Thuật Toán**: Expectimax với cắt tỉa và lưu đệm để ra quyết định hiệu quả.
- **Heuristic**: Đánh giá trạng thái lưới dựa trên:
  - Tính đơn điệu (sắp xếp ô)
  - Số ô trống
  - Ô giá trị lớn nhất ở góc
- **Hiệu Suất**:
  - Độ sâu 2: 78% đạt 2048, điểm trung bình ~43k
  - Độ sâu 3: 90.3% đạt 2048, điểm trung bình ~65k

## Cài Đặt
1. Tải kho lưu trữ:
   ```bash
   git clone <đường-dẫn-kho-lưu-trữ>
   cd <thư-mục-dự-án>
   ```
2. Cài đặt các thư viện yêu cầu:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy trò chơi:
   ```bash
   python main.py
   ```

## Sử Dụng
- AI tự động chơi 2048 với giao diện Tkinter để hiển thị.
- Độ sâu tìm kiếm Expectimax được đặt ở 3 để cân bằng tốc độ và hiệu suất.
- Kết quả được ghi lại, bao gồm điểm số và ô cao nhất đạt được.
