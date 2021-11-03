import json
import logging
import utils


async def send_async_request(url, user, password):
    response_json_list = []
    try:
        response = await utils.rest_get_tornado_httpclient(url, user, password)
        response_json = json.loads(response)
        if type(response_json) is dict:
            response_json_list.append(response_json)
            response = json.dumps(response_json_list, indent=2, sort_keys=True)
        with open("jsongets/response.json", 'w', encoding="utf8") as f:
            # json.dump(response, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.write(response)
            f.close()
        result = {'action': 'collect', 'status': 'completed', 'body': response}
        return result
    except Exception as err:
        result = {'action': 'collect', 'status': 'failed', 'body': response}
        logging.info(response)
        return result


def get_response():
    with open("jsonfiles/topo_data.json", 'r', ) as f:
        response = json.load(f)
        f.close()
    return json.dumps(response)


def process_ws_message(message):
    # response = "Got the message from websocket, here's my reply"
    response = ",".join(str(i['name']) for i in message)
    return response

def add_node(message):
    node_count = len(json.loads(get_topology_data("foo"))['nodes'])
    node_dict = {'name': message + "_processed_by_server", 'id': node_count}
    result = {'action': 'add-node', 'status': 'completed', 'body': json.dumps(node_dict)}
    return result

def get_topology_data(message):
    with open("jsonfiles/topo_data.json", 'r', ) as f:
        topo_data = json.load(f)
        f.close()
    return json.dumps(topo_data)

def update_topology_data(message):
    with open("jsonfiles/topo_data.json", 'w', encoding="utf8") as f:
        # json.dump(response, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.write(json.dumps(message,sort_keys=False, indent=4))
        f.close()
    return "Server updated topology data."
