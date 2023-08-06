from flask.globals import current_app
from viggocore.celery import celery, decide_on_run
from vcfiscal.subsystem.sysadmin.arquivo_sync.sync_managers.sync_manager_ibpt \
    import SyncManagerIBPT


@decide_on_run
@celery.task
def process_arquivo_sync(filename: str,
                         upload_folder: str,
                         user_id: str,
                         entity_name: str,
                         sigla_uf: None) -> None:
    api = current_app.api_handler.api()

    if entity_name == 'ibpt':
        sync_manager_ibpt = SyncManagerIBPT(
            api, sigla_uf, filename, upload_folder, user_id)
        sync_manager_ibpt.sincronizar_ibpt()
    elif entity_name == 'cfop':
        pass
    elif entity_name == 'cest':
        pass
