from big_thing_py.tests.tools.simulator import *
from big_thing_py.utils.file_util import *

import configparser
import random
import requests
import shutil
import toml

FUNCTION_TEMPLATE = '''\
def function_%s() -> int:
    SOPLOG_DEBUG(f'function {get_current_function_name()} run... return %s')
    time.sleep(%s)
    return %s
'''
SUPER_FUNCTION_TEMPLATE = '''\
def super_function_%s(self, key) -> int:
    SOPLOG_DEBUG(
        f'super function {get_current_function_name()} run...')
    results = []

    %s

    result_sum = 0
    for result in results:
        for subresult in result:
            return_value = subresult['return_value']
            result_sum += return_value

    return result_sum   
'''
SUBFUNCTION_TEMPLATE = '''\
results += [self.req(key, subfunction_name='%s', tag_list=%s, arg_list=(), service_type=SoPServiceType.FUNCTION, policy=SoPPolicy.%s)]'''
FUNCTION_INSTANCE_TEMPLATE = '''\
SoPFunction(func=%s, return_type=SoPType.INTEGER, tag_list=[%s], arg_list=[], exec_time=%s, energy=%s)'''
SUPER_FUNCTION_INSTANCE_TEMPLATE = '''\
SoPSuperFunction(func=self.%s, return_type=SoPType.INTEGER, tag_list=[%s], arg_list=[], exec_time=%s, energy=%s)'''
THING_TEMPLATE = '''\
from big_thing_py.big_thing import *

import time
import random
import argparse

%s

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='%s', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='%s', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=%s, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=%s, help="refresh_cycle")
    parser.add_argument("--refresh_cycle", '-rc', action='store', type=int,
                        required=False, default=%s, help="refresh_cycle")
    parser.add_argument("--append_mac", '-am', action='%s',                         # store_true, store_false
                        required=False, help="append mac address to thing name")
    args, unknown = parser.parse_known_args()
    return args


def main():
    args = arg_parse()
    function_list = \\
        [%s]
    value_list = []
    thing = SoPBigThing(name=args.name, service_list=function_list + value_list,
                        alive_cycle=args.alive_cycle, is_super=False, is_parallel=%s, ip=args.host, port=args.port,
                        ssl_ca_path=None, ssl_enable=None, append_mac_address=False, log_name='%s')
    thing.setup(avahi_enable=False)
    thing.run()


if __name__ == '__main__':
    main()

'''
SUPER_THING_TEMPLATE = '''\
from big_thing_py.super_thing import *

import argparse


class SoPBasicSuperThing(SoPSuperThing):

    def __init__(self, name: str = None, service_list: List[SoPService] = [], alive_cycle: float = 60, is_super: bool = False, is_parallel: bool = True,
                 ip: str = None, port: int = None, ssl_ca_path: str = None, ssl_enable: bool = None, refresh_cycle: float = 10, append_mac_address: bool = True, log_name=None):
        super_function_list = \\
            [%s]

        super().__init__(name=name, service_list=service_list + super_function_list, alive_cycle=alive_cycle, is_super=True,
                         is_parallel=is_parallel, ip=ip, port=port, ssl_ca_path=ssl_ca_path, ssl_enable=ssl_enable, refresh_cycle=refresh_cycle, append_mac_address=append_mac_address, log_name=log_name)

%s

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", '-n', action='store', type=str,
                        required=False, default='%s', help="thing name")
    parser.add_argument("--host", '-ip', action='store', type=str,
                        required=False, default='%s', help="host name")
    parser.add_argument("--port", '-p', action='store', type=int,
                        required=False, default=%s, help="port")
    parser.add_argument("--alive_cycle", '-ac', action='store', type=int,
                        required=False, default=%s, help="alive cycle")
    parser.add_argument("--refresh_cycle", '-rc', action='store', type=int,
                        required=False, default=%s, help="refresh cycle")
    parser.add_argument("--auto_scan", '-as', action='%s',
                        required=False, help="middleware auto scan enable")
    parser.add_argument("--log", action='store_true',
                        required=False, help="log enable")
    parser.add_argument("--append_mac", '-am', action='store_true',                         # store_true, store_false
                        required=False, help="append mac address to thing name")
    args, unknown = parser.parse_known_args()

    return args


def generate_thing(args):
    super_thing = SoPBasicSuperThing(name=args.name, ip=args.host, port=args.port, is_super=True, is_parallel=%s, ssl_ca_path=None, ssl_enable=None,
                                     alive_cycle=args.alive_cycle, refresh_cycle=args.refresh_cycle, append_mac_address=False, log_name='%s')
    return super_thing


if __name__ == '__main__':
    args = arg_parse()
    thing = generate_thing(args)
    thing.setup(avahi_enable=args.auto_scan)
    thing.run()

'''
SCENARIO_TEMPLATE = '''\
[%s]
loop(%s) {
%s}
'''


class SimulationGenerator:
    def __init__(self, simulation_name: str = None, middleware_tree_config_path: str = None, simulation_config_path: str = None, name_file_path: str = None) -> None:
        self.middleware_tree_config = None
        self.simulation_config = None
        self._simulation_name = simulation_name
        self._name_file_path = name_file_path

        self.tag_names_pool = []
        self.function_names_pool = []
        self.thing_names_pool = []

        self.generated_middlewares = []
        self.generated_local_functions: List[dict] = []
        self.generated_super_functions: List[dict] = []
        self.generated_local_things = []
        self.generated_super_things = []
        self.geterated_scenarios = []
        self._simulation_code = None

        self.init(middleware_tree_config_path, simulation_config_path)

    def init(self, middleware_tree_config_path: str = None, simulation_config_path: str = None):
        self.middleware_tree_config = json_file_read(
            middleware_tree_config_path)
        self.simulation_config = self.load_config_file(
            simulation_config_path)

    def append_indent(self, code: str, indent: int = 1):
        code_lines = code.split('\n')
        tabs = '    ' * indent
        for i, code_line in enumerate(code_lines):
            code_lines[i] = tabs + code_lines[i] + '\n'
        return ''.join(code_lines)

    def generate_simulation_code(self):
        self.tag_names_pool = self.generate_random_words(
            int(self.simulation_config['service']['tag_type_num']))
        self.function_names_pool = self.generate_random_words(
            int(self.simulation_config['service']['service_type_num']) * 5)
        self.thing_names_pool = self.generate_random_words(1000)

        self.generated_middlewares: List[dict] = sorted(
            self.get_whole_middleware_list(), key=lambda x: x['level'], reverse=True)
        self.generated_local_functions = self.generate_local_function()
        self.generated_local_things, self.generated_super_things = self.generate_thing()
        self.geterated_local_scenarios, self.geterated_super_scenarios = self.generate_scenario()
        self.geterated_scenarios = self.geterated_local_scenarios + \
            self.geterated_super_scenarios

        self._simulation_code = dict(name=self._simulation_name,
                                     simulation=[dict(level=middleware['level'],
                                                      event_type=EventType.MIDDLEWARE_RUN.value.lower(),
                                                      timestamp=0,
                                                      name=middleware['name'],
                                                      host=middleware['host'],
                                                      port=middleware['port'],
                                                      parent_host=middleware.get(
                                         'parent_host', None),
                                         parent_port=middleware.get(
                                         'parent_port', None),
                                         web_socket_port=middleware['web_socket_port'],
                                         ssl_port=middleware['ssl_port'],
                                         ssl_web_socket_port=middleware['ssl_web_socket_port'],
                                         local_server_port=middleware['local_server_port'],
                                         is_local=False,
                                         remote_user=middleware['user'],
                                         remote_host=middleware['host'],
                                         remote_port=middleware['ssh_port'],
                                         remote_password=middleware['password'],
                                         middleware_path=middleware['middleware_path'],
                                         middleware_out_path=middleware['middleware_config_path']) for middleware in self.generated_middlewares] +
                                     [dict(level=thing['level'],
                                           event_type=EventType.THING_RUN.value.lower(),
                                           timestamp=0,
                                           name=thing['name'],
                                           host=thing['host'],
                                           port=thing['port'],
                                           raw_thing_file_path=thing['raw_thing_file_path'],
                                           thing_file_path=thing['thing_file_path'],
                                           is_super=thing['is_super'],
                                           is_local=thing['is_local'],
                                           is_parallel=thing['is_parallel'],
                                           remote_user=thing['user'],
                                           remote_host=thing['host'],
                                           remote_port=thing['ssh_port'],
                                           remote_password=thing['password'],
                                           args=[]) for thing in self.generated_local_things + self.generated_super_things] +
                                     [dict(event_type='delay',
                                           duration=5)] +
                                     [dict(level=scenario['middleware']['level'],
                                           event_type=EventType.SCENARIO_ADD.value.lower(),
                                           timestamp=0,
                                           name=scenario['name'],
                                           host=scenario['middleware']['host'],
                                           port=scenario['middleware']['port'],
                                           raw_scenario_file_path=scenario['raw_scenario_file_path'],
                                           scenario_file_path=scenario['scenario_file_path'],
                                           is_super=scenario['is_super'],
                                           is_local=scenario['is_local'],
                                           remote_user=scenario['middleware']['user'],
                                           remote_host=scenario['middleware']['host'],
                                           remote_port=scenario['middleware']['ssh_port'],
                                           remote_password=scenario['middleware']['password'],
                                           period=scenario['period'],
                                           first_service=scenario['first_service'],
                                           last_service=scenario['last_service'],
                                           service_num=scenario['service_num']) for scenario in self.geterated_super_scenarios + self.geterated_local_scenarios] +
                                     [dict(level=scenario['middleware']['level'],
                                           event_type=EventType.SCENARIO_RUN.value.lower(),
                                           timestamp=0,
                                           name=scenario['name'],
                                           host=scenario['middleware']['host'],
                                           port=scenario['middleware']['port'],
                                           raw_scenario_file_path=scenario['raw_scenario_file_path'],
                                           scenario_file_path=scenario['scenario_file_path'],
                                           is_super=scenario['is_super'],
                                           is_local=scenario['is_local'],
                                           remote_user=scenario['middleware']['user'],
                                           remote_host=scenario['middleware']['host'],
                                           remote_port=scenario['middleware']['ssh_port'],
                                           remote_password=scenario['middleware']['password'],
                                           ) for scenario in self.geterated_local_scenarios + self.geterated_super_scenarios] +
                                     [dict(event_type='delay',
                                           duration=float(f"{max([scenario['period'] for scenario in self.geterated_scenarios]):.2f}") / 1000 * 3)] +
                                     [dict(level=middleware['level'],
                                           event_type=EventType.MIDDLEWARE_KILL.value.lower(),
                                           timestamp=0,
                                           name=middleware['name'],
                                           host=middleware['host'],
                                           port=middleware['port'],
                                           parent_host=middleware.get(
                                         'parent_host', None),
                                         parent_port=middleware.get(
                                         'parent_port', None),
                                         web_socket_port=middleware['web_socket_port'],
                                         ssl_port=middleware['ssl_port'],
                                         ssl_web_socket_port=middleware['ssl_web_socket_port'],
                                         local_server_port=middleware['local_server_port'],
                                         is_local=False,
                                         remote_user=middleware['user'],
                                         remote_host=middleware['host'],
                                         remote_port=middleware['ssh_port'],
                                         remote_password=middleware['password'],
                                         middleware_path=middleware['middleware_path'],
                                         middleware_out_path=middleware['middleware_config_path']) for middleware in self.generated_middlewares] +
                                     [dict(level=thing['level'],
                                           event_type=EventType.THING_KILL.value.lower(),
                                           timestamp=0,
                                           name=thing['name'],
                                           host=thing['host'],
                                           port=thing['port'],
                                           raw_thing_file_path=thing['raw_thing_file_path'],
                                           thing_file_path=thing['thing_file_path'],
                                           is_super=thing['is_super'],
                                           is_local=thing['is_local'],
                                           remote_user=thing['user'],
                                           remote_host=thing['host'],
                                           remote_port=thing['ssh_port'],
                                           remote_password=thing['password'],
                                           args=[]) for thing in self.generated_local_things + self.generated_super_things])

        sim_code_path = f'{self._simulation_name}/simulation_code.json'
        json_file_write(sim_code_path, self._simulation_code)
        return sim_code_path

    def load_config_file(self, path: str):
        if path:
            config = toml.load(path)
            # config.read(path)
            return config
        else:
            raise SOPTEST_LOG_DEBUG(f'File not found: {path}', -1)

    def generate_random_words(self, word_num: int = None, word_len: tuple = None, custom_words_file: List[str] = None) -> List[str]:
        picked_words = []
        whole_words = []
        ban_word_list = ['if', 'else', 'and', 'or', 'loop', 'wait_until', 'msec',
                         'sec', 'min', 'hour', 'day', 'month', 'all', 'single', 'random']

        if not custom_words_file:
            response = requests.get(
                "https://www.mit.edu/~ecprice/wordlist.10000")
            whole_words = response.content.splitlines()
            for word in ban_word_list:
                try:
                    whole_words.remove(word)
                except Exception:
                    pass
        else:
            file: List[str] = read_file(custom_words_file)
            whole_words = [line.strip() for line in file]
            return whole_words

        while len(picked_words) < word_num:
            picked_word = random.choice(whole_words)
            if picked_word in picked_words:
                continue

            if isinstance(picked_word, bytes):
                picked_word = picked_word.decode('utf-8')

            if word_len:
                if len(picked_word) >= word_len[0] and len(picked_word) <= word_len[1]:
                    picked_words.append(picked_word)
            else:
                picked_words.append(picked_word)

        return picked_words

    def generate_basic_function_info(self, function_config: dict):
        tag_per_function = random.randint(int(function_config['min_tag_per_service']), int(
            function_config['max_tag_per_service']))
        energy = random.randint(
            int(function_config['min_energy']), int(function_config['max_energy']))
        execute_time_in_code = random.randint(int(function_config['min_execute_time']), int(
            function_config['max_execute_time']))
        execute_time = execute_time_in_code - \
            random.randint(
                int(function_config['min_execute_time_margin']), execute_time_in_code)
        return_value = random.randint(0, 1000)
        function_name = random.choice(self.function_names_pool)

        return tag_per_function, energy, execute_time_in_code, execute_time, return_value, function_name

    def generate_super_function_info(self, picked_local_functions: List[dict], function_config: dict):
        tag_per_function = random.randint(int(function_config['min_tag_per_service']), int(
            function_config['max_tag_per_service']))

        super_energy = 0
        super_execute_time = 0
        for local_function in picked_local_functions:
            super_energy += local_function['energy']
            super_execute_time += local_function['execute_time']

        function_name = f'{random.choice(self.function_names_pool)}'

        return tag_per_function, super_energy, super_execute_time, function_name

    def generate_local_function(self) -> None:
        function_config = self.simulation_config['service']
        function_type_num = int(
            self.simulation_config['service']['service_type_num'])

        local_functions = []
        for _ in range(function_type_num):
            # 중복된 함수이름으로 생성되는 경우 다시 생성
            while True:
                tag_per_function, energy, execute_time_in_code, execute_time, return_value, function_name = self.generate_basic_function_info(
                    function_config)
                if function_name not in [function['name'] for function in local_functions]:
                    break

            # function name, return value(int), return value, execute time(reduced), return value
            tags = list(
                set(random.sample(self.tag_names_pool, tag_per_function)))
            tag_code = ', '.join([f'SoPTag("{tag}")' for tag in tags])
            local_function_instance_code = FUNCTION_INSTANCE_TEMPLATE % (f'function_{function_name}',
                                                                         tag_code,
                                                                         execute_time_in_code,
                                                                         energy)
            local_function_code = FUNCTION_TEMPLATE % (
                function_name, return_value, execute_time / 1000, return_value)
            local_functions.append(
                dict(tags=tags,
                     name=function_name,
                     energy=energy,
                     execute_time=execute_time_in_code,
                     code=local_function_code,
                     instance_code=local_function_instance_code))

        return local_functions

    def generate_super_function(self, local_functions: List[dict]) -> None:

        def generate_subfunction_req_lines(picked_local_functions: List[dict]) -> List[str]:
            req_lines = []
            picked_subfunction_list = []

            for picked_local_function in picked_local_functions:
                picked_subfunction = picked_local_function
                picked_tag_list = random.sample(picked_subfunction['tags'], random.randint(
                    1, len(picked_subfunction['tags'])))
                policy = random.choice(['ALL', 'SINGLE'])
                req_lines.append(SUBFUNCTION_TEMPLATE % (
                    f"function_{picked_subfunction['name']}", picked_tag_list, policy))
                picked_subfunction_list.append(picked_subfunction['name'])

            return req_lines

        function_config = self.simulation_config['service']
        super_function_type_num = int(
            self.simulation_config['service']['super_service_type_num'])
        subfunction_per_super_function1 = random.randint(int(self.simulation_config['service']['min_subservice_per_super_service']),
                                                         int(self.simulation_config['service']['max_subservice_per_super_service']))
        super_functions = []
        for _ in range(super_function_type_num):
            while True:
                subfunction_per_super_function2 = random.randint(
                    1, min(len(local_functions), subfunction_per_super_function1))
                picked_local_functions = random.sample(
                    local_functions, subfunction_per_super_function2)
                tag_per_function, energy, execute_time, function_name = self.generate_super_function_info(
                    picked_local_functions, function_config)
                if function_name not in [function['name'] for function in super_functions]:
                    break

            req_lines = generate_subfunction_req_lines(picked_local_functions)

            # super function name, req lines
            tags = list(
                set(random.sample(self.tag_names_pool, tag_per_function)))
            tag_code = ', '.join([f'SoPTag("{tag}")' for tag in tags])
            super_function_instance_code = SUPER_FUNCTION_INSTANCE_TEMPLATE % (f'super_function_{function_name}',
                                                                               tag_code,
                                                                               execute_time,
                                                                               energy)
            req_lines_code = '\n\t'.join(req_lines)
            super_function_code = SUPER_FUNCTION_TEMPLATE % (
                function_name, req_lines_code)
            # write_file('./test', super_function_code)
            super_functions.append(
                dict(tags=tags,
                     name=f'{function_name}',
                     energy=energy,
                     execute_time=execute_time,
                     code=super_function_code,
                     instance_code=super_function_instance_code))

        return super_functions

    def get_whole_middleware_list(self):

        def get_child_middleware_list(whole_middleware_list: list, middleware: dict):
            child_middleware_list = middleware.get('child_middlewares', None)
            if child_middleware_list:
                for child_middleware in child_middleware_list:
                    child_middleware['parent_host'] = middleware['host']
                    child_middleware['parent_port'] = middleware['port']
                    whole_middleware_list.append(child_middleware)
                    get_child_middleware_list(
                        whole_middleware_list, child_middleware)
            else:
                return

        whole_middleware_list = []
        for middleware in self.middleware_tree_config['middleware_tree']:
            middleware['parent_host'] = None
            middleware['parent_port'] = None
            whole_middleware_list.append(middleware)
            get_child_middleware_list(whole_middleware_list, middleware)
        return whole_middleware_list

    def generate_local_thing(self, thing_code_path: str, thing_config: dict):
        thing_list = []
        local_thing_num = int(thing_config['thing_type_num'])
        is_parallel = True
        new_line = '\n'
        tab = '\t'

        for middleware in self.generated_middlewares:
            for i in range(local_thing_num):
                while True:
                    picked_thing_name = random.choice(self.thing_names_pool)
                    picked_middleware = middleware
                    picked_thing_name_with_level_index = f'{picked_thing_name}_level{picked_middleware["level"]}_{i}'.replace(
                        ' ', '_')
                    if picked_thing_name_with_level_index not in [thing['name'] for thing in thing_list]:
                        break

                function_num = random.randint(int(thing_config['min_service_per_thing']),
                                              int(thing_config['max_service_per_thing']))
                picked_functions = random.sample(
                    self.generated_local_functions, k=function_num)
                raw_thing_file_path = f'{thing_code_path}/{picked_thing_name_with_level_index}.py'
                thing_file_path = f'~/Workspace/{self._simulation_name}/generated_local_things/{picked_thing_name_with_level_index}.py'

                local_function_code = '\n'.join(
                    [function['code'] for function in picked_functions])
                local_function_list_code = ',\n\t\t'.join(
                    [function['instance_code'] for function in picked_functions])
                # name, host name, port, alive cycle, refresh cycle, append mac, function list, is_super
                thing_code = THING_TEMPLATE % (local_function_code,
                                               picked_thing_name_with_level_index,
                                               picked_middleware['host'],
                                               picked_middleware['port'],
                                               60,
                                               60,
                                               'store_true',
                                               local_function_list_code,
                                               is_parallel,
                                               f'./log/{picked_thing_name_with_level_index}.log')
                thing = dict(level=picked_middleware['level'],
                             name=picked_thing_name_with_level_index,
                             middleware_name=picked_middleware['name'],
                             host=picked_middleware['host'],
                             port=picked_middleware['port'],
                             user=picked_middleware['user'],
                             password=picked_middleware['password'],
                             ssh_port=picked_middleware['ssh_port'],
                             is_super=False,
                             is_local=False,
                             raw_thing_file_path=raw_thing_file_path,
                             thing_file_path=thing_file_path,
                             args=[],
                             service_list=picked_functions,
                             is_parallel=is_parallel,
                             code=thing_code)
                thing_list.append(thing)
                picked_middleware['things'].append(thing)
                write_file(raw_thing_file_path, thing_code)
                SOPLOG_DEBUG(
                    f'''middleware_name: {picked_middleware['name']}, thing_name: {picked_thing_name_with_level_index}, {new_line + tab} service_list: {', '.join([f"service_name: {service['name']}, execute_time: {service['execute_time']}, energy: {service['energy']}" for service in picked_functions])}''')

        return thing_list

    def generate_super_thing(self, thing_code_path: str, local_function_pool: list, thing_config: dict):
        super_thing_list = []
        super_thing_num = int(thing_config['super_thing_type_num'])
        is_parallel = True

        for i in range(super_thing_num):
            while True:
                picked_super_thing_name = random.choice(self.thing_names_pool)
                picked_middleware = self.generated_middlewares[0]
                picked_super_thing_name_with_level_index = f'super_{picked_super_thing_name}_level{picked_middleware["level"]}_{i}'.replace(
                    ' ', '_')
                if picked_super_thing_name_with_level_index not in [thing['name'] for thing in super_thing_list]:
                    self.generated_super_functions = self.generate_super_function(
                        local_function_pool)
                    break

            super_function_num = random.randint(int(thing_config['min_service_per_thing']),
                                                int(thing_config['max_service_per_thing']))

            picked_super_functions = random.sample(
                self.generated_super_functions, k=super_function_num)

            # super thing only exist in root_middleware
            picked_middleware = self.generated_middlewares[0]
            raw_thing_file_path = f'{thing_code_path}/{picked_super_thing_name_with_level_index}.py'
            thing_file_path = f'~/Workspace/{self._simulation_name}/generated_super_things/{picked_super_thing_name_with_level_index}.py'

            super_function_list_code = ',\n\t\t\t'.join(
                [super_function['instance_code'] for super_function in picked_super_functions])
            super_function_code = self.append_indent('\n'.join(
                [super_function['code'] for super_function in picked_super_functions]).replace('\n', '\t\n')).replace('\t', '    ')
            # write_file('./test.py', super_function_list_code)
            # name, host name, port, alive cycle, refresh cycle, append mac, function list, is_super
            thing_code = SUPER_THING_TEMPLATE % (super_function_list_code,
                                                 super_function_code,
                                                 picked_super_thing_name_with_level_index,
                                                 picked_middleware['host'],
                                                 picked_middleware['port'],
                                                 60,
                                                 60,
                                                 'store_true',
                                                 is_parallel,
                                                 f'./log/{picked_super_thing_name_with_level_index}.log')
            new_line = '\n'
            tab = '\t'
            write_file(raw_thing_file_path, thing_code)
            SOPLOG_DEBUG(
                f'''middleware_name: {picked_middleware['name']}, thing_name: {picked_super_thing_name_with_level_index}, {new_line + tab} service_list: {', '.join([f"service_name: {service['name']}, execute_time: {service['execute_time']}, energy: {service['energy']}" for service in picked_super_functions])}''')
            super_thing = dict(level=picked_middleware['level'],
                               name=picked_super_thing_name_with_level_index,
                               middleware_name=picked_middleware['name'],
                               host=picked_middleware['host'],
                               port=picked_middleware['port'],
                               user=picked_middleware['user'],
                               password=picked_middleware['password'],
                               ssh_port=picked_middleware['ssh_port'],
                               is_super=True,
                               is_local=False,
                               raw_thing_file_path=raw_thing_file_path,
                               thing_file_path=thing_file_path,
                               args=[],
                               service_list=picked_super_functions,
                               is_parallel=is_parallel,
                               code=thing_code)
            super_thing_list.append(super_thing)
            picked_middleware['things'].append(super_thing)

        # self.mapping_thing(thing_list)
        return super_thing_list

    def generate_thing(self):
        thing_config = self.simulation_config['thing']

        local_thing_code_path = f'{os.getcwd()}/{self._simulation_name}/local_things'
        super_thing_code_path = f'{os.getcwd()}/{self._simulation_name}/super_things'

        if os.path.exists(local_thing_code_path):
            shutil.rmtree(local_thing_code_path)
        os.makedirs(local_thing_code_path, exist_ok=True)
        if os.path.exists(super_thing_code_path):
            shutil.rmtree(super_thing_code_path)
        os.makedirs(super_thing_code_path, exist_ok=True)

        local_thing_list = self.generate_local_thing(
            local_thing_code_path, thing_config)

        local_function_pool = []
        for local_thing in local_thing_list:
            for function_service in local_thing['service_list']:
                if function_service in local_function_pool:
                    continue
                local_function_pool.append(function_service)
        # local_function_pool = list(local_function_pool)

        super_thing_list = self.generate_super_thing(
            super_thing_code_path, local_function_pool, thing_config)

        return local_thing_list, super_thing_list

    def mapping_thing(self, thing_list: List[dict]):
        for thing in thing_list:
            print(thing)

    def generate_local_scenario(self, scenario_code_path: str, scenario_config: dict):
        local_scenario_list = []

        for picked_middleware in self.generated_middlewares:
            # scenario_num = random.randint(int(scenario_config['min_scenario_per_middleware']),
            #                               int(scenario_config['max_scenario_per_middleware']))
            scenario_num = int(scenario_config['scenario_type_num'])

            for i in range(scenario_num):
                # scenario_period = random.randint(int(scenario_config['min_scenario_period']),
                #                                  int(scenario_config['max_scenario_period']))
                thing_list = picked_middleware['things']
                service_list = []
                for thing in thing_list:
                    if not thing['is_super']:
                        tmp_service_list = thing['service_list']
                        for service in tmp_service_list:
                            service_list.append(service)

                # TODO: determine what to do when the min_scenario_per_middleware is larger than 0
                if (service_list == [] and int(scenario_config['min_scenario_per_middleware']) == 0):
                    continue
                elif (service_list == [] and int(scenario_config['min_scenario_per_middleware']) > 0):
                    # TODO: determine what to do when the min_scenario_per_middleware is larger than 0
                    continue
                    # raise SOPTEST_LOG_DEBUG(
                    #     f'no service in middleware: {picked_middleware["name"]}', -1)

                function_num = random.randint(min([int(scenario_config['min_service_per_scenario']), len(service_list)]),
                                              min([int(scenario_config['max_service_per_scenario']), len(service_list)]))
                picked_functions = random.sample(service_list, function_num)

                scenario_name = f'local_scenario_{picked_middleware["name"]}_{i}'
                raw_scenario_file_path = f'{scenario_code_path}/{scenario_name}.txt'
                # TODO: set root path
                scenario_file_path = f'~/Workspace/{self._simulation_name}/generated_local_scenarios/{scenario_name}.txt'

                function_code = ''
                scenario_period = 0
                first_service = ''
                last_service = ''
                for i, function in enumerate(picked_functions):
                    tag_num = random.randint(1, len(function['tags']))
                    tag_code = f"({f' '.join(random.sample([f'#{tag}' for tag in function['tags']], tag_num))})"
                    function_line_code = f'{tag_code}.function_{function["name"]}()' + \
                        '\n'
                    function_code += function_line_code
                    scenario_period += function['execute_time']
                    if i == 0:
                        first_service = f'function_{function["name"]}'
                    elif i == len(picked_functions) - 1:
                        last_service = f'function_{function["name"]}'
                # scenario period margin
                # TODO: make scenario period margin configurable
                scenario_period += 1000

                scenario_code = (SCENARIO_TEMPLATE % (scenario_name, f'{scenario_period} MSEC',
                                                      self.append_indent(function_code.rstrip())))

                write_file(raw_scenario_file_path, scenario_code)
                local_scenario_list.append(dict(name=scenario_name,
                                                middleware=picked_middleware,
                                                raw_scenario_file_path=raw_scenario_file_path,
                                                scenario_file_path=scenario_file_path,
                                                is_local=False,
                                                is_super=False,
                                                period=scenario_period,
                                                first_service=first_service,
                                                last_service=last_service,
                                                service_num=len(
                                                    picked_functions),
                                                code=scenario_code))

        return local_scenario_list

    def generate_super_scenario(self, scenario_code_path: str, scenario_config: dict):
        super_scenario_list = []
        # TODO: make it random num
        # super_scenario_num = random.randint(int(scenario_config['min_super_scenario_per_middleware']),
        #                                     int(scenario_config['max_super_scenario_per_middleware']))
        super_scenario_num = int(scenario_config['super_scenario_type_num'])

        for i in range(super_scenario_num):
            super_function_num = random.randint(int(scenario_config['min_super_service_per_scenario']),
                                                int(scenario_config['max_super_service_per_scenario']))
            # scenario_period = random.randint(int(scenario_config['min_scenario_period']),
            #                                  int(scenario_config['max_scenario_period']))
            picked_middleware = self.generated_middlewares[0]

            thing_list = picked_middleware['things']
            super_service_list = []
            for thing in thing_list:
                if thing['is_super']:
                    tmp_service_list = thing['service_list']
                    for service in tmp_service_list:
                        super_service_list.append(service)
            super_function_num = random.randint(int(scenario_config['min_super_service_per_scenario']), min(
                super_function_num, len(super_service_list)))

            picked_super_functions = random.sample(
                super_service_list, super_function_num)
            scenario_name = f'super_scenario_{picked_middleware["name"]}_{i}'
            raw_scenario_file_path = f'{scenario_code_path}/{scenario_name}.txt'
            scenario_file_path = f'~/Workspace/{self._simulation_name}/generated_super_scenarios/{scenario_name}.txt'

            function_code = ''
            scenario_period = 0
            first_service = ''
            last_service = ''
            for i, super_function in enumerate(picked_super_functions):
                tag_num = random.randint(1, len(super_function['tags']))
                tag_code = f"({f' '.join(random.sample([f'#{tag}' for tag in super_function['tags']], tag_num))})"
                function_line_code = f'{tag_code}.super_function_{super_function["name"]}()' + \
                    '\n'
                function_code += function_line_code
                scenario_period += super_function['execute_time']
                if i == 0:
                    first_service = f'super_function_{super_function["name"]}'
                elif i == len(picked_super_functions) - 1:
                    last_service = f'super_function_{super_function["name"]}'
            # scenario period margin
            scenario_period += 20000

            scenario_code = (SCENARIO_TEMPLATE % (scenario_name, f'{scenario_period} MSEC',
                                                  self.append_indent(function_code.rstrip())))

            write_file(raw_scenario_file_path, scenario_code)
            super_scenario_list.append(dict(name=scenario_name,
                                            middleware=picked_middleware,
                                            raw_scenario_file_path=raw_scenario_file_path,
                                            scenario_file_path=scenario_file_path,
                                            is_local=False,
                                            is_super=False,
                                            period=scenario_period,
                                            first_service=first_service,
                                            last_service=last_service,
                                            service_num=len(
                                                picked_super_functions),
                                            code=scenario_code))

        return super_scenario_list

    def generate_scenario(self):
        scenario_config = self.simulation_config['scenario']

        local_scenario_code_path = f'{os.getcwd()}/{self._simulation_name}/local_scenarios'
        super_scenario_code_path = f'{os.getcwd()}/{self._simulation_name}/super_scenarios'

        if os.path.exists(local_scenario_code_path):
            shutil.rmtree(local_scenario_code_path)
        os.makedirs(local_scenario_code_path, exist_ok=True)
        if os.path.exists(super_scenario_code_path):
            shutil.rmtree(super_scenario_code_path)
        os.makedirs(super_scenario_code_path, exist_ok=True)

        local_scenario_list = self.generate_local_scenario(
            local_scenario_code_path, scenario_config)
        super_scenario_list = self.generate_super_scenario(
            super_scenario_code_path, scenario_config)

        return local_scenario_list, super_scenario_list
