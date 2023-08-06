class Mixin:
    def get_bot_messages_for_user(self, user, environment=None):
        pipeline = [
                {
                    '$match': {
                        'receiver': user.chat_id, 
                        'environment': environment
                    }
                }, 
                { '$count': 'count_messages' }
        ]

        return pipeline

    def get_bot_messages_count(self, environment=None):
        pipeline = [
                {
                    '$match': {
                        'environment': environment
                    }
                }, 
                { '$count': 'count_messages' }
        ]

        return pipeline

    def get_bot_messages_per_type(self, environment=None):
        pipeline = [
                {
                    '$match': {
                        'environment': environment
                    }
                }, 
                { '$sortByCount': '$type' }
        ]

        return pipeline