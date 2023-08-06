from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import status_me


class NlpLaYouTlmController(ServiceInterface):
	def __init__(self, check_result, service_path):
		super(NlpLaYouTlmController, self).__init__(check_result, service_path)
		self.tf_name = "nlp-layoutlm"

	@status_me("nlp_layoutlm")
	def push_nlp_layoutlm_images(self):
		self.push_images(self.project)

	@status_me("nlp_layoutlm")
	def start_nlp_layoutlm_service(self):
		self._create_namespace(namespaces=self.namespaces,
		                       istio_injection_namespaces=self.istio_injection_namespaces)
		self.start_service(project=self.project, version=self.private_deploy_version, tf_name=self.tf_name)

	@status_me("nlp_layoutlm")
	def prepare_nlp_layoutlm_data(self):
		self.prepare_data(project=self.project)

	def run(self):
		self.push_nlp_layoutlm_images()
		self.start_nlp_layoutlm_service()
		self.prepare_nlp_layoutlm_data()
