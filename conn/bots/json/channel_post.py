from conn.mission.sorting import Sorting


class Channel_post:

    def __init__(self):
        """
        频道帖子数据更新
        """
        self.sorting = Sorting()

    def channel_main(self, channel_post):
        """
        处理频道消息进行分类
        :param channel_post:
        :return:
        """
        self.sorting.dispatch(channel_post['text'])
