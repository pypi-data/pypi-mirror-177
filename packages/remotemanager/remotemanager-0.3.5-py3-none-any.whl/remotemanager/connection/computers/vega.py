from remotemanager.connection.computers.base import BaseComputer, \
    required, optional
from remotemanager.utils import safe_divide


class Vega(BaseComputer):
    """
    example class for connecting to a remote computer

    initial info used from vega docs
    https://en-vegadocs.vega.izum.si/slurm/

    completed using vega.py from BigDFT, 221114
    """

    def __init__(self, **kwargs):

        # default host to vega's IP
        if 'host' not in kwargs:
            kwargs['host'] = 'login.vega.izum.si'

        # initialise the base URL
        super().__init__(**kwargs)

        # script housekeeping
        self.submitter = 'sbatch'
        self.shebang = '#!/bin/bash -l'
        self.pragma = '#SBATCH'

        # resources
        self.mpi = required('--ntasks')
        self.omp = required('--cpus-per-task')
        self.time = required('--time')

        self.nodes = optional('--nodes')
        self.jobname = optional('--job-name', 'remote_run')
        self.outfile = optional('--output')
        self.errfile = optional('--error')
        self.gpus = optional('--gres gpus')
        self.queue = optional('--queue')
        self.reservation = optional('--reservation')

        # modules
        self.modules = ['Python/3.10.4-GCCcore-11.3.0']
        self.modules_gpu = []

    @property
    def cpu_node(self):
        return {'cores_per_node': 256,
                'partition': 'cpu'}

    @property
    def gpu_node(self):
        return {'cores_per_node': 128,
                'gpus_per_node': 4,
                'partition': 'gpu'}

    def resources_block(self, **kwargs):
        self.update_resources(**kwargs)

        self.enable_gpu = kwargs.get('gpu', False)

        if not self.enable_gpu and self.gpus:
            self.enable_gpu = True

        if not self.valid:
            raise RuntimeError(f'missing required arguments: {self.missing}')

        node_specs = self.gpu_node if self.enable_gpu else self.cpu_node

        cores_per_node = node_specs['cores_per_node']
        nodes = safe_divide(self.mpi.value * self.omp.value, cores_per_node)

        ### safeguards ###
        # limit OMP to cores_per_machine
        if self.omp.value > cores_per_node:
            raise ValueError(f'OMP={self.omp.value} is larger than the number of '
                             f'cores per node ({cores_per_node})')
        # limit GPU request to 4 per node
        if self.gpus and self.gpus.value > node_specs['gpus_per_node']:
            raise ValueError(f'gpus={self.gpus.value} is larger than the number of '
                             f'gpus per node ({node_specs["gpus_per_node"]})')

        output = []
        for k, v in self.argument_dict.items():
            if k in ['nodes', 'gpus']:
                continue

            if v:
                output.append(f'{self.pragma} {v.flag}={v.value}')

        if self.enable_gpu:
            gpus = self.gpus.value if self.gpus else node_specs["gpus_per_node"]

            output.append(f'{self.pragma} --gres=gpu:{gpus * nodes}')
            output.append(f'{self.pragma} --partition=gpu')

        output.append(f'{self.pragma} --nodes={nodes}')

        return output

    def modules_block(self):
        if self.enable_gpu:
            modules = self.modules_gpu
        else:
            modules = self.modules
        return ['\nmodule purge'] + [f'module load {m}' for m in modules]

    def script(self,
               **kwargs) -> str:
        """
        Takes job arguments and produces a valid jobscript

        Returns:
            (str):
                script
        """
        self.enable_gpu = False  # default off
        script = [self.shebang]

        script += self.resources_block(**kwargs)
        script += self.modules_block()

        if self.enable_gpu:
            try:
                script.append(self.extra_gpu)
            except AttributeError:
                script.append(self.extra)

        elif hasattr(self, 'extra') and self.extra is not None:
            script.append(self.extra)

        return '\n'.join(script)
