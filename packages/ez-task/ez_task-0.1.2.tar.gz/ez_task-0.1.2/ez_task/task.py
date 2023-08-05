from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
import multiprocessing as mp
import traceback
from typing import Any, Callable, List, Tuple
import time
from .types.health_check import HealthCheck
from .gatherer import Gatherer
from . import config
from .types.exceptions.task import TaskRunFailed

class Task():
    def __init__(self, target: Callable, daemon=True, manager = None, use_gatherer=False, start_method=None) -> None:
        """
        Creates an instance of the Task object.

        A Task will call the target parameter whenever Task.run is invoked

        Parameters
        ----------
        target : Callable
            Any top level python function or callable class attribute
        daemon: bool (default True)
            Sets subordinate multiprocessing.Process daemon value
        use_gatherer: bool (default True)
            Controls whether Task utilizes threaded ez_task.gatherer.Gatherer
        start_method: string (default None)
            Sets the start method ('fork', 'spawn', 'forkserver') for subordinate
            multiprocessing.Process 
        Returns
        -------
        Task
            An instance of ez_task.task.Task 

        """
        self.manager = manager 
        connections: Tuple[Connection, Connection] = Pipe()
        self._internal_connection, self._external_connection = connections
        self.gatherer: Gatherer = None
        if (use_gatherer):
            self.gatherer = Gatherer(self._external_connection, self)
        self._target = target
        ctx = mp.get_context(method=start_method)
        self.process: Process = ctx.Process(target=Task._call_loop, args=(self._internal_connection, self._target), daemon=daemon)
        self.process.start()
        self.is_initialized: bool = False
        self._invocations = 0
        self._gathered = 0
        pass

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, tb):
        try:
            self.terminate()
        except:
            traceback.print_exc()
            return

    def respawn(self):
        """
        Attempts to revive a dead process
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            self.terminate()
        except:
            pass
        connections: Tuple[Connection, Connection] = Pipe()
        self._internal_connection, self._external_connection = connections
        self.process: Process = Process(target=Task._call_loop, args=(self._internal_connection, self._target), daemon=True)
        self.process.start()
        self.is_initialized: bool = False

    def __safe_delete_attributes(self):
        attribute_keys = list(self.__dict__.keys())
        for attribute in attribute_keys:
            try:
                delattr(self, attribute)
            except:
                pass

    def is_alive(self):
        try:
            return self.process.is_alive()
        except:
            return False

    def terminate(self) -> None:
        """
        Terminates Task's running process and associated piped connections.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.gatherer:
            self.gatherer.kill()

        try:
            self.process.terminate()
        except:
            pass

        try:
            self.process.kill()
        except:
            pass
        try:
            self.process.join()
        except:
            pass
        try:
            self.process.close()
        except:
            pass
        try:
            self._internal_connection.close()
            self._external_connection.close()
        except:
            pass
        self.__safe_delete_attributes()

    def run(self, *args, **kwargs) -> None:
        """
        Asychronously applies target function upon an number of valid positional arguments.

        Parameters
        ----------
        *args : 
            Accepts any number of positional arguments that are also accepted by specified target function
        **kwargs:
            Accepts any number of keyword arguments
        Returns
        -------
        None
        """
        if self.gatherer:
            self.gatherer.record_invocation()
        self._invocations += 1

        if not args and not kwargs:
            self._external_connection.send(None)
        else:
            self._external_connection.send((args, kwargs))
    
    def _blocking_health_check(self):
        if self.is_alive():
            self.is_initialized = True
            return True
        elif self.is_initialized:
            raise(Exception('Process has terminated'))
        while True:
            healthy = self.is_alive()
            if healthy:
                self.is_initialized = True
                return True
            elif not healthy and self.is_initialized:
                return False
            time.sleep(0.01)
        pass

    def get_result(self) -> Any:
        """
        Returns the result of a previous invocation of Task.run
        Blocks until a result of Task.run is available.

        Parameters
        ----------
        None

        Returns
        -------
        Any :
            The result of invoking the target function upon the positional arguments specified in Task.run invocation
        """

        if (self.gatherer):
            result = self.gatherer.get_result()
            return result
        
        result = self._external_connection.recv()
        self._gathered += 1
        return result

    def get_all_results(self) -> List[Any]:
        """
        
        """
        if self.gatherer:
            return self.gatherer.get_all_results()

        result_list = []
        while self._invocations > self._gathered:
            result = self._external_connection.recv()
            self._gathered += 1
            result_list.append(result)
        return result_list

    @staticmethod
    def _call_loop(conn, function) -> None:
        if config.verbose:
            print(f'EZ-TASK started {mp.current_process()} calling {function}')
        while True:
            res = conn.recv()
            out = Task._call_function(function, res)
            
            if config.verbose:
                start_time = time.time()
            conn.send(out)
            if config.verbose:
                print(f'EZ-TASK result {mp.current_process()} time to write {time.time() - start_time}')

    @staticmethod
    def _call_function(func, res: Any) -> Any:
        try:
            if (isinstance(res, tuple)):
                args, kwargs = res
                if args and len(args) > 0 and isinstance(args[0], HealthCheck):
                        return True
                else:
                    return func(*args, **kwargs)
            else:
                return func()
        except:
            return TaskRunFailed(message=traceback.format_exc())




