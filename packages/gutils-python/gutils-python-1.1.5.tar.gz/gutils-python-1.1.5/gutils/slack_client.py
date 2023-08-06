from slack import WebClient


class SlackClient(object):
    def __init__(self, token):
        self._client = WebClient(token=token)

    def get_chat_history(self, channel_id, limit=100, oldest=0):
        """
        Get chat history from specific channel
        :param channel_id: channel id, e.g. CMM4X9M43
        :param limit: message numbers; 100 by default
        :param oldest: oldest message
        :return: List chat history messages
        """
        response = self._client.conversations_history(channel=channel_id, limit=limit, oldest=oldest)
        if not (response.status_code == 200 and response.data['ok'] and 'messages' in response.data):
            raise RuntimeError(
                'Failed to get chat history for {}; response: {} - {}'.format(channel_id, response.status_code,
                                                                              response.data))

        return response['messages']

    def send_message(self, channel_id, message=None, blocks=None):
        """
        Send message to specific channel
        :param channel_id: channel id, e.g. CMM4X9M43
        :param message: message to be sent
        :param blocks: blocks to be sent
        :return: Response data
        """
        response = self._client.chat_postMessage(channel=channel_id, text=message, blocks=blocks)
        if not (response.status_code == 200 and response.data['ok']):
            raise RuntimeError('Failed to send message to {}; response:{} - {}'.format(channel_id, response.status_code,
                                                                                       response.data))
        return response.data
