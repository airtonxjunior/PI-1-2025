document.getElementById('editForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const id_usuario = document.getElementById('editForm').dataset.id;
    const data_registro = document.getElementById('data').value;
    const parametro = document.getElementById('tipo').value;
    const valor = parseFloat(document.getElementById('valor').value);
    const tipoTransporteSelecionado = document.querySelector('input[name="transporte"]:checked');
    const tipo_transporte = tipoTransporteSelecionado ? tipoTransporteSelecionado.value : null;
    const distancia = parseFloat(document.getElementById('distancia').value);

    let payload = {
        data_registro,
        parametro
    };

    if (parametro === 'transporte') {
        payload.tipo_transporte = tipo_transporte;
        payload.distancia = distancia;
    } else {
        payload.valor = valor;
    }

    try {
        const response = await fetch(`/perfil/${id_usuario}/editar-dados`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            location.reload(); // Ou redirecionar para a página de perfil
        } else {
            alert("Erro ao atualizar: " + result.message);
        }
    } catch (err) {
        alert("Erro ao enviar requisição: " + err.message);
    }
});
