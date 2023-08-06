from __future__ import absolute_import
from __future__ import unicode_literals

import os
import requests
from minio import Minio
from laipvt.interface.middlewareinterface import MiddlewareInterface
from laipvt.handler.confighandler import CheckResultHandler
from laipvt.handler.middlewarehandler import MinioConfigHandler
from laipvt.sysutil.template import FileTemplate
from laipvt.sysutil.util import path_join, log, status_me, ssh_obj
from laipvt.helper.errors import Helper
from laipvt.model.server import ServerModel


class MinioController(MiddlewareInterface):
    def __init__(self, result: CheckResultHandler, handler: MinioConfigHandler, template: str):
        super(MinioController, self).__init__(result, handler, template)
        self.minio_cfg = MinioConfigHandler().get_config_with_check_result()
        self.minio_nginx_tmp = path_join("/tmp", "nginx-minio.conf")
        self.minio_nginx_template = path_join(self.template, "nginx-minio.tmpl")
        self.minio_nginx_file = path_join(self.deploy_dir, "nginx/http/nginx-minio.conf")
        self.minio_cfg["minio"]["ipaddress"] = self.handler.cfg["ipaddress"]

        self.docker_conf_tmpl = path_join(self.template, "init_readonly_user.sh")
        self.docker_conf_file_tmp = path_join("/tmp", "init_readonly_user.sh")
        self.docker_conf_file = path_join(self.base_dir, "init_readonly_user.sh")
        
        self.minio_service_file_template = path_join(self.template, "minio_service.tmpl")
        self.minio_service_file_dest = path_join("/tmp", "minio_service.yaml")
        self.minio_service_file_remote = path_join(self.base_dir, "svc", "minio_service.yaml")


    def generate_conf_file(self) -> bool:
        FileTemplate(self.minio_cfg, self.docker_conf_tmpl, self.docker_conf_file_tmp).fill()
        return True if os.path.isfile(self.docker_conf_file_tmp) else False

    def send_docker_conf_file(self):
        for server in self.master_server:
            log.info(Helper().SEND_FILE.format(self.docker_conf_file_tmp, server.ipaddress, self.docker_conf_file))
            ssh_cli = ssh_obj(ip=server.ipaddress, user=server.username, password=server.password, port=server.port)
            try:
                ssh_cli.put(self.docker_conf_file_tmp, self.docker_conf_file)
            except Exception as e:
                log.error(e)
                exit(2)
            finally:
                ssh_cli.close()

    def _proxy_on_nginx(self):
        FileTemplate(self.minio_cfg, self.minio_nginx_template, self.minio_nginx_tmp).fill()
        self.update_nginx_config()
        self.generate_docker_compose_file(self.minio_cfg)

    def _create_bucket(self, bucket: str):
        log.info(Helper().CREATE_BUCKET.format(bucket))
        try:
            self.endpoint = "{}:{}".format(self.minio_cfg["minio"]["lb"], self.minio_cfg["minio"]["nginx_proxy_port"])
            cli = Minio(
                self.endpoint,
                self.minio_cfg["minio"]["username"],
                self.minio_cfg["minio"]["password"],
                secure=False
            )
            if not cli.bucket_exists(bucket):
                cli.make_bucket(bucket)
                return True
        except Exception as e:
            log.error(e)
            exit(2)

    def create_minio_service_kubernetes(self):
        server = ServerModel(self.harbor_server)
        FileTemplate(self.minio_cfg, self.minio_service_file_template, self.minio_service_file_dest).fill()
        server.send_file(self.minio_service_file_dest, self.minio_service_file_remote)

        cmd = "kubectl apply -f {}".format(self.minio_service_file_remote)
        ssh_cli = ssh_obj(ip=self.harbor_server[0].ipaddress, user=self.harbor_server[0].username,
                          password=self.harbor_server[0].password, port=self.harbor_server[0].port)
        results = ssh_cli.run_cmd(cmd)
        if results["code"] != 0:
            log.error("{} {}".format(results["stdout"], results["stderr"]))
            exit(2)
            
    def check(self):
        super().wait_for_service_start()
        for ip in self.master_server:
            try:
                log.info(Helper().CHECK_MIDDLEWARE_SERVICE.format(self.middleware_name, ip.ipaddress,
                                                                  self.minio_cfg["minio"]["port"]))
                requests.get(
                    "http://{IP}:{PORT}/minio/health/live".format(
                        IP=ip.ipaddress, PORT=self.minio_cfg["minio"]["port"]
                    )
                )
                log.info(Helper().CHECK_MIDDLEWARE_SERVICE_PORT_SUCCEED.format(ip.ipaddress, self.minio_cfg["minio"]["port"]))
            except Exception as e:
                log.info(Helper().CHECK_MIDDLEWARE_SERVICE_PORT_FAILED.format(ip.ipaddress, self.minio_cfg["minio"]["port"]))
                log.error(e)
                exit(2)

    @status_me("middleware")
    def deploy_minio(self):
        if self.check_is_deploy(self.minio_cfg):
            self._proxy_on_nginx()
            self.send_docker_compose_file()
            self.generate_conf_file()
            self.send_docker_conf_file()
            self.start()
            self.check()
            self._create_bucket("mysql-backup")
        self.create_minio_service_kubernetes()

    def deploy(self, force=False):
        self.deploy_minio.set_force(force)
        self.deploy_minio()
