# -*- coding: utf-8 -*-

_SfQyPgComparedSql ="""
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