import logging
from cmreslogging.handlers import CMRESHandler

# handler = CMRESHandler(hosts=[{'host': 'localhost', 'port': 9200}],
#                        auth_type=CMRESHandler.AuthType.BASIC_AUTH,
#                        es_index_name="my_python_index")

handler = CMRESHandler(
    hosts=[
        {
            "host": "search-discord-log2-e22jfdiyin6rblshxfml3hcqaa.ap-northeast-1.es.amazonaws.com",
            "port": 443,
        }
    ],
    auth_type=CMRESHandler.AuthType.BASIC_AUTH,
    es_index_name="my_python_index1",
    use_ssl=True,
    auth_details=("user1", "]iQFWF^q]=4uw8-"),
    es_additional_fields={"App": "MyAppName", "Environment": "Dev"},
)
log = logging.getLogger("PythonTest1")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
