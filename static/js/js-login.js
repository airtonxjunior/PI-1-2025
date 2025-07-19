document.addEventListener('DOMContentLoaded', function () {

    //encontra o elemento HTML com o ID form-login
    const form = document.getElementById('form-login');

    if (form) {
        //adiciona um ouvinte ao evento submit do formulário.
        //significa que a função interna será chamada quando o usuário tentar enviar o formulário
        form.addEventListener('submit', async function (event) {
            //impede recarregar a página.
            event.preventDefault();

            //pega o valor digitado no campo com os ids email e senha
            const email = document.querySelector('#email').value;
            const senha = document.querySelector('#senha').value;
 
            //cria um objeto com esses dados
            const dados = { email, senha };

            try {
                //envia uma requisição para '/login' no servidor.
                //await faz o código esperar a resposta do servidor antes de continuar
                const resposta = await fetch('/login', {
                    method: 'POST', //define o método da requisição como POST para enviar dados
                    headers: {
                        //informa ao servidor que o corpo da requisição está no formato JSON
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dados) // Converte o objeto 'dados' para uma string JSON para ser enviada no corpo da requisição
                });
                
                //resultado recebe a resposta da requisição
                const resultado = await resposta.json();
                console.log('Resultado do login:', resultado); 

                //se ok, redireciona para o perfil, se não, exibe a mensagem de erro
                if (resposta.ok) {
                    const id = resultado.id;  
                    window.location.href = `/perfil/${id}`; 
                } else {
                    alert(resultado.Status || 'Erro ao fazer login');
                } 
            } 
              //se ocorrer qualquer erro durante o try
            catch (erro) {
                console.error('Erro:', erro);
                alert('Erro na requisição');
            }
        });
    }
});

