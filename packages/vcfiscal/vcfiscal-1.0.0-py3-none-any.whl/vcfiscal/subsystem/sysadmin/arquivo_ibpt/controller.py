import flask

from viggocore.subsystem.file import controller
from viggocore.subsystem.file.controller import get_bad_request


class Controller(controller.Controller):

    def create(self, **kwargs):
        sigla_uf = flask.request.form.get('sigla_uf', None)
        if not sigla_uf:
            return get_bad_request('sigla_uf é obrigatório')

        kwargs['sigla_uf'] = sigla_uf

        return super().create(**kwargs)
        # try:
        #     file = flask.request.files.get('file', None)
        #     if not file:
        #         return get_bad_request('file é obrigatório')
        #
        #     domain_id = self.get_domain_id()
        #     if not domain_id:
        #         return get_bad_request(
        #             'Não foi possível determinar o domain_id')
        #
        #     sigla_uf = flask.request.form.get('sigla_uf', None)
        #     if not sigla_uf:
        #         return get_bad_request('sigla_uf é obrigatório')
        #
        #     user_id = self.get_token(self.get_token_id()).user_id
        #     if not user_id:
        #         return get_bad_request()
        #
        #     entity = self.manager.create(file=file, domain_id=domain_id,
        #                                  sigla_uf=sigla_uf, user_id=user_id)
        # except exception.ViggoCoreException as exc:
        #     return flask.Response(response=exc.message,
        #                           status=exc.status)
        #
        # response = {self.resource_wrap: entity.to_dict()}
        #
        # return flask.Response(response=json.dumps(response, default=str),
        #                       status=201,
        #                       mimetype="application/json")
