document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form-cadastro');

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault(); 


            const nome = document.querySelector('#nome').value;
            const email = document.querySelector('#email').value;
            const senha = document.querySelector('#senha').value;

            const dados = { nome, email, senha };

            try {
                const resposta = await fetch('/cadastro', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dados)
                });

                const resultado = await resposta.json();
                if (resposta.ok) {
                    window.location.href = `/perfil/${resultado.id}`;
                } else {
                    alert(resultado.erro || 'Erro ao criar conta');
                }
            } catch (erro) {
                console.error('Erro:', erro);
                alert('Erro na requisição');
            }
        });
    }
});
