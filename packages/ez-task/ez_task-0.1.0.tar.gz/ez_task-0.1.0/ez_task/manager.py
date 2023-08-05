from typing import Callable, List, Tuple
import multiprocessing as mp
from .types.health_check import HealthCheck
from .task import Task
class TaskManager():

    def __init__(self, daemon=True, use_gatherer=True, default_start_method=None) -> None:
        """
        Initializes instance of TaskManager
        TaskManager will automatically close all subordinate Tasks on __exit__ call

        Parameters
        ----------
        target : Callable
            Any top level python function or callable class attribute
        daemon: bool (default True)
            Default setting inheritied by subordinate Tasks
        use_gatherer: bool (default True)
            Default setting inheritied by subordinate Tasks
            Controls whether subordinate Tasks utilize threaded ez_task.gatherer.Gatherer
        default_start_method: string (default None)
            Sets the default start method ('fork', 'spawn', 'forkserver') for subordinate Tasks
            Can be overridden for specific Tasks on definition

        Returns
        -------
        TaskManager
            An instance of ez_task.manager.TaskManager 
        """
        self._task_list: List[Task] = []
        self.daemon: bool = daemon
        self.use_gatherer: bool = use_gatherer
        if not default_start_method:
            self.default_start_method = mp.get_start_method()
        else:
            self.default_start_method = default_start_method

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        try:
            self.terminate_tasks()
        except Exception as e:
            print(e)
            return

    def define_task(self, target: Callable, start_method=None) -> Task:
        """
        Creates a managed instance of the Task object.

        A Task will call the target parameter whenever Task.run is invoked

        Parameters
        ----------
        target : Callable
            Any top level python function or callable class attribute
        start_method: str (default None)
            Sets the start method ('fork', 'spawn', 'forkserver') of defined Task

        Returns
        -------
        Task
            An instance of ez_task.task.Task 

        """
        task = self._add_task(target, start_method)
        return task

    def define_task_set(self, *targets: Tuple[Callable], start_method=None) -> List[Task]:
        """
        Creates multiple managed instances of the Task object and sends a dummy health check to ready the pipe.
        Preferable if Tasks need to be available in the future with low latency

        A Task will call the target parameter whenever Task.run is invoked

        Parameters
        ----------
        targets : Tuple[Callable]
            A list of any top level python function or callable class attribute
        start_method: str (default None)
            Sets the start method ('fork', 'spawn', 'forkserver') of defined Tasks

        Returns
        -------
        Tuple[Task]
            An instance of ez_task.task.Task 

        """
        tasks: List[Task] = []
        for target in targets:
            task = self._add_task(target, start_method)
            tasks.append(task)
        
        return (*tasks,)

    def terminate_tasks(self) -> None:
        """
        Terminates all managed Task instances along with their respective resources.
        Returns
        -------
        None
        """
        for task in self._task_list:
            task.__exit__(None, None, None)
        

    def _add_task(self, target: Callable, start_method_override) -> Task:
        """
        <Private> Initializes task and adds it to manager self._task_list

        Parameters
        ----------
        target : Callable
            Any top level python function or callable class attribute
        start_method_override: string
            Override's manager's self.default_start_method for this Task

        Returns
        -------
        Task
            An instance of ez_task.task.Task 

        """
        start_method = start_method_override
        if not start_method:
            start_method = self.default_start_method

        task: Task = Task(target, daemon=self.daemon, manager=self, use_gatherer=self.use_gatherer, start_method=start_method)
        self._task_list.append(task)
        task._blocking_health_check()
        task.run(HealthCheck())
        task.get_result()
        return task

        




    



