const { mediaFinal, pontuacaoAgua, pontuacaoEnergia, pontuacaoResiduo, pontuacaoTransporte, datas } = window.dadosGraficos;

const corAgua = '#4FC3F7';       
const corEnergia = '#FFD54F';    
const corResiduos = '#81C784';   
const corTransporte = '#E57373';  
const corMedia = '#9575CD';      

const configuracaoBase = {
    type: 'bar',
    options: {
        scales: {
            y: {
                min: 0,
                max: 3,
                beginAtZero: true
            }
        }
    }
};

// Gráfico principal
new Chart(document.getElementById('graficoPrincipal'), {
    ...configuracaoBase,
    data: {
        labels: datas,  // Passa as datas dos resultados
        datasets: [{
            label: 'Pontuação',
            data: mediaFinal,  // Agora é um array de médias, baseado no período
            backgroundColor: corMedia,
            borderColor: corMedia,
            borderWidth: 2
        }]
    }
});

// Gráfico Água
new Chart(document.getElementById('graficoAgua'), {
    ...configuracaoBase,
    data: {
        labels: datas,
        datasets: [{
            label: 'Pontuação',
            data: pontuacaoAgua,  // Pontuação de água, agora será um array
            backgroundColor: corAgua,
            borderColor: corAgua,
            borderWidth: 2
        }]
    }
});

// Gráfico Energia
new Chart(document.getElementById('graficoEnergia'), {
    ...configuracaoBase,
    data: {
        labels: datas,
        datasets: [{
            label: 'Pontuação',
            data: pontuacaoEnergia,
            backgroundColor: corEnergia,
            borderColor: corEnergia,
            borderWidth: 2
        }]
    }
});

// Gráfico Resíduos
new Chart(document.getElementById('graficoResiduo'), {
    ...configuracaoBase,
    data: {
        labels: datas,
        datasets: [{
            label: 'Pontuação',
            data: pontuacaoResiduo,
            backgroundColor: corResiduos,
            borderColor: corResiduos,
            borderWidth: 2
        }]
    }
});

// Gráfico Transporte
new Chart(document.getElementById('graficoTransporte'), {
    ...configuracaoBase,
    data: {
        labels: datas,
        datasets: [{
            label: 'Pontuação',
            data: pontuacaoTransporte,
            backgroundColor: corTransporte,
            borderColor: corTransporte,
            borderWidth: 2
        }]
    }
});