


import re
import time

from collections import defaultdict as DD

class Script:
    def __init__(self, script, trigger, execute):
        pass

    def run(self, arg):
        pass

    @staticmethod
    def parse_script(script):
        res = locals()
        exec(script, globals(), res) #FIXME: what's it doing with the globals?

        return res

    @staticmethod
    def parse_trigger(trigger):
        # example: cron */5 * * * *
        # example: 1 new result from script1
        new_result = re.match(r'[ ]*([0-9]+)[ ]*new[ ]+result[ ]+from[ ]+([a-zA-Z_][a-zA-Z0-9_]+)', trigger)
        cron_result = re.match(r'cron[ ]*(.*)', trigger)

        if new_result:
            return {
                'type': 'new',
                'num': new_result.group(1),
                'script': new_result.group(2),
            }
        elif cron_result:
            cron = cron_result.group(1)
            #TODO: test cron
            return {
                'type': 'cron',
                'cron': cron,
            }
        else:
            raise ValueError('trigger not recognized')

    @staticmethod
    def parse_execute(execute):
        def parse_single_arg(execution):
            # example: take 1 from script1
            take_result = re.match(r'[ ]*take[ ]*([0-9]+)[ ]*from[ ]+([a-zA-Z_][a-zA-Z0-9_]+)', execution)
            if take_result:
                return {
                    'type': 'take',
                    'num': take_result.group(1),
                    'script': take_result.group(2),
                }
            else:
                raise ValueError('execution not recognized')

        return { arg: parse_single_arg(ex) for arg, ex in execute.items() }


class PythonScript(Script):
    def __init__(self, script, trigger, execute):
        self.script = Script.parse_script(script)
        self.trigger = Script.parse_trigger(trigger)
        self.execute = Script.parse_execute(execute)

        self.dependencies = self._find_dependencies()

    def run(self, arg):
        return self.script['main'](arg)

    def arg(self, from_script, result):

        #TODO: what about multiple ids
        for arg_id, ex in self.execute.items():
            if ex['type'] == 'take' and ex['script'] == from_script:
                return {arg_id: result}

        return {}

    def _find_dependencies(self):

        dependencies = set()
        if self.trigger['type'] == 'new':
            dependencies |= {self.trigger['script']}

        for arg, ex in self.execute.items():
            if ex['type'] == 'take':
                dependencies |= {ex['script']}

        return dependencies


class EyeScript(Script):
    pass



class RuntimeEngine:
    def __init__(self, language='.py'):
        self.script_loader = None
        self.scripts = {}

        try:
            Loader = {
                '.py': PythonScript,
                #'.eye': EyeScript, #TODO: implement me
            }[language]
            self.ScriptLoader = Loader
        except KeyError:
            raise ValueError('language not supported: {}'.format(language))


    def load(self, name, script, trigger, execute):
        if name in self.scripts:
            raise ValueError('value `{}` already exists'.format(name))

        self.scripts[name] = self.ScriptLoader(script, trigger, execute)

    def resolve_dependencies(self):

        available_names = set(self.scripts.keys())

        #1. test if all dependencies for all scripts are valid
        for script_name, script in self.scripts.items():
            for script_dependency in script.dependencies:
                if script_dependency not in available_names:
                    raise ValueError('dependency `{}` not found'.format(script_dependency))

        #2. test for circular dependencies
        #TODO: pirate CLRS

        return {
            "script1" : {
                "script2" : {

                }
            }
        }

    def execute(self):


        db_hack = DD(lambda: {})
        scripts = self.resolve_dependencies()

        def execute_hack(scripts_to_run):
            for script_name, dependencies in scripts_to_run.items():
                arg = db_hack[script_name]
                result = self.scripts[script_name].run(arg)
                for dep in dependencies.keys():
                    new_arg = self.scripts[dep].arg(script_name, result)
                    db_hack[dep] = {
                        **db_hack[dep],
                        **new_arg
                    }

                execute_hack(dependencies)


        while True:
            time.sleep(5) #TODO: remove hack
            execute_hack(scripts)
