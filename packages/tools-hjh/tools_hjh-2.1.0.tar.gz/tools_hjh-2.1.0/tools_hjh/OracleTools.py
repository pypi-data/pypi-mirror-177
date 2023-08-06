# coding:utf-8
from tools_hjh import other as tools
from tools_hjh.DBConn import DBConn
from tools_hjh.DBConn import QueryResults
from tools_hjh.MemoryDB import MemoryDB


def main():
    rows = []
    for idx in range(0, 10):
        row = (idx, idx, idx)
        rows.append(row)
    testDB = DBConn('sqlite', db='test.ora_conn')
    num = testDB.insert('t1', rows, 'c1')
    print(num)
    testDB.close()


class OracleTools:
    """ 用于Oracle的工具类 """

    @staticmethod
    def desc(ora_conn, username, table):
        """ 类似于sqlplus中的desc命令 """
        username = username.upper()
        table = table.upper()
        sql = '''
            select column_name, 
                case 
                    when data_type = 'VARCHAR2' or data_type = 'CHAR' or data_type = 'VARCHAR' then 
                        data_type || '(' || data_length || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale > 0 then 
                        data_type || '(' || data_precision || ', ' || data_scale || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale = 0 then 
                        data_type || '(' || data_precision || ')'
                    when data_type = 'NUMBER' and data_precision = 0 and data_scale = 0 then 
                        data_type
                    else data_type 
                end column_type
            from dba_tab_cols where owner = ? and table_name = ? and column_name not like '%$%' order by column_id
        '''
        tab = ''
        cols_ = ora_conn.run(sql, (username, table)).get_rows()
        lenNum = 0
        for col_ in cols_:
            if lenNum < len(col_[0]):
                lenNum = len(col_[0])
        for col_ in cols_:
            tablename = col_[0]
            typestr = col_[1]
            spacesnum = lenNum - len(tablename) + 1
            colstr = tablename + ' ' * (spacesnum) + typestr
            tab = tab + colstr + '\n'
        return tab
    
    @staticmethod
    def get_ddl(ora_conn, username, table):
        """ 需要dba权限，得到目标user.table的单元性的建表语句，包括约束，索引和注释等 """
        username = username.upper()
        table = table.upper()
        rssqls = []
        # 建表
        rssqls.append('create table ' + username + '.' + table + '(test_col number)')
        # 按顺序建列
        sql = '''
            select column_name, 
                case 
                    when data_type = 'VARCHAR2' or data_type = 'CHAR' or data_type = 'VARCHAR' or data_type = 'NVARCHAR2' then 
                        data_type || '(' || data_length || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale > 0 then 
                        data_type || '(' || data_precision || ', ' || data_scale || ')'
                    when data_type = 'NUMBER' and data_precision > 0 and data_scale = 0 then 
                        data_type || '(' || data_precision || ')'
                    when data_type = 'NUMBER' and data_precision = 0 and data_scale = 0 then 
                        data_type
                    else data_type 
                end column_type
            from dba_tab_cols where owner = ? and table_name = ? and column_name not like '%$%' order by column_id
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' add ' + r[0] + ' ' + r[1].strip())
        rssqls.append('alter table ' + username + '.' + table + ' drop column test_col')
        # 建主键
        sql = '''
            select t.constraint_name, to_char(wm_concat(t2.column_name)) cols
            from dba_constraints t, dba_cons_columns t2
            where t.owner = ?
            and t.table_name = ?
            and t.constraint_name = t2.constraint_name
            and t.table_name = t2.table_name
            and t.constraint_type = 'P'
            group by t.constraint_name
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' add constraint ' + r[0] + ' primary key(' + r[1] + ')')
        # 建非空约束
        sql = '''
            select t.search_condition
            from dba_constraints t, dba_cons_columns t2
            where t.owner = ?
            and t.table_name = ?
            and t.constraint_name = t2.constraint_name
            and t.table_name = t2.table_name
            and t.constraint_type = 'C'
            and t.search_condition is not null
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            if 'IS NOT NULL' in r[0]:
                col = r[0].split(' ')[0]
                rssqls.append('alter table ' + username + '.' + table + ' modify ' + col + ' not null')
        # 建唯一约束
        sql = '''
            select t.constraint_name, to_char(wm_concat(t2.column_name)) cols
            from dba_constraints t, dba_cons_columns t2
            where t.owner = ?
            and t.table_name = ?
            and t.constraint_name = t2.constraint_name
            and t.table_name = t2.table_name
            and t.constraint_type = 'U'
            group by t.constraint_name
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' add constraint ' + r[0] + ' unique(' + r[1] + ')')
        # 建默认值
        sql = '''
            select column_name, data_default
            from dba_tab_columns
            where owner = ? 
            and table_name = ? 
            and column_name not like '%$%'
            and data_default is not null
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            rssqls.append('alter table ' + username + '.' + table + ' modify ' + r[0] + ' default ' + r[1].strip())
        # 建普通索引
        sql = '''
            select t.index_name, to_char(wm_concat(t2.column_name)) cols
            from dba_indexes t, dba_ind_columns t2
            where t.owner = ? 
            and t.table_name = ? 
            and t.index_name = t2.index_name
            and t.owner = t2.table_owner
            and t.uniqueness = 'NONUNIQUE'
            and t.index_type = 'NORMAL'
            group by t.index_name
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            rssqls.append('create index ' + username + '.' + r[0] + ' on ' + username + '.' + table + '(' + r[1] + ')')
        # 建函数索引
        sql = '''
            select t.index_name, t3.column_expression
            from dba_indexes t, dba_ind_expressions t3
            where t.owner = ? 
            and t.table_name = ? 
            and t.index_name = t3.index_name
            and t.table_name = t3.table_name
            and t.owner = t3.table_owner
            and t.uniqueness = 'NONUNIQUE'
            and t.index_type = 'FUNCTION-BASED NORMAL'
            order by t3.column_position
        '''
        col, rows = ora_conn.run(sql, (username, table))
        mdb = MemoryDB()
        mdb.set('t_idx', col, rows)
        rs = mdb.ora_conn.run('select index_name, group_concat(column_expression) from t_idx group by index_name').get_rows()
        mdb.close()
        for r in rs:
            rssqls.append('create index ' + username + '.' + r[0] + ' on ' + username + '.' + table + '(' + r[1] + ')')
        # 建注释
        sql = '''
            select column_name, comments
            from dba_col_comments
            where owner = ? 
            and table_name = ? 
            and comments is not null
        '''
        for r in ora_conn.run(sql, (username, table)).get_rows():
            rssqls.append("comment on column " + username + "." + table + "." + r[0] + " is '" + r[1] + "'")
        # 建外键
        pass
        return rssqls
    
    @staticmethod
    def get_dbms_ddl(ora_conn, username, table):
        """ 得到目标user.table的的建表语句，直接调用dbms_metadata.get_ddl得到结果 """
        username = username.upper()
        table = table.upper()
        sql = '''
            select to_char(
                dbms_metadata.get_ddl('TABLE', ?, ?)
            ) from dual
        '''
        return ora_conn.run(sql, (table, username)).get_rows()[0]
    
    @staticmethod
    def compare_table(src_ora_conn, src_username, dst_ora_conn, dst_username):
        """ 比较两个不同用户下同名表表结构，输出不一致的表清单，和一段报告 """
        src_username = src_username.upper()
        dst_username = dst_username.upper()
        out = ''
        table_list = []
        sql = 'select table_name from dba_tables where owner = ?'
        srctabs = src_ora_conn.run(sql, (src_username,)).get_rows()
        for tab in srctabs:
            src_desc = OracleTools.desc(src_ora_conn, src_username, tab[0])
            dst_desc = OracleTools.desc(dst_ora_conn, dst_username, tab[0])
            if src_desc != dst_desc:
                table_list.append(tab[0])
                out = out + tools.line_merge_align(src_username + '.' + tab[0] + '\n' + src_desc
                                           , dst_username + '.' + tab[0] + '\n' + dst_desc
                                           , True) + '\n\n'
        return table_list, out
    
    @staticmethod
    def sync_table(src_ora_conn, src_username, dst_ora_conn, dst_username, table, mode=1):
        """ 同步表，mode：
        0：仅输出增量同步表结构的sql
        1：增量同步表结构
        2：重建表结构，不包含外键
        3：重建表，且同步数据，数据量大的问题暂没考虑 """
        report = ''
        if mode == 0:
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                report = report + sql + ';\n'
        if mode == 1:
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                try:
                    dst_ora_conn.run(sql)
                    report = report + 'ok:' + sql + '\n'
                except:
                    report = report + 'err:' + sql + '\n'
        if mode == 2:
            try:
                sql = 'drop table ' + dst_username + '.' + table
                dst_ora_conn.run(sql)
                report = report + 'ok:' + sql + '\n'
            except:
                report = report + 'err:' + sql + '\n'
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                dst_ora_conn.run(sql)
                report = report + 'ok:' + sql + '\n'
        if mode == 3:
            try:
                sql = 'drop table ' + dst_username + '.' + table + ' cascade constraints purge'
                # dst_ora_conn.run(sql)
                report = report + 'ok:' + sql + '\n'
            except:
                report = report + 'err:' + sql + '\n'
            sqls = OracleTools.get_ddl(src_ora_conn, src_username, table)
            for sql in sqls:
                sql = sql.replace(src_username + '.', dst_username + '.')
                try:
                    # dst_ora_conn.run(sql)
                    report = report + 'ok:' + sql + '\n'
                except:
                    report = report + 'err:' + sql + '\n'
            sql = 'select * from ' + src_username + '.' + table
            conn = src_ora_conn.dbpool.acquire()
            cur = conn.cursor()
            cur.execute(sql)
            while True:
                rs = cur.fetchone()
                if rs is not None:
                    pa = str(rs)
                    sql = 'insert into ' + dst_username + '.' + table + ' values' + pa
                    # dst_ora_conn.run(sql)
                    print(sql)
                else:
                    break
            cur.close()
            conn.close()
        return report
    
    @staticmethod
    def get_sids_by_host(host_conn):
        """ 根据给入的linux系统tools_hjh.SSHConn对象获取这台主机运行的全部SID实例名称 """
        try:
            sids = []
            pros = host_conn.exec_command("source .bash_profile && cd $ORACLE_HOME/dbs && ls -l init*.ora | awk '{print $9}'").split('\n')
            for pro in pros:
                sid = pro.replace('init', '').replace('.ora', '')
                if len(sid) > 0:
                    sids.append()
        except:
            sids = []
            pros = host_conn.exec_command("ps -ef | grep ora_smon | grep -v grep | awk '{print $8}'").split('\n')
            for pro in pros:
                sids.append(pro.replace('ora_smon_', ''))
        return sids

    @staticmethod
    def get_tablespace_state(dba_conn):
        """ 根据dba_extents查询用户、表空间、数据文件的占用情况，顺便统计用户状态，这里面会算入预分配块的占用 """
        sql = '''
            select (select utl_inaddr.get_host_address from dual) ip
            , (select global_name from global_name) server_name
            , t.owner
            , t.tablespace_name
            , t.file_id
            , (select t2.file_name from dba_data_files t2 where t2.file_id = t.file_id) file_name
            , (select sum(t2.bytes) / 1024 / 1024 from dba_data_files t2 where t2.file_id = t.file_id) all_size_m
            , max(nvl(t.block_id, 0)) * 8 / 1024 use_size_m
            , (select t2.account_status from dba_users t2 where t2.username = t.owner) user_status
            , (select to_char(nvl(t2.lock_date, t2.expiry_date), 'yyyy-mm-dd hh24:mi:ss') from dba_users t2 where t2.username = t.owner) lock_or_expiry_date
            from dba_extents t 
            group by t.owner, t.tablespace_name, t.file_id
        '''
        return dba_conn.run(sql)
    
    @staticmethod
    def get_tablespace_file_state(dba_conn):
        """ 根据dba_extents查询数据文件的占用情况，这里面会算入预分配块的占用 """
        ip = dba_conn.run("select utl_inaddr.get_host_address ip from dual").get_rows()[0][0]
        server_name = dba_conn.run("select global_name from global_name").get_rows()[0][0]
        sql = '''
            select t.tablespace_name
            ,t.file_name
            ,t.file_id 
            ,round(t.bytes / 1024 / 1024, 2) all_size
            from dba_data_files t
        '''
        rss = dba_conn.run(sql).get_rows()
        col = ('ip', 'server_name', 'tablespace_name', 'file_name', 'file_id', 'all_size', 'use_size')
        rows = []
        sql2 = "select block_id from (select t.* from dba_extents t where t.file_id = ? order by block_id desc) where rownum = 1"
        for rs in rss:
            tablespace_name = rs[0]
            file_name = rs[1]
            file_id = rs[2]
            all_size = rs[3]
            try:
                max_block_id = dba_conn.run(sql2, (file_id,)).get_rows()[0][0]
            except:
                max_block_id = 0
            use_size = round(max_block_id * 8 / 1024, 2)
            rows.append((ip, server_name, tablespace_name, file_name, file_id, all_size, use_size))

        return QueryResults(col, rows)

    @staticmethod
    def get_tablespace_file_state_fast(dba_conn):
        """ 根据dba_free_space查询数据文件的占用情况，这里面不会算入预分配块的占用 """
        sql = '''
            select (select utl_inaddr.get_host_address from dual) ip
            ,(select global_name from global_name) server_name
            ,b.tablespace_name
            ,b.file_name
            ,b.file_id
            ,round(b.bytes / 1024 / 1024, 2) all_size
            ,round((b.bytes - sum(nvl(a.bytes, 0))) / 1024 / 1024, 2) use_size
            from dba_free_space a, dba_data_files b
            where a.file_id(+) = b.file_id
            group by b.tablespace_name, b.file_name, b.bytes, b.file_id order by 6 desc
        '''
        return dba_conn.run(sql)
    
    @staticmethod     
    def expdp_user_scp_impdp(src_host_conn, src_dba_conn, src_ora_sid, src_ora_user, dst_host_conn, dst_dba_conn, dst_ora_sid, dump_tmp_py='/tmp/oracle_dump_py'):
        """ 
        0.需要事项创建好表空间
        1.源端和目标端新建 directory DUMP_TMP_PY /tmp/oracle_dump_py
        2.源端获取 需要导出用户的表空间名称和大小
        3.源端执行 expdp 导出数据文件到 DUMP_TMP_PY
        4.scp文件到目标端 dump_tmp_py
        5.目标端执行 impdp 导入数据文件
        """
        date_str = tools.locatdate()
        dump_filename = src_ora_user + '_' + date_str + '.dmp'
        dump_logname = src_ora_user + '_' + date_str + '.log'
        log = tools.Log('logs/expdp_scp_impdp.log')

        # 源端创建DUMP_TMP_PY
        src_host_ip = src_host_conn.host
        try:
            src_dba_conn.run('drop directory DUMP_TMP_PY')
            src_dba_conn.run("create directory DUMP_TMP_PY as '" + dump_tmp_py + "'")
            log.info('源端', src_host_ip, 'DUMP_TMP_PY 创建成功')
        except Exception as e:
            log.error('源端', src_host_ip, 'DUMP_TMP_PY 创建失败，程序终止', e)
            log.error(str(e))
            return
        
        # 目标端创建DUMP_TMP_PY
        dst_host_ip = dst_host_conn.host
        try:
            dst_dba_conn.run('drop directory DUMP_TMP_PY')
            dst_dba_conn.run("create directory DUMP_TMP_PY as '" + dump_tmp_py + "'")
            log.info('目标端', dst_host_ip, 'DUMP_TMP_PY 创建成功')
        except Exception as e:
            log.error('目标端', dst_host_ip, 'DUMP_TMP_PY 创建失败，程序终止', e)
            log.error(str(e))
            return
        
        # 源端导出dmp
        sh = '''
            rm -f ''' + dump_tmp_py + '''/{dump_filename}
            source ~/.bash_profile
            export ORACLE_SID={oracle_sid}
            expdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} schemas={src_ora_user} compression=all cluster=n parallel=4
        '''
        sh = tools.remove_leading_space(sh)
        sh = sh.replace('{oracle_sid}', src_ora_sid)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{src_ora_user}', src_ora_user)
        mess = src_host_conn.exec_script(sh)
        if 'successfully completed' in mess:
            log.info('源端', src_host_ip, 'DMP导出成功')
        else:
            log.error('源端', src_host_ip, 'DMP导出失败，程序终止')
            log.error(mess)
            return

        # scp到目标端
        sh = '''
            source ~/.bash_profile
            expect -c "
            spawn scp -P {dst_host_port} -r ''' + dump_tmp_py + '''/tmp/oracle_dump_py/{dump_filename} {dst_host_user}@{dst_host_ip}:''' + dump_tmp_py + '''/
            expect {
                \\"*assword\\" {set timeout 30; send \\"{dst_host_password}\\r\\";}
                \\"yes/no\\" {send \\"yes\\r\\"; exp_continue;}
            }
            expect eof"
        '''
        dst_host_port = dst_host_conn.port
        dst_host_user = dst_host_conn.username
        dst_host_password = dst_host_conn.password
        sh = tools.remove_leading_space(sh)
        sh = sh.replace('{dst_host_port}', dst_host_port)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{dst_host_user}', dst_host_user)
        sh = sh.replace('{dst_host_ip}', dst_host_ip)
        sh = sh.replace('{dst_host_password}', dst_host_password)
        mess = src_host_conn.exec_script(sh)
        if '100%' in mess:
            log.info('源端', src_host_ip, 'SCP成功')
        else:
            log.error('源端', src_host_ip, 'SCP失败，程序终止')
            log.error(mess)
            return
        
        # 目标端导入dmp
        sh = '''
            source ~/.bash_profile
            export ORACLE_SID={oracle_sid}
            impdp \\'/ as sysdba \\' directory=DUMP_TMP_PY dumpfile={dump_filename} logfile={dump_logname} schemas={src_ora_user} transform=segment_attributes:n table_exists_action=replace
        '''
        sh = tools.remove_leading_space(sh)
        sh = sh.replace('{oracle_sid}', dst_ora_sid)
        sh = sh.replace('{src_ora_user}', src_ora_user)
        sh = sh.replace('{dump_filename}', dump_filename)
        sh = sh.replace('{dump_logname}', dump_logname)
        mess = dst_host_conn.exec_script(sh)
        if 'completed' in mess:
            log.info('目标端', dst_host_ip, 'DMP导入结束')
        else:
            log.error('目标端', dst_host_ip, 'DMP导入失败，程序终止')
            log.error(mess)
            return


if __name__ == '__main__':
    main()
