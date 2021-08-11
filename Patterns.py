import enum

'''
Collection of pattern matching that's used when parsing log files
'''
class Patterns(enum.Enum):
    agent_id = '\"agentId\":[ ]*\"(.*?)\"'
    exceptions = 'Exception'
    errors = 'Error'
    render_id = '\"renderId\":[ ]*\"(.*?)\"'
    account_id = '[?]accountId=(.*?)\"'
    api_key = '\"apiKey\":[ ]*\"(.*?)\"'

