import unittest
import time
from test.util import HTMLTestRunner

# discover = unittest.defaultTestLoader.discover("./test/cases", pattern="test_*.py")
# runner = unittest.TextTestRunner()
# runner.run(discover)


discover = unittest.defaultTestLoader.discover("./test/cases", pattern="test_*.py")
with open("./test/reports/dwf-sdk-python%s.html" % time.strftime("%Y%m%d%H%M%S"),"wb") as f:
    HTMLTestRunner.HTMLTestRunner(f,title="dwf-sdk-python",description="win10").run(discover)