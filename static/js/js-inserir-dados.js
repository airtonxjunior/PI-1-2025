document.getElementById('form-dados').addEventListener('submit', async function(event) {
    //impede recarregar a pagina
    event.preventDefault();

    //pega os dados pelo id
    const agua = document.getElementById('agua').value;
    const energia = document.getElementById('energia').value;
    const residuo = document.getElementById('residuo').value;
    const transporte = document.getElementById('transporte').value;
    const distancia = document.getElementById('distancia').value;

    //pega o id do usuário
    const id_usuario = this.dataset.id;

    //cria um objeto com os dados
    const dados = { agua, energia, residuo, transporte, distancia };

    try {
        //envia uma requisição para '/login' no servidor.
        //await faz o código esperar a resposta do servidor antes de continuar
        const resposta = await fetch(`/perfil/${id_usuario}/inserir-dados`, {
            method: 'POST',  //define o método da requisição como POST para enviar dados
            headers: {
                //informa ao servidor que o corpo da requisição está no formato JSON
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify(dados) //converte o objeto 'dados' para uma string JSON para ser enviada no corpo da requisição
        });

        //dados recebe a resposta da requisição
        const data = await resposta.json();

        //verifica se a resposta do servidor contém uma propriedade message
        if (data.message) {
            alert(data.message);
        } else {
            alert('Erro ao enviar os dados.');
        }
    } //se ocorrer qualquer erro durante o try
    catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao enviar os dados. Tente novamente.');
    }
});
