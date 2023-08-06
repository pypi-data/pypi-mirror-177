class Mixin:
    def get_bot_messages_for_user(self, user):
        pipeline = [
                {
                    '$match': {
                        'receiver': user.chat_id, 
                        'environment': 'dev'
                    }
                }, 
                { '$count': 'count_messages' }
        ]

        return pipeline

    def get_bot_messages_count(self, branch=None):
        pipeline = [
                {
                    '$match': {
                        'environment': branch
                    }
                }, 
                { '$count': 'count_messages' }
        ]

        return pipeline

    def get_bot_messages_per_type(self, branch=None):
        pipeline = [
                {
                    '$match': {
                        'environment': branch
                    }
                }, 
                { '$sortByCount': '$type' }
        ]

        return pipeline