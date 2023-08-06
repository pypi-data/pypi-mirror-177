from __future__ import absolute_import
import sys
import os

from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.command import Command

from blended.blendedcli.accounts import *
from blended.blendedcli.packages import *
from blended.blendedcli.set_up import *
from blended.blendedcli.help import Help
from blended.blendedcli.settings import BLENDED_DIR as blended_dir

os_name = sys.platform.lower()
if os_name == 'linux':
    import readline
elif os_name == 'darwin':
    import readline

# App.NAME = 'blended_cli'

class Blended(App):
    """
    Command line App for Blended.
    """
    def __init__(self):
        command = CommandManager('blended')
        super(Blended, self).__init__(
            description='Blended App for Command Line Interface',
            version='0.39',
            command_manager=command,
        )
        commands = {
            'account accept': AccountAccept,
            'account add': AccountAdd,
            'account create': AccountCreate,
            'account current': AccountCurrent,
            'account email-verification': AccountEmailVerification,
            'account list': AccountList,
            'account login': AccountLogin,
            'account logout': AccountLogout,
            'account revoke': AccountRevoke,
            'account set': AccountSetCurrent,
            'account set-current': AccountSetCurrent,
            'account password-reset': AccountPasswordUpdate,
            'help': Help,
            'package accept': PackageAccept,
            'package as-json': PackageAsJson,
            'package canonize': PackageCanonical,
            'package clone': ClonePackage,
            'package compare': PackageCompare,
            'package create': PackageCreate,
            'package detail': PackageDetail,
            'package extend': PackageExtend,
            'package get': GetPackage,
            'package install': InstallPackage,
            'package list': PackageList,
            'package preview': PackagePreview,
            'package publish': PackagePublish,
            'package pull': DownloadPackage,
            'package push': PackageSave,
            'package retract': PackageRetract,
            'package reject': PackageReject,
            'package revoke': PackageRevoke,
            'package share': PackageShare,
            'package snapshot': PackageSnapshot,
            'package transfer': PackageTransfer,
            'package up': PackageUpdate,
            'package update': PackageUpdate,
            'package validate': PackageValidate,
            'package version': PackageVersion,
            'setup': SetUp,

            'accept': PackageAccept,
            'as-json': PackageAsJson,
            'canonize': PackageCanonical,
            'clone': ClonePackage,
            'compare': PackageCompare,
            'create': PackageCreate,
            'detail': PackageDetail,
            'extend': PackageExtend,
            'get': GetPackage,
            'install': InstallPackage,
            'list': PackageList,
            'preview': PackagePreview,
            'publish': PackagePublish,
            'pull': DownloadPackage,
            'push': PackageSave,
            'retract': PackageRetract,
            'reject': PackageReject,
            'revoke': PackageRevoke,
            'share': PackageShare,
            'snapshot': PackageSnapshot,
            'transfer': PackageTransfer,
            'up': PackageUpdate,
            'update': PackageUpdate,
            'validate': PackageValidate,
            'version': PackageVersion,
        }
        for k, v in commands.items():
            command.add_command(k, v)


def main(argv=sys.argv[1:],subcommand=False):
    """
    """
    blended_app = Blended()
    result = blended_app.run(argv)
    if subcommand: 
        return result

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
