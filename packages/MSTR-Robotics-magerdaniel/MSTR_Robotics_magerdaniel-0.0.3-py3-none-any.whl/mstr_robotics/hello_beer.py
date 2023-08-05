import mig_create_short_cut

inst_pre = mig_create_short_cut.prepare_mig_obj()
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
migration_folder_id = "354E7E684B32AF5A3B037CAAA6C1D541"
mtdi_id = ""  # "E37952C94F2195BF15BF6B953C84AD58"

chg_log_rep_proj_id = "4CD4CC13436857E505C9CD93F0013FCE"
chg_log_report_id = "BD47C6554CD382D32A7535B2A2540944"
chg_log_from_date_prompt_id = "12B868354916C703B3404DA58A02E917"
chg_log_to_date_prompt_id = "3F2AF24F44758C11E4E5E895EB35666D"
chg_log_proj_prompt_id = "39CCD3724DFE6695752375A2104B98FA"
cube_name = "TestCube"

inst_pre.set_env_var(chg_log_rep_proj_id=chg_log_rep_proj_id,chg_log_report_id=chg_log_report_id,chg_log_from_date_prompt_id=chg_log_from_date_prompt_id,
                     chg_log_to_date_prompt_id=chg_log_to_date_prompt_id,chg_log_proj_prompt_id=chg_log_proj_prompt_id,
                     short_cut_proj_id=short_cut_proj_id, chg_log_proj_name=chg_log_proj_name,
                     short_cut_folder_id=short_cut_folder_id, chg_log_from_date=chg_log_from_date,
                     chg_log_to_date=chg_log_to_date, conn_det=conn_det, migration_folder_id=migration_folder_id,
                     mtdi_id=mtdi_id, cube_name=cube_name)
inst_pre.main()
