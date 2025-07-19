document.addEventListener('DOMContentLoaded', function() {


    //função que alterna os campos do formulário se selecionado transporte
    window.toggleFields = function(selectedType) {
        const transportFields = document.getElementById('transportFields');
        const valueField = document.getElementById('valueField');
        const valorInput = document.getElementById('valor');
        const valueLabel = document.getElementById('valueLabel');
        const distanciaInput = document.getElementById('distancia');

        //verifica se os elementos necessários para a função existem.
        if (!transportFields || !valueField || !valorInput || !valueLabel || !distanciaInput) {
            console.error("Um ou mais elementos do formulário para toggleFields (transportFields, valueField, valor, valueLabel, distancia) não foram encontrados.");
            return;
        }

        if (selectedType === 'transporte') {
            transportFields.style.display = 'block';
            valueField.style.display = 'none';
            valorInput.removeAttribute('required'); //campo valor não é obrigatório para transporte
            distanciaInput.setAttribute('required', 'required'); //campo distância é obrigatório
        } else {
            transportFields.style.display = 'none';
            valueField.style.display = 'block';
            valorInput.setAttribute('required', 'required'); //campo valor é obrigatório
            distanciaInput.removeAttribute('required'); //campo distância não é obrigatório
            
            //atualiza o campo valor conforme o tipo
            switch(selectedType) {
                case 'agua':
                    valueLabel.textContent = 'Consumo de Água (m³)';
                    break;
                case 'energia':
                    valueLabel.textContent = 'Consumo de Energia (kWh)';
                    break;
                case 'residuo':
                    valueLabel.textContent = 'Resíduos Produzidos (kg)';
                    break;
                default:
                    valueLabel.textContent = 'Valor (m³/kWh/kg)'; //rótulo padrão
            }
        }
    }



    //adiciona o listener de evento para o envio do formulário
    const editForm = document.getElementById('editForm');
    if (editForm) {
        editForm.addEventListener('submit', async function (e) {
            e.preventDefault(); //impede recarregar a pag

            //obtém os valores dos campos do formulário no momento do submit
            const id_usuario = editForm.dataset.id_usuario;

            //pega o valor do campo data
            const data_registro_input = document.getElementById('data');
            const data_registro = data_registro_input.value;

            //pega o valor selecionado no HTML com id 'tipo'
            const parametro = document.getElementById('tipo').value;

            //pega o valor do campo 'valor'. se tiver um valor, converte para número, vazio, então null
            const valorElement = document.getElementById('valor');
            const valor = valorElement.value ? parseFloat(valorElement.value) : null;

            //procura por um input com name="transporte" que esteja marcado (:checked).
            const tipoTransporteSelecionado = document.querySelector('input[name="transporte"]:checked');

            //se transporte estiver selecionado, tipo_transporte recebe o seu valor, ne não, recebe null
            const tipo_transporte = tipoTransporteSelecionado ? tipoTransporteSelecionado.value : null;

            // Pega o valor do campo 'distancia'. Se tiver valor, converte para número.
            const distanciaElement = document.getElementById('distancia');
            const distancia = distanciaElement.value ? parseFloat(distanciaElement.value) : null;

            //verificar se a data é futura
            if (data_registro) {
                const hoje = new Date();
                 //zera as horas da data atual para comparar apenas o dia
                hoje.setHours(0, 0, 0, 0);

                //converte a string da data do input para um objeto Date
                const dataSelecionada = new Date(data_registro + 'T00:00:00');

                if (dataSelecionada > hoje) {
                    alert("A data do registro não pode ser uma data futura.");
                    return;
                }
            }


            //monta o objeto com os dados a serem enviados
            let payload = {
                data_registro,
                parametro
            };

            //se transporte for selecionado
            if (parametro === 'transporte') {
                //adiciona tipo_transporte e distancia ao payload
                if (tipo_transporte) payload.tipo_transporte = tipo_transporte;
                if (distancia !== null && !isNaN(distancia)) payload.distancia = distancia;
                delete payload.valor; //remove 'valor' se for transporte

            } else { //se não for transporte
                //adiciona valor ao payload
                if (valor !== null && !isNaN(valor)) payload.valor = valor;
                delete payload.tipo_transporte; //remove campos de transporte se não for
                delete payload.distancia;
            }

            //envia a requisição para o servidor.
            try {
                const resposta = await fetch(`/perfil/${id_usuario}/editar-dados`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                //coloca a resposta em resultado
                const resultado = await resposta.json();
                if (resposta.ok) {
                    alert(resultado.message || 'Dados atualizados com sucesso!');
                } else {
                    alert("Erro ao atualizar: " + (resultado.message || "Ocorreu um erro."));
                }
            } catch (err) {
                console.error("Erro na requisição:", err);
                alert("Erro ao enviar requisição: " + err.message);
            }
        });
    } else {
        console.warn("Formulário com ID 'editForm' não encontrado no DOM.");
    }
});