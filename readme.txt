*VSCode Extensions*
- Proto Lint
- Python
- vscode-proto3

*Python Pip Packages*
- google 2.0.3
- protobuf 3.11.3
- pylint 2.4.4


*Run Instructions*
- to run: execute driver.py
- execution order:
    1. driver.py spawns master.py and client.py processes
    2. master.py spawns 3 replica.py processes
    3. client.py sends all messages in static 'messages' list to master
    4. master catalogs requests and forwards to replica (logic for which replica may depend on consistency model)
    5. replicas do their thing and respond to master
    6. master looks up original request to find client ip and sends message to client

*Run notes*
- For testing, add your messages/requests to messages list and run normally
- Sending messages:
    > use start_connections(dest_ip, <Message>.SerializeToString()) to send messages to other processes
    > Message object is a protobuffer, if you have issues working with them please contact Dexter or Travis
    > build_msg utility: we have a basic method to help build Message objects, example below
    > msg = build_msg.build(<sender_ip>, <consistency_model>, <request_type>, <acknowledgement>, <data>, <logical_clock_stamp>, <request_id>)
- Logger: a logger object is auto-generated with the instantiation of each Node (Master, Client, Replica) class
    > currently all connections and messages are logged automatically
    > to log additional data, call self.node_log.write(<str>)
    > keyboard interupt will kill all nodes and output logs