from flask.globals import current_app
from viggocore.celery import celery, decide_on_run
from vcfiscal.subsystem.sysadmin.ibpt_sync.sync_manager import SyncManager


@decide_on_run
@celery.task
def process_arquivo_ibpt(sigla_uf: str,
                         filename: str,
                         upload_folder: str,
                         user_id: str) -> None:
    api = current_app.api_handler.api()
    sync_manager = SyncManager(api, sigla_uf, filename, upload_folder,
                               user_id)
    sync_manager.sincronizar_ibpt()
