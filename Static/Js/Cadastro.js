
const cpf = document.getElementById("cpf");
const cpfErro = document.getElementById("cpfErro");

function validarPrimeiroDigito(cpf){
    let sum = 0
    for(let i = 0;i < 9;i++){
        sum += cpf[i] * (10 - i);
    }
    const resto = (sum*10) % 11;
    if(resto < 10){
        return resto == cpf[9];
    }else{
        return cpf[9] == 0;
    }
}

function validarSegundoDigito(cpf){
    let sum = 0
    for(let i = 0;i < 10;i++){
        sum += cpf[i] * (11 - i);
    }
    const resto = (sum*10) % 11;
    if(resto < 10){
        return resto == cpf[10];
    }else{
        return cpf[10] == 0;
    }
}

function validarRepetido(cpf){
    const primeiro = cpf[0];
    let diferente = false
    for(let i = 1;i < cpf.lenght;i++){
        if(cpf[i] != primeiro){
            diferente = true
        }
    }
    return diferente
}

function validarCPF(cpf){
    if(cpf.lenght != 11){
        return false;
    }
    if(!validarRepetido(cpf)){
        return false
    }
    if(!validarPrimeiroDigito(cpf)){
        return false;
    }
    if(!validarSegundoDigito(cpf)){
        return false;
    }
    return true;
}

function validacao(){
    const cpf = document.getElementById("cpf");
    const cpfErro = document.getElementById("cpfErro");
    const cpfValido = validarCPF(cpf);

    cpf = cpf.split('').map(Number);
    
    if (cpfValido) {
        cpfErro.textContent = '';
    } else {
        cpfErro.textContent = 'CPF inválido'; 
    }
}
const cpfvalido = validarCPF(cpf);