-- Dados fictícios para demonstração.
-- Compatível com o esquema esperado atualmente pelos arquivos Python:
-- cliente(id_cliente, nome, cpf, telefone)
-- carro(id_carro, modelo, marca, placa, valor_diaria)
-- locacao(id_locacao, id_cliente, id_carro, data_locacao, dias, valor_total)
--
-- Execute somente depois de confirmar o esquema definitivo com o grupo.
-- Os INSERTs não definem IDs explicitamente; as locações localizam os registros
-- por CPF e placa. Se seu banco já possuir esses CPFs/placas, revise os dados
-- antes de executar para evitar duplicidades.

START TRANSACTION;

INSERT INTO cliente (nome, cpf, telefone) VALUES
('Mariana Alves', '90000000001', '(27) 99911-1001'),
('Rafael Costa', '90000000002', '(27) 99911-1002'),
('Beatriz Oliveira', '90000000003', '(27) 99911-1003'),
('Pedro Martins', '90000000004', '(27) 99911-1004'),
('Camila Souza', '90000000005', '(27) 99911-1005'),
('Lucas Ferreira', '90000000006', '(27) 99911-1006'),
('Isabela Rocha', '90000000007', '(27) 99911-1007'),
('Gabriel Lima', '90000000008', '(27) 99911-1008');

INSERT INTO carro (modelo, marca, placa, valor_diaria) VALUES
('Onix', 'Chevrolet', 'ABC1D01', 150.00),
('HB20', 'Hyundai', 'ABC1D02', 145.00),
('Corolla', 'Toyota', 'ABC1D03', 230.00),
('Civic', 'Honda', 'ABC1D04', 240.00),
('Argo', 'Fiat', 'ABC1D05', 135.00),
('T-Cross', 'Volkswagen', 'ABC1D06', 210.00),
('Kwid', 'Renault', 'ABC1D07', 110.00),
('Compass', 'Jeep', 'ABC1D08', 280.00);

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-02', 3, 450.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000001' AND k.placa = 'ABC1D01';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-05', 2, 290.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000002' AND k.placa = 'ABC1D02';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-08', 4, 920.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000003' AND k.placa = 'ABC1D03';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-12', 2, 480.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000004' AND k.placa = 'ABC1D04';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-15', 5, 675.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000005' AND k.placa = 'ABC1D05';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-18', 3, 630.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000006' AND k.placa = 'ABC1D06';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-20', 2, 220.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000007' AND k.placa = 'ABC1D07';

INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total)
SELECT c.id_cliente, k.id_carro, '2026-09-24', 3, 840.00
FROM cliente c JOIN carro k
WHERE c.cpf = '90000000008' AND k.placa = 'ABC1D08';

COMMIT;
