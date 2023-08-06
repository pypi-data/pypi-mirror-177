import os
import csv
import uuid
from datetime import datetime
from viggocore.common.exception import BadRequest, NotFound
from vcfiscal.subsystem.parametrizacao.ncm.resource import NCM
from vcfiscal.subsystem.parametrizacao.ibpt.resource import IBPT
from vcfiscal.subsystem.parametrizacao.ibpt_ncm.resource import IBPTNCM
from vcfiscal.subsystem.sysadmin.ibpt_sync.resource import MessageType, \
    Status, IBPTSync


class SyncManager():

    def __init__(self, api, sigla_uf: str, filename: str, upload_folder: str,
                 user_id: str):
        self.api = api
        self.sigla_uf = sigla_uf
        self.user_id = user_id
        file = self.get_file(filename, upload_folder)

        # pegar as linhas do arquivo em listas para processar
        with open(file, mode='r', encoding='ISO-8859-1') as csv_file:
            # preparando as informações
            self.get_listas(csv_file)

    def sincronizar_ibpt(self):
        # montar a classe IBPTSync
        self.ibpt_sync = IBPTSync(uuid.uuid4().hex,
                                  sigla_uf=self.sigla_uf,
                                  created_at=datetime.now(),
                                  created_by=self.user_id)

        self.ibpt_sync.addMsg(
            MessageType.Info,
            self.make_msg('Iniciando a sincronização do IBPT')
        )

        # verificar se já tem sincronização para este arquivo
        self.check_ibpt_processado()

        if not self.ibpt_sync.contains_error():
            try:
                self.api.ibpt_syncs().driver.transaction_manager.count += 1
                # get ibpt
                ibpt = self.get_ibpt()

                if ibpt is not None:
                    self.ibpt_sync.ibpt_id = ibpt.id

                    # cadastrar os ncm
                    self.register_ncms(ibpt)

                    # cadastrar os nbs
                    # self.register_nbs(ibpt)

                    # cadastrar os lc116
                    # self.register_lc116(ibpt)
                self.api.ibpt_syncs().driver.transaction_manager.commit()
            except Exception:
                self.api.ibpt_syncs().driver.transaction_manager.rollback()
                self.api.ibpt_syncs().driver.transaction_manager.count = 0

        # cadastrar o IBPTSync
        if self.ibpt_sync.contains_error():
            self.ibpt_sync.ibpt_id = None
            self.ibpt_sync.status = Status.Erro
            self.ibpt_sync.addMsg(
                MessageType.Error,
                self.make_msg('Sincronização falhou!')
            )
        else:
            self.ibpt_sync.status = Status.Sucesso
            self.ibpt_sync.addMsg(
                MessageType.Info,
                self.make_msg('Sincronização concluida!')
            )

        self.api.ibpt_syncs().create(**self.ibpt_sync.to_dict())

    def get_now(self):
        return f'[{datetime.now()}] '

    def make_msg(self, msg: str):
        return self.get_now() + msg

    def get_file(self, filename: str, upload_folder: str):
        if not filename:
            raise BadRequest()

        file = os.path.join(upload_folder, filename)
        if not os.path.exists(file):
            error = NotFound()
            error.message = 'File {} Not Found'.format(filename)
            raise error

        return file

    def get_listas(self, csv_file):
        self.first_line_file = {}
        self.ncm_lines_file = []
        self.nbs_lines_file = []
        self.lc116_lines_file = []

        ibpt_file_lines = csv.DictReader(csv_file, delimiter=';')

        line_count = 0
        for ibpt_file_line in ibpt_file_lines:
            if line_count > 0:
                # INFO: o ibpt pode ter os seguintes tipos:
                #     0 -> NCM
                #     1 -> NBS
                #     2 -> LC116
                # monta a lista de ncm
                if ibpt_file_line['tipo'] == '0':
                    self.ncm_lines_file.append(ibpt_file_line)

                # monta a lista de nbs
                if ibpt_file_line['tipo'] == '1':
                    self.nbs_lines_file.append(ibpt_file_line)

                # monta a lista de lc116
                if ibpt_file_line['tipo'] == '2':
                    self.lc116_lines_file.append(ibpt_file_line)
            else:
                line_count += 1
                # pega a primeira linha do arquivo
                self.first_line_file = ibpt_file_line

    def get_ibpt(self):
        chave = self.first_line_file['chave']
        versao = self.first_line_file['versao']
        ibpts = self.api.ibpts().list(chave=chave, versao=versao)

        self.ibpt_sync.addMsg(MessageType.Info,
                              self.make_msg('Cadastrando IBPT {}.{} {}'.format(
                                chave, versao, self.sigla_uf)))
        try:
            if not ibpts:
                fonte = self.first_line_file['fonte']
                data_ini_vigencia = datetime.strptime(
                    self.first_line_file['vigenciainicio'], '%d/%m/%Y')
                data_fim_vigencia = datetime.strptime(
                    self.first_line_file['vigenciafim'], '%d/%m/%Y')

                ibpt = IBPT(
                    id=uuid.uuid4().hex,
                    data_ini=data_ini_vigencia,
                    data_fim=data_fim_vigencia,
                    chave=chave,
                    versao=versao,
                    fonte=fonte,
                    created_at=datetime.now(),
                    created_by=self.user_id)
                self.api.ibpts().create(**ibpt.to_dict())
            else:
                ibpt = ibpts[0]
        except Exception:
            ibpt = None
            self.ibpt_sync.addMsg(MessageType.Error,
                                  self.make_msg(
                                    'Erro ao cadastrar o IBPT {}.{} {}'.format(
                                        chave, versao, self.sigla_uf)))

        return ibpt

    def check_ibpt_processado(self):
        # verifica se um mesmo arquivo com essa chave e versão já
        # foi sincronizado para essa uf
        filter_dict = {
            'chave': self.first_line_file['chave'],
            'versao': self.first_line_file['versao'],
            'sigla_uf': self.sigla_uf
        }
        # exists é 0 ou 1, 0 não existe e 1 para existe
        exists = self.api.ibpt_syncs().verify_sync(**filter_dict)

        if exists:
            msg = ('IBPT Sync já foi realizado para IBPT {}.{} {}')
            self.ibpt_sync.addMsg(
                MessageType.Error,
                self.make_msg(
                    msg.format(self.first_line_file['chave'],
                               self.first_line_file['versao'],
                               self.sigla_uf)))

    def get_ncm(self, ncm_line):
        # ex = None
        # if ibpt_ncm["ex"].strip() != '':
        #     ex = ibpt_ncm["ex"].strip()
        ex = ncm_line['ex'].strip()
        codigo = ncm_line['codigo']
        descricao = ncm_line['descricao']
        tipo = ncm_line['tipo']
        ncms = self.api.ncms().list(codigo=codigo, ex=ex)
        if not ncms:
            ncm = NCM(
                id=uuid.uuid4().hex,
                codigo=codigo,
                ex=ex,
                descricao=descricao,
                tipo=tipo,
                created_at=datetime.now(),
                created_by=self.user_id)
            self.api.ncms().create(**ncm.to_dict())
        else:
            ncm = ncms[0]

        return ncm

    def get_ibpt_ncm(self, ibpt_id, ncm_id, ncm_line):
        aliq_nac_fed = ncm_line['nacionalfederal']
        aliq_imp_fed = ncm_line['importadosfederal']
        aliq_est = ncm_line['estadual']
        aliq_mun = ncm_line['municipal']

        ibpt_ncms = self.api.ibpt_ncms().list(
            ibpt_id=ibpt_id, ncm_id=ncm_id, sigla_uf=self.sigla_uf)
        if not ibpt_ncms:
            ibpt_ncm = IBPTNCM(
                id=uuid.uuid4().hex,
                ibpt_id=ibpt_id,
                ncm_id=ncm_id,
                sigla_uf=self.sigla_uf,
                aliq_nac_fed=aliq_nac_fed,
                aliq_imp_fed=aliq_imp_fed,
                aliq_est=aliq_est,
                aliq_mun=aliq_mun,
                created_at=datetime.now(),
                created_by=self.user_id)
            self.api.ibpt_ncms().create(**ibpt_ncm.to_dict())
        else:
            ibpt_ncm = ibpt_ncms[0]

        return ibpt_ncm

    def register_ncms(self, ibpt):
        self.ibpt_sync.addMsg(
            MessageType.Info,
            self.make_msg(
                'Iniciando processamento dos ncm'))

        for ncm_line in self.ncm_lines_file:
            try:
                ncm = self.get_ncm(ncm_line)
                if ncm:
                    self.get_ibpt_ncm(ibpt.id, ncm.id, ncm_line)
            except Exception as e:
                msg = ('Error: codigo_ncm={}, \ndescricao={}')
                self.ibpt_sync.addMsg(
                    MessageType.Error,
                    self.make_msg(
                        msg.format(ncm_line['codigo'],
                                   str(e)[:150])))
                raise e

        self.ibpt_sync.addMsg(
            MessageType.Info,
            self.make_msg('Finalizado o processamento dos ncm'))
