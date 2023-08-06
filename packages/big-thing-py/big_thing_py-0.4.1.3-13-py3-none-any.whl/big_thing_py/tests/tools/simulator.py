from big_thing_py.tests.tools.test_tools_utils import *
from big_thing_py.tests.tools.elements import *
from tabulate import tabulate
import numpy as np
import csv


class Simulator():

    def __init__(self, simulation_file_path: str = None, clean_start: bool = True, debug: bool = False) -> None:
        self._name = None
        self._middleware_list: List[SoPMiddlewareElement] = []

        self._simulation_file_path = simulation_file_path
        self._simulation_code: List[SimulationData] = []
        self._simulation_start_time = None
        self._middleware_tree_config = None
        self._check_thing_list = []

        self._clean_start = clean_start

        self._simulation_statistics = {
            'middleware_list': []
        }

        self._user_data = {'function': self._on_message, 'user_data': None}
        self._debug = debug

        self._event_log: List[EventHolder] = []
        self._new_event_log: List[EventHolder] = []
        self._event_queue: Queue = Queue()

    @exception_wrapper
    def init(self):
        simulation_file = json_file_read(
            self._simulation_file_path)
        self._name = simulation_file['name']
        for chunk in simulation_file['simulation']:
            self._simulation_code.append(SimulationData(chunk=chunk))

    @exception_wrapper
    def wrapup(self):
        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                thing.kill()
            middleware.kill()

    def make_middleware_tree(self):
        middleware_tree = {}
        middleware_events: List[SimulationData] = []

        for event in self._simulation_code:
            if event.event_type == EventType.MIDDLEWARE_RUN:
                middleware_events.append(event)
        middleware_events = sorted(
            middleware_events, key=lambda x: x.level, reverse=True)

        for event in middleware_events:
            if event.level not in middleware_tree:
                middleware_tree[event.level] = [event]
            else:
                middleware_tree[event.level].append(event)
        return middleware_tree

    def make_thing_tree(self):
        thing_tree = dict(super=[], basic=[])
        thing_events: List[SimulationData] = []

        for event in self._simulation_code:
            if event.event_type == EventType.THING_RUN:
                thing_events.append(event)
        thing_events = sorted(
            thing_events, key=lambda x: x.is_super, reverse=True)

        for event in thing_events:
            if event.is_super:
                thing_tree['super'].append(event)
            else:
                thing_tree['basic'].append(event)
        return thing_tree

    def build_middleware_env(self):
        middleware_tree = self.make_middleware_tree()
        for level, layer in middleware_tree.items():
            layer: List[SimulationData]
            thread_list: List[Thread] = []

            SOPTEST_LOG_DEBUG(
                f'start to build Middleware layer level{level}...', 0)
            for middleware_data in layer:
                self._simulation_code.remove(middleware_data)
                mqtt_monitor_client = SoPMQTTMonitor(
                    name=middleware_data.name, host=middleware_data.host, port=middleware_data.port, debug=self._debug, level=middleware_data.level)
                self.user_data_set(mqtt_monitor_client, self._user_data)

                if middleware_data.parent_host:
                    middleware = SoPMiddlewareElement(parent_mqtt_monitor_client=self.select_middleware(middleware_data.parent_host, middleware_data.parent_port)._mqtt_monitor_client,
                                                      data=middleware_data, clean_start=self._clean_start, with_parent=True, debug=self._debug)
                else:
                    middleware = SoPMiddlewareElement(
                        mqtt_monitor_client=mqtt_monitor_client, data=middleware_data, clean_start=self._clean_start, with_parent=False, debug=self._debug)

                thread = Thread(target=middleware.run, args=(),
                                name=f'{middleware._name}_thread')
                self._middleware_list.append(middleware)
                thread_list.append(thread)
                thread.start()
                self._event_log.append(EventHolder(
                    middleware_name=middleware._name, event_type=EventType.MIDDLEWARE_RUN, level=middleware._level, timestamp=time.time(),
                    host=middleware._host, port=middleware._port))

            for thread in thread_list:
                thread_name = thread.getName()
                thread.join()
                for event in self._event_log:
                    if event.middleware_name == thread_name.split('_')[-1]:
                        event.duration = time.time() - event.timestamp

            SOPTEST_LOG_DEBUG(
                f'Middleware layer level {level} online...', 0)

    def build_thing_env(self):
        thing_tree = self.make_thing_tree()

        thing_type = 'basic'
        layer: List[SimulationData] = thing_tree[thing_type]
        thread_list: List[Thread] = []
        SOPTEST_LOG_DEBUG(
            f'start to build register {thing_type} things...', 0)
        for thing_data in layer:
            self._simulation_code.remove(thing_data)

            sel_middleware = self.select_middleware(
                host=thing_data.host, port=thing_data.port)
            mqtt_monitor_client = SoPMQTTMonitor(name=thing_data.name,
                                                 host=thing_data.host,
                                                 port=thing_data.port,
                                                 level=thing_data.level,
                                                 debug=self._debug)
            self.user_data_set(mqtt_monitor_client, self._user_data)
            thing = SoPThingElement(mqtt_monitor_client=mqtt_monitor_client,
                                    data=thing_data,
                                    debug=self._debug)
            sel_middleware._thing_list.append(thing)
            thread = Thread(target=thing.run,
                            args=(),
                            name=f'{thing._name}_thread')
            thread_list.append(thread)
            thread.start()
            self._event_log.append(EventHolder(
                thing_name=thing._name, event_type=EventType.THING_RUN, level=thing._level, timestamp=time.time(),
                host=thing._host, port=thing._port))

        for thread in thread_list:
            thread_name = thread.getName()
            thread.join()
            for event in self._event_log:
                if event.thing_name == thread_name.split('_')[-1]:
                    event.duration = time.time() - event.timestamp

        SOPTEST_LOG_DEBUG(
            f'thing register {thing_type} type finish...', 0)

        thing_type = 'super'
        layer: List[SimulationData] = thing_tree[thing_type]
        thread_list: List[Thread] = []

        SOPTEST_LOG_DEBUG(
            f'start to build register {thing_type} things...', 0)
        for thing_data in layer:
            self._simulation_code.remove(thing_data)

            sel_middleware = self.select_middleware(
                host=thing_data.host, port=thing_data.port)
            mqtt_monitor_client = SoPMQTTMonitor(name=thing_data.name,
                                                 host=thing_data.host,
                                                 port=thing_data.port,
                                                 level=thing_data.level,
                                                 debug=self._debug)
            self.user_data_set(mqtt_monitor_client, self._user_data)
            thing = SoPThingElement(mqtt_monitor_client=mqtt_monitor_client,
                                    data=thing_data,
                                    debug=self._debug)
            sel_middleware._thing_list.append(thing)
            thread = Thread(target=thing.run,
                            args=(),
                            name=f'{thing._name}_thread')
            thread_list.append(thread)
            thread.start()
            self._event_log.append(EventHolder(
                thing_name=thing._name, event_type=EventType.THING_RUN, level=thing._level, timestamp=time.time(),
                host=thing._host, port=thing._port))

        for thread in thread_list:
            thread_name = thread.getName()
            thread.join()
            for event in self._event_log:
                if event.thing_name == thread_name.split('_')[-1]:
                    event.duration = time.time() - event.timestamp

        SOPTEST_LOG_DEBUG(
            f'thing register {thing_type} type finish...', 0)

    def kill_env(self):
        for event in self._simulation_code:
            if event.event_type == EventType.MIDDLEWARE_RUN:
                if event.parent_host:
                    middleware = SoPMiddlewareElement(parent_mqtt_monitor_client=self.select_middleware(event.parent_host, event.parent_port)._mqtt_monitor_client,
                                                      data=event, clean_start=self._clean_start, with_parent=True, debug=self._debug)
                else:
                    middleware = SoPMiddlewareElement(
                        data=event, clean_start=self._clean_start, with_parent=False, debug=self._debug)

                middleware.make_middleware_config_file()
                self._middleware_list.append(middleware)

        for middleware in self._middleware_list:
            middleware.kill()

        SOPTEST_LOG_DEBUG('All Middleware was killed!', 0)

    @exception_wrapper
    def start(self, user_interaction=True):
        self._simulation_start_time = time.time()

        self.build_middleware_env()
        self.build_thing_env()

        for event in self._simulation_code:
            cur_time = time.time()
            sel_middleware = self.select_middleware(
                host=event.host, port=event.port)

            if event.event_type == EventType.DELAY:
                delay = SoPDelayElement(data=event)
                SOPTEST_LOG_DEBUG(f'Delay {delay._duration} Sec start...', 0)
                delay.run()
                # self._event_log.append(EventHolder(
                #     event_type=event.event_type, timestamp=cur_time))
            else:
                # wait until timestamp is reached
                if event.timestamp:
                    while time.time() - self._simulation_start_time < event.timestamp:
                        time.sleep(0.0001)

                if event.event_type == EventType.SCENARIO_VERIFY:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            scenario.verify()
                            break
                elif event.event_type == EventType.SCENARIO_ADD:
                    # sel_mqtt_monitor_client = sel_middleware.get_mqtt_monitor_client()
                    mqtt_monitor_client = SoPMQTTMonitor(
                        name=event.name, host=event.host, port=event.port, level=event.level, debug=self._debug)
                    scenario = SoPScenarioElement(
                        mqtt_monitor_client=mqtt_monitor_client, data=event, debug=self._debug)
                    self.user_data_set(mqtt_monitor_client, self._user_data)
                    scenario._mqtt_monitor_client.run()

                    # scenario._element_controller.send_file(
                    #     scenario._raw_scenario_file_path, scenario._scenario_file_path)

                    # if super thing is include in scenario, then run check_pc_service_list first
                    # TODO: 시나리오가 super service를 포함하고 있어야만, check_thing_exist를 실행해야 한다.
                    for thing in sel_middleware._thing_list:
                        if thing._is_super == True:
                            if not self.check_thing_exist(host=event.host, port=event.port, thing_name=thing._name, is_super=True):
                                raise SOPTEST_LOG_DEBUG(
                                    f'[{get_current_function_name()}] Super thing {thing._name} was not detected...', -1)

                    # 시나리오를 추가하자마자 schedule이 시작되는데 해당 과정에 middleware에 저장된 scenario_list를 활용해야한다.
                    # 근데 지금의 add 함수는 middleware의 DB에 시나리오가 저장되기 까지 기다리므로 schedule이 시작되는 시점에 sel_middleware의 scenario_list에는
                    # scenario가 추가되어있지 않다. 따라서 에러가 발생하므로 다음과 같이 먼저 _scenario_list.append를 하고 add를 실행한다.
                    sel_middleware._scenario_list.append(scenario)
                    scenario.add()
                    # 시나리오가 준비 되었는지 확인하고 넘어간다.
                    while True:
                        if not scenario.check_scenario_ready():
                            SOPTEST_LOG_DEBUG(
                                f'Scenario {scenario._name} was scheduling... wait for schedule finish', -1)
                            # scenario.update()
                            time.sleep(1)
                        else:
                            SOPTEST_LOG_DEBUG(
                                f'Scenario {scenario._name} was initialized', 0)
                            break
                elif event.event_type == EventType.SCENARIO_RUN:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            scenario.run()
                            break
                elif event.event_type == EventType.SCENARIO_STOP:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            while True:
                                scenario_state = scenario.check_scenario_state()
                                if scenario_state == ScenarioStateType.RUNNING:
                                    scenario.stop()
                                elif scenario_state in [ScenarioStateType.COMPLETED, ScenarioStateType.INITIALIZED, ScenarioStateType.STUCKED]:
                                    SOPTEST_LOG_DEBUG(
                                        f'Scenario {scenario._name} is already in {scenario_state}', 1)
                                time.sleep(1)
                            break
                elif event.event_type == EventType.SCENARIO_UPDATE:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            while not scenario.check_scenario_state([ScenarioStateType.RUNNING,
                                                                     ScenarioStateType.EXECUTING,
                                                                     ScenarioStateType.COMPLETED,
                                                                     ScenarioStateType.INITIALIZED,
                                                                     ScenarioStateType.STUCKED]):
                                time.sleep(1)
                            scenario.update()
                            break
                elif event.event_type == EventType.SCENARIO_DELETE:
                    for scenario in sel_middleware._scenario_list:
                        if scenario._name == event.name:
                            while not scenario.check_scenario_state([ScenarioStateType.COMPLETED,
                                                                     ScenarioStateType.INITIALIZED,
                                                                     ScenarioStateType.STUCKED]):
                                time.sleep(1)
                            scenario.delete()
                            break

            if not event.name:
                event_name = ''
            else:
                event_name = event.name
            if not event.host:
                event_host = ''
            else:
                event_host = event.host
            if not event.port:
                event_port = ''
            else:
                event_port = event.port

            # if event.event_type in [EventType.MIDDLEWARE_RUN, EventType.MIDDLEWARE_KILL, EventType.THING_KILL]:
            #     SOPTEST_LOG_DEBUG(
            #         f"""[EVENT][{event.event_type.value:<{max([len(e.value) for e in EventType])}}]: {event_name:<40}|{f'{event_host}:{event_port}':<21}|{f'{"SUPER" if event.is_super else "BASIC"}':<6}|{f'{"LOCAL" if event.is_local else "REMOTE"}':<6}""", 0)
            SOPTEST_LOG_DEBUG(
                f"""[EVENT][{event.event_type.value:<{max([len(e.value) for e in EventType])}}]: {event_name:<40}|{f'{event_host}:{event_port}':<21}|{f'{"SUPER" if event.is_super else "BASIC"}':<6}|{f'{"LOCAL" if event.is_local else "REMOTE"}':<6}""", 0)

        self.wrapup()
        self.post_processing_event_log()
        self.show_simulation_result(user_interaction)

    @exception_wrapper
    def _on_message(self, client: SoPMQTTMonitor, user_data: Any, message: mqtt.MQTTMessage):
        topic, payload, timestamp = decode_MQTT_message(message)
        timestamp = time.time()
        host = client._host
        port = client._port
        level = client._level
        scenario_name = payload.get('scenario', None)
        return_type = SoPType.get(payload.get('return_type', None))
        return_value = payload.get('return_value', None)
        error_type = SoPErrorType.get(payload.get('error', None))

        user_data = user_data['user_data']

        sel_middleware = self.select_middleware(host=host, port=port)
        # print(f'{client._host}:{client._port}')

        if SoPProtocolType.Base.TM_REGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[2]
            self._event_log.append(EventHolder(thing_name=thing_name, middleware_name=sel_middleware._name,
                                               event_type=EventType.THING_REGISTER, level=level, timestamp=timestamp,
                                               host=host, port=port))
        elif SoPProtocolType.Base.MT_RESULT_REGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[3]
            for event in list(reversed(self._event_log)):
                if thing_name == event.thing_name and event.event_type == EventType.THING_REGISTER:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[REGISTER] thing: {thing_name} duration: {event.duration}', 0)
                    break
        elif SoPProtocolType.Base.TM_UNREGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[2]
            self._event_log.append(EventHolder(thing_name=thing_name, middleware_name=sel_middleware._name,
                                               event_type=EventType.THING_UNREGISTER, level=level, timestamp=timestamp,
                                               host=host, port=port))
        elif SoPProtocolType.Base.MT_RESULT_UNREGISTER.get_prefix() in topic:
            thing_name = topic.split('/')[3]

            for event in list(reversed(self._event_log)):
                if thing_name == event.thing_name and event.event_type == EventType.THING_UNREGISTER:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[UNREGISTER] thing: {thing_name} duration: {event.duration}', 0)
                    break
        elif SoPProtocolType.Base.MT_EXECUTE.get_prefix() in topic:
            if len(topic.split('/')) > 4:
                middleware_name = topic.split('/')[4]
                request_ID = topic.split('/')[5]
                requester_middleware_name = request_ID.split('@')[0]
                super_thing_name = request_ID.split('@')[1]
                super_function_name = request_ID.split('@')[2]
                subrequest_order = request_ID.split('@')[3]
            else:
                requester_middleware_name = None

            thing_name = topic.split('/')[3]
            function_name = topic.split('/')[2]

            energy = None
            for thing in sel_middleware._thing_list:
                for function in thing._function_list:
                    if function_name == function['name']:
                        energy = function['energy']

            self._event_log.append(EventHolder(thing_name=thing_name, function_name=function_name, middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.FUNCTION_EXECUTE, level=level, timestamp=timestamp, energy=energy, requester_middleware_name=requester_middleware_name,
                                               host=host, port=port))
        elif SoPProtocolType.Base.TM_RESULT_EXECUTE.get_prefix() in topic:
            if len(topic.split('/')) > 5:
                middleware_name = topic.split('/')[5]
                request_ID = topic.split('/')[6]
                requester_middleware_name = request_ID.split('@')[0]
                super_thing_name = request_ID.split('@')[1]
                super_function_name = request_ID.split('@')[2]
                subrequest_order = request_ID.split('@')[3]
            else:
                requester_middleware_name = None

            thing_name = topic.split('/')[4]
            function_name = topic.split('/')[3]

            scenario = self.select_scenario(name=scenario_name)
            sel_thing = self.select_thing(name=thing_name)
            target_super_function = sel_thing.find_function(name=function_name)
            target_super_function['total_energy_consumption'] += target_super_function['energy']
            target_super_function['call_count'] += 1
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if thing_name == event.thing_name and function_name == event.function_name and scenario_name == event.scenario_name and event.event_type == EventType.FUNCTION_EXECUTE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    event.requester_middleware_name = requester_middleware_name

                    target_super_function['total_duration'] += event.duration

                    SOPTEST_LOG_DEBUG(
                        f'[EXECUTE] thing: {thing_name} function: {function_name} scenario: {scenario_name} duration: {event.duration} return value:{return_value} - {return_type.value}', 0)
                    break
        elif SoPProtocolType.WebClient.EM_VERIFY_SCENARIO.get_prefix() in topic:
            scenario_name = payload.get('name', None)
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_VERIFY, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_VERIFY_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_VERIFY:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_VERIFY] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_ADD_SCENARIO.get_prefix() in topic:
            scenario_name = payload.get('name', None)
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_ADD, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_ADD_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_ADD:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_ADD] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_RUN_SCENARIO.get_prefix() in topic:
            scenario_name = payload.get('name', None)
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_RUN, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_RUN_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_RUN:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_RUN] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_STOP_SCENARIO.get_prefix() in topic:
            scenario_name = payload.get('name', None)
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_STOP, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_STOP_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_STOP:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_STOP] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_UPDATE_SCENARIO.get_prefix() in topic:
            scenario_name = payload.get('name', None)
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_UPDATE, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_UPDATE_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_UPDATE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_UPDATE] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.WebClient.EM_DELETE_SCENARIO.get_prefix() in topic:
            scenario_name = payload.get('name', None)
            self._event_log.append(EventHolder(middleware_name=sel_middleware._name, scenario_name=scenario_name,
                                               event_type=EventType.SCENARIO_DELETE, level=level, timestamp=timestamp,
                                               result=error_type,
                                               host=host, port=port))
        elif SoPProtocolType.WebClient.ME_RESULT_DELETE_SCENARIO.get_prefix() in topic:
            for event in list(reversed(self._event_log)):
                if scenario_name == event.scenario_name and event.event_type == EventType.SCENARIO_DELETE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    SOPTEST_LOG_DEBUG(
                        f'[SCENE_DELETE] scenario: {scenario_name} duration: {event.duration}', 1)
                    break
        elif SoPProtocolType.Super.MS_SCHEDULE.get_prefix() in topic:
            requester_middleware_name = topic.split('/')[5]
            super_middleware_name = topic.split('/')[4]
            super_thing_name = topic.split('/')[3]
            super_function_name = topic.split('/')[2]

            self._event_log.append(EventHolder(thing_name=super_thing_name, function_name=super_function_name, middleware_name=super_middleware_name, requester_middleware_name=requester_middleware_name, scenario_name=scenario_name,
                                               event_type=EventType.SUPER_SCHEDULE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'[SUPER_SCHEDULE_START] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.SM_SCHEDULE.get_prefix() in topic:
            request_ID = topic.split('/')[5]
            requester_middleware_name = request_ID.split('@')[0]
            super_thing_name = request_ID.split('@')[1]
            super_function_name = request_ID.split('@')[2]
            subrequest_order = request_ID.split('@')[3]

            target_middleware_name = topic.split('/')[4]
            target_thing_name = topic.split('/')[3]
            target_function_name = topic.split('/')[2]

            self._event_log.append(EventHolder(thing_name=super_thing_name, target_thing_name=target_thing_name, target_function_name=target_function_name, target_middleware_name=target_middleware_name, scenario_name=scenario_name,
                                               event_type=EventType.SUB_SCHEDULE, level=level, timestamp=timestamp, requester_middleware_name=requester_middleware_name, super_thing_name=super_thing_name, super_function_name=super_function_name,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'  [SUB_SCHEDULE_START] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.MS_RESULT_SCHEDULE.get_prefix() in topic:
            request_ID = topic.split('/')[5]
            requester_middleware_name = request_ID.split('@')[0]
            super_thing_name = request_ID.split('@')[1]
            super_function_name = request_ID.split('@')[2]
            subrequest_order = request_ID.split('@')[3]

            target_middleware_name = topic.split('/')[4]
            target_thing_name = topic.split('/')[3]
            target_function_name = topic.split('/')[2]

            scenario = self.select_scenario(name=scenario_name)
            if not scenario:
                raise SOPTEST_LOG_DEBUG(
                    f'Scenario was not found in sel_middleware', -1)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        target_function_name == event.target_function_name and \
                        target_middleware_name == event.target_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUB_SCHEDULE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'  [SUB_SCHEDULE_END] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result}', 0)
                    break
        elif SoPProtocolType.Super.SM_RESULT_SCHEDULE.get_prefix() in topic:
            requester_middleware_name = topic.split('/')[6]
            super_middleware_name = topic.split('/')[5]
            super_thing_name = topic.split('/')[4]
            super_function_name = topic.split('/')[3]

            sel_thing = self.select_thing(name=super_thing_name)
            target_super_function = sel_thing.find_function(
                name=super_function_name)
            target_super_function['total_energy_consumption'] += target_super_function['energy']
            target_super_function['call_count'] += 1

            scenario = self.select_scenario(name=scenario_name)
            if not scenario:
                raise SOPTEST_LOG_DEBUG(
                    f'Scenario was not found in sel_middleware', -1)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        super_function_name == event.function_name and \
                        super_middleware_name == event.middleware_name and \
                        requester_middleware_name == event.requester_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUPER_SCHEDULE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    target_super_function['total_duration'] += event.duration

                    SOPTEST_LOG_DEBUG(
                        f'[SUPER_SCHEDULE_END] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result}', 0)
                    break

        ################################################################################################################################################################################################################################################

        elif SoPProtocolType.Super.MS_EXECUTE.get_prefix() in topic:
            super_function_name = topic.split('/')[2]
            super_thing_name = topic.split('/')[3]
            super_middleware_name = topic.split('/')[4]
            requester_middleware_name = topic.split('/')[5]

            self._event_log.append(EventHolder(thing_name=super_thing_name, function_name=super_function_name, middleware_name=super_middleware_name, requester_middleware_name=requester_middleware_name, scenario_name=scenario_name,
                                               event_type=EventType.SUPER_FUNCTION_EXECUTE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'[SUPER_EXECUTE_START] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.SM_EXECUTE.get_prefix() in topic:
            request_ID = topic.split('/')[5]
            requester_middleware_name = request_ID.split('@')[0]
            super_thing_name = request_ID.split('@')[1]
            super_function_name = request_ID.split('@')[2]
            subrequest_order = request_ID.split('@')[3]

            target_middleware_name = topic.split('/')[4]
            target_thing_name = topic.split('/')[3]
            target_function_name = topic.split('/')[2]

            self._event_log.append(EventHolder(thing_name=super_thing_name, target_middleware_name=target_middleware_name, target_thing_name=target_thing_name, target_function_name=target_function_name, scenario_name=scenario_name,
                                               event_type=EventType.SUB_FUNCTION_EXECUTE, level=level, timestamp=timestamp,
                                               host=host, port=port))
            SOPTEST_LOG_DEBUG(
                f'  [SUB_EXECUTE_START] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name}', 0)
        elif SoPProtocolType.Super.MS_RESULT_EXECUTE.get_prefix() in topic:
            request_ID = topic.split('/')[5]
            requester_middleware_name = request_ID.split('@')[0]
            super_thing_name = request_ID.split('@')[1]
            super_function_name = request_ID.split('@')[2]
            subrequest_order = request_ID.split('@')[3]

            target_middleware_name = topic.split('/')[5]
            target_thing_name = topic.split('/')[4]
            target_function_name = topic.split('/')[3]

            scenario = self.select_scenario(name=scenario_name)
            if not scenario:
                raise SOPTEST_LOG_DEBUG(
                    f'Scenario was not found in sel_middleware', -1)
            sel_thing = self.select_thing(name=super_thing_name)
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        target_thing_name == event.target_thing_name and \
                        target_function_name == event.target_function_name and \
                        target_middleware_name == event.target_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUB_FUNCTION_EXECUTE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'  [SUB_EXECUTE_END] target_middleware: {target_middleware_name} target_thing: {target_thing_name} target_function: {target_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result} return value:{return_value} - {return_type.value}', 0)
                    break
        elif SoPProtocolType.Super.SM_RESULT_EXECUTE.get_prefix() in topic:
            requester_middleware_name = topic.split('/')[6]
            super_middleware_name = topic.split('/')[5]
            super_thing_name = topic.split('/')[4]
            super_function_name = topic.split('/')[3]

            scenario = self.select_scenario(name=scenario_name)
            if not scenario:
                raise SOPTEST_LOG_DEBUG(
                    f'Scenario was not found in sel_middleware', -1)

            sel_thing = self.select_thing(name=super_thing_name)
            target_super_function = sel_thing.find_function(
                name=super_function_name)
            target_super_function['total_energy_consumption'] += target_super_function['energy']
            target_super_function['call_count'] += 1
            if not sel_thing in scenario._thing_list:
                scenario._thing_list.append(sel_thing)

            for event in list(reversed(self._event_log)):
                if super_thing_name == event.thing_name and \
                        super_function_name == event.function_name and \
                        super_middleware_name == event.middleware_name and \
                        requester_middleware_name == event.requester_middleware_name and \
                        scenario_name == event.scenario_name and \
                        event.event_type == EventType.SUPER_FUNCTION_EXECUTE:
                    event.duration = timestamp - event.timestamp
                    event.result = error_type
                    event.return_type = return_type
                    event.return_value = return_value
                    SOPTEST_LOG_DEBUG(
                        f'[SUPER_EXECUTE_END] super_middleware: {super_middleware_name} requester_middleware: {requester_middleware_name} super_thing: {super_thing_name} super_function: {super_function_name} scenario: {scenario_name} duration: {event.duration} result: {event.result} return value:{return_value} - {return_type.value}', 0)
                    break
        # elif SoPProtocolType.Default.TM_VALUE_PUBLISH.get_prefix() in topic:
        #     pass
        # elif SoPProtocolType.Default.TM_VALUE_PUBLISH_OLD.get_prefix() in topic:
        #     pass

    # ====================================
    #    _____  _                  _
    #   / ____|| |                | |
    #  | |     | |__    ___   ___ | | __
    #  | |     | '_ \  / _ \ / __|| |/ /
    #  | |____ | | | ||  __/| (__ |   <
    #   \_____||_| |_| \___| \___||_|\_\
    # ====================================

    @exception_wrapper
    def check_pc_service_list(self, host: str = None, port: int = None, timeout: int = 10):
        sel_mqtt_monitor_client = self.select_middleware(
            host=host, port=port).get_mqtt_monitor_client()
        topic, payload, timestamp = sel_mqtt_monitor_client.expect(
            SoPProtocolType.Super.PC_SERVICE_LIST.value % ('#'), timeout=timeout)
        if payload is not None:
            SOPTEST_LOG_DEBUG(
                f'Service list packet detected!', 0)
            return True
        else:
            SOPTEST_LOG_DEBUG('get service list failed...', -1)
            return False

    @exception_wrapper
    def check_thing_exist(self, host: str = None, port: int = None, thing_name: str = None, is_super: bool = False, timeout: int = 30):
        retry_period = 0.5

        if dict(host=host, port=port, thing_name=thing_name, is_super=is_super) in self._check_thing_list:
            thing_name_prefix = 'Super ' if is_super else ''
            sel_mqtt_monitor_client = self.select_middleware(
                host=host, port=port).get_mqtt_monitor_client()
            SOPTEST_LOG_DEBUG(
                f'{thing_name_prefix}Thing {thing_name} detected at {sel_mqtt_monitor_client._client_id}!', 0)
            return True
        else:
            while timeout:
                sel_mqtt_monitor_client = self.select_middleware(
                    host=host, port=port).get_mqtt_monitor_client()
                topic, payload, timestamp = sel_mqtt_monitor_client.publish_and_expect(
                    encode_MQTT_message(
                        SoPProtocolType.WebClient.EM_REFRESH.value % sel_mqtt_monitor_client._client_id, f'{{}}'),
                    SoPProtocolType.WebClient.ME_RESULT_SERVICE_LIST.value % (sel_mqtt_monitor_client._client_id), timeout=timeout)
                if payload is not None:
                    service_list = payload['services']
                    for service in service_list:
                        thing_list = service['things']
                        for thing in thing_list:
                            if thing_name == thing['id'] and is_super == bool(thing['is_super']):
                                thing_name_prefix = 'Super ' if is_super else ''
                                SOPTEST_LOG_DEBUG(
                                    f'{thing_name_prefix}Thing {thing_name} detected at {sel_mqtt_monitor_client._client_id}!', 0)
                                self._check_thing_list.append(
                                    dict(host=host, port=port, thing_name=thing_name, is_super=is_super))
                                return True
                    else:
                        SOPTEST_LOG_DEBUG(
                            f'Thing {thing_name} not exist! retry...', 1)
                        timeout -= retry_period
                        time.sleep(retry_period)
                        return False
                else:
                    raise SOPTEST_LOG_DEBUG('get thing list failed...', -1)
            else:
                raise SOPTEST_LOG_DEBUG(
                    f'[{get_current_function_name()}] Check thing {thing_name} exist check failed...', -1)

    # ========================
    #         _    _  _
    #        | |  (_)| |
    #  _   _ | |_  _ | | ___
    # | | | || __|| || |/ __|
    # | |_| || |_ | || |\__ \
    #  \__,_| \__||_||_||___/
    # ========================

    def select_middleware(self, host: str = None, port: int = None, name: str = None) -> SoPMiddlewareElement:
        for middleware in self._middleware_list:
            if (host == middleware._host and port == middleware._port) or name == middleware._name:
                return middleware

    def select_scenario(self, middleware: SoPMiddlewareElement = None, name: str = None) -> SoPScenarioElement:
        if middleware:
            for scenario in middleware._scenario_list:
                if name == scenario._name:
                    return scenario
        else:
            for middleware in self._middleware_list:
                for scenario in middleware._scenario_list:
                    if name == scenario._name:
                        return scenario

        return False

    def select_thing(self, middleware: SoPMiddlewareElement = None, name: str = None) -> SoPThingElement:
        if middleware:
            for thing in middleware._thing_list:
                if name == thing._name:
                    return thing
        else:
            for middleware in self._middleware_list:
                for thing in middleware._thing_list:
                    if name == thing._name:
                        return thing

        return False

    def user_data_set(self, sel_mqtt_monitor_client: SoPMQTTMonitor, user_data):
        self._user_data['user_data'] = user_data
        sel_mqtt_monitor_client._client.user_data_set(self._user_data)

    def get_function_energy_list(self, function_name: str):
        function_energy_list = []
        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                for function in thing._function_list:
                    if function['name'] == function_name:
                        function_energy_list.append(
                            function['energy'])
        function_energy_list = sorted(
            function_energy_list, reverse=True)
        return function_energy_list

    def calculate_utilization_and_energy(self):
        total_simulation_time = self._event_log[-1].timestamp - \
            self._event_log[0].timestamp

        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                for function in thing._function_list:
                    function['utilization'] = function['total_duration'] / \
                        total_simulation_time
                    thing._total_energy_consumption += function['total_energy_consumption']

    def calculate_energy_score(self):
        function_energy_info = {}
        for middleware in self._middleware_list:
            for thing in middleware._thing_list:
                for function in thing._function_list:
                    if function['name'] not in function_energy_info:
                        function_energy_info[function['name']] = [
                            function['energy'], ]
                    else:
                        function_energy_info[function['name']].append(
                            function['energy'])

            score = 0
            cnt = 0
            for event in middleware._event_log:
                if event.function_name in function_energy_info:
                    energy_list = sorted(
                        function_energy_info[event.function_name])
                    for i, energy in enumerate(energy_list):
                        if energy == event.energy:
                            energy_score = 100 / (i + 1)
                            score += energy_score
                            cnt += 1
            middleware._energy_score = score / cnt

    def calculate_qos_score(self):
        for middleware in self._middleware_list:
            cnt = 0
            execute_event_list = [
                event for event in middleware._event_log if event.event_type == EventType.FUNCTION_EXECUTE]
            for event in execute_event_list:
                if event.result == SoPErrorType.NO_ERROR:
                    cnt += 1
            middleware._qos_score = (cnt / len(execute_event_list)) * 100.0

    def calculate_scenario_cycle_avg(self):

        # 리스트 안에서 반복되는 패턴을 찾아 리턴하는 함수
        def find_pattern(event_list: List[EventHolder]):
            for i in range(1, len(event_list)):
                if [event.function_name for event in event_list[:i]] == [event.function_name for event in event_list[i:i+i]]:
                    return event_list[:i]
            return event_list

        for middleware in self._middleware_list:
            for scenario in middleware._scenario_list:
                # capture execute pattern
                scenario_latency_list = []
                loop_check = True
                if 'super' in scenario._name:
                    execute_event_list: List[EventHolder] = [
                        event for event in scenario._event_log if event.event_type in [EventType.SUPER_FUNCTION_EXECUTE]]
                else:
                    execute_event_list: List[EventHolder] = [
                        event for event in scenario._event_log if event.event_type in [EventType.FUNCTION_EXECUTE]]
                execute_pattern = find_pattern(execute_event_list)

                for i in range(0, len(execute_event_list), len(execute_pattern)):
                    if i + len(execute_pattern) - 1 >= len(execute_event_list):
                        break
                    elif not execute_event_list[i + len(execute_pattern) - 1].duration:
                        break

                    cycle_start_time = execute_event_list[i].timestamp
                    cycle_end_time = execute_event_list[i + len(
                        execute_pattern) - 1].timestamp + execute_event_list[i + len(execute_pattern) - 1].duration
                    cycle_duration = cycle_end_time - cycle_start_time

                    if cycle_duration > scenario._period / 1000:
                        loop_check = False
                    scenario_latency_list.append(cycle_duration)

                scenario._loop_check = loop_check
                if len(scenario_latency_list) > 0:
                    scenario._avg_latency = sum(
                        scenario_latency_list) / len(scenario_latency_list)
                else:
                    scenario._avg_latency = 0
                    scenario._loop_check = False
                    SOPTEST_LOG_DEBUG(
                        f'scenario was failed!!!. scenario: {scenario._name}', -1)

    def post_processing_event_log(self):
        for event in self._event_log:
            event.timestamp -= self._simulation_start_time
            if event.event_type in [EventType.MIDDLEWARE_RUN,
                                    EventType.MIDDLEWARE_KILL,
                                    EventType.THING_REGISTER,
                                    EventType.THING_UNREGISTER,
                                    EventType.THING_KILL,
                                    EventType.FUNCTION_EXECUTE,
                                    EventType.SCENARIO_VERIFY,
                                    EventType.SCENARIO_ADD,
                                    EventType.SCENARIO_RUN,
                                    EventType.SCENARIO_STOP,
                                    EventType.SCENARIO_UPDATE,
                                    EventType.SCENARIO_DELETE,
                                    EventType.SUPER_FUNCTION_EXECUTE,
                                    EventType.SUPER_SCHEDULE,
                                    EventType.SUB_FUNCTION_EXECUTE,
                                    EventType.SUB_SCHEDULE]:
                middleware = self.select_middleware(
                    event.host, event.port, event.middleware_name)
                middleware._event_log.append(event)

                for thing in middleware._thing_list:
                    if event.event_type in [EventType.THING_REGISTER,
                                            EventType.THING_UNREGISTER,
                                            EventType.THING_KILL,
                                            EventType.FUNCTION_EXECUTE,
                                            EventType.SUPER_FUNCTION_EXECUTE]:
                        if not thing._name == event.thing_name:
                            continue
                        thing._event_log.append(event)

                for scenario in middleware._scenario_list:
                    if event.event_type in [EventType.THING_REGISTER,
                                            EventType.THING_UNREGISTER,
                                            EventType.THING_KILL,
                                            EventType.FUNCTION_EXECUTE,
                                            EventType.SUPER_FUNCTION_EXECUTE,
                                            EventType.SCENARIO_VERIFY,
                                            EventType.SCENARIO_ADD,
                                            EventType.SCENARIO_RUN,
                                            EventType.SCENARIO_STOP,
                                            EventType.SCENARIO_UPDATE,
                                            EventType.SCENARIO_DELETE]:
                        if not scenario._name == event.scenario_name:
                            continue
                        if event.event_type in [EventType.THING_REGISTER,
                                                EventType.THING_UNREGISTER,
                                                EventType.THING_KILL,
                                                EventType.FUNCTION_EXECUTE,
                                                EventType.SUPER_FUNCTION_EXECUTE]:
                            if event.thing_name in [thing._name for thing in scenario._thing_list]:
                                scenario._event_log.append(event)
                        elif event.event_type in [EventType.SCENARIO_VERIFY,
                                                  EventType.SCENARIO_ADD,
                                                  EventType.SCENARIO_RUN,
                                                  EventType.SCENARIO_STOP,
                                                  EventType.SCENARIO_UPDATE,
                                                  EventType.SCENARIO_DELETE]:
                            scenario._event_log.append(event)

        # service, thing utilization
        self.calculate_utilization_and_energy()
        self.calculate_scenario_cycle_avg()
        # self.calculate_energy_score()
        # self.calculate_qos_score()

    def convert_return_type(self, return_type):
        if return_type.value == -1:
            return_type = 'UNDEFINED'
        else:
            return_type = return_type
        return return_type

    def convert_execute_result(self, execute_result):
        if execute_result.value == 0:
            return 'NO_ERROR'
        elif execute_result.value == -1:
            return 'FAILED'
        elif execute_result.value == -2:
            return 'TIMEOUT'
        elif execute_result.value == -3:
            return 'NO_PARALLEL'
        elif execute_result.value == -4:
            return 'DUPLICATE'
        elif execute_result.value == -5:
            return 'UNDEFINED'

    def print_table(self, table, header, scenario_name: str = None):
        title_filler = '-'
        table = tabulate(table, headers=header, tablefmt='fancy_grid')

        if scenario_name:
            print(
                f"{f' scenario {scenario_name} ':{title_filler}^{len(table.split()[0])}}")
        print(table)

    @exception_wrapper
    def print_simulation_result(self, target_middleware: SoPMiddlewareElement, user_interaction: bool):

        def check_service_contain_in_scenario(target_middleware: SoPMiddlewareElement, function_name: str):
            for scenario in target_middleware._scenario_list:
                if f'.{function_name}' in scenario._scenario_code:
                    return True

            return False

        def make_service_utilization_table(target_middleware: SoPMiddlewareElement):
            header = ['thing(is_parallel)', 'service(call count)',
                      'energy consumption', 'utilization']
            table = []
            for thing in target_middleware._thing_list:
                for function in thing._function_list:
                    # service_postfix = '*' if not check_service_contain_in_scenario(
                    #     target_middleware, function['name']) else ''
                    service_postfix = ''
                    utilization = function['utilization']
                    call_count = function['call_count']
                    total_energy_consumption = function['total_energy_consumption']
                    if utilization > 0:
                        table.append(
                            [f'{thing._name}({thing._is_parallel})', f"{function['name']}({call_count}){service_postfix}", total_energy_consumption, f'{utilization * 100:.2f}%'])
            return table, header

        def make_scenario_score_table(target_middleware: SoPMiddlewareElement):
            header = ['scenario', 'avg latency', 'period', 'deadline meet']
            table = []
            for scenario in target_middleware._scenario_list:
                table.append(
                    [scenario._name, f'{scenario._avg_latency:.2f}s', f'{(scenario._period / 1000):.2f}s', scenario._loop_check])
            return table, header

        def make_whole_timeline_table(target_middleware: SoPMiddlewareElement):
            header = ['time', 'duration', 'event_type', 'level', 'middleware', 'thing',
                      'service(delay)', 'scenario(period)', 'result', 'return_value', 'return_type']
            table = []
            for event in target_middleware._event_log:
                if event.event_type == EventType.FUNCTION_EXECUTE and not event.duration:
                    continue
                table.append([event.timestamp, event.duration, event.event_type.value, event.level, event.middleware_name,
                              event.thing_name, event.function_name, event.scenario_name, self.convert_execute_result(event.result), event.return_value, self.convert_return_type(event.return_type)])
            return table, header

        while user_interaction:
            print()
            print('0: Service Utilization\n'
                  '1: Scenario Score\n'
                  '2: Whole Timeline\n')
            # print('0: Middleware score\n'
            #       '1: Thing Utilization\n'
            #       '2: Service Utilization\n'
            #       '3: Scenario Score\n'
            #       '4: Whole Timeline\n')
            user_input = input(
                'Select Menu (press \'q\' to select middleware): ')

            if user_input == 'q' or not user_input.isdigit():
                break

            user_input = int(user_input)

            # if user_input == 0:
            #     # print middleware score
            #     print(f'== Middleware {target_middleware._name} Score == ')
            #     header = ['energy_score', 'qos_score']
            #     table = []
            #     for scenario in target_middleware._scenario_list:
            #         table.append([target_middleware._energy_score,
            #                       target_middleware._qos_score])
            #         self.print_table(table, header)
            # elif user_input == 1:
            #     # print thing utilization
            #     print(f'== Thing Utilization ==')
            #     header = ['thing', 'utilization']
            #     table = []
            #     for k, i in target_middleware._thing_utilization_info.items():
            #         table.append([k, f'{i * 100:.2f}%'])
            #     self.print_table(table, header)
            if user_input == 0:
                # print service utilization
                print(f'== Service Utilization ==')
                table, header = make_service_utilization_table(
                    target_middleware)
                self.print_table(table, header)
            elif user_input == 1:
                # print scenario score
                print(f'== Scenario Score ==')
                table, header = make_scenario_score_table(target_middleware)
                self.print_table(table, header)
            elif user_input == 2:
                # print scenario timeline
                print(f'== Whole Timeline ==')
                table, header = make_whole_timeline_table(target_middleware)
                self.print_table(table, header)
        else:
            table = []
            table.append([f'{target_middleware._name}'])
            table.append(['Service Utilization'])
            service_utilization_table, header = make_service_utilization_table(
                target_middleware)
            table.append(header)
            for line in service_utilization_table:
                table.append(line)
            table.append(['Scenario Score'])
            scenario_score_table, header = make_scenario_score_table(
                target_middleware)
            table.append(header)
            for line in scenario_score_table:
                table.append(line)
            table.append(['Whole Timeline'])
            whole_timeline_table, header = make_whole_timeline_table(
                target_middleware)
            table.append(header)
            for line in whole_timeline_table:
                table.append(line)

            return table

    def export_simulation_result(self):
        simulation_result_table = []
        simulation_result_table.append(['middleware name', 'service utilization deviation(local)', 'service duration avg(local)', 'service utilization deviation(super)',
                                        'service duration avg(super)', 'scenario duty ratio(local)', 'scenario success(local)', 'scenario duty ratio(super)', 'scenario success(super)'])
        for middleware in self._middleware_list:
            middleware_result = [middleware._name]

            # export service utilization info
            service_utilization_deviation_table = []
            service_duration_avg_table = []
            super_service_utilization_deviation_table = []
            super_service_duration_avg_table = []
            for thing in middleware._thing_list:
                if thing._is_super:
                    for function in thing._function_list:
                        utilization = function['utilization']
                        duration = function['total_duration'] / \
                            function['call_count'] if function['call_count'] != 0 else 0
                        if utilization > 0:
                            super_service_duration_avg_table.append(duration)
                            super_service_utilization_deviation_table.append(
                                utilization)
                else:
                    for function in thing._function_list:
                        utilization = function['utilization']
                        duration = function['total_duration'] / \
                            function['call_count'] if function['call_count'] != 0 else 0
                        if utilization > 0:
                            service_duration_avg_table.append(duration)
                            service_utilization_deviation_table.append(
                                utilization)

            middleware_result.append(
                np.var(service_utilization_deviation_table) if np.var(service_utilization_deviation_table) != 'nan' else '')
            middleware_result.append(
                np.average(service_duration_avg_table))
            middleware_result.append(np.var(super_service_utilization_deviation_table) if len(
                super_service_utilization_deviation_table) > 0 else '')
            middleware_result.append(np.average(super_service_duration_avg_table) if len(
                super_service_duration_avg_table) > 0 else '')

            # export scenario score info
            scenario_duty_ratio_table = []
            scenario_fail_table = []
            super_scenario_duty_ratio_table = []
            super_scenario_fail_table = []
            for scenario in middleware._scenario_list:
                if scenario._thing_list[0]._is_super:
                    super_scenario_duty_ratio_table.append(
                        scenario._avg_latency * 1000 / scenario._period)
                    super_scenario_fail_table.append(scenario._loop_check)
                else:
                    scenario_duty_ratio_table.append(
                        scenario._avg_latency * 1000 / scenario._period)
                    scenario_fail_table.append(scenario._loop_check)

            middleware_result.append(np.average(scenario_duty_ratio_table))
            middleware_result.append(
                False if False in scenario_fail_table else True)
            middleware_result.append('' if (len(super_scenario_duty_ratio_table) == 0) else np.average(
                super_scenario_duty_ratio_table))
            middleware_result.append(
                False if False in super_scenario_fail_table else '' if (len(super_scenario_fail_table) == 0) else True)

            simulation_result_table.append(middleware_result)

            # export whole timeline info
            # whole_timeline_table = []
            # for event in middleware._event_log:
            #     if event.event_type == EventType.FUNCTION_EXECUTE and not event.duration:
            #         continue
            #     whole_timeline_table.append([event.timestamp, event.duration, event.event_type.value, event.level, event.middleware_name,
            #                                  event.thing_name, event.function_name, event.scenario_name, self.convert_execute_result(event.result), event.return_value, self.convert_return_type(event.return_type)])

        csv_file_path = f'{os.path.dirname(self._simulation_file_path)}/{os.path.basename(self._simulation_file_path)}_result.csv'
        f = open(csv_file_path, 'w')
        wr = csv.writer(f)
        for row in simulation_result_table:
            print(row)
            wr.writerow(row)

        def cal_avg(simulation_result_table, index):
            return f'{np.average([result[index] for result in simulation_result_table[1:] if result[index] not in [0.0, ""]]):0.5f}'

        def cal_success(simulation_result_table, index):
            return all([result[index] for result in simulation_result_table[1:] if result[index] not in [0.0, ""]])

        simulation_config_name = self._simulation_file_path.split('/')[-3]

        # ['middleware name', 'service utilization deviation(local)', 'service duration avg(local)', 'service utilization deviation(super)',
        # 'service duration avg(super)', 'scenario duty ratio(local)', 'scenario success(local)', 'scenario duty ratio(super)', 'scenario success(super)'])
        total_service_utilization_deviation_avg = cal_avg(
            simulation_result_table, 1)
        total_service_duration_avg = cal_avg(simulation_result_table, 2)
        total_super_service_utilization_deviation_avg = cal_avg(
            simulation_result_table, 3)
        total_super_service_duration_avg = cal_avg(simulation_result_table, 4)
        total_scenario_duty_ratio_avg = cal_avg(simulation_result_table, 5)
        total_scenario_success = cal_success(simulation_result_table, 6)
        total_super_scenario_duty_ratio_avg = cal_avg(
            simulation_result_table, 7)
        total_super_scenario_success = cal_success(simulation_result_table, 8)
        wr.writerow([])
        wr.writerow(['middleware name', 'total service utilization deviation(local)', 'total service duration avg(local)', 'total service utilization deviation(super)',
                     'total service duration avg(super)', 'total scenario duty ratio(local)', 'total scenario success(local)', 'total scenario duty ratio(super)', 'total scenario success(super)'])
        wr.writerow([simulation_config_name,
                     total_service_utilization_deviation_avg,
                     total_service_duration_avg,
                     total_super_service_utilization_deviation_avg,
                     total_super_service_duration_avg,
                     total_scenario_duty_ratio_avg,
                     total_scenario_success,
                     total_super_scenario_duty_ratio_avg,
                     total_super_scenario_success])
        f.close()
        return csv_file_path

    @exception_wrapper
    def show_simulation_result(self, user_interaction: bool = True):
        csv_file_path = self.export_simulation_result()

        while user_interaction:
            for i, middleware in enumerate(self._middleware_list):
                print(f'{i:<2}: {middleware._name}')
            else:
                user_input = int(input('select middleware: ') or -1)

            if user_input == -1:
                print(
                    f'please select correct middleware number. (0 ~ {len(self._middleware_list) - 1})')
            middleware = self._middleware_list[user_input]

            self.print_simulation_result(middleware, user_interaction)
        else:
            f = open(csv_file_path, 'a')
            wr = csv.writer(f)
            wr.writerow([])
            wr.writerow(['==== middleware_results ===='])
            wr.writerow([])

            for middleware in self._middleware_list:
                middleware_result_table = self.print_simulation_result(
                    middleware, user_interaction)
                wr.writerows(middleware_result_table)


if __name__ == '__main__':
    pass
