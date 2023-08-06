# -*- coding: utf-8 -*-


class _QyPgSql:
    SfQyPgComparedSql = """
    with tmp_s1 as (
        select {join_list_str}
        ,{poly_list_str_s1}
        from (
            select {dim_list_str}
            ,{mea_list_str_s1}
            from {source_data} t
            {where_s1}
            group by {dim_list_str}
            ) t
        group by {join_list_str}
    ),tmp_s2 as (
        select {join_list_str}
        ,{poly_list_str_s2}
        from (
            select {dim_list_str}
            ,{mea_list_str_s2}
            from {source_data} t
            {where_s2}
            group by {dim_list_str}
            ) t
        group by {join_list_str}
    )
    select {join_list_str}
    ,case when s1.* is null then 1 else 0 end as is_s1null
    ,case when s2.* is null then 1 else 0 end as is_s2null
    ,{poly_list_str}
    ,{cp_mea_list_str}
    ,{result_mea_list_str}
    from tmp_s1 s1
    full join tmp_s2 s2 {using_str}
    """

    # 创建数据质量的配置表
    SfQyPgCreateQualityConfigSql = """
    -- 函数-触发更新操作时，用来执行update_time的更新
    CREATE OR REPLACE FUNCTION {table_name}_upd_time()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.update_time = floor(extract(epoch from now()));
        RETURN NEW;
    END;
    $$ language 'plpgsql'
    ;
    
    create table {table_name}(
        id serial PRIMARY KEY,
        task_group text,
        task_name text,
        source_data text,
        sql text,
        source_config_dict text,
        monitor_type text,
        feedback_code text,
        bot_dict_list text,
        parameter_dict text,
        create_time integer NOT NULL DEFAULT floor(extract(epoch from now())),
        update_time integer NOT NULL DEFAULT floor(extract(epoch from now()))
    );
    CREATE TRIGGER "update_time" BEFORE UPDATE ON {table_name}
        FOR EACH ROW
        EXECUTE PROCEDURE {table_name}_upd_time()
        ;
    """

    # 创建数据质量的日志表
    SfQyPgCreateQualityLogSql = """
    -- 函数-触发更新操作时，用来执行update_time的更新
    CREATE OR REPLACE FUNCTION {table_name}_upd_time()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.update_time = floor(extract(epoch from now()));
        RETURN NEW;
    END;
    $$ language 'plpgsql'
    ;
    
    create table {table_name}(
        id serial PRIMARY KEY,
        result_data text,
        create_time integer NOT NULL DEFAULT floor(extract(epoch from now())),
        update_time integer NOT NULL DEFAULT floor(extract(epoch from now()))
    );
    CREATE TRIGGER "update_time" BEFORE UPDATE ON {table_name}
        FOR EACH ROW
        EXECUTE PROCEDURE {table_name}_upd_time()
        ;
    """

    SfQyPgExistsTableSql = """
    select count(*) as cnt 
    from information_schema.tables 
    where table_schema='{schema_name}' 
        and table_type='BASE TABLE' 
        and table_name='{table_name}';
    """


class _QyMysqlSql:
    pass
