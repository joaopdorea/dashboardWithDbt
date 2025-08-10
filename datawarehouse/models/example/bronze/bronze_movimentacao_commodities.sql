-- import

with source as (
    select "date",
            "symbol",
            "action",
            "quantity"
            from {{source ('dbfinance_g3yx', 'movimentacao_commodities')}}
),
-- renamed - renomear ou mudar o tipo da coluna

renamed as (
    select cast("date" as date) as data,
    "symbol" as simbolo,
    "action" as tipo_acao,
    "quantity" as quantidade
 from source
)

--select * from

select * from renamed