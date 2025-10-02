
const botao = document.getElementById('botao');
const meuAlert = document.getElementById('meuAlert');
const body = document.getElementById('body');
const fecharAlert = () => {
    meuAlert.classList.add('sumir');
}
const submit = document.getElementById('submit');

botao.addEventListener('click', function () {
    meuAlert.classList.remove('sumir');
    meuAlert.classList.add('alert');
    body.classList.add('travar-scroll');
});
