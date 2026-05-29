const mensagensDiv = document.getElementById("mensagens");
const usuariosOnline = document.getElementById("usuariosOnline");
const formMensagem = document.getElementById("formMensagem");
const inputMensagem = document.getElementById("mensagem");
const themeButton = document.getElementById("themeButton");

// ENVIAR MENSAGEM
formMensagem?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const mensagem = inputMensagem.value;

  await fetch("/enviar", {
    method: "POST",

    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },

    body: `mensagem=${mensagem}`,
  });

  inputMensagem.value = "";

  carregarMensagens();
});

// CARREGAR MENSAGENS
async function carregarMensagens() {
  const resposta = await fetch("/mensagens");

  const mensagens = await resposta.json();

  if (!mensagensDiv) return;

  mensagensDiv.innerHTML = "";

  mensagens.forEach((msg) => {
    mensagensDiv.innerHTML += `
            <div class="msg">
                <strong>${msg.usuario}</strong>
                ${msg.mensagem}
                <br>
                <small>${msg.horario}</small>
            </div>
        `;
  });

  mensagensDiv.scrollTop = mensagensDiv.scrollHeight;
}

// USUÁRIOS ONLINE
async function carregarUsuarios() {
  const resposta = await fetch("/usuarios_online");

  const usuarios = await resposta.json();

  if (!usuariosOnline) return;

  usuariosOnline.innerHTML = "";

  usuarios.forEach((usuario) => {
    usuariosOnline.innerHTML += `
            <li>${usuario}</li>
        `;
  });
}

// TEMA
themeButton?.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
});

// ATUALIZAÇÃO AUTOMÁTICA
setInterval(() => {
  carregarMensagens();
  carregarUsuarios();
}, 2000);

carregarMensagens();
carregarUsuarios();
