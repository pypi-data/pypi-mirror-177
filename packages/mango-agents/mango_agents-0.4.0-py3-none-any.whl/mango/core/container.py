"""
This module contains the abstract Container class and the subclasses
TCPContainer and MQTTContainer
"""
from abc import ABC, abstractmethod
import asyncio
import logging
import warnings
from typing import Optional, Union, Tuple, Dict, Any, Set
import paho.mqtt.client as paho
from .container_protocols import ContainerProtocol
from ..messages.message import ACLMessage
from ..messages.codecs import Codec, JSON
from ..util.clock import Clock, AsyncioClock

logger = logging.getLogger(__name__)

AGENT_PATTERN_NAME_PRE = "agent"


class Container(ABC):
    """Superclass for a mango container"""

    @classmethod
    async def factory(
        cls,
        *,
        connection_type: str = "tcp",
        codec: Codec = None,
        clock: Clock = None,
        addr: Optional[Union[str, Tuple[str, int]]] = None,
        proto_msgs_module=None,
        mqtt_kwargs: Dict[str, Any] = None,
    ):
        """
        This method is called to instantiate a container instance, either
        a TCPContainer or a MQTTContainer, depending on the parameter
        connection_type.
        :param connection_type: Defines the connection type. So far only 'tcp'
        or 'mqtt' are allowed
        :param codec: Defines the codec to use. Defaults to JSON
        :param clock: The clock that the scheduler of the agent should be based on. Defaults to the AsyncioClock
        :param addr: the address to use. If connection_type == 'tcp': it has
        to be a tuple of (host, port). If connection_type == 'mqtt' this can
        optionally define an inbox_topic that is used similarly than
        a tcp address.
        :param proto_msgs_module: The compiled python module where the
         additional proto msgs are defined. Ignored if codec != 'protobuf'
        :param mqtt_kwargs: Dictionary of keyword arguments for connection to a mqtt broker. At least
        the keys 'broker_addr' and 'client_id' have to be provided.
        Ignored if connection_type != 'mqtt'
        :return: The instance of a MQTTContainer or a TCPContainer
        """
        connection_type = connection_type.lower()
        if connection_type not in ["tcp", "mqtt"]:
            raise ValueError(f"Unknown connection type {connection_type}")

        loop = asyncio.get_running_loop()

        if codec is None:
            codec = JSON()
        if clock is None:
            clock = AsyncioClock()

        if connection_type == "tcp":
            # initialize TCPContainer
            container = TCPContainer(
                addr=addr, codec=codec, loop=loop, proto_msgs_module=proto_msgs_module, clock=clock
            )

            # create a TCP server bound to host and port that uses the
            # specified protocol
            container.server = await loop.create_server(
                lambda: ContainerProtocol(container=container, loop=loop, codec=codec),
                addr[0],
                addr[1],
            )
            return container

        if connection_type == "mqtt":
            # get and check relevant kwargs from mqtt_kwargs
            # client_id
            client_id = mqtt_kwargs.pop("client_id", None)
            if not client_id:
                raise ValueError("client_id is requested within mqtt_kwargs")

            # broker_addr
            broker_addr = mqtt_kwargs.pop("broker_addr", None)
            if not broker_addr:
                raise ValueError("broker_addr is requested within mqtt_kwargs")

            # get parameters for Client.init()
            init_kwargs = {}
            possible_init_kwargs = (
                "clean_session",
                "userdata",
                "protocol",
                "transport",
            )
            for possible_kwarg in possible_init_kwargs:
                if possible_kwarg in mqtt_kwargs.keys():
                    init_kwargs[possible_kwarg] = mqtt_kwargs.pop(possible_kwarg)

            # check if addr is a valid topic without wildcards
            if addr is not None and (
                not isinstance(addr, str) or "#" in addr or "+" in addr
            ):
                raise ValueError(
                    "addr is not set correctly. It is used as "
                    "inbox topic and must be a  string without "
                    "any wildcards ('#' or '+')"
                )

            # create paho.Client object for mqtt communication
            mqtt_messenger: paho.Client = paho.Client(
                client_id=client_id, **init_kwargs
            )

            # set TLS options if provided
            # expected as a dict:
            # {ca_certs, certfile, keyfile, cert_eqs, tls_version, ciphers}
            tls_kwargs = mqtt_kwargs.pop("tls_kwargs", None)
            if tls_kwargs:
                mqtt_messenger.tls_set(**tls_kwargs)

            # Future that is triggered, on successful connection
            connected = asyncio.Future()

            # callbacks to check for successful connection
            def on_con(client, userdata, flags, returncode):
                print(f"Connection Callback with the following flags: {flags}")
                loop.call_soon_threadsafe(connected.set_result, returncode)

            mqtt_messenger.on_connect = on_con

            # check broker_addr input and connect
            if isinstance(broker_addr, tuple):
                if not 0 < len(broker_addr) < 4:
                    raise ValueError(f"Invalid broker address")
                if len(broker_addr) > 0 and not isinstance(broker_addr[0], str):
                    raise ValueError("Invalid broker address")
                if len(broker_addr) > 1 and not isinstance(broker_addr[1], int):
                    raise ValueError("Invalid broker address")
                if len(broker_addr) > 2 and not isinstance(broker_addr[2], int):
                    raise ValueError("Invalid broker address")
                mqtt_messenger.connect(*broker_addr, **mqtt_kwargs)

            elif isinstance(broker_addr, dict):
                if "hostname" not in broker_addr.keys():
                    raise ValueError("Invalid broker address")
                mqtt_messenger.connect(**broker_addr, **mqtt_kwargs)

            else:
                if not isinstance(broker_addr, str):
                    raise ValueError("Invalid broker address")
                mqtt_messenger.connect(broker_addr, **mqtt_kwargs)

            print(
                f"[{client_id}]: Going to connect to broker " f"at {broker_addr}... ",
                end="",
            )

            counter = 0
            # process MQTT messages for maximum of 10 seconds to
            # receive connection callback
            while not connected.done() and counter < 100:
                mqtt_messenger.loop()
                # wait for the thread to trigger the future
                await asyncio.sleep(0.1)
                counter += 1

            if not connected.done():
                # timeout
                raise ConnectionError(
                    f"Connection to {broker_addr} could not be "
                    f"established after {counter * 0.1} seconds"
                )
            if connected.result() != 0:
                raise ConnectionError(
                    f"Connection to {broker_addr} could not be "
                    f"set up. Callback returner error code "
                    f"{connected.result()}"
                )

            print("done.")
            if addr is not None:
                # connection has been set up, subscribe to inbox topic now
                print(
                    f"[{client_id}]: Going to subscribe to {addr} "
                    f"as inbox topic... ",
                    end="",
                )

                # create Future that is triggered on successful subscription
                subscribed = asyncio.Future()

                # set up subscription callback
                def on_sub(*args):
                    loop.call_soon_threadsafe(subscribed.set_result, True)

                mqtt_messenger.on_subscribe = on_sub

                # subscribe topic
                result, _ = mqtt_messenger.subscribe(addr, 2)
                if result != paho.MQTT_ERR_SUCCESS:
                    # subscription to inbox topic was not successful
                    mqtt_messenger.disconnect()
                    raise ConnectionError(
                        f"Subscription request to {addr} at {broker_addr} "
                        f"returned error code: {result}"
                    )

                counter = 0
                while not subscribed.done() and counter < 100:
                    # wait for subscription
                    mqtt_messenger.loop(timeout=0.1)
                    await asyncio.sleep(0.1)
                    counter += 1
                if not subscribed.done():
                    raise ConnectionError(
                        f"Subscription request to {addr} at {broker_addr} "
                        f"did not succeed after {counter * 0.1} seconds."
                    )
                print("done.")

            # connection and subscription is successful, remove callbacks
            mqtt_messenger.on_subscribe = None
            mqtt_messenger.on_connect = None

            return MQTTContainer(
                client_id=client_id,
                addr=addr,
                loop=loop,
                clock=clock,
                mqtt_client=mqtt_messenger,
                codec=codec,
                proto_msgs_module=proto_msgs_module,
            )

    def __init__(self, *, addr, name: str, codec, proto_msgs_module=None, loop, clock: Clock):
        self.name: str = name
        self.addr = addr
        self.clock = clock

        self.codec: Codec = codec
        if codec == "protobuf":
            self.other_msgs = proto_msgs_module
        self.loop: asyncio.AbstractEventLoop = loop

        # dict of agents. aid: agent instance
        self._agents: Dict = {}
        self._aid_counter: int = 0  # counter for aids

        self.running: bool = True  # True until self.shutdown() is called
        self._no_agents_running: asyncio.Future = asyncio.Future()
        self._no_agents_running.set_result(
            True
        )  # signals that currently no agent lives in this container

        # inbox for all incoming messages
        self.inbox: asyncio.Queue = asyncio.Queue()

        # task that processes the inbox.
        self._check_inbox_task: asyncio.Task = asyncio.create_task(self._check_inbox())

    def is_aid_available(self, aid):
        """
        Check if the aid is available and allowed.
        It is not possible to register aids matching the regular pattern "agentX".
        :param aid: the aid you want to check
        :return True if the aid is available, False if it is not
        """
        return aid not in self._agents and not self.__check_agent_aid_pattern_match(aid)

    def __check_agent_aid_pattern_match(self, aid):
        return aid.startswith(AGENT_PATTERN_NAME_PRE) and aid[len(AGENT_PATTERN_NAME_PRE):].isnumeric()

    def _register_agent(self, agent, suggested_aid: str = None):
        """
        Register *agent* and return the agent id
        :param agent: The agent instance
        :param suggested_aid: (Optional) suggested aid, if the aid is already taken, a generated aid is used. 
                              Using the generated aid-style ("agentX") is not allowed.
        :return The agent ID
        """
        if not self._no_agents_running or self._no_agents_running.done():
            self._no_agents_running = asyncio.Future()
        if suggested_aid is None or \
           suggested_aid in self._agents or \
           self.__check_agent_aid_pattern_match(suggested_aid):
            aid = f"{AGENT_PATTERN_NAME_PRE}{self._aid_counter}"
            self._aid_counter += 1
        else:
            aid = suggested_aid
        self._agents[aid] = agent
        logger.info(f"Successfully registered agent;{aid}")
        return aid

    def deregister_agent(self, aid):
        """
        Deregister an agent
        :param aid:
        :return:

        """
        del self._agents[aid]
        if len(self._agents) == 0:
            self._no_agents_running.set_result(True)

    @abstractmethod
    async def send_message(
        self,
        content,
        receiver_addr: Union[str, Tuple[str, int]],
        *,
        receiver_id: Optional[str] = None,
        create_acl: bool = None,
        acl_metadata: Optional[Dict[str, Any]] = None,
        mqtt_kwargs: Dict[str, Any] = None,
        **kwargs
    ) -> bool:
        """
        The Container sends a message to an agent according the container protocol.
        
        :param content: The content of the message
        :param receiver_addr: In case of TCP this is a tuple of host, port
            In case of MQTT this is the topic to publish to.
        :param receiver_id: The agent id of the receiver
        :param create_acl: True if an acl message shall be created around the
            content.
            
            .. deprecated:: 0.4.0
                Use 'container.send_acl_message' instead. In the next version this parameter
                will be dropped entirely.
        :param acl_metadata: metadata for the acl_header.
            Ignored if create_acl == False
            
            .. deprecated:: 0.4.0
                Use 'container.send_acl_message' instead. In the next version this parameter
                will be dropped entirely.
        :param mqtt_kwargs: Dict with possible kwargs for publishing to a mqtt broker
            Possible fields:
            qos: The quality of service to use for publishing
            retain: Indicates, weather the retain flag should be set
            Ignored if connection_type != 'mqtt'
            .. deprecated:: 0.4.0
                Use 'kwargs' instead. In the next version this parameter
                will be dropped entirely.
        :param kwargs: Additional parameters to provide protocol specific settings 
        """
        raise NotImplementedError

    async def send_acl_message(
        self,
        content,
        receiver_addr: Union[str, Tuple[str, int]],
        *,
        receiver_id: Optional[str] = None,
        acl_metadata: Optional[Dict[str, Any]] = None,
        is_anonymous_acl=False,
        **kwargs
    ) -> bool:
        """
        The Container sends a message, wrapped in an ACL message, to an agent according the container protocol.

        :param content: The content of the message
        :param receiver_addr: In case of TCP this is a tuple of host, port
        In case of MQTT this is the topic to publish to.
        :param receiver_id: The agent id of the receiver
        :param acl_metadata: metadata for the acl_header.
        :param is_anonymous_acl: If set to True, the sender information won't be written in the ACL header 
        :param kwargs: Additional parameters to provide protocol specific settings 
        """
        return await self.send_message(self._create_acl(
            content,
            receiver_addr=receiver_addr,
            receiver_id=receiver_id,
            acl_metadata=acl_metadata,
            is_anonymous_acl=is_anonymous_acl),
            receiver_addr=receiver_addr, 
            receiver_id=receiver_id,
            **kwargs
        )

    def _create_acl(
        self,
        content,
        receiver_addr: Union[str, Tuple[str, int]],
        receiver_id: Optional[str] = None,
        acl_metadata: Optional[Dict[str, Any]] = None,
        is_anonymous_acl=False
    ):
        """
        :param content:
        :param receiver_addr:
        :param receiver_id:
        :param acl_metadata:
        :return:
        """
        acl_metadata = {} if acl_metadata is None else acl_metadata.copy()
        # analyse and complete acl_metadata
        if "receiver_addr" not in acl_metadata.keys():
            acl_metadata["receiver_addr"] = receiver_addr
        if "receiver_id" not in acl_metadata.keys() and receiver_id:
            acl_metadata["receiver_id"] = receiver_id
        # add sender_addr if not defined and not anonymous
        if not is_anonymous_acl:
            if "sender_addr" not in acl_metadata.keys() and self.addr is not None:
                acl_metadata["sender_addr"] = self.addr

        message = ACLMessage()
        message.content = content

        for key, value in acl_metadata.items():
            setattr(message, key, value)
        return message

    async def _check_inbox(self):
        """
        Task that checks, if there is a message in inbox and then creates a
        task to handle message
        """

        def raise_exceptions(result):
            """
            Inline function used as a callback to tasks to raise exceptions
            :param result: result object of the task
            """
            exception = result.exception()
            if exception is not None:
                logger.warning("Exception in _check_inbox_task.")
                raise exception

        while True:
            data = await self.inbox.get()
            priority, content, meta = data
            task = asyncio.create_task(
                self._handle_message(priority=priority, content=content, meta=meta)
            )
            task.add_done_callback(raise_exceptions)
            self.inbox.task_done()  # signals that the queue object is
            # processed

    @abstractmethod
    async def _handle_message(self, *, priority: int, content, meta: Dict[str, Any]):
        """
        This is called as a separate task for every message that is read
        :param priority: priority of the message
        :param content: Deserialized content of the message
        :param meta: Dict with additional information (e.g. topic)
        """
        raise NotImplementedError

    async def shutdown(self):
        """Shutdown all agents in the container and the container itself"""
        self.running = False
        futs = []
        for agent in self._agents.values():
            # shutdown all running agents
            futs.append(agent.shutdown())
        await asyncio.gather(*futs)

        # cancel check inbox task
        if self._check_inbox_task is not None:
            logger.debug("check inbox task will be cancelled")
            self._check_inbox_task.cancel()
            try:
                await self._check_inbox_task
            except asyncio.CancelledError:
                pass
            finally:
                logger.info("Successfully shutdown")


class MQTTContainer(Container):
    """
    Container for agents.

       The container allows its agents to send messages to specific topics
       (via :meth:`send_message()`).
    """

    def __init__(
        self,
        *,
        client_id: str,
        addr: Optional[str],
        loop: asyncio.AbstractEventLoop,
        clock: Clock,
        mqtt_client: paho.Client,
        codec: Codec = JSON,
        proto_msgs_module=None,
    ):
        """
        Initializes a container. Do not directly call this method but use
        the factory method instead
        :param client_id: The ID that the container should use when connecting
        to the broker
        :param addr: A string of the unique inbox topic to use.
        No wildcards are allowed. If None, no inbox topic will be set
        :param mqtt_client: The paho.Client object that is used for the
        communication with the broker
        :param codec: The codec to use. Currently only 'json' or 'protobuf' are
         allowed
        :param proto_msgs_module: The compiled python module where the
         additional proto msgs are defined
        """
        super().__init__(
            codec=codec,
            addr=addr,
            proto_msgs_module=proto_msgs_module,
            loop=loop,
            clock=clock,
            name=client_id,
        )

        self.client_id: str = client_id
        # the configured and connected paho client
        self.mqtt_client: paho.Client = mqtt_client
        self.inbox_topic: Optional[str] = addr
        # dict mapping additionally subscribed topics to a set of aids
        self.additional_subscriptions: Dict[str, Set[str]] = {}
        # dict mapping subscribed topics to the expected class
        self.subscriptions_to_class: Dict[str, Any] = {}
        # Future for pending sub requests
        self.pending_sub_request: Optional[asyncio.Future] = None

        # set the callbacks
        self._set_mqtt_callbacks()

        # start the mqtt client
        self.mqtt_client.loop_start()

    def _set_mqtt_callbacks(self):
        """
        Sets the callbacks for the mqtt paho client
        """

        def on_con(client, userdata, flags, rc):
            if rc != 0:
                logger.info("Connection attempt to broker failed")
            else:
                logger.debug("Successfully reconnected to broker.")

        self.mqtt_client.on_connect = on_con

        def on_discon(client, userdata, rc):
            if rc != 0:
                logger.warning("Unexpected disconnect from broker. Trying to reconnect")
            else:
                logger.debug("Successfully disconnected from broker.")

        self.mqtt_client.on_disconnect = on_discon

        def on_sub(client, userdata, mid, granted_qos):
            self.loop.call_soon_threadsafe(self.pending_sub_request.set_result, 0)

        self.mqtt_client.on_subscribe = on_sub

        def on_message(client, userdata, message):
            # extract the meta information first
            meta = {
                "network_protocol": "mqtt",
                "topic": message.topic,
                "qos": message.qos,
                "retain": message.retain,
            }
            # decode message and extract content and meta
            content, message_meta = self.decode_mqtt_message(
                payload=message.payload, topic=message.topic
            )
            # update meta dict
            meta.update(message_meta)

            # put information to inbox
            if content is not None:
                self.loop.call_soon_threadsafe(
                    self.inbox.put_nowait, (0, content, meta)
                )

        self.mqtt_client.on_message = on_message

        self.mqtt_client.enable_logger(logger)

    async def shutdown(self):
        """
        Shutdown container, disconnect from broker and stop mqtt thread
        """
        await super().shutdown()
        # disconnect to broker
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()

    def decode_mqtt_message(self, *, topic, payload):
        """
        deserializes a mqtt message.
        Checks if for the topic a special class is defined, otherwise assumes
        an ACLMessage
        :param topic: the topic on which the message arrived
        :param payload: the serialized message
        :return: content and meta
        """
        meta = {}
        content = None

        # check if there is a class definition for the topic
        for sub, sub_class in self.subscriptions_to_class.items():
            if paho.topic_matches_sub(sub, topic):
                # instantiate the provided class
                content = sub_class()
                break

        decoded = self.codec.decode(payload)
        if isinstance(content, ACLMessage):
            meta = decoded.extract_meta()
            content = decoded.content

        return decoded, meta

    async def _handle_message(self, *, priority: int, content, meta: Dict[str, Any]):
        """
        This is called as a separate task for every message that is read
        :param priority: priority of the message
        :param content: Deserialized content of the message
        :param meta: Dict with additional information (e.g. topic)

        """
        topic = meta["topic"]
        logger.debug(
            f"Received message with content and meta;{str(content)};{str(meta)}"
        )

        if hasattr(content, "split_content_and_meta"):
            content, message_meta = content.split_content_and_meta()
            meta.update(message_meta)
            content = content

        if topic == self.inbox_topic:
            # General inbox topic, so no receiver is specified by the topic
            # try to find the receiver from meta
            receiver_id = meta.get("receiver_id", None)
            if receiver_id and receiver_id in self._agents.keys():
                receiver = self._agents[receiver_id]
                await receiver.inbox.put((priority, content, meta))
            else:
                logger.warning(f"Receiver ID is unknown;{receiver_id}")
        else:
            # no inbox topic. Check who has subscribed the topic.
            receivers = set()
            for sub, rec in self.additional_subscriptions.items():
                if paho.topic_matches_sub(sub, topic):
                    receivers.update(rec)
            if not receivers:
                logger.warning(
                    f"Received a message at a topic which no agent subscribed;{topic}"
                )
            else:
                for receiver_id in receivers:
                    receiver = self._agents[receiver_id]

                    await receiver.inbox.put((priority, content, meta))

    async def send_message(
        self,
        content,
        receiver_addr: Union[str, Tuple[str, int]],
        *,
        receiver_id: Optional[str] = None,
        create_acl: bool = None,
        acl_metadata: Optional[Dict[str, Any]] = None,
        mqtt_kwargs: Dict[str, Any] = None,
        **kwargs
    ):
        """
        The container sends the message of one of its own agents to a specific topic.
        
        :param content: The content of the message
        :param receiver_addr: The topic to publish to.
        :param receiver_id: The agent id of the receiver
        :param create_acl: True if an acl message shall be created around the
            content.
            
            .. deprecated:: 0.4.0
                Use 'container.send_acl_message' instead. In the next version this parameter
                will be dropped entirely.
        :param acl_metadata: metadata for the acl_header.
            Ignored if create_acl == False
            
            .. deprecated:: 0.4.0
                Use 'container.send_acl_message' instead. In the next version this parameter
                will be dropped entirely.
        :param mqtt_kwargs: Dict with possible kwargs for publishing to a mqtt broker
            Possible fields:
            qos: The quality of service to use for publishing
            retain: Indicates, weather the retain flag should be set
            Ignored if connection_type != 'mqtt'
            .. deprecated:: 0.4.0
                Use 'kwargs' instead. In the next version this parameter
                will be dropped entirely.
        :param kwargs: Additional parameters to provide protocol specific settings 
            Possible fields:
            qos: The quality of service to use for publishing
            retain: Indicates, weather the retain flag should be set
            Ignored if connection_type != 'mqtt'

        """

        if create_acl is not None or acl_metadata is not None:
            warnings.warn("The parameters create_acl and acl_metadata are deprecated and will "
                          "be removed in the next release. Use send_acl_message instead.", DeprecationWarning)
        if mqtt_kwargs is not None:
            warnings.warn("The parameter mqtt_kwargs is deprecated and will "
                          "be removed in the next release. Use kwargs instead.", DeprecationWarning)

        if create_acl:
            message = self._create_acl(
                content=content,
                receiver_addr=receiver_addr,
                receiver_id=receiver_id,
                acl_metadata=acl_metadata,
            )
        else:
            # the message is already complete
            message = content

        # internal message first (if retain Flag is set, it has to be sent to
        # the broker
        actual_mqtt_kwargs = mqtt_kwargs if kwargs is None else kwargs
        actual_mqtt_kwargs = {} if actual_mqtt_kwargs is None else actual_mqtt_kwargs
        if (
            self.addr
            and receiver_addr == self.addr
            and not actual_mqtt_kwargs.get("retain", False)
        ):
            meta = {
                "topic": self.addr,
                "qos": actual_mqtt_kwargs.get("qos", 0),
                "retain": False,
                "network_protocol": "mqtt",
            }

            if hasattr(message, "split_content_and_meta"):
                content, message_meta = message.split_content_and_meta()
                meta.update(message_meta)
            else:
                content = message

            self.inbox.put_nowait((0, content, meta))
            return True

        else:
            self._send_external_message(topic=receiver_addr, message=message)
            return True

    def _send_external_message(self, *, topic: str, message):
        """

        :param topic: MQTT topic
        :param message: The ACL message
        :return:
        """
        encoded_message = self.codec.encode(message)
        logger.debug(f"Sending message;{message};{topic}")
        self.mqtt_client.publish(topic, encoded_message)

    async def subscribe_for_agent(
        self, *, aid: str, topic: str, qos: int = 0, expected_class=None
    ) -> bool:
        """

        :param aid: aid of the corresponding agent
        :param topic: topic to subscribe (wildcards are allowed)
        :param qos: The quality of service for the subscription
        :param expected_class: The class to expect from the topic, defaults
        to ACL
        :return: A boolean signaling if subscription was true or not
        """
        if aid not in self._agents.keys():
            raise ValueError("Given aid is not known")
        if expected_class:
            self.subscriptions_to_class[topic] = expected_class

        if topic in self.additional_subscriptions.keys():
            self.additional_subscriptions[topic].add(aid)
            return True

        self.additional_subscriptions[topic] = {aid}
        self.pending_sub_request = asyncio.Future()
        result, _ = self.mqtt_client.subscribe(topic, qos=qos)

        if result != paho.MQTT_ERR_SUCCESS:
            self.pending_sub_request.set_result(False)
            return False

        await self.pending_sub_request
        return True

    def set_expected_class(self, *, topic: str, expected_class):
        """
        Sets an expected class to a subscription
        wildcards are allowed here
        :param topic: The subscription
        :param expected_class: The expected class
        :return:
        """
        self.subscriptions_to_class[topic] = expected_class
        logger.debug(f"Expected class updated;{self.subscriptions_to_class}")

    def deregister_agent(self, aid):
        """

        :param aid:
        :return:
        """
        super().deregister_agent(aid)
        empty_subscriptions = []
        for subscription, aid_set in self.additional_subscriptions.items():
            if aid in aid_set:
                aid_set.remove(aid)
            if len(aid_set) == 0:
                empty_subscriptions.append(subscription)

        for subscription in empty_subscriptions:
            self.additional_subscriptions.pop(subscription)
            self.mqtt_client.unsubscribe(topic=subscription)


class TCPContainer(Container):
    """
    This is a container that communicate directly with other containers
    via tcp
    """

    def __init__(
        self,
        *,
        addr: Tuple[str, int],
        codec: Codec,
        loop: asyncio.AbstractEventLoop,
        proto_msgs_module=None,
        clock: Clock,
    ):
        """
        Initializes a TCP container. Do not directly call this method but use
        the factory method of **Container** instead
        :param addr: The container address
        :param codec: The codec to use
        :param loop: Current event loop
        :param proto_msgs_module: The module for proto msgs in case of
        proto as codec
        """
        super().__init__(
            addr=addr,
            codec=codec,
            proto_msgs_module=proto_msgs_module,
            loop=loop,
            name=f"{addr[0]}:{addr[1]}",
            clock=clock,
        )

        self.server = None  # will be set within the factory method
        self.running = True

    async def _handle_message(self, *, priority: int, content, meta: Dict[str, Any]):
        """

        :param priority:
        :param content:
        :param meta:
        :return:
        """
        logger.debug(
            f"Received message with content and meta;{str(content)};{str(meta)}"
        )
        receiver_id = meta.get("receiver_id", None)
        if receiver_id and receiver_id in self._agents.keys():
            receiver = self._agents[receiver_id]
            await receiver.inbox.put((priority, content, meta))
        else:
            logger.warning(f"Received a message for an unknown receiver;{receiver_id}")

    async def send_message(
        self,
        content,
        receiver_addr: Union[str, Tuple[str, int]],
        *,
        receiver_id: Optional[str] = None,
        create_acl: bool = None,
        acl_metadata: Optional[Dict[str, Any]] = None,
        mqtt_kwargs: Dict[str, Any] = None,
        **kwargs
    ) -> bool:
        """
        The Container sends a message to an agent using TCP.
        
        :param content: The content of the message
        :param receiver_addr: Tuple of host, port
        :param receiver_id: The agent id of the receiver
        :param create_acl: True if an acl message shall be created around the
            content.
            
            .. deprecated:: 0.4.0
                Use 'container.send_acl_message' instead. In the next version this parameter
                will be dropped entirely.
        :param acl_metadata: metadata for the acl_header.
            Ignored if create_acl == False
            
            .. deprecated:: 0.4.0
                Use 'container.send_acl_message' instead. In the next version this parameter
                will be dropped entirely.
        :param mqtt_kwargs: 
            .. deprecated:: 0.4.0
                Use 'kwargs' instead. In the next version this parameter
                will be dropped entirely.
        :param kwargs: Additional parameters to provide protocol specific settings 
        """
        if create_acl is not None or acl_metadata is not None:
            warnings.warn("The parameters create_acl and acl_metadata are deprecated and will "
                          "be removed in the next release. Use send_acl_message instead.", DeprecationWarning)
        if mqtt_kwargs is not None:
            warnings.warn("The parameter mqtt_kwargs is deprecated and will "
                          "be removed in the next release. Use kwargs instead.", DeprecationWarning)

        if isinstance(receiver_addr, str) and ":" in receiver_addr:
            receiver_addr = receiver_addr.split(":")
        elif isinstance(receiver_addr, (tuple, list)) and len(receiver_addr) == 2:
            receiver_addr = tuple(receiver_addr)
        else:
            logger.warning(f"Address for sending message is not valid;{receiver_addr}")
            return False

        if create_acl is not None and create_acl:
            message = self._create_acl(
                content=content,
                receiver_addr=receiver_addr,
                receiver_id=receiver_id,
                acl_metadata=acl_metadata,
            )
        else:
            message = content

        if receiver_addr == self.addr:
            if not receiver_id:
                receiver_id = message.receiver_id
            # internal message

            success = self._send_internal_message(receiver_id, message)
        else:
            success = await self._send_external_message(receiver_addr, message)

        return success

    def _send_internal_message(self, receiver_id, message) -> bool:
        """
        Sends a message to an agent that lives in the same container
        :param receiver_id: ID of the receiver
        :param message:
        :return: boolean indicating whether sending was successful
        """

        receiver = self._agents.get(receiver_id, None)
        if receiver is None:
            logger.warning(
                f"Sending internal message not successful, receiver id unknown;{receiver_id}"
            )
            return False
        # TODO priority assignment could be specified here,
        priority = 0
        if hasattr(message, "split_content_and_meta"):
            content, meta = message.split_content_and_meta()
        else:
            content = message
            meta = {}
        meta["network_protocol"] = "tcp"
        receiver.inbox.put_nowait((priority, content, meta))
        return True

    async def _send_external_message(self, addr, message) -> bool:
        """
        Sends *message* to another container at *addr*
        :param addr: Tuple of (host, port)
        :param message: The message
        :return:
        """
        if addr is None or not isinstance(addr, (tuple, list)) or len(addr) != 2:
            logger.warning(
                f"Sending external message not successful, invalid address;{str(addr)}"
            )
            return False

        try:
            transport, protocol = await self.loop.create_connection(
                lambda: ContainerProtocol(
                    container=self, loop=self.loop, codec=self.codec
                ),
                addr[0],
                addr[1],
            )
            logger.debug(f"Connection established to addr;{str(addr)}")

            protocol.write(self.codec.encode(message))

            logger.debug(f"Message sent to addr;{str(addr)}")
            await protocol.shutdown()
        except OSError:
            logger.warning(
                f"Could not establish connection to receiver of a message;{str(addr)}"
            )
            return False
        return True

    async def shutdown(self):
        """
        calls shutdown() from super class Container and closes the server
        """
        await super().shutdown()
        self.server.close()
        await self.server.wait_closed()
