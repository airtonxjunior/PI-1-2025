document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-login');

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();

            const email = document.querySelector('#email').value;
            const senha = document.querySelector('#senha').value;

            const dados = { email, senha };

            try {
                const resposta = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dados)
                });

                const resultado = await resposta.json();
                console.log('Resultado do login:', resultado);  // Verifique o resultado aqui!

                if (resposta.ok) {
                    const id = resultado.id;  // Pegue o id diretamente
                    window.location.href = `/perfil/${id}`;  // Redireciona para o perfil do usuário
                } else {
                    alert(resultado.Status || 'Erro ao fazer login');
                }
            } catch (erro) {
                console.error('Erro:', erro);
                alert('Erro na requisição');
            }
        });
    }
});
