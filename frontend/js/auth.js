// ============================================================
// js/auth.js — Funções compartilhadas de autenticação
// Descrição: Usadas por toda tela protegida, pra checar login
//            e mandar o token em toda requisição pra API.
// ============================================================

function protegerPagina() {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = 'login.html'
  }
}

async function fetchAutenticado(url, opcoes = {}) {
  const token = localStorage.getItem('token')

  opcoes.headers = {
    ...opcoes.headers,
    'Authorization': `Bearer ${token}`
  }

  const resposta = await fetch(url, opcoes)

  if (resposta.status === 401) {
    localStorage.removeItem('token')
    window.location.href = 'login.html'
  }

  return resposta
}

function sair() {
  localStorage.removeItem('token')
  window.location.href = 'login.html'
}
