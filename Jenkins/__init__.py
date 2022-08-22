import allure-pytest

pytest.main(["-m", "smoke",
             "--alluredir=Report\\test"])  # 这个目录就是存放allure生成的xml文件的目录