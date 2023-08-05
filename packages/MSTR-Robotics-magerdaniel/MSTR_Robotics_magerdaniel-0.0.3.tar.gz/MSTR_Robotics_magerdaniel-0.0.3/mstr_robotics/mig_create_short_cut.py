from mstrio.connection import Connection
from mstrio.connection import get_connection
from mstrio.utils import parser
from mstrio.project_objects.datasets import SuperCube
from mstrio.api import reports
from mstrio.api import projects
from mstrio.api import objects as api_obj
from mstrio.project_objects import report
from mstrio.object_management import object
from mstrio.object_management import folder
from datetime import datetime
import pandas as pd
import json


class prepare_mig_obj():

    def set_env_var(self, chg_log_rep_proj_id=None,chg_log_report_id=None,
                    chg_log_from_date_prompt_id=None,chg_log_to_date_prompt_id=None,
                    chg_log_proj_prompt_id=None,short_cut_proj_id=None, chg_log_proj_name=None,
                    short_cut_folder_id=None, chg_log_from_date=None,
                    chg_log_to_date=None, conn_det=None,migration_folder_id=None,
                     mtdi_id=None,cube_name=None):
        self.chg_log_rep_proj_id = chg_log_rep_proj_id
        self.chg_log_report_id = chg_log_report_id  # 4
        self.chg_log_from_date_prompt_id = chg_log_from_date_prompt_id
        self.chg_log_to_date_prompt_id = chg_log_to_date_prompt_id
        self.chg_log_proj_prompt_id = chg_log_proj_prompt_id
        self.short_cut_proj_id = short_cut_proj_id
        self.chg_log_proj_name = chg_log_proj_name
        self.short_cut_folder_id = short_cut_folder_id
        self.chg_log_from_date = chg_log_from_date
        self.chg_log_to_date = chg_log_to_date
        self._stop_execution_fg = False
        self.i_object = object
        self.i_api_obj = api_obj
        self.i_reports = reports
        self.i_parser = parser
        self.i_datetime = datetime
        self.conn_det=conn_det
        self.conn = self.get_conn()
        self.migration_folder_id=migration_folder_id
        self.mtdi_id=mtdi_id
        self.cube_name=cube_name
        self.rep_col_names=['transaction_id','project_id','project_name','user_id','username','comment_val',
                            'object_id','object_type','subtype','object_name','transaction_timestamp','user_login',
                            'transaction_name','transaction_type','transaction_source','transaction_project_id','foder_name']


    def logger(func):
        def try_func(*args, **kwargs):

            try:
                result =func(*args, **kwargs)
                log_step = {"step": func.__name__, "result":result, "exe_time": datetime.now()}
                print(log_step)
                return result
            except Exception as err:
                desc = ""
                if func.__name__ == 'get_conn':
                    desc = "Login credentials where wrong. Otherwise check code :-)"
                if func.__name__ == 'bld_chg_log_report_df':
                    desc = "Report execution failed or no changes identitfied to fetch changes failed."
                if func.__name__ == '_get_project_id':
                    desc = "Project not found"
                if func.__name__ == '_open_Instance':
                    if e.args[0].__contains__("ERR004"):
                        desc = f'Please check the access to the change log report ' \
                               f'(id:"{self.chg_log_report_id}" ) in project:" ' \
                               f'self.chg_log_rep_proj_id = "{self.chg_log_rep_proj_id}""'

                log_step = {"step": func.__name__, "desc": desc, "err": err, "exe_time": datetime.now()}
                print(log_step)
                raise SystemExit()

        return try_func

    def get_conn(self):
        if self.conn_det:
            conn = Connection(base_url=self.conn_det["base_url"], username=self.conn_det["username"],
                              password=self.conn_det["password"], project_id=self.chg_log_rep_proj_id)
            conn.headers['Content-type'] = "application/json"
            return conn

        if 'workstationData' in locals():
            print("halloWorsk")
            conn = get_connection(workstationData)
            conn.headers['Content-type'] = "application/json"
            return conn
        return None

    @logger
    def bld_chg_log_report_df(self, instance_id=None):
        report_ds=self.i_reports.report_instance_id(connection=self.conn, report_id=self.chg_log_report_id, instance_id=instance_id)
        report_dict=self.i_parser.Parser(report_ds.json())._Parser__map_attributes(report_ds.json())
        report_list=self.read_obj(report_dict)
        report_df = pd.DataFrame(report_list,columns =self.rep_col_names)
        self.cube_upload(report_df, "changes")
        return report_df

    @logger
    def bld_short_cut(self, short_cut_folder_j=None, short_cut_url=None, obj=None, desc_str=None):
        short_cut_obj_j = self._cr_short_cut(obj=obj)
        base_obj = object.Object(connection=self.conn, type=18, id=short_cut_obj_j.json()["id"])
        new_name = obj[1] + "__" + obj[3] + "__" + self._bld_mstr_obj_guid(obj[2])
        self._rename_shortCut(base_obj=base_obj, new_name=new_name, desc_str=desc_str)

    @logger
    def get_folder_obj_l(self):
        i_folder = folder.Folder(connection=self.conn, id=self.short_cut_folder_id)
        existing_obj_l = i_folder.get_contents(to_dictionary=True)
        return existing_obj_l

    @logger
    def clean_shortcut_folder(self):
        existing_obj_l = self.get_folder_obj_l()
        obj_l = self._get_id_from_obj_l(dict_l=existing_obj_l, key_col="id")
        self._delete_object(existing_obj_l=existing_obj_l, new_short_cut_id=obj_l)

    @logger
    def bld_short_cuts(self, chg_log_report_df=None):
        short_cut_col = chg_log_report_df.groupby(["user_id", "user_login", "object_id", "object_name", "object_type"])[
            "transaction_id"].agg("count").reset_index()
        self.clean_shortcut_folder()
        for index, obj in short_cut_col.iterrows():
            desc_str = self._bld_desc_str(short_cut_col.loc[short_cut_col["OBJECT_ID"] == obj[2]])
            short_cut_folder_j = f'{{"folderId": "{self.short_cut_folder_id}"}}'
            short_cut_url = f'{self.conn_det["base_url"]}/objects/{self._bld_mstr_obj_guid(obj[2])}/type/{obj[4]}/shortcuts'
            self.bld_short_cut(short_cut_folder_j=short_cut_folder_j, short_cut_url=short_cut_url, obj=obj,
                               desc_str=desc_str)

    @logger
    def _get_id_from_obj_l(self, dict_l=None, key_col=None):
        key_val_l = []
        for o in dict_l:
            key_val_l.append(o[key_col])
        return key_val_l

    @logger
    def _set_inst_prompt_ans(self, instance_id=None):
        prompt_answ_url = f'{self.conn_det["base_url"]}/reports/{self.chg_log_report_id}/instances/{instance_id}/prompts/answers'
        ret_prompt_ans = self.conn.put(prompt_answ_url, data=self._build_val_answ())
        return ret_prompt_ans

    @logger
    def _get_project_id(self):
        resp_project = projects.get_project(connection=self.conn, name=self.chg_log_proj_name)
        return resp_project

    @logger
    def _open_Instance(self):
        rep_chg_log_inst = self.i_reports.report_instance(connection=self.conn, report_id=self.chg_log_report_id)
        self._stop_execution_fg = False
        return rep_chg_log_inst.json()["instanceId"]

    @logger
    def _bld_desc_str(self, all_changes=None):
        desc_str = ""
        all_changes_sum = all_changes.groupby(["user_id", "user_login", "object_id", "object_name", "object_type"])[
            "transaction_id"].agg("sum").reset_index()
        for index, s in all_changes.iterrows():
            desc_str += s["user_login"] + " (" + str(s["transaction_id"]) + "), "
        return desc_str

    @logger
    def _rename_shortCut(self, base_obj=None, new_name=None, desc_str=""):
        base_obj.alter(name=new_name, description=desc_str)
        return

    @logger
    def _delete_object(self, existing_obj_l=None, new_short_cut_id=None):
        for o in existing_obj_l:
            if o["id"] != new_short_cut_id:
                ddd = self.i_api_obj.delete_object(connection=self.conn, id=self._bld_mstr_obj_guid(o["id"])
                                                   , object_type=o["type"])
        return

    @logger
    def _cr_short_cut(self, obj=None):
        short_cut_folder_j = f'{{"folderId": "{self.short_cut_folder_id}"}}'
        short_cut_url = f'{self.conn_det["base_url"]}/objects/{self._bld_mstr_obj_guid(obj[2])}/type/{str(obj[4])}/shortcuts'
        short_cut_obj_j = self.conn.post(short_cut_url, data=short_cut_folder_j)
        return short_cut_obj_j

    #@logger
    def _bld_mstr_obj_guid(self, obj_md_id=None):
        # in the MSTR MD, for what ever reason, they're changin
        # 2276AC06-7A55-473C-9AC4-35A4E28C8021
        # 2276AC06473C7A55A435C49A21808CE2
        mstr_obj_guid = obj_md_id[0:8]
        mstr_obj_guid += obj_md_id[14:18]
        mstr_obj_guid += obj_md_id[9:13]
        mstr_obj_guid += obj_md_id[26:28]
        mstr_obj_guid += obj_md_id[24:26]
        mstr_obj_guid += obj_md_id[21:23]
        mstr_obj_guid += obj_md_id[19:21]
        mstr_obj_guid += obj_md_id[34:36]
        mstr_obj_guid += obj_md_id[32:34]
        mstr_obj_guid += obj_md_id[30:32]
        mstr_obj_guid += obj_md_id[28:30]
        return mstr_obj_guid

    @logger
    def _build_val_answ(self):
        prompt_ans = f'{{"key":"{self.chg_log_proj_prompt_id}@0@10","type":"VALUE","answers": "{self.chg_log_proj_name}"}},'
        prompt_ans += f'{{"key":"{self.chg_log_from_date_prompt_id}@0@10","type":"VALUE","answers": "{self.chg_log_from_date}"}},'
        prompt_ans += f'{{"key":"{self.chg_log_to_date_prompt_id}@0@10","type":"VALUE","answers": "{self.chg_log_to_date}"}}'
        prompt_ans = f'{{"prompts":[{prompt_ans}]}}'
        return prompt_ans

    def main(self):

        print("hallo Daniel")
        # conn=self.get_conn()
        self.chg_log_proj_name = self.chg_log_proj_name
        # instance_id=self.get_change_log()
        self.conn.headers["X-MSTR-ProjectID"] = self.short_cut_proj_id
        instance_id = self._open_Instance()
        self._set_inst_prompt_ans(instance_id=instance_id)
        #re = self.i_reports.get_prompted_instance(connection=self.conn, report_id=self.chg_log_report_id,
        #                                          instance_id=instance_id)
        report_df = self.bld_chg_log_report_df(instance_id)
        self.bld_short_cuts(chg_log_report_df=report_df)
        return

    def _set_proj_g(self, proj_id=None):
        self.conn.headers["X-MSTR-ProjectID"] = proj_id

    def _rem_last_char(self, str_, i=1):
        return str_[:-i]

    def cube_upload(self,load_df,tbl_name,updatePolicy="REPLACE",cube_name=None,folder_id=None,mtdi_id=None):
        if mtdi_id ==None:
            ds = SuperCube(connection=self.conn, name=self.cube_name)
            ds.add_table(name=tbl_name, data_frame=load_df, update_policy="replace")
            ds.create(folder_id=self.migration_folder_id)
            mtdi_id=ds.id
        else:
            ds = SuperCube(connection=self.conn, id=self.mtdi_id)
            ds.add_table(name=tbl_name, data_frame=load_df, update_policy=updatePolicy)
            ds.update()
            mtdi_id=ds.id
        return ds.id

    def bld_obj_path(self,fld_d=None,proj_id=None,proj_name=None):
        path_s="\\"
        for f in fld_d:
            #do not include project in the path
            if f["name"] != proj_name:
                path_s += f["name"] + "\\"

        path_s= self._rem_last_char(path_s)
        return path_s

    def bld_obj_l(self,obj_d,proj_g):
        task_sid = 80
        val_l = []
        obj_row_l = [proj_g,
                     str(obj_d.get('id'))
                     ,str(obj_d.get('version'))
                     ,str(obj_d.get('name'))
                     ,str(self.bld_obj_path(fld_d=obj_d["ancestors"], proj_id=self.short_cut_proj_id,proj_name=self.chg_log_proj_name ))
                     ,str(obj_d.get('type'))
                     ,str(obj_d.get('subtype'))
                     ,str(obj_d["owner"].get('id'))
                     ,str(obj_d["owner"].get('name'))
                     ]
        val_l.append(self.merge_val_l(obj_row_l))
        #print("project: " + proj_g + "object: " + str(obj_d.get('id')) )
        return val_l
    """ 
        ['transaction_id', 'project_id', 'project_name', 'user_id', 'username', 'comment_val',
         'object_id', 'object_type', 'subtype', 'object_name', 'transaction_timestamp', 'user_login',
         'transaction_name', 'transaction_type', 'transaction_source', 'transaction_project_id']
    """

    def read_obj(self,report_dict=None):
        transaction_id_ind = 0
        project_id_ind = 1
        project_name_ind = 2
        user_id_ind = 3
        username_ind = 4
        comment_val_ind = 5
        object_id_ind = 6
        object_type_ind = 7
        subtype_ind = 8
        object_name_ind = 9
        transaction_timestamp_ind = 10
        user_login_ind = 11
        transaction_name_ind = 12
        transaction_type_ind = 13
        transaction_source_ind = 14
        transaction_project_id_ind = 15

        obj_g_ind=6
        obj_typ_ind=7
        val_l = []
        all_obj_l = []
        cnt_obj = 0

        for o in report_dict:
            self._set_proj_g(self._bld_mstr_obj_guid(o[project_id_ind]))
            #self.MstrConn.cHeaders.update({'X-MSTR-ProjectID': o[proj_g_ind] })
            obj_d =  self.i_api_obj.get_object_info(connection=self.conn, id=self._bld_mstr_obj_guid(o[obj_g_ind]),
                                                    object_type=o[obj_typ_ind],
                                                    project_id=self._bld_mstr_obj_guid(o[project_id_ind]))

            #obj_l=self.bld_obj_l(obj_d=obj_d.json(),proj_g=self._bld_mstr_obj_guid(o[project_id_ind]))

            if obj_d.status_code == 200:
               val_l.append(o[transaction_id_ind])
               val_l.append(self._bld_mstr_obj_guid(o[project_id_ind]))
               val_l.append(o[project_name_ind])
               val_l.append(self._bld_mstr_obj_guid(o[user_id_ind]))
               val_l.append(o[username_ind])
               val_l.append(o[comment_val_ind])
               val_l.append(self._bld_mstr_obj_guid(o[object_id_ind]))
               val_l.append(o[object_type_ind])
               val_l.append(o[subtype_ind])
               val_l.append(o[object_name_ind])
               val_l.append(o[transaction_timestamp_ind])
               val_l.append(o[user_login_ind])
               val_l.append(o[transaction_name_ind])
               val_l.append(o[transaction_type_ind])
               val_l.append(o[transaction_source_ind])
               val_l.append(self._bld_mstr_obj_guid(o[transaction_project_id_ind]))
               val_l.append(str(self.bld_obj_path(fld_d=obj_d.json()["ancestors"], proj_id=self.short_cut_proj_id,proj_name=self.chg_log_proj_name )))
               cnt_obj +=+1
               all_obj_l.append(val_l)
               val_l=[]

        return all_obj_l


if __name__ == "__main__":
    """
    username = "Administrator"
    password = "IBCS"
    base_url = "http://85.214.60.83:8080/MicroStrategyLibrary/api"
    conn_det = {"username": username, "password": password,
                "base_url": base_url}
    # conn_det=None
    chg_log_from_date = "2022-11-01"
    chg_log_to_date = "2022-11-06"
    chg_log_proj_name = "MicroStrategy Tutorial_"
    short_cut_proj_id = "4CD4CC13436857E505C9CD93F0013FCE"
    short_cut_folder_id = "3E256FA7462A5C766FD720847491B8D1"
    migration_folder_id ="354E7E684B32AF5A3B037CAAA6C1D541"
    mtdi_id = "" #"E37952C94F2195BF15BF6B953C84AD58"
    cube_name = "TestCube"
    inst_pre = prepare_mig_obj()
    inst_pre.set_env_var(short_cut_proj_id=short_cut_proj_id, chg_log_proj_name=chg_log_proj_name,
                     short_cut_folder_id=short_cut_folder_id, chg_log_from_date=chg_log_from_date,
                     chg_log_to_date=chg_log_to_date, conn_det=conn_det,migration_folder_id=migration_folder_id,
                     mtdi_id=mtdi_id,cube_name=cube_name    )
    inst_pre.main()
    """
