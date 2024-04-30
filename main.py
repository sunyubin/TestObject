from common.Time_now import time_now
import pytest

if __name__ == '__main__':
    pytest.main(["-s",
                 "./TestCase.py",
                 f"--html=./report/TestReport_{time_now()[-1]}.html"])
