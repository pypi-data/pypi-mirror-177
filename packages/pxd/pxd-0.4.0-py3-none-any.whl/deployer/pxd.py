#   Copyright [2013-2021], Alibaba Group Holding Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import click

from deployer.config.config import setup_pxd_context, Config
from deployer.pxc.polardbx_manager import create_tryout_pxc, list_all_pxc, delete_pxc, cleanup_all_pxc, create_full_pxc, \
    print_pxd_version, check_pxc


@click.group()
def main():
    pass


@click.command(help='Create a minimum PolarDB-X cluster on local machine for tryout.')
@click.option("-name", default="pxc-tryout", help="PolarDB-X Cluster name, default: pxc-tryout")
@click.option("-cn_replica", default=1, help='cn node count')
@click.option("-cn_version", default="latest", help='cn node version')
@click.option("-dn_replica", default=1, help='dn node count')
@click.option("-dn_version", default="latest", help='dn node version')
@click.option("-cdc_replica", default=1, help='cdc node count')
@click.option("-cdc_version", default="latest", help='cdc node version')
@click.option("-repo", default="polardbx/", help="docker repo url, default is docker hub")
@click.option("-leader_only", default=True, help="create gms and dn with single node by default, otherwise a x-paxos "
                                                 "cluster")
@click.option("-debug", "-d", default=False, help='debug mode for troubleshooting')
@click.option("-ssh_port", default=22, help='debug mode for troubleshooting')
@click.option("-pull_latest_images", default=True, help='pull latest images, if false will use local image')
def tryout(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version, repo, leader_only, debug,
           ssh_port, pull_latest_images):
    setup_pxd_context()
    Config.instance().load_config(CN_IMAGE_VERSION=cn_version, DN_IMAGE_VERSION=dn_version,
                                  CDC_IMAGE_VERSION=cdc_version, DOCKER_REPO_URL=repo,
                                  DEBUG_MODE=debug, SSH_PORT=ssh_port, PULL_LATEST_IMAGES=pull_latest_images)
    create_tryout_pxc(name, cn_replica, cn_version, dn_replica, dn_version, cdc_replica, cdc_version, leader_only)


@click.command(help="Create a full PolarDB-X cluster on multi hosts.")
@click.option("-file", "-f", default=None, help='PolarDB-X cluster topology yaml file')
@click.option("-cn_version", default="latest", help='cn node version')
@click.option("-dn_version", default="latest", help='dn node version')
@click.option("-cdc_version", default="latest", help='cdc node version')
@click.option("-repo", default="polardbx/", help="docker repo url, default is docker hub")
@click.option("-debug", "-d", default=False, help='debug mode for troubleshooting')
@click.option("-ssh_port", default=22, help='ssh port')
@click.option("-pull_latest_images", default=True, help='pull latest images, if false will use local image')
@click.option("-mycnf_template", default="", help='my.cnf template file')
def create(file, cn_version, dn_version, cdc_version, repo, debug, ssh_port, pull_latest_images, mycnf_template):
    setup_pxd_context()
    Config.instance().load_config(CN_IMAGE_VERSION=cn_version, DN_IMAGE_VERSION=dn_version,
                                  CDC_IMAGE_VERSION=cdc_version, DOCKER_REPO_URL=repo,
                                  DEBUG_MODE=debug, SSH_PORT=ssh_port,
                                  PULL_LATEST_IMAGES=pull_latest_images,
                                  MYCNF_TEMPLATE=mycnf_template)

    create_full_pxc(file, cn_version, dn_version, cdc_version)


@click.command(help="List PolarDB-X clusters.")
def list():
    setup_pxd_context()
    list_all_pxc()


@click.command(help="Clean up all PolarDB-X clusters.")
def cleanup():
    setup_pxd_context()
    cleanup_all_pxc()

@click.command(help="Delete specific PolarDB-X cluster.")
@click.option("-ssh_port", default=22, help='debug mode for troubleshooting')
@click.argument("name", default=None)
def delete(name, ssh_port):
    setup_pxd_context()
    Config.instance().load_config(SSH_PORT=ssh_port)
    delete_pxc(name)

@click.command(help="Print pxd version.")
def version():
    print_pxd_version()


@click.command(help="Check dn leader.")
@click.argument("name", default=None)
@click.option("-t", "--type", default=None, help='check cn or dn, values: [cn, dn]')
@click.option("-r", "--repair", default=False, help='set dn leader to correct container')
def check(name, type, repair):
    setup_pxd_context()
    check_pxc(name, type, repair)


main.add_command(tryout)
main.add_command(create)
main.add_command(list)
main.add_command(cleanup)
main.add_command(delete)
main.add_command(version)
main.add_command(check)

if __name__ == '__main__':
    main()
