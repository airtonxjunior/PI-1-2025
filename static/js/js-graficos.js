//pega os valores do html enviado pelo backend
const { mediaFinal, pontuacaoAgua, pontuacaoEnergia, pontuacaoResiduo, pontuacaoTransporte, datas } = window.dadosGraficos;

//cores dos gráficos
const corAgua = '#4FC3F7';       
const corEnergia = '#FFD54F';    
const corResiduos = '#81C784';   
const corTransporte = '#E57373';  
const corMedia = '#9575CD';      

//foi usado os charts.js 
//configuração para os gráficos
const configuracaoBase = {
    type: 'bar',
    options: {
        responsive: true,
        scales: {
            y: {
                min: 0,
                max: 3,
                beginAtZero: true,
                ticks: {
                    color: 'rgba(255, 255, 255, 0.71)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0)'
                }
            },
            x: {
                ticks: {
                    color: 'rgba(255, 255, 255, 0.71)'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0)'
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: 'rgb(255, 255, 255)'
                }
            }
        }
    }
};

//gráfico principal
new Chart(document.getElementById('graficoPrincipal'), {
    ...configuracaoBase,
    data: {
        labels: datas,//datas dos resultados do bd
        datasets: [{
            label: 'Pontuação',
            data: mediaFinal, 
            backgroundColor: corMedia,
            borderColor: corMedia,
            borderWidth: 2
        }]
    }
});

//gráfico Água
new Chart(document.getElementById('graficoAgua'), {
    ...configuracaoBase,
    data: {
        labels: datas,
        datasets: [{
            label: 'Pontuação',
            data: pontuacaoAgua,
            backgroundColor: corAgua,
            borderColor: corAgua,
            borderWidth: 2
        }]
    }
});

//gráfico Energia
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

//gráfico resíduos
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

//gráfico transporte
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