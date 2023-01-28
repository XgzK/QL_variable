class JdQl:
    def __init__(self, gone: tuple):
        """
        JdQl数据库的表
        :param gone:
        """
        self.id = gone[0]
        self.jd_name = gone[1]
        self.jd_js = gone[2]
        self.jd_value1 = gone[3]
        self.jd_value2 = gone[4]
        self.jd_value3 = gone[5]
        self.jd_url = gone[6]
        self.jd_re = gone[7]
        self.jd_type = gone[8]
        self.partition = gone[9]
        self.interval = gone[10]
        self.Change = [gone[3], gone[4], gone[5]]

    def toString(self):
        """
        打印输出
        :return:
        """
        print(f"ID: {self.id}\t任务名称: {self.jd_name}\t脚本名称: {self.jd_js}\n"
              f"参数一: {self.jd_value1}\t参数二: {self.jd_value2}\t参数三: {self.jd_value3}\t"
              f"首次匹配链接: {self.jd_url}\t最终获取关键字: {self.jd_re}\t支持类型: {self.jd_type}\n"
              f"分割关键字: {self.partition}\t延迟秒数: {self.interval}")
