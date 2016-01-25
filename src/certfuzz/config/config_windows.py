'''
Created on Feb 9, 2012

@organization: cert.org
'''
import logging
from string import Template

from certfuzz.config.config_base import ConfigBase
from certfuzz.config.errors import ConfigError
from certfuzz.helpers import quoted


logger = logging.getLogger(__name__)


class WindowsConfig(ConfigBase):
    def _add_validations(self):
        self.validations.append(self._validate_debugger_timeout_exceeds_runner)
        self.validations.append(self._validate_new_options)

    def _set_derived_options(self):
        ConfigBase._set_derived_options(self)

        # interpolate program name
        # add quotes around $SEEDFILE
        t = Template(self.config['target']['cmdline_template'])
        self.config['target']['cmdline_template'] = t.safe_substitute(PROGRAM=quoted(self.config['target']['program']),
                          SEEDFILE=quoted('$SEEDFILE'))

    def _validate_new_options(self):
        if 'minimizer_timeout' not in self.config['runoptions']:
            self.config['runoptions']['minimizer_timeout'] = 3600

    def _validate_debugger_timeout_exceeds_runner(self):
        try:
            runner_section = self.config['runner']
        except KeyError:
            return

        # if runner is null, we're just going to use the debugger timeout
        try:
            runner = runner_section['runner']
            if not runner:
                return

        except KeyError:
            return

        try:
            run_timeout = runner_section['runtimeout']
        except KeyError:
            return

        if not run_timeout:
            raise ConfigError('Runner timeout cannot be zero')

        try:
            debugger_section = self.config['debugger']
        except KeyError:
            return

        try:
            dbg_timeout = debugger_section['runtimeout']
        except KeyError:
            return

        if not dbg_timeout:
            raise ConfigError('Debugger timeout cannot be zero')

        if dbg_timeout < (2 * run_timeout):
            logger.warning('Debugger timeout must be >= 2 * runner timeout.')
            self.config['debugger']['runtimeout'] = 2.0 * run_timeout
            logger.warning('Setting debugger timeout = %s instead', self.config['debugger']['runtimeout'])
