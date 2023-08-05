"""
Handles file transfer via the `rsync` protocol
"""

from remotemanager.transport.transport import Transport


class rsync(Transport):
    """
    Class for `rsync` protocol

    Args:
        checksum (bool):
            Adds checksum arg, which if True will add --checksum flag to
            parameters
    """
    def __init__(self,
                 *args,
                 **kwargs):

        super().__init__(*args, **kwargs)

        # flags can be exposed, to utilise their flexibility
        flags = kwargs.pop('flags', 'auv')
        self.flags = flags

        if kwargs.get('checksum', False):
            print('adding checksum to rsync')
            self.flags += '--checksum'

        self._logger.info('created new rsync transport')

        self._cmd = 'rsync {flags} --rsync-path="mkdir -p {remote_dir} && ' \
                    'rsync" {primary} {secondary}'

    @property
    def cmd(self):
        base = self._cmd.format(flags=self.flags,
                                primary='{primary}',
                                secondary='{secondary}',
                                remote_dir='{remote_dir}')
        self._logger.debug(f'returning semi-formatted cmd: "{base}"')
        return base
