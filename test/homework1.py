from selenium import webdriver
import time, yaml
from selenium.common.exceptions import NoSuchElementException


class GetGithubStuff():
    def __init__(self):
        # 初始化
        self.url = "https://book.douban.com/"
        # 启动driver
        self.driver = webdriver.Chrome()
        # 访问url
        self.driver.get(self.url)

    def get_books(self, search_url):
        # 请求搜索URL
        self.driver.get(search_url)

        # 获取数据块部分元素
        book_list = self.driver.find_elements_by_tag_name("li")
        # 打开gdata.yaml文件，为后期存储做准备
        # f = open("douban.yaml", "w")
        with open("douban.yml", "w") as f:
            # 循环获取数据
            for book in book_list:
                # 捕获异常
                # print('book', book)
                try:
                    name = book.find_element_by_class_name("title").text
                    book_name = name
                    book_url = book.find_element_by_tag_name("img")
                    href = book_url.get_attribute('src')
                    # 组装数据
                    if len(book_name) > 1:
                        data = {
                            book_name: {
                                "book_name": book_name,
                                "img_href": href,

                            }
                        }
                        print(data)

                        # 写yaml文件
                        f.write(book_name)

                        yaml.dump(data, f,encoding='utf-8',allow_unicode=True)
                # 捕获找不到元素的异常
                except NoSuchElementException as e:
                    pass
                    # print(e)
                # 捕获其他异常，当出现时，关闭文件
                except Exception as e:
                    pass
        # 关闭文件
        # f.close()
        # 关闭浏览器driver
        self.driver.close()

    def run(self):
        # 要获取多少页数据
        # for n in range(1, 101, 1):
        # 定义搜索url
        url = "https://book.douban.com/"
        self.get_books(url)


if __name__ == '__main__':
    g = GetGithubStuff()
    g.run()
