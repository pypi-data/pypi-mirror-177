class Mixin:
    def search_transfers_mongo(self, transfer_type, gte, lte, start_date, end_date, skip, limit):
        
        sort = 'date'
        sort_condition = { '$sort':      { 'amount_ccd': -1} } if sort =='amount' else { '$sort':      { 'blockInfo.blockSlotTime': -1} }
        pipeline = [
            {
                '$match': { 'type.contents': { '$in': ['transfer','transferWithMemo'] } }
            }, 
            { '$addFields': 
                { 'amount_ccd': 
                { '$first' :
                    {
                    '$map':
                        {
                        'input': "$result.events",
                        'as': "events",
                        'in': { '$trunc': { '$divide': [{'$toDouble': '$$events.amount'}, 1000000] } }
                        }
                    }
                }
                }
            },
            { '$match':     { 'amount_ccd': { '$gte': gte } } },
            { '$match':     { 'amount_ccd': { '$lt':  lte } } },
            { "$match":     {"blockInfo.blockSlotTime": {"$gte": start_date, "$lt": end_date } } },
            sort_condition,
            {'$facet': {
            'metadata': [ { '$count': 'total' } ],
            'data': [ { '$skip': int(skip) }, { '$limit': int(limit) } ]
            }},
            {'$project': { 
                'data': 1,
                'total': { '$arrayElemAt': [ '$metadata.total', 0 ] }
            }
            }
        ]

        return pipeline