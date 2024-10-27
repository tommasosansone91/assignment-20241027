# these queries are also useful to query the database manually

GET_ALL_JOKES_EVEN_PRECEDENT_VERSIONS = """
select 
    * 
from 
    joke j
    join joke_version jv on(
            j.id = jv.joke_id
            )
where
    j.is_active = True
"""

GET_ALL_JOKES_LATEST_VERSIONS = """
WITH latest_joke_versions AS (
    SELECT 
        joke_id, 
        MAX(creation_timestamp) AS max_creation_timestamp
    FROM 
        joke_version
    GROUP BY 
        joke_id
)

SELECT 
    *
FROM 
    joke j
    JOIN joke_version jv 
        ON j.id = jv.joke_id
    JOIN latest_joke_versions ljv 
        ON 
            jv.joke_id = ljv.joke_id 
            AND jv.creation_timestamp = ljv.max_creation_timestamp
WHERE 
    j.is_active = TRUE
"""


GET_JOKES_BY_FREE_TEXT = """
WITH latest_joke_versions AS (
    SELECT 
        joke_id, 
        MAX(creation_timestamp) AS max_creation_timestamp
    FROM 
        joke_version
    GROUP BY 
        joke_id
)
,
latest_joke_and_versions AS (
    SELECT 
        *
    FROM 
        joke j
        JOIN joke_version jv 
            ON j.id = jv.joke_id
        JOIN latest_joke_versions ljv 
            ON 
                jv.joke_id = ljv.joke_id 
                AND jv.creation_timestamp = ljv.max_creation_timestamp
    WHERE 
        j.is_active = TRUE
)

select 
    * 
from 
    latest_joke_and_versions
where
    lower(content) like '%{}%'
    and is_active = True
"""


GET_LATEST_JOKE_VERSION_FOR_A_JOKE_ID = """
select 
    * 
from 
    joke j
    join joke_version jv on(
            j.id = jv.joke_id
            )
where
    jv.joke_id = {}
order by 
    jv.creation_timestamp desc
limit 1
"""