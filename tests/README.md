# 测试文件目录

本目录包含项目的所有测试文件和性能测试脚本。

## 文件说明

### 功能测试
- `test_gui_backend.py` - GUI后端功能测试
- `test_tkinter.py` - tkinter GUI显示测试
- `test_anti_jitter.py` - 防抖动功能测试
- `test_ellipse_mosaic.py` - 椭圆马赛克效果测试

### 性能测试
- `performance_test.py` - 整体性能测试

### 比较测试
- `compare_ellipse_sizes.py` - 椭圆大小比较测试
- `compare_jitter_fix.py` - 抖动修复效果比较

## 运行测试

```bash
# 运行单个测试
python3 tests/test_gui_backend.py

# 运行性能测试
python3 tests/performance_test.py

# 运行GUI测试
python3 tests/test_tkinter.py
```

## 注意事项

- 某些测试需要安装额外依赖（如DeepFace）
- GUI相关测试需要图形界面支持
- 性能测试可能需要较长时间运行