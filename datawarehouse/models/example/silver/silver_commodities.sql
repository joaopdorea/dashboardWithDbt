-- import

with commodities as (
    select "data",
            "valor_fechamento",
            "simbolo" 
            from {{ref ('bronze_commodities')}}
),

movimentacao as (
    select "data",
            "simbolo",
            "tipo_acao",
            "quantidade"
            from {{ref ('bronze_movimentacao_commodities')}}
),
-- renamed - renomear ou mudar o tipo da coluna

joined as (
    select
        m.data,
        m.simbolo,
        c.valor_fechamento,
        m.tipo_acao,
        m.quantidade,
        (m.quantidade * c.valor_fechamento) as valor,
        case
            when m.tipo_acao = 'sell' then (m.quantidade * c.valor_fechamento)
            else -(m.quantidade * c.valor_fechamento)
        end as ganho
    from
        movimentacao m
    left join
        commodities c
    on
        m.data = c.data
        and m.simbolo = c.simbolo
)

select
    data,
    simbolo,
    valor_fechamento,
    tipo_acao,
    quantidade,
    valor,
    ganho
from
    joined