"""
Internal module, which implements the framework API of the role package. Provides an
implementation of the :class:`RoleContext`, the RoleAgent and some internal handlers
for the communication between roles.
"""

import asyncio

from typing import Any, Dict, Optional, Union, Tuple, List
import datetime

from mango.util.scheduling import ScheduledProcessTask, ScheduledTask, Scheduler
from mango.core.agent import Agent
from mango.role.api import Role, RoleContext


class DataContainer:

    def __getitem__(self, key):
        return self.__getattribute__(key)


class RoleHandler:
    """Contains all roles and their models. Implements the communication between roles.
    """

    def __init__(self, container, scheduler):
        self._role_models = {}
        self._roles = []
        self._role_to_active = {}
        self._role_model_type_to_subs = {}
        self._message_subs = []
        self._send_msg_subs = {}
        self._container = container
        self._scheduler = scheduler
        self._data = DataContainer()

    def get_or_create_model(self, cls):
        """Creates or return (when already created) a central role model.

        Returns:
            [type]: the model
        """
        if cls in self._role_models:
            return self._role_models[cls]

        self._role_models[cls] = cls()
        return self._role_models[cls]

    def update(self, role_model) -> None:
        """Notifies all subscribers of an update of the given role_model.

        Args:
            role_model ([type]): the role model to notify about
        """
        role_model_type = type(role_model)
        self._role_models[role_model_type] = role_model

        # Notify all subscribing agents
        if role_model_type in self._role_model_type_to_subs:
            for role in self._role_model_type_to_subs[role_model_type]:
                if self._is_role_active(role):
                    role.on_change_model(role_model)

    def subscribe(self, role: Role, role_model_type) -> None:
        """Subscribe a role to change events of a specific role model type

        Args:
            role ([type]): the role
            role_model_type ([type]): the type of the role model
        """
        if role_model_type in self._role_model_type_to_subs:
            self._role_model_type_to_subs[role_model_type].append(role)
        else:
            self._role_model_type_to_subs[role_model_type] = [role]

    def add_role(self, role: Role) -> None:
        """Add a new role

        Args:
            role ([type]): the role
        """
        self._roles.append(role)
        self._role_to_active[role] = True

    @property
    def roles(self) -> List[Role]:
        """Returns all roles

        Returns:
            List[Role]: the roles hold by this handler
        """
        return self._roles

    def deactivate(self, role) -> None:
        """Deactivates the role. This includes all tasks (soft suspending)

        :param role: the role to deactivate
        :type role: Role
        """
        self._role_to_active[role] = False
        self._scheduler.suspend(role)

    def activate(self, role) -> None:
        """Activates the given role. 

        :param role: the role to activate
        :type role: Role
        """
        self._role_to_active[role] = True
        self._scheduler.resume(role)

    def _is_role_active(self, role) -> bool:
        if role in self._role_to_active:
            return self._role_to_active[role]
        return True

    async def on_stop(self):
        """Notify all roles when the container is shutdown
        """
        for role in self._roles:
            await role.on_stop()

    def handle_msg(self, content, meta: Dict[str, Any]):
        """Handle an incoming message, delegating it to all applicable subscribers
        for role in self._role_handler.roles:
            if role.is_applicable(content, meta):
                role.handle_msg(content, meta, self)

        :param content: content
        :param meta: meta
        """
        for role, message_condition, method, _ in self._message_subs:
            if self._is_role_active(role):
                if message_condition(content, meta):
                    method(content, meta)

    def _notify_send_message_subs(self, content, receiver_addr, receiver_id, **kwargs):
        for role in self._send_msg_subs:
            for sub in self._send_msg_subs[role]:
                if self._is_role_active(role):
                    sub(content=content, receiver_addr=receiver_addr,
                        receiver_id=receiver_id,
                        **kwargs)


    async def send_message(self, content,
                           receiver_addr: Union[str, Tuple[str, int]], *,
                           receiver_id: Optional[str] = None,
                           **kwargs
    ):
        self._notify_send_message_subs(content, receiver_addr, receiver_id, **kwargs)
        return await self._container.send_message(
            content=content,
            receiver_addr=receiver_addr,
            receiver_id=receiver_id,
            **kwargs)

    async def send_acl_message(self, content,
                           receiver_addr: Union[str, Tuple[str, int]], *,
                           receiver_id: Optional[str] = None,
                           acl_metadata: Optional[Dict[str, Any]] = None,
                           **kwargs):
        self._notify_send_message_subs(content, receiver_addr, receiver_id, **kwargs)
        return await self._container.send_acl_message(
            content=content,
            receiver_addr=receiver_addr,
            receiver_id=receiver_id,
            acl_metadata=acl_metadata,
            **kwargs)
        
    def subscribe_message(self, role, method, message_condition, priority=0):
        if len(self._message_subs) == 0:
            self._message_subs.append((role, message_condition, method, priority))
            return

        for i in range(len(self._message_subs)):
            _, _, _, other_prio = self._message_subs[i]
            if priority < other_prio:
                self._message_subs.insert(i, (role, message_condition, method, priority))
                break
            elif i == len(self._message_subs) - 1:
                self._message_subs.append((role, message_condition, method, priority))

    def subscribe_send(self, role, method):
        if role in self._send_msg_subs:
            self._send_msg_subs[role].append(method)
        else:
            self._send_msg_subs[role] = [method]


class RoleAgentContext(RoleContext):
    """Implementation of the RoleContext-API.
    """

    def __init__(self, container, role_handler: RoleHandler, aid: str, inbox, scheduler: Scheduler):
        self._role_handler = role_handler
        self._container = container
        self._aid = aid
        self._scheduler = scheduler
        self._inbox = inbox

    @property
    def current_timestamp(self) -> float:
        return self._container.clock.time

    def _get_container(self):
        return self._role_handler._data

    def inbox_length(self):
        return self._inbox.qsize()

    def get_or_create_model(self, cls):
        return self._role_handler.get_or_create_model(cls)

    def update(self, role_model):
        self._role_handler.update(role_model)

    def subscribe_model(self, role, role_model_type):
        self._role_handler.subscribe(role, role_model_type)

    def subscribe_message(self, role, method, message_condition, priority=0):
        self._role_handler.subscribe_message(role, method, message_condition, priority=priority)

    def subscribe_send(self, role, method):
        self._role_handler.subscribe_send(role, method)

    def add_role(self, role: Role):
        """Add a role to the context.

        :param role: the Role
        """
        self._role_handler.add_role(role)

    def handle_msg(self, content, meta: Dict[str, Any]):
        """Handle an incoming message, delegating it to all applicable subscribers
        for role in self._role_handler.roles:
            if role.is_applicable(content, meta):
                role.handle_msg(content, meta, self)

        :param content: content
        :param meta: meta
        """
        self._role_handler.handle_msg(content, meta)

    def schedule_conditional_process_task(self, coroutine_creator, condition_func, lookup_delay=0.1, src=None):
        return self._scheduler.schedule_conditional_process_task(coroutine_creator=coroutine_creator, 
                                                                 condition_func=condition_func, 
                                                                 lookup_delay=lookup_delay, 
                                                                 src=src)

    def schedule_conditional_task(self, coroutine, condition_func, lookup_delay=0.1, src=None):
        return self._scheduler.schedule_conditional_task(coroutine=coroutine, condition_func=condition_func,
                                                         lookup_delay=lookup_delay, src=src)

    def schedule_datetime_process_task(self, coroutine_creator, date_time: datetime.datetime, src=None):
        return self._scheduler.schedule_datetime_process_task(coroutine_creator=coroutine_creator, 
                                                              date_time=date_time, 
                                                              src=src)

    def schedule_datetime_task(self, coroutine, date_time: datetime.datetime, src=None):
        return self._scheduler.schedule_datetime_task(coroutine=coroutine, date_time=date_time, src=src)

    def schedule_timestamp_task(self, coroutine, timestamp: float, src=None):
        return self._scheduler.schedule_timestamp_task(coroutine=coroutine, timestamp=timestamp, src=src)

    def schedule_timestamp_process_task(self, coroutine_creator, timestamp: float, src=None):
        return self._scheduler.schedule_timestamp_process_task(coroutine_creator=coroutine_creator,
                                                               timestamp=timestamp, src=src)

    def schedule_periodic_process_task(self, coroutine_creator, delay, src=None):
        return self._scheduler.schedule_periodic_process_task(coroutine_creator=coroutine_creator, 
                                                              delay=delay, 
                                                              src=src)

    def schedule_periodic_task(self, coroutine_func, delay, src=None):
        return self._scheduler.schedule_periodic_task(coroutine_func=coroutine_func, delay=delay, src=src)

    def schedule_instant_process_task(self, coroutine_creator, src=None):
        return self._scheduler.schedule_instant_process_task(coroutine_creator=coroutine_creator, 
                                                             src=src)

    def schedule_instant_task(self, coroutine, src=None):
        return self._scheduler.schedule_instant_task(coroutine=coroutine, src=src)

    def schedule_process_task(self, task: ScheduledProcessTask):
        return self._scheduler.schedule_process_task(task)

    def schedule_task(self, task: ScheduledTask, src=None):
        return self._scheduler.schedule_task(task, src=src)

    async def send_message(self, content,
                           receiver_addr: Union[str, Tuple[str, int]], *,
                           receiver_id: Optional[str] = None,
                           **kwargs
    ):
        return await self._role_handler.send_message(
            content=content,
            receiver_addr=receiver_addr,
            receiver_id=receiver_id,
            **kwargs)

    async def send_acl_message(self, content,
                           receiver_addr: Union[str, Tuple[str, int]], *,
                           receiver_id: Optional[str] = None,
                           acl_metadata: Optional[Dict[str, Any]] = None,
                           **kwargs
    ):
        return await self._role_handler.send_acl_message(
            content=content,
            receiver_addr=receiver_addr,
            receiver_id=receiver_id,
            acl_metadata=acl_metadata,
            **kwargs)

    @property
    def addr(self):
        return self._container.addr

    @property
    def aid(self):
        return self._aid

    def deactivate(self, role) -> None:
        self._role_handler.deactivate(role)

    def activate(self, role) -> None:
        self._role_handler.activate(role)


class RoleAgent(Agent):
    """Agent, which support the role API-system. When you want to use the role-api you always need
    a RoleAgent as base for your agents. A role can be added with :func:`RoleAgent.add_role`.
    """

    def __init__(self, container, suggested_aid: str = None):
        """Create a role-agent

        :param container: container the agent lives in
        :param suggested_aid: (Optional) suggested aid, if the aid is already taken, a generated aid is used. 
                              Using the generated aid-style ("agentX") is not allowed.
        """
        super().__init__(container, suggested_aid=suggested_aid)

        self._role_handler = RoleHandler(container, self._scheduler)
        self._agent_context = RoleAgentContext(
            container, self._role_handler, self.aid, self.inbox, self._scheduler)

    def add_role(self, role: Role):
        """Add a role to the agent. This will lead to the call of :func:`Role.setup`.

        :param role: the role to add
        """
        role.bind(self._agent_context)
        self._agent_context.add_role(role)

        # Setup role
        role.setup()

    def remove_role(self, role: Role):
        """Remove a role permanently from the agent.

        :param role: [description]
        :type role: Role
        """
        self._agent_context.remove_role(role)
        asyncio.create_task(role.on_stop())

    @property
    def roles(self) -> List[Role]:
        """Returns list of roles

        :return: list of roles
        """
        return self._role_handler.roles

    def handle_message(self, content, meta: Dict[str, Any]):
        self._agent_context.handle_msg(content, meta)

    async def shutdown(self):
        await self._role_handler.on_stop()
        await super().shutdown()
