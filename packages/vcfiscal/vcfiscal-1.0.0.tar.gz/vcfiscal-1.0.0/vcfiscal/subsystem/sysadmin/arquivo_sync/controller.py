import flask

from viggocore.subsystem.file import controller
from viggocore.subsystem.file.controller import get_bad_request


class Controller(controller.Controller):

    def create(self, **kwargs):
        sigla_uf = flask.request.form.get('sigla_uf', None)
        entity_name = flask.request.form.get('entity_name', None)
        if not sigla_uf and entity_name == 'ibpt':
            return get_bad_request('sigla_uf é obrigatório no sync de ibpt')

        kwargs['sigla_uf'] = sigla_uf
        kwargs['entity_name'] = entity_name

        return super().create(**kwargs)
