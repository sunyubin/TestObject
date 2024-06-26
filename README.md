project/
├── app/
│   ├── __init__.py        # 使 app 目录成为一个 Python 包
│   ├── main.py            # FastAPI 应用的入口点，设置路由和中间件
│   ├── routers/           # 存放所有路由文件
│   │   ├── __init__.py    # 使 routers 目录成为一个 Python 包
│   │   ├── tests.py       # 定义与测试用例相关的路由
│   ├── models/            # 存放数据模型和业务逻辑文件
│   │   ├── __init__.py    # 使 models 目录成为一个 Python 包
│   │   ├── test_case.py   # 定义测试用例的数据模型和业务逻辑
├── tests/                 # 存放实际的测试文件
│   ├── __init__.py        # 使 tests 目录成为一个 Python 包
│   ├── test_sample.py     # 示例测试文件，可以包含测试用例
├── static/                # 存放静态文件，如 HTML、CSS、JavaScript
│   ├── index.html         # 前端界面，用于与用户交互
├── templates/             # 存放 Jinja2 模板文件
│   ├── index.html         # 用于渲染的模板文件
├── requirements.txt       # 项目依赖的 Python 包
└── README.md              # 项目说明文档
