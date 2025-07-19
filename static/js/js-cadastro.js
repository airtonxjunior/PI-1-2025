//executa após o carregamento completo do DOM
document.addEventListener('DOMContentLoaded', function () {
    //referência ao formulário de cadastro
    const form = document.getElementById('form-cadastro');

    //referências aos campos de input
    const nomeInput = document.getElementById('nome');
    const emailInput = document.getElementById('email');
    const senhaInput = document.getElementById('senha');
    const confirmaSenhaInput = document.getElementById('confirma-senha');

    //referências aos elementos para exibir mensagens de erro
    const nomeError = document.getElementById('nome-error');
    const emailError = document.getElementById('email-error');
    const senhaError = document.getElementById('senha-error');
    const confirmaSenhaError = document.getElementById('confirma-senha-error');

    //alfabeto permitido para a cifra/validação da senha
    const alfabetoCifra = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    //validação do nome de usuário
    if (nomeInput) {
        const nomeInputBox = nomeInput.closest('.input-box'); //elemento para estilização de erro
        function handleNomeValidation() {
            const value = nomeInput.value.trim(); //pega o valor sem espaços extras
            if (value === '') { //se vazio:
                nomeError.textContent = 'O nome é obrigatório.'; //mostra erro.
                if (nomeInputBox) nomeInputBox.classList.add('input-box-error'); //adiciona classe de erro
                return false;
            }
            nomeError.textContent = ''; //limpa erro
            if (nomeInputBox) nomeInputBox.classList.remove('input-box-error'); //remove classe de erro
            return true;
        }
        nomeInput.addEventListener('input', handleNomeValidation); //valida ao digitar
        nomeInput.addEventListener('blur', handleNomeValidation);  //valida ao perder o foco
    }

    //validação do email
    if (emailInput) {
        const emailInputBox = emailInput.closest('.input-box');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; //expressão regular para formato de email
        function handleEmailValidation() {
            const value = emailInput.value.trim();
            if (value === '') {
                emailError.textContent = 'O e-mail é obrigatório.';
                if (emailInputBox) emailInputBox.classList.add('input-box-error');
                return false;
            }
            if (!emailRegex.test(value)) { //se não corresponder ao formato:
                emailError.textContent = 'Por favor, insira um e-mail válido.';
                if (emailInputBox) emailInputBox.classList.add('input-box-error');
                return false;
            }
            emailError.textContent = '';
            if (emailInputBox) emailInputBox.classList.remove('input-box-error');
            return true;
        }
        emailInput.addEventListener('input', handleEmailValidation);
        emailInput.addEventListener('blur', handleEmailValidation);
    }
    
    //validação da confirmação de senha
    function handleConfirmaSenhaValidation() {
        if (!confirmaSenhaInput || !senhaInput) return true; //se campos não existem, não valida

        const senhaValue = senhaInput.value;
        const confirmaValue = confirmaSenhaInput.value;
        const confirmaInputBox = confirmaSenhaInput.closest('.input-box');
        let message = '';

        //verifica se a confirmação é obrigatória ou se as senhas não coincidem
        if (senhaValue !== '' && confirmaValue === '') {
            message = 'A confirmação da senha é obrigatória.';
        } else if (senhaValue !== '' && confirmaValue !== '' && senhaValue !== confirmaValue) {
            message = 'As senhas não coincidem.';
        }
        
        confirmaSenhaError.textContent = message; //exibe mensagem de erro
        if (message) { //se houver erro:
            if (confirmaInputBox) confirmaInputBox.classList.add('input-box-error');
            return false;
        }
        if (confirmaInputBox) confirmaInputBox.classList.remove('input-box-error');
        return true;
    }

    if (confirmaSenhaInput) {
        confirmaSenhaInput.addEventListener('input', handleConfirmaSenhaValidation);
        confirmaSenhaInput.addEventListener('blur', handleConfirmaSenhaValidation);
    }


    //validação da senha
    if (senhaInput) {
        const senhaInputBox = senhaInput.closest('.input-box');
        function handleSenhaValidation() {
            const value = senhaInput.value;
            let message = '';
            let isValid = true;

            if (value === '') {
                message = 'A senha é obrigatória.';
                isValid = false;
            } else if (value.length < 6) { //verifica comprimento mínimo
                message = 'A senha deve ter pelo menos 6 caracteres.';
                isValid = false;
            } else { //verifica caracteres permitidos
                for (let i = 0; i < value.length; i++) {
                    if (alfabetoCifra.indexOf(value[i].toUpperCase()) === -1) {
                        message = 'A senha deve conter apenas letras (A-Z) e números (0-9).';
                        isValid = false;
                        break;
                    }
                }
            }
            
            senhaError.textContent = message;
            if (!isValid) {
                if (senhaInputBox) senhaInputBox.classList.add('input-box-error');
            } else {
                if (senhaInputBox) senhaInputBox.classList.remove('input-box-error');
            }
            handleConfirmaSenhaValidation(); //revalida a confirmação, pq a senha principal mudou
            return isValid;
        }
        senhaInput.addEventListener('input', handleSenhaValidation);
        senhaInput.addEventListener('blur', handleSenhaValidation);
    }





    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();

            //revalida todos os campos antes de submeter
            const isNomeValid = nomeInput ? handleNomeValidation() : true;
            const isEmailValid = emailInput ? handleEmailValidation() : true;
            const isSenhaValid = senhaInput ? handleSenhaValidation() : true;
            const isConfirmaSenhaValid = confirmaSenhaInput ? handleConfirmaSenhaValidation() : true;


            //se alguma validação falhar, interrompe o envio
            if (!isNomeValid || !isEmailValid || !isSenhaValid || !isConfirmaSenhaValid) {
                const firstInvalidInputBox = form.querySelector('.input-box.input-box-error input');
                if (firstInvalidInputBox) {
                    firstInvalidInputBox.focus();
                }
                return;
            }

            //coleta os dados do formulário
            const dados = {
                nome: nomeInput.value.trim(),
                email: emailInput.value.trim(),
                senha: senhaInput.value
            };

            //envia os dados para o servidor.
            try {
                const resposta = await fetch('/cadastro', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }, //informa que o corpo é JSON
                    body: JSON.stringify(dados) //converte objeto JS para string JSON
                });

                const resultado = await resposta.json();
                if (resposta.ok) { 
                    window.location.href = `/perfil/${resultado.id}`; //redireciona para o perfil do novo usuário
                } else { // Se houve erro no servidor
                    if (resultado.erro) { 
                        //tenta exibir o erro do backend no campo
                        const emailInputBox = emailInput.closest('.input-box');
                        const senhaInputBox = senhaInput.closest('.input-box');

                        if (resultado.erro.toLowerCase().includes('email') || resultado.erro.toLowerCase().includes('usuário já cadastrado')) {
                            emailError.textContent = resultado.erro;
                            if (emailInputBox) emailInputBox.classList.add('input-box-error');
                        } else if (resultado.erro.toLowerCase().includes('senha') || resultado.erro.toLowerCase().includes('caractere')) {
                            senhaError.textContent = resultado.erro;
                            if (senhaInputBox) senhaInputBox.classList.add('input-box-error');
                        } else { 
                            alert(resultado.erro);
                        }
                    } else {
                        alert('Erro ao criar conta. Tente novamente.');
                    }
                }
            } catch (erro) { 
                console.error('Erro na requisição de cadastro:', erro);
                alert('Erro ao tentar se conectar ao servidor. Tente novamente mais tarde.');
            }
        });
    }
});