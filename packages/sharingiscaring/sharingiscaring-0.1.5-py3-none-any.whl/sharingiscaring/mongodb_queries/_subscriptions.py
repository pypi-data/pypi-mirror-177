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