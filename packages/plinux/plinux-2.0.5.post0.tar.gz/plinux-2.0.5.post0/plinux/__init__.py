import datetime
import json
import os
import re
import shlex
import socket
import subprocess
from json import JSONDecodeError
from pathlib import Path
from typing import Union

import plogger
from paramiko import SSHClient, ssh_exception, AutoAddPolicy

from plinux.exceptions import RemoteCommandExecutionError


class SSHResponse:
    """Response parser"""

    def __init__(self, out, err, exited: int, command: str = None):
        self.__out = out
        self.__err = err
        self.__exited = exited
        self.command = command

    def __str__(self):
        return json.dumps(self._dict, indent=4)

    @property
    def stdout(self):
        """STDOUT

        Can be:
            - None
            - str
            - dict
            - list
        """

        out = self.__out
        try:
            out = json.loads(out)
        except (TypeError, JSONDecodeError):
            ...

        return out

    @property
    def stderr(self) -> None | str:
        return self.__err if self.__err else None

    @property
    def exited(self) -> int:
        """Get exit code"""
        return self.__exited

    @property
    def ok(self) -> bool:
        return self.exited == 0

    @property
    def _dict(self):
        """Get raw response from WinRM and return result dict"""

        result = {
            'exit_code': self.exited,
            'ok': self.ok,
            'stdout': self.stdout,
            'stderr': self.stderr,
            'cmd': self.command,
        }

        return result


class Plinux:
    """Base class to work with linux OS"""

    def __init__(self,
                 host: str = '127.0.0.1',
                 username: str = None,
                 password: str = None,
                 port: int = 22,
                 logger_enabled: bool = True,
                 log_level: str | int = 'INFO'):
        """Create a client object to work with linux host"""

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = plogger.logger('Plinux', enabled=logger_enabled, level=log_level)

    def __str__(self):
        str_msg = (f'==========================\n'
                   f'Remote IP: {self.host}\n'
                   f'Username: {self.username}\n'
                   f'Password: {self.password}\n'
                   f'Host available: {self.is_host_available()}\n'
                   f'==========================')
        return str_msg

    def is_host_available(self, port: int = 0, timeout: int = 5):
        """Check remote host is available using specified port"""

        port_ = port or self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((self.host, port_))
            return False if result else True

    def list_all_methods(self):
        """Returns all available public methods"""

        return [method for method in dir(self) if not method.startswith('_')]

    def run_cmd_local(self, cmd: str, timeout: int = 60):
        """Main function to send commands using subprocess

        :param cmd: string, command
        :param timeout: timeout for command
        :return: Decoded response

        """

        try:
            self.logger.info(f'COMMAND: "{cmd}"')
            cmd_divided = shlex.split(cmd)
            result = subprocess.run(cmd_divided, capture_output=True, timeout=timeout)

            out = result.stdout.decode().strip()
            err = result.stderr.decode().strip()

            return SSHResponse(out, err, result.returncode, cmd)
        except subprocess.TimeoutExpired as err:
            self.logger.exception('Connection timeout')
            raise err

    def run_cmd_local_native(self, *popenargs,
                             stdin_input=None,
                             capture_output: bool = False,
                             timeout: int = 60,
                             check: bool = False,
                             **kwargs):
        """It's just native subprocess' .run invocation.

        The returned instance will have attributes args, returncode, stdout and
        stderr. By default, stdout and stderr are not captured, and those attributes
        will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them.

        If check is True and the exit code was non-zero, it raises a
        CalledProcessError. The CalledProcessError object will have the return code
        in the returncode attribute, and output & stderr attributes if those streams
        were captured.

        If timeout is given, and the process takes too long, a TimeoutExpired
        exception will be raised.

        There is an optional argument "stdin_input", allowing you to
        pass bytes or a string to the subprocess's stdin.  If you use this argument
        you may not also use the Popen constructor's "stdin" argument, as
        it will be used internally.

        By default, all communication is in bytes, and therefore any "stdin_input" should
        be bytes, and the stdout and stderr will be bytes. If in text mode, any
        "stdin_input" should be a string, and stdout and stderr will be strings decoded
        according to locale encoding, or by "encoding" if set. Text mode is
        triggered by setting any of text, encoding, errors or universal_newlines.

        The other arguments are the same as for the Popen constructor.

        :param popenargs:
        :param stdin_input:
        :param capture_output:
        :param timeout:
        :param check:
        :param kwargs:
        :return:
        """

        cmd = shlex.split(*popenargs)
        cmd_to_log = ' '.join(cmd)
        self.logger.info(f'{self.host:<14} | {cmd_to_log}')

        result = subprocess.run(cmd, input=stdin_input, capture_output=capture_output, timeout=timeout, check=check,
                                **kwargs)

        self.logger.info(f'{self.host:<14} | {result.returncode}:\n\t{result}')
        return result

    def _client(self, sftp: bool = False, timeout: int = 15):
        """https://www.paramiko.org/"""

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            client.connect(self.host, username=self.username, password=self.password, timeout=timeout)

            if sftp:
                return client.open_sftp()
            return client
        except ssh_exception.AuthenticationException as err:
            msg = f'{self.host:<14}| Invalid credentials: {self.username}@{self.password}:\n{err}.'
            self.logger.exception(msg)
            raise err
        except ssh_exception.NoValidConnectionsError as err:
            msg = f'{self.host:<14}| There is no valid connection. Try to use "_local" or vice versa method.'
            self.logger.exception(msg)
            raise err
        except TimeoutError as err:
            self.logger.exception(f'{self.host:<14}| Timeout exceeded.')
            raise err
        except Exception as err:
            self.logger.exception(f'{self.host:<14}| Something went wrong:\n{err}.')
            raise err

    def run_cmd(self, cmd: str, sudo: bool = False, timeout: int = 30, ignore_errors: bool = False) -> SSHResponse:
        """Base method to execute SSH command on remote server

        Exit codes: https://tldp.org/LDP/abs/html/exitcodes.html

        Args:
            cmd: SSH command
            sudo: Execute specified command as sudo user
            timeout: Execution timeout
            ignore_errors: Ignore errors

        Returns:
            SSHResponse class
        """

        client = self._client()

        try:
            command = f"sudo -S -p '' -- sh -c '{cmd}'" if sudo else cmd
            self.logger.info(f'{self.host:<14} | {command}')

            stdin, out, err = client.exec_command(command, timeout=timeout)

            if sudo:
                stdin.write(self.password + '\n')
                stdin.flush()

            exited = out.channel.recv_exit_status()
            out_ = out.read().decode().strip()
            err_ = err.read().decode().strip()
            parsed = SSHResponse(out=out_, err=err_, exited=exited, command=cmd)

            # Log ERROR / Exit code != 0 (operation is failed)
            def_log = f'{self.host:<14} | {parsed.exited}:'
            err_to_log = f'{def_log} STDERR:\n\t{parsed.stderr}' if parsed.stderr else def_log
            if parsed.exited:
                self.logger.error(err_to_log)

                if not ignore_errors:  # Exit code != 0 and ignore_errors=True
                    raise RemoteCommandExecutionError(parsed.stderr)

            # Log INFO / Exit code == 0 (operation is success)
            else:
                # Log WARNING
                if parsed.stderr:  # Exit code != 0 and stderr contains message
                    self.logger.warning(err_to_log)

                out_to_log = json.dumps(parsed.stdout, indent=4) if isinstance(parsed.stdout, dict) else parsed.stdout
                msg_to_log = f'{parsed.exited}:\n\t{out_to_log}' if out_to_log else f'{parsed.exited}:'
                self.logger.info(f'{self.host:<14} | {msg_to_log}')

            return parsed
        finally:
            client.close()

    def sqlite3(self, db: str, sql: str, sudo: bool = False, params: str = '', timeout: int = 1000):
        """Simple work with the SQLite.

        - sqlite3 -cmd ".timeout {timeout}" {db} "{sql}" {params}

        Args:
            db: DB path
            sql: SQL request
            params: i.e. "-line -header", "-csv"
            sudo:
            timeout: ms. 1000 by default
        """

        cmd = f'sqlite3 -cmd ".timeout {timeout}" {db} "{sql}" {params}'
        result = self.run_cmd(cmd, sudo=sudo)
        return result

    def is_credentials_valid(self) -> bool:
        try:
            self.run_cmd('whoami')
            return True
        except ssh_exception.AuthenticationException:
            self.logger.exception(f'Invalid credentials ({self.username, self.password})')
            return False

    def get_os_version(self) -> dict:
        """Get OS version

        :return: {'distributor_id': 'Ubuntu', 'desc...': 'Ub..20.04.2 LTS', 'release': '20.04', 'codename': 'focal'}
        """

        result = self.run_cmd('lsb_release -a').stdout

        parsed_result = {}
        for line in result.splitlines():
            kev, value = line.split(':')
            new_key = kev.strip().lower().replace(' ', '_')
            parsed_result[new_key] = value.strip()

        return parsed_result

    def get_ip(self) -> str:
        """Get IP address of remote server"""

        return self.run_cmd('hostname -I').stdout

    def get_hostname(self) -> str:
        """Get hostname of remote server

        :return: Hostname. auto-test-node1
        """

        return self.run_cmd('hostname').stdout

    def get_ufw_status(self) -> dict:
        """Get uwf status.

        - sudo ufw status

        Returns:
            {
                'Status': 'active', 'entities_quantity': 30, 'rules': [{'to': '22/tcp', 'action': 'ALLOW IN',
                'from': 'Anywhere', 'port': '22', 'network_protocol': 'ipv4', 'samba': False, 'transport': 'tcp'},...}
        """

        cmd = 'ufw status verbose'
        result = self.run_cmd(cmd, sudo=True).stdout  # Status: inactive

        result_dict = {}
        lines = result.splitlines()

        for raw_line in lines:
            # Skip empty and header lines
            if not raw_line or '-' in raw_line or 'To' in raw_line:
                continue

            # ['Status', 'active'], ['Logging', 'on (low)'], ['New profiles', 'skip']...
            text_line = raw_line.split(': ')

            # Get Status, Logging, Default, New profiles keys
            try:
                key = text_line[0]
                value = text_line[1]
                result_dict[key] = value

                result_dict['entities_quantity'] = 0
                result_dict['rules'] = []
                continue
            except IndexError:
                ...

            # Get rules
            keys = 'to', 'action', 'from'
            for line in text_line:
                result_dict['entities_quantity'] += 1

                # "22/tcp                     ALLOW IN    Anywhere" -> ['22/tcp', 'ALLOW IN', 'Anywhere']
                rule = [kv.strip() for kv in line.split('  ') if kv]

                # 137,138/udp (Samba (v6)) -> 137,138_v6; 5044/tcp -> 5044
                port_raw = rule[0]
                port_re = re.search(r'\d+[:,/.\d ]*\d+', port_raw).group()
                port = port_re.replace(' ', '_').replace(':', '-')  # "5044", "137,138", "6000-6007"

                rule_dict = dict(zip(keys, rule))
                rule_dict['port'] = port
                rule_dict['network_protocol'] = 'ipv6' if 'v6' in line else 'ipv4'
                rule_dict['samba'] = True if 'Samba' in line else False

                if 'tcp' in line:
                    transport = 'tcp'
                elif 'udp' in line:
                    transport = 'udp'
                else:
                    transport = 'any'

                rule_dict['transport'] = transport
                result_dict['rules'].append(rule_dict)

        return result_dict

    # Package, Deb
    def get_package_version(self, package: str) -> str:
        """Get package (.deb) version

        :param package: Deb name
        :return: 1.0.9.1503
        """

        cmd = f"dpkg -s {package} | grep Version | awk '{{print $2}}'"
        result = self.run_cmd(cmd)
        return result.stdout

    def get_installed_packages_versions(self) -> dict:
        """Get all installed packages and their versions"""

        response = self.run_cmd('dpkg --list | grep ii').stdout
        result = {package.split()[1].removesuffix(':amd64'): package.split()[2] for package in response.splitlines()}
        return result

    def is_package_upgradable(self, package: str, show_version: bool = True) -> Union[bool, str]:
        """Check package newer version. Return it if exists.

        :param show_version:
        :param package:
        :return:
        """

        cmd = fr"apt list --installed {package} 2>/dev/null | egrep -o '\[.*\]'"
        result = self.run_cmd(cmd).stdout

        try:
            if 'upgradable' in result:  # There is newer package version
                if show_version:  # Get precise version
                    new_version = result.split('to: ')[1].removesuffix(']')
                    return new_version
                return True
        except TypeError:
            self.logger.error(f'Package ({package}) not found on destination server.')
        return False

    def is_security_update_available(self) -> bool:
        """Verify security update availability. Returns True is available. Otherwise, returns False"""

        result = self.run_cmd('apt-get upgrade -s | grep -i security', ignore_errors=True)
        return result.ok

    def get_package_info(self, package: str) -> dict:
        """Get package info"""

        cmd = f'dpkg -s {package}'
        result = self.run_cmd(cmd).stdout
        res_dict = {}
        for line in result.splitlines():
            data = line.split(': ')
            key = data[0]
            value = data[1]

            if key == 'Depends':
                # [['starwind-san-and-nas-console', '(>= 1.1809.2586)'], ['starwind-virtual-san', '(>= 1.0.14398)']]
                depends_list = [x.split(' (', maxsplit=1) for x in value.split(', ')]
                depends_dict = {x[0]: x[1].removesuffix(')') for x in depends_list}
                res_dict[key] = depends_dict
            else:
                res_dict[key] = value

        return res_dict

    def get_date(self) -> datetime:
        """Get date from remote server"""

        result = self.run_cmd('date')
        return to_known_type(result.stdout)

    def get_time_date(self) -> dict:
        """Get time and date from remote server

        - time_sync_mode: service key with "ntp" or "host" value

        :return:
        """

        response = self.run_cmd('timedatectl').stdout.splitlines()

        response_dict = {}
        for line in response:
            key, value = line.strip().split(': ')
            key_new = key.replace(' ', '_').lower()

            if key_new == 'time_zone':
                value = value.split(' ')[0]
            response_dict[key_new] = to_known_type(value)

        response_dict['time_sync_mode'] = 'ntp' if response_dict['ntp_service'] == 'active' else 'host'

        return response_dict

    # ---------- Service management ----------
    def get_service(self, name: str) -> str:
        """Get whole service info

        - systemctl status {name}

        Args:
            name: Service name

        Returns:

        """

        cmd = f'systemctl status {name}'
        result = self.run_cmd(cmd)
        return result.stdout

    def is_service_active(self, name: str) -> bool:
        """Is service active?

        - systemctl is-active --quiet {name}

        Args:
            name: service name

        Returns:
            True or False
        """

        cmd = f'systemctl is-active --quiet {name}'
        result = self.run_cmd(cmd, ignore_errors=True)
        return result.ok

    def stop_service(self, name: str) -> bool:
        """Stop service

        - systemctl stop {name}

        Args:
            name: service name

        Returns:

        """

        cmd = f'systemctl stop {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    def kill_service(self, name: str) -> bool:
        """Kill service

        - systemctl kill {name}

        Args:
            name: service name

        Returns:

        """

        cmd = f'systemctl kill {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    def start_service(self, name: str) -> bool:
        """Start service

        - systemctl start {name}

        Args:
            name: service name

        Returns:

        """

        cmd = f'systemctl start {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    def restart_service(self, name: str) -> bool:
        """Restart service

        - systemctl restart {name}

        Args:
            name: service name

        Returns:

        """

        cmd = f'systemctl restart {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    def get_service_journal(self, name: str) -> str:
        """Get service journal

        - journalctl -u {name}

        Args:
            name: Service name

        Returns:

        """

        cmd = f'journalctl -u {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.stdout

    def list_active_services(self, no_legend: bool = True, all_services: bool = False):
        """List all active services and it's status

        - systemctl list-units -t service

        :param no_legend:
        :param all_services: To see loaded but inactive units, too
        :return:
        """

        cmd = 'systemctl list-units -t service'
        if no_legend:
            cmd += ' --no-legend'
        if all_services:
            cmd += ' --all'
        return self.run_cmd(cmd)

    def enable(self, name: str) -> bool:
        """Enable service using systemctl

        - systemctl enable {name}

        Args:
            name: Service name

        Returns:

        """

        cmd = f'systemctl enable {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    def disable(self, name: str) -> bool:
        """Disable service

        - systemctl disable {name}

        Args:
            name: Service name

        Returns:

        """

        cmd = f'systemctl disable {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    def is_service_enabled(self, name: str) -> bool:
        """Get unit service status

        - systemctl is-enabled {name}

        :param name: Service name
        :return:
        """

        cmd = f'systemctl is-enabled {name}'
        response = self.run_cmd(cmd, ignore_errors=True).stdout

        try:
            return True if 'enabled' in response else False
        except TypeError:
            return False

    def get_pid(self, name: str, sudo: bool = False) -> Union[int, list]:
        """Get process pid

        - pidof {name}

        :param name: Process name
        :param sudo: To elevate permission (in CentOS)
        """

        cmd = f'pidof {name}'
        result = self.run_cmd(cmd, sudo=sudo).stdout

        try:
            return int(result)
        except ValueError:
            return list(map(int, result.split()))
        except TypeError as err:
            self.logger.exception(f'Cannot get pid ({name}). Try to use sudo.')
            raise err

    def get_netstat_info(self, params: str = '') -> str:
        """Get netstat info

        - netstat

        Necessary to install net-tool: "yum -y install net-tools"

        :param params: "ltpu" - Active Internet connections (only servers)
        :return:
        """

        cmd = 'netstat' if not params else f'netstat -{params}'
        result = self.run_cmd(cmd)
        return result.stdout

    # ----------- File and directory management ----------
    def exists(self, path: str, sudo: bool = False) -> bool:
        r"""Check file and directory exists.

        For windows path: specify network path in row format or use escape symbol.
        You must be connected to the remote host.
        Usage: check_exists('\\\\172.16.0.25\\d$\\New Text Document.txt')

        For linux path: linux style path.
        Usage: check_exists('/home/user/test.txt')

        :param path: Full path to file/directory
        :param sudo:
        :return:
        """

        self.logger.info(f'-> Verify entity ({path}) existence')

        # Linux
        if '/' in path:
            cmd = f'test -e {path}'
            response = self.run_cmd(cmd, sudo=sudo, ignore_errors=True)
            result = response.ok
            self.logger.info(f'<- {result}')
            return result
        # Windows
        elif '\\' in path:
            return os.path.exists(path)
        raise SyntaxError('Incorrect method usage. Check specified path.')

    def cat_file(self, path: str, sudo: bool = False, pprint: bool = False) -> str | dict:
        """Get file content"""

        cmd = f'cat {path}'
        result = self.run_cmd(cmd, sudo=sudo)
        file = result.stdout

        if pprint:
            print(json.dumps(file, indent=4), sep='')
        return file

    def get_prelogin(self, path: str) -> dict:
        """Read PreLogin (MOTD) message and return dict.

            ===\n
            Build: 1.2.3.4 (2022-06-20)\n
            Web console: https://IP\n
            SSL certificate fingerprint: F8E5BCB26...7399EDA48E5DAE41D06\n
            ===

        Args:
            path: Filepath. /etc/issue

        Returns:
            {
              'keys': [
                'Build',
                'Web console',
                'SSL certificate fingerprint'
              ],
              'delimiter': '=====================================================================',
              'build': '1.2.3.4 (2022-06-20)',
              'web_console': 'https://IP',
              'ssl_certificate_fingerprint': 'F8E5BCB26...7399EDA48E5DAE41D06'}
        """

        cat_result = self.cat_file(path)
        result = {'keys': []}

        for line in cat_result.splitlines():
            split_line = line.split(':', maxsplit=1)
            try:
                k, v = split_line
            except ValueError:
                result['delimiter'] = split_line[0]
            else:
                result['keys'].append(k)
                key = k.replace(' ', '_').lower()
                result[key] = v.strip()

        return result

    def create_file(self, path: str, sudo: bool = True) -> bool:
        """Create file

        Args:
            path: Filepath
            sudo:

        Returns:
            True or False
        """

        cmd = f'touch {path}'
        result = self.run_cmd(cmd, sudo=sudo)
        return result.ok

    def clear_file(self, path: str, sudo: bool = True) -> bool:
        """Clear file.

        - cat /dev/null > {path}

        :param path: Filepath
        :param sudo:
        :return:
        """

        cmd = f'cat /dev/null > {path}'
        result = self.run_cmd(cmd, sudo=sudo)
        return result.ok

    def stat_file(self, path: str, sudo: bool = False) -> dict:
        """Get file information

        - %a access rights in octal
        - %A access rights in human-readable form
        - %g group ID of owner
        - %G group name of owner
        - %u user ID of owner
        - %U username of owner
        - %F file type
        - %i inode number
        - %s total size, in bytes
        - %m mount point
        - %w time of file birth, human-readable; - if unknown
        - %X time of last access, seconds since Epoch
        - %Y time of last data modification, seconds since Epoch
        - %Z time of last status change, seconds since Epoch
        - executable: True if there are 3 "x" in access right. Otherwise, False

        Args:
            path: File path. /home/username/just_file
            sudo: Use sudo

        Returns:
            {
              'access_rights': 775,
              'access_rights_human': '-rwxrwxr-x',
              'executable': True,
              'group': 1000,
              'group_human': 'objectfirst',
              'user': 1000,
              'user_human': 'objectfirst',
              'file_type': 'regular file',
              'inode': 927734,
              'size': 13325572,
              'mount_point': '/',
              'time_birth': '-',
              'datetime_last_access': datetime.datetime(2021, 11, 10, 11, 27, 29),
              'datetime_data_modification': datetime.datetime(2021, 11, 1, 17, 59, 55),
              'datetime_status_modification': datetime.datetime(2021, 11, 1, 18, 0, 26)}
        """

        params = ('access_rights:%a|'
                  'access_rights_human:%A|'
                  'group:%g|'
                  'group_human:%G|'
                  'user:%u|'
                  'user_human:%U|'
                  'file_type:%F|'
                  'inode:%i|'
                  'size:%s|'
                  'mount_point:%m|'
                  'time_birth:%w|'
                  'datetime_last_access:%X|'
                  'datetime_data_modification:%Y|'
                  'datetime_status_modification:%Z'
                  )

        cmd = f'stat -c "{params}" {path}'
        result = self.run_cmd(cmd, sudo=sudo)
        res_dict = {}

        for i in result.stdout.split('|'):
            k, v = i.split(':', maxsplit=1)

            if k == 'access_rights_human':  # Check executable or not
                count_x = v.count('x')
                res_dict[k] = v
                res_dict['executable'] = True if count_x == 3 else False

            elif 'datetime' in k:
                epoch_time = int(v)
                date_time = datetime.datetime.fromtimestamp(epoch_time)
                res_dict[k] = date_time
            else:
                try:
                    res_dict[k] = int(v)
                except ValueError:
                    res_dict[k] = v

        return res_dict

    def grep_line_in_file(self, path: str, string: str, directory: bool = False, sudo: bool = True):
        """Grep line in file or directory

        :param sudo:
        :param path: File/directory path
        :param string: string pattern to grep
        :param directory: If True - grep in directory with files
        :return:
        """

        self.logger.info(f'-> Grep line in file or directory')

        cmd = f'grep -rn "{string}" {path}' if directory else f'grep -n "{string}" {path}'

        result = self.run_cmd(cmd, sudo=sudo, ignore_errors=True)

        match result.exited:
            case 0:
                self.logger.info(f'<- Pattern "{string}" found in {path}')
            case 1:
                self.logger.info(f'<- Pattern "{string}" not found')
            case _:
                self.logger.error(f'<- {result.stderr}')
                raise RemoteCommandExecutionError

        return result

    def change_line_in_file(self, path: str, old: str, new: str, sudo: bool = True):
        """Replace line and save file.

        :param sudo:
        :param path: File path
        :param old: String to replace
        :param new: New string
        :return:
        """

        return self.run_cmd(f'sed -i "s!{old}!{new}!" {path}', sudo=sudo)

    def delete_line_from_file(self, path: str, string: str, sudo: bool = True):
        return self.run_cmd(f"sed -i '/{string}/d' {path}", sudo=sudo)

    def get_last_file(self, directory: str = '', name: str = '', sudo: bool = True) -> str:
        """Get last modified file in a directory

        - ls /home/username/scripts -Art | tail -n 1

        :param name: Filename to grep
        :param directory: Directory path to precess. Home by default
        :param sudo:
        :return:
        """

        directory_ = directory or f'/home/{self.username}'
        cmd = f'ls {directory_} -Art| grep {name} | tail -n 1' if name else f'ls {directory} -Art | tail -n 1'
        result = self.run_cmd(cmd, sudo=sudo)

        return result.stdout

    def compare_files(self, file1: str | Path, file2: str | Path, params: str = '', sudo: bool = False) -> bool:
        """Compare two files byte by byte.

        Command:
            - cmp -s {params} {file1} {file2}

        Args:
            file1: /home/objectfirst/file_bin_1
            file2: /home/objectfirst/file_text_2
            params:
            sudo:

        Returns:
            Bool
        """

        self.logger.info(f'-> Compare two files byte by byte\n\t1. {file1}\n\t2. {file2}')

        cmd = f'cmp -s {params} {file1} {file2}'
        result = self.run_cmd(cmd, sudo=sudo, ignore_errors=True)

        match result.exited:
            case 0:
                self.logger.info(f'<- Files are equal')
                return True
            case 1:
                self.logger.info(f'<- Files are different')
                return False
            case _:
                self.logger.error(f'<- File(s) not found: {result.stderr}')
                raise FileNotFoundError(f'"{file1}" or "{file2}" not found')

    def remove(self, path: str, sudo: bool = True) -> bool:
        """Remove file(s) and directories

        - for file in {path}; do rm -rf "$file"; done

        Usage:

        - path=/opt/1 remove the directory
        - path=/opt/1/* remove all file in the directory
        - path=/opt/1/file.txt remove specified file in the directory

        :param sudo:
        :param path: Path to a file or directory.
        """

        cmd = f'for file in {path}; do rm -rf "$file"; done'
        result = self.run_cmd(cmd, sudo=sudo)
        return result.ok

    def extract_files(self, src: str, dst: str, mode: str = 'tar', quite: bool = True, sudo: bool = False) -> bool:
        """Extract file to specific directory

        :param sudo:
        :param src: Full path to archive (with extension)
        :param dst:
        :param mode: "tar", "zip"
        :param quite: Suppress list of unpacked files
        :return:
        """

        unzip_cmd = f'unzip -q {src} -d {dst}' if quite else f'unzip {src} -d {dst}'
        tar_cmd = f'tar -xzvf {src}.tar.gz -C {dst}'

        cmd = tar_cmd if mode == 'tar' else unzip_cmd
        result = self.run_cmd(cmd, sudo=sudo)

        return result.ok

    def copy_file(self, src: str, dst: str, sudo: bool = True) -> bool:
        """Copy file to another location

        :param sudo:
        :param src: Source full path
        :param dst: Destination
        :return:
        """

        cmd = f'cp {src} {dst}'
        result = self.run_cmd(cmd, sudo=sudo)
        return result.ok

    def get_md5(self, path: str, sudo: bool = True) -> str:
        """Get file md5

        - md5sum {path}

        :param sudo:
        :param path: File path
        :return: Return md5 sum only
        """

        cmd = f'md5sum {path}'
        result = self.run_cmd(cmd, sudo=sudo).stdout
        return result.split(path)[0].strip()

    def get_processes(self) -> list:
        """Get processes using PS

        - ps -aux
        """

        result = self.run_cmd('ps -aux')
        split_result = result.stdout.splitlines()
        return split_result

    #  ----------- Power management -----------
    def reboot(self) -> bool:
        """Reboot remote host

        - shutdown -r now

        Returns:

        """

        cmd = 'shutdown -r now'
        result = self.run_cmd(cmd, sudo=True, ignore_errors=True)
        return result.ok

    def shutdown(self) -> bool:
        """Shutdown remote host

        - shutdown -h now

        Returns:

        """

        cmd = 'shutdown -h now'
        result = self.run_cmd(cmd, sudo=True, ignore_errors=True)
        return result.ok

    #  ----------- Directory management -----------
    def create_directory(self, path: str, sudo: bool = True) -> bool:
        """Create directory

        - mkdir {path}

        Args:
            path:
            sudo:

        Returns:

        """

        cmd = f'mkdir {path}'
        result = self.run_cmd(cmd, sudo=sudo)
        return result.ok

    def list_dir(self, path: str, params=None, sudo: bool = False) -> list:
        """List directory

        - ls

        :param path: Directory path
        :param params: Additional params. For example: "la"
        :param sudo:
        :return: List of files
        """

        cmd = f'ls {path} -{params}' if params else f'ls {path}'
        result = self.run_cmd(cmd, sudo=sudo)

        try:
            return result.stdout.splitlines()
        except AttributeError:
            return []

    def count_files(self, path: str) -> int:
        """Count files number in directory.

        :param path:
        :return:
        """

        result = self.run_cmd(f'ls {path} | wc -l')
        return int(result.stdout)

    #  ----------- SFTP -----------
    @property
    def sftp(self):
        return self._client(sftp=True)

    def upload(self, local: str, remote: str):
        r"""Upload file/dir to the host and check exists after.

        Usage: tool.upload(r'd:\python_tutorial.pdf', '/home/user/python_tutorial.pdf'')

        :param local: Source full path
        :param remote: Destination full path
        :return: bool
        """

        self.sftp.put(local, remote, confirm=True)
        self.logger.info(f'Uploaded {local} to {remote}')
        return self.exists(remote)

    def download(self, remote: str, local: str, callback=None) -> bool:
        r"""Download a file from the current connection to the local filesystem and check exists after.

        Usage: tool.download('/home/user/python_tutorial.pdf', 'd:\dust\python_tutorial.pdf')

        :param remote: Remote file to download. May be absolute, or relative to the remote working directory.
        :param local: Local path to store downloaded file in, or a file-like object
        :param callback: func(int, int)). Accepts the bytes transferred so far and the total bytes to be transferred
        :return: bool
        """

        self.sftp.get(remote, local, callback=callback)
        self.logger.info(f'Downloaded {remote} to {local}')
        return self.exists(local)

    # ------------ END -----------

    def change_password(self, new_password: str):
        """Change password

        BEWARE USING! You'll lost connection to a server after completion.

        echo username:new_password | sudo chpasswd

        :param new_password: New password with no complex check.
        :return:
        """

        return self.run_cmd(f'sudo -S <<< {self.password} -- sh -c "echo {self.username}:{new_password} | chpasswd"')

    # ---------- Disk ----------
    def get_disk_usage(self, mount_point: str = '/') -> dict:
        """Get disk usage

        :param mount_point:
        :return: {'Filesystem': '/dev/mapper/ubuntu--vg-ubuntu--lv', 'Size': '19G', 'Used': '12G', 'Avail': '6.5G',
        'Use%': '64%', 'Mounted': '/'}
        """

        cmd = f'df {mount_point} -h' if mount_point else 'df -h'
        result = self.run_cmd(cmd).stdout
        parsed_result = dict(zip(result.splitlines()[0].split(), result.splitlines()[1].split()))
        return parsed_result

    def get_free_space(self, mount_point: str = '/', *params) -> str:
        """Get free space.

        By default, with -h parameter.

        >>> self.get_free_space('')  # get all info
        >>> self.get_free_space('/opt')  # df / -h --output=avail | tail -n 1
        >>> self.get_free_space('/opt', '--block-size=K')  # df /opt --block-size=K --output=avail | tail -n 1
        >>> self.get_free_space('/opt', '-h', '-H')  # df /opt -h -H --output=avail | tail -n 1

        :param mount_point: /, /opt
        :return: 5G
        """

        params_ = shlex.join(params) if params else '-h'
        cmd = f'df {mount_point} {params_} --output=avail | tail -n 1'

        return self.run_cmd(cmd).stdout

    def get_disk_size(self, path: str, sudo: bool = False) -> int:
        """Get disk size.

        df /mnt/xfs/ --block-size=1 --output=size | tail -n 1

        :param path: /mnt/xfs/
        :param sudo:
        :return: Size in bytes
        """

        cmd = f'df {path} --block-size=1 --output=size | tail -n 1'
        result = self.run_cmd(cmd, sudo=sudo).stdout
        try:
            return int(result)
        except TypeError as err:
            msg = f'Path ({path}) not found or something went wrong.'
            self.logger.exception(msg)
            raise RemoteCommandExecutionError(msg) from err

    def get_dir_size(self, path: str, sudo: bool = False) -> int:
        """Get directory size

        Command:
            - du -s --block-size=1 /mnt/ssd-cache | awk {'print $1'}

        Args:
            path: /mnt/ssd-cache/
            sudo:

        Returns:
            Size in bytes
        """

        cmd = f"du -s --block-size=1 {path} | awk {{'print $1'}}"
        result = self.run_cmd(cmd, sudo=sudo).stdout  # 876592118

        try:  # Use try-block to process invalid paths. Returns string if path is invalid
            return int(result)
        except ValueError as err:
            msg = f'Path ({path}) not found or something went wrong.'
            self.logger.exception(msg)
            raise RemoteCommandExecutionError(msg) from err

    def get_port_listeners_process_id(self, port: int) -> Union[int, list[int]]:
        r"""Get processes ids of port listeners

        sudo -S -p '' -- sh -c 'ss -ltpn | grep ":44301\s" | grep -Po "(?<=pid=)(\d*)" | uniq '

        :param port: /mnt/ssd-cache/
        :return: Size in bytes
        """

        cmd = fr'ss -ltpn | grep ":{port}\s" | grep -Po "(?<=pid=)(\d*)" | uniq'
        result = self.run_cmd(cmd, sudo=True).stdout
        try:
            return int(result)
        except TypeError as err:
            msg = f'Port ({port}) not found or something went wrong.'
            self.logger.exception(msg)
            raise RemoteCommandExecutionError(msg) from err
        except ValueError:
            return list(map(int, result.splitlines()))

    def get_process_cmdline(self, *process_id: int, sudo: bool = False) -> list:
        """Get process command line

        - ps h -p 507034,507033,507032,507031,507030,507029,507028,507027,507026 -o args

        :param process_id:
        :param sudo:
        :return: List of processes
        """

        ids = ','.join(map(str, process_id))  # convert to str comma separated
        cmd = f'ps h -p {ids} -o args'
        result = self.run_cmd(cmd, sudo=sudo).stdout

        return result.splitlines()

    # ---------- User management ----------
    def get_user_id(self, user: str = None) -> int:
        """Get Linux OS user ID

        - id -u {user}

        :param user: Username. By default, connecting user used.
        :return: integer
        """

        user = self.username if user is None else user
        result = self.run_cmd(f'id -u {user}')
        return int(result.stdout)

    def kill_user_session(self, name: str) -> bool:
        """Kill all user's ssh session and processes

        - pkill -9 -u {name}

        :param name: User name
        :return:
        """

        cmd = f'pkill -9 -u {name}'
        result = self.run_cmd(cmd, sudo=True)
        return result.ok

    # OpenSSL
    def validate_ssl_key(self, path: str) -> bool:
        """Validate key

        - openssl rsa -in {path} -check

        :param path: key path
        :return: True if 'RSA key ok' in response.
        """

        cmd = f'openssl rsa -in {path} -check'
        result = self.run_cmd(cmd)
        return True if 'RSA key ok' in result.stdout else False

    def get_ssl_md5(self, path: str) -> str:
        """Get cert or key md5

        - openssl x509 -noout -modulus -in {path} | openssl md5

        :param path:
        :return:
        """

        cmd = f'openssl x509 -noout -modulus -in {path} | openssl md5'
        result = self.run_cmd(cmd)
        return result.stdout

    def get_ssl_certificate(self, x509: bool = True, port: int = 443) -> str:
        """Get certificate info

        - openssl s_client -showcerts -connect {self.host}:{port} </dev/null

        :param x509: Get x509 if specified
        :param port: 443 by default
        :return:
        """

        cmd = f'openssl s_client -showcerts -connect {self.host}:{port} </dev/null'
        if x509:
            cmd += ' | openssl x509 -text'
        result = self.run_cmd(cmd)

        return result.stdout

    def get_ssl_fingerprint(self, path: str, algorithm: str = 'sha1', brief: bool = True) -> str:
        """Get SSL/TLS thumbprint

        - openssl x509 -noout -fingerprint -{algorithm} -inform pem -in {path}

        :param path: Cert path
        :param algorithm:
        :param brief: Get fingerprint in "C3587D1515236324AB03686BF7F23B015D284351" format
        :return:
        """

        cmd_general = f'openssl x509 -noout -fingerprint -{algorithm} -inform pem -in {path}'
        if brief:
            cmd = f'{cmd_general} | awk -F "=" \'{{gsub(":","");print $2}}\''
        else:
            cmd = f'{cmd_general} | awk -F "=" \'{{print $2}}\''

        result = self.run_cmd(cmd)
        return result.stdout

    def get_ssl_serial(self, path: str) -> str:
        """Get serial number from certificate

        :param path:
        :return:
        """

        cmd_general = f'openssl x509 -noout -serial -inform pem -in {path}'  # | awk -F "=" \'{{print $2}}\''
        cmd = f'{cmd_general} | awk -F "=" \'{{print $2}}\''
        result = self.run_cmd(cmd)

        return result.stdout

    # NETWORK
    def get_ip_addresses_show(self, name: str = None) -> dict:
        """Show IP addresses info.

        - ip --json addr show

        Note:
            - If name is specified, return only info about this interface.
            - If name is not specified, return all interfaces info.

        :param name: Interface name. Returns for specific iface info if used. For example: ens160, enp0s10f0
        :return:
        """

        cmd = 'ip --json addr show'
        result = self.run_cmd(cmd).stdout

        result_dict = {iface.get('ifname'): iface for iface in result}

        for key, value in result_dict.items():
            # Set IP address as keys in addr_info dict
            addr_info_dict = {addr['local']: addr for addr in value['addr_info']}
            result_dict[key]['addr_info'] = addr_info_dict
            result_dict[key]['ipv4_addresses'] = [k for k, v in addr_info_dict.items() if v['family'] == 'inet']
            result_dict[key]['ipv6_addresses'] = [k for k, v in addr_info_dict.items() if v['family'] == 'inet6']

        result_dict['entities_quantity'] = len(result)

        return result_dict if name is None else result_dict[name]

    def get_ntp_servers(self) -> list:
        """Get NTP servers list

        - grep "NTP" /etc/systemd/timesyncd.conf | grep -v "#"

        :return: List of NTP servers. {'172.16.0.1', '192.168.12.1'}
        """

        cmd = 'grep "NTP" /etc/systemd/timesyncd.conf | grep -v "#"'
        response = self.run_cmd(cmd).stdout
        values = re.findall(r'NTP=(.+)', response)  # ['172.16.0.3 ntp.com'] or ['172.16.0.3', '172.16.0.4']

        if len(values) > 1:
            # NTP=172.16.0.3
            # FallbackNTP=172.16.0.4
            return values

        # For NTP=172.16.0.3 ntp.com
        try:
            return values[0].split()
        except IndexError:
            return []

    # Aliases
    cat = cat_file
    ps = get_processes
    ls = list_dir
    cp = copy_file
    date = get_date
    os = get_os_version
    netstat = get_netstat_info
    start = start_service
    stop = stop_service
    status = is_service_active
    restart = restart_service
    version = get_os_version
    rm = remove
    chpasswd = change_password
    count = count_files
    stat = stat_file
    md5 = get_md5
    ufw = get_ufw_status


def to_known_type(value: str):
    """Convert string data into known Python's data types.

    - date/time => datetime.datetime
    - "yes"/"no"/"true"/"false" => True/False
    - "none", "empty", ""  => True/False
    - "123"  => int
    - "000000"  => "000000"

    :param value:
    :return:
    """

    from dateutil import parser
    from dateutil.parser import ParserError

    try:
        value_lower = value.lower()
    except AttributeError:
        value_lower = value

    try:
        return int(value_lower)
    except (TypeError, ValueError):
        ...

    if value_lower in ('yes', 'true'):
        return True
    if value_lower in ('no', 'false'):
        return False
    if value_lower in ('none', 'empty', ''):
        return None
    if value_lower.startswith('00'):
        return value

    try:
        return parser.parse(value)
    except ParserError:
        ...

    return value
