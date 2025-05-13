document.getElementById('form-dados').addEventListener('submit', async function(event) {
    event.preventDefault();

    const agua = document.getElementById('agua').value;
    const energia = document.getElementById('energia').value;
    const lixo = document.getElementById('lixo').value;
    const transporte = document.getElementById('transporte').value;
    const distancia = document.getElementById('distancia').value;

    const id_usuario = this.dataset.id;

    const dados = { agua, energia, lixo, transporte, distancia };

    try {
        const resposta = await fetch(`/perfil/${id_usuario}/inserir-dados`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        const data = await resposta.json();

        if (data.message) {
            alert(data.message);
        } else {
            alert('Erro ao enviar os dados.');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao enviar os dados. Tente novamente.');
    }
});
