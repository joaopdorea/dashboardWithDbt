-- import

with source as (
    select "Date",
            "Close",
            "simbolo" 
            from {{source ('dbfinance_g3yx', 'commodities')}}
),
-- renamed - renomear ou mudar o tipo da coluna

renamed as (
    select cast("Date" as date) as data,
    "Close" as valor_fechamento,
    simbolo
 from source
)

--select * from

select * from renamed