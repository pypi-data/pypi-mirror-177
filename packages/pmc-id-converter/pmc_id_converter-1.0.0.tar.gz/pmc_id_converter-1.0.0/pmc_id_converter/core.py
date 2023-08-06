import urllib

import requests
from simple_loggers import SimpleLogger


class Record(object):
    def __init__(self, **kwargs):
        self.data = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data.get('pmcid') or self.data.get('_id'))


class API(object):
    """Document: https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

    >>> from pmc_id_converter import API
    >>> API.idconv('PMC3531190', 'PMC3531191123', 'PMC3531191')
    >>> API.idconv('23193287')
    >>> API.idconv('10.1093/nar/gks1195')

    >>> API.idconv('10.1093/nar/gks1195-xxx')
    >>> API.idconv('PMC3531190x')
    >>> API.idconv('PMC353119123123')
    """

    service_root = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
    logger = SimpleLogger('ID_CONV_API')

    @classmethod
    def idconv(cls, *ids, tool='my_tool', email='my_email@example.com', versions='no'):
        params = {
            'ids': ','.join(ids),
            'tool': tool,
            'email': email,
            'versions': versions,
            'format': 'json',
        }

        res = requests.get(cls.service_root, params=params).json()
        # print(res)
        if res['status'] == 'error':
            message = urllib.parse.unquote(res['message'])
            cls.logger.error(f'RequestError: {message}')
            return []

        data = []
        for record in res['records']:
            if record.get('status') == 'error':
                errmsg = record['errmsg']
                _id = record.get('pmid') or record.get('pmcid') or record.get('doi')
                cls.logger.error(f'RecordError: {errmsg} for "{_id}"')
                context = Record(errmsg=errmsg, _id=_id)
            else:
                context = Record(**record)
            data += [context]
        return data


if __name__ == '__main__':
    API.idconv('PMC3531190')
    API.idconv('PMC3531190', 'PMC3531191123', 'PMC3531191')
    API.idconv('23193287')
    API.idconv('10.1093/nar/gks1195')
    API.idconv('10.1093/nar/gks1195-xxx')
    API.idconv('PMC3531190x')
    API.idconv('PMC353119123123')
