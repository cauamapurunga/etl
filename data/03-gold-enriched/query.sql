SELECT 
    DISTINCT
    users.id,
    users.nome,
    users.email,
    users.data_nascimento,
    users.genero,
    cep_info.logradouro,
    cep_info.complemento,
    cep_info.unidade,
    cep_info.localidade,
    cep_info.uf,
    cep_info.estado,
    cep_info.regiao,
    cep_info.ibge,
    cep_info.gia,
    cep_info.ddd,
    cep_info.siafi
FROM users
INNER JOIN cep_info
ON cep_info.cep = users.cep
ORDER BY id;