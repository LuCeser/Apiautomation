这是一个用Python编写的REST接口自动化测试项目。

运行以下指令启动

```bash
python test_main/run_main.py
```

## 项目结构

```
├── README.md
├── base
├── config
├── log
├── reports
├── requirements.txt
├── test_case
│   ├── conftest.py
│   └── testRequest
├── test_data
│   ├── exceldata
│   └── jsondata
│       └── testRequest
├── test_main
│   ├── reports
└── util
```

## JSON格式测试用例

一个JSON文件代表一类测试，使用同一个URL