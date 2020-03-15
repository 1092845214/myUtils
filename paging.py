"""

django 中分页功能, 封装成工聚类

"""


class MyPage(object):

    def __init__(self, data_total, current_page, url_prefix, data_per_page=10, page_num_count=7):
        """
        
        	初始化一个分页示例

        :param data_total: 数据总数
        :param current_page: 当前页码数
        :param url_prefix: 分页中 a 标签 url 前缀
        :param data_per_page: 每页显示数据数量
        :param page_num_count: 显示多少个页码
        
        """

        self.data_total = data_total
        self.url_prefix = url_prefix
        self.data_per_page = data_per_page
        self.page_num_count = page_num_count

        try:
            # 为 current_page 参数容错, 如果输入的页码不是数字, 默认显示第一页
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        self.current_page = current_page

        # 当前页码两侧的页码数量
        page_num_half = page_num_count // 2

        # divmod(总数据量, 每页数据量), 返回商和余数, 若余数存在, 则总页数+1
        page_num_total, more = divmod(data_total, data_per_page)
        if more:
            page_num_total += 1

        # 如果请求的页码大于总数据的页码, 默认显示最后一页
        if current_page > page_num_total:
            current_page = page_num_total

        # 如果请求的页码小于1, 默认显示第一页
        if current_page < 1:
            current_page = 1

        # 计算展示页码的起点和终点
        page_num_start = current_page - page_num_half
        page_num_end = current_page + page_num_half

        # 特殊情况特殊处理
        # 1. 当前页码 - 左侧页码数量 <= 0
        if current_page - page_num_half <= 0:
            page_num_start = 1
            page_num_end = page_num_count

        # 2. 当前页码数 + 右侧页码数 > 页码总数
        if current_page + page_num_half >= page_num_total:
            page_num_end = page_num_total
            page_num_start = page_num_total - page_num_count + 1

        # 3. 数据量不足 page_num_count 展示
        if page_num_total < page_num_count:
            page_num_start = 1
            page_num_end = page_num_total

        self.page_num_start = page_num_start
        self.page_num_end = page_num_end
        self.page_num_total = page_num_total

    @property
    def start(self):
        return (self.current_page - 1) * self.data_per_page

    @property
    def end(self):
        return self.current_page * self.data_per_page

    def make_html(self):
        """
            生成分页的 html 代码

        :return:
        """
        tmp = list()

        # 页码 html 起始
        tmp.append('<nav aria-label="Page navigation" class="text-center"><ul class="pagination">')

        # 添加一个首页
        tmp.append('<li><a href="/{}/?page=1">首页</a></li>'.format(self.url_prefix))

        # 添加上一页按钮
        # 当当前页为第一页时, 上一页按钮禁用
        if self.current_page <= 1:
            tmp.append('<li class="disabled"<span><span aria-hidden="true">&laquo;</span></span></li>')
        else:
            tmp.append(
                '<li><a href="/{0}/?page={1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.url_prefix, self.current_page - 1))

        # for 循环添加要展示的页码
        for i in range(self.page_num_start, self.page_num_end + 1):
            # 如果循环页码等于当前页码, 显示高亮
            if self.current_page == i:
                tmp.append('<li class="active"><a href="/{0}/?page={1}">{1}</a></li>'.format(self.url_prefix, i))
            else:
                tmp.append('<li><a href="/{0}/?page={1}">{1}</a></li>'.format(self.url_prefix, i))

        # 添加下一页按钮
        # 当当前页为最后一页时, 下一页按钮禁用
        if self.current_page >= self.page_num_total:
            tmp.append('<li class="disabled"><span><span aria-hidden="true">&raquo;</span></span></li>')
        else:
            tmp.append(
                '<li><a href="/{0}/?page={1}" aria-label="Previous"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.url_prefix, self.current_page + 1))

        # 添加一个尾页
        tmp.append('<li><a href="/{0}/?page={1}">尾页</a></li>'.format(self.url_prefix, self.page_num_total))

        # 页码 html 结尾
        tmp.append('</ul></nav>')

        # 将 html 代码整合到一起
        page_html = "".join(tmp)

        return page_html
