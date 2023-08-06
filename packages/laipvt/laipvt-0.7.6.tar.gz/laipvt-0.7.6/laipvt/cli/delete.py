import os

from laipvt.handler.confighandler import CheckResultHandler
from laipvt.sysutil.gvalue import CHECK_FILE, LAIPVT_BASE_DIR, LOG_TO_TTY
from laipvt.sysutil.log import Logger
from laipvt.sysutil.ssh import SSHConnect


class DeletePackageHandler:
    """ 删除程序功能 """

    def __init__(self):
        # 获取前置检查结果
        self.check_result_file = CHECK_FILE
        self.check_result = CheckResultHandler(self.check_result_file)
        self.deploy_dir = self.check_result.deploy_dir
        self.servers = self.check_result.servers.servers
        self.servers_all_ip = self.check_result.servers.get_all_ip()
        self.python_path = "/usr/local/python-3.7.6"
        self.laipvt_base_path = LAIPVT_BASE_DIR
        self.laipvt_middleware_path = "{}/middleware".format(self.laipvt_base_path)
        self.tmp_path = "/tmp/rpa"

    def stopserver(self, server: str):
        """ 停止服务 """
        cmd = "systemctl stop {server}".format(server=server)
        return cmd

    def removedir(self, dir_path: str):
        """ 移动目录到/tmp/rpa下 """
        cmd = "mv {dir_path} {tmp}".format(dir_path=dir_path, tmp=self.tmp_path)
        return cmd

    def deldir(self, dir_path: str):
        """ 删除目录到/tmp/rpa下 """
        cmd = "rm -rf {dir_path}".format(dir_path=dir_path)
        return cmd

    def downserver(self, yaml_path: str):
        """ Down服务 """
        cmd = "docker-compose -f {path} down".format(path=yaml_path)
        return cmd

    def checkdirpath(self, dir_path: str):
        """ 检查目录是否存在 """
        if os.path.isdir(dir_path):
            return True
        return False

    def sshclient(self, cmd):
        """ 直接执行命令 """
        for server in self.servers:
            ip = server.d["ipaddress"]
            username = server.d["username"]
            password = server.d["password"]
            port = server.d["port"]
            ssh_cli = SSHConnect(hostip=ip, username=username, password=password, port=port)
            self.log.info("{} 执行 {} 命令".format(ip, cmd))
            ssh_cli.run_cmd(cmd)
            ssh_cli.close()


class DeleteMiddleware(DeletePackageHandler):
    """ 移除各中间件服务 """

    def __init__(self):
        super(DeleteMiddleware, self).__init__()
        self.log = Logger(
                tty=os.environ.get("LOG_TO_TTY", LOG_TO_TTY),
                log_name="delete_middleware.log",
                log_path="/tmp/log",
        ).get()

    def get_all_middleware_name(self):
        """ 获取所有中间件的名称 """
        _path = self.laipvt_middleware_path
        if self.checkdirpath(_path):
            middleware = [os.path.splitext(fn)[0] for fn in os.listdir(_path)]
        return middleware

    def get_dockercompose_yaml(self, middleware_name):
        """ 获取docker-compose文件 """
        middleware_yaml = "{}/{}/{}".format(self.deploy_dir, middleware_name, "docker-compose.yml")
        return middleware_yaml

    def run(self):
        self.log.info("开始清除Middleware环境")
        middlewares = self.get_all_middleware_name()
        for name in middlewares:
            yaml_path = self.get_dockercompose_yaml(name)
            downcmd = self.downserver(yaml_path=yaml_path)
            mvcmd = self.deldir("{}/{}".format(self.deploy_dir, name))
            cmd = "{downcmd};{mvcmd}".format(downcmd=downcmd, mvcmd=mvcmd)
            self.sshclient(cmd)
        self.log.info("Middleware环境清理完成")


class DeleteKubernetes(DeletePackageHandler):
    """ 移除k8s """

    def __init__(self):
        super(DeleteKubernetes, self).__init__()
        self.kubernetes_path = ["/etc/kubernetes", "/var/lib/kubelet", "/var/lib/etcd", "~/.kube"]
        self.kubelet = "kubelet"
        self.tiller = "tiller"
        self.kubeadm_reset = "kubeadm reset -f"
        self.log = Logger(
                tty=os.environ.get("LOG_TO_TTY", LOG_TO_TTY),
                log_name="delete_k8s.log",
                log_path="/tmp/log",
        ).get()

    def run(self):
        self.log.info("开始清除Kubernetes环境")
        self.sshclient(self.kubeadm_reset)
        for path in self.kubernetes_path:
            cmd = self.deldir(path)
            self.sshclient(cmd)
        cmd = """cat > /tmp/clear_k8s << EOF
kubeadm reset -f
systemctl stop kubelet 
systemctl stop tiller
rm -rf /var/lib/cni
rm -rf /var/lib/kubelet
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
rm -rf /usr/lib/systemd/system/kubelet.service.d
rm -rf /opt/cni/bin
rm -rf /usr/bin/kubeadm
rm -f /lib/systemd/system/kubelet.service
EOF"""
        self.sshclient(cmd)
        self.sshclient("bash /tmp/clear_k8s && rm -f /tmp/clear_k8s")
        self.log.info("Kubernetes环境清理完成")


class DeleteDocker(DeletePackageHandler):
    """ 停止Docker并移除Docker """

    def __init__(self):
        super(DeleteDocker, self).__init__()
        self.docker_path = "{}/{}".format(self.deploy_dir, "Docker")
        self.log = Logger(
                tty=os.environ.get("LOG_TO_TTY", LOG_TO_TTY),
                log_name="delete_docker.log",
                log_path="/tmp/log",
        ).get()

    def run(self):
        self.log.info("开始清除Docker环境")
        cmd = """cat > /tmp/clear_docker << EOF
systemctl stop docker
rm -rf /var/lib/docker
ip link delete docker0
ip link delete kube-ipvs0
rm -f /usr/lib/systemd/system/containerd.service
rm -f /usr/lib/systemd/system/docker.socket
rm -f /usr/lib/systemd/system/docker.service
rm -f /usr/bin/docker
EOF"""
        self.log.info(cmd)
        self.sshclient(cmd)
        self.sshclient("bash /tmp/clear_docker && rm -f /tmp/clear_docker")
        self.log.info("Docker环境清理完成")


class DeleteAll(DeletePackageHandler):
    def __init__(self):
        super(DeleteAll, self).__init__()
        self.log = Logger(
                tty=os.environ.get("LOG_TO_TTY", LOG_TO_TTY),
                log_name="delete_all.log",
                log_path="/tmp/log",
        ).get()

    def Clear(self):
        """ 移除整个部署目录 """
        cmd1 = "{}".format(self.deldir(self.deploy_dir))
        self.log.info(cmd1)
        self.sshclient(cmd1)
        cmd2 = "{};{};{}".format(self.deldir(self.laipvt_base_path), self.deldir(self.python_path), self.deldir("/tmp/log"))
        self.log.info(cmd2)
        self.sshclient(cmd2)

    def run(self):
        """ 移除所有目录 """
        DeleteMiddleware().run()
        DeleteKubernetes().run()
        DeleteDocker().run()
        self.Clear()


def delete_main(args):
    if args.Middleware:
        """ 停止中间件服务并移除中间件目录 """
        DeleteMiddleware().run()

    if args.Docker:
        """ 移除Docker并停止Docker服务 """
        DeleteDocker().run()

    if args.Kubernetes:
        """ 移除K8S环境，并停止k8s服务 """
        DeleteKubernetes().run()

    if args.All:
        """ 移除所有环境 """
        DeleteAll().run()


if __name__ == "__main__":
    def delete_main(args):
        if args.Middleware:
            """ 停止中间件服务并移除中间件目录 """
            DeleteMiddleware().run()

        if args.Docker:
            """ 移除Docker并停止Docker服务 """
            DeleteDocker().run()

        if args.Kubernetes:
            """ 移除K8S环境，并停止k8s服务 """
            DeleteKubernetes().run()

        if args.All:
            """ 移除所有环境 """
            DeleteAll().run()
